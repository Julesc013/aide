"""Acquire this task's exact upstream wheels; never import or install them."""
import sys
sys.dont_write_bytecode = True
import email.parser
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import time
import urllib.parse
import urllib.request
import zipfile

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[2]
# Reuse the previously qualified no-redirect policy; this module has no main effect.
spec = importlib.util.spec_from_file_location(
    "aide_disked_wheel_acquisition", ROOT / ".aide/queue/AIDE-DAILY-DISKED-EXPORT-01/acquire_wheels.py")
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def main():
    expected = json.loads((TASK / "evidence/wheel-inputs.json").read_text(encoding="utf-8"))
    pins = json.loads((TASK / "evidence/upstream-source-pins.json").read_text(encoding="utf-8"))
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    assert len(expected["wheels"]) == expected["wheel_count"] == 14
    assert sum(w["bytes"] for w in expected["wheels"]) == expected["compressed_bytes"] == 4716392
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), prior.RefuseRedirect())
    began = time.monotonic()
    rows, total_bytes, total_members = [], 0, 0
    seen_paths = set()

    def save(status):
        report = {"schema": "aide.mini-worker.acquisition.v1", "status": status,
                  "wheels": rows, "compressed_bytes": sum(w["bytes"] for w in rows),
                  "unpacked_bytes": total_bytes, "archive_members": total_members,
                  "selected_profile": expected["profile"],
                  "downloaded_code_executed": False, "global_installation": False,
                  "model_requests": 0, "authenticity_qualification": "not_claimed"}
        data = (json.dumps(report, indent=2) + "\n").encode("utf-8")
        assert len(data) <= expected["maximum_report_bytes"]
        (output / "acquisition.json").write_bytes(data)

    save("INCOMPLETE")
    for wheel in expected["wheels"]:
        assert time.monotonic() - began < 120, "acquisition deadline"
        url = urllib.parse.urlsplit(wheel["url"])
        assert url.scheme == "https" and url.netloc == "files.pythonhosted.org"
        assert url.path.startswith("/packages/") and not url.query and not url.fragment
        filename = wheel["filename"]
        assert re.fullmatch(r"[A-Za-z0-9_.-]+\.whl", filename)
        assert filename == urllib.parse.unquote(url.path.rsplit("/", 1)[1])
        with opener.open(wheel["url"], timeout=15) as response:
            if response.headers.get("Content-Length") is not None:
                assert int(response.headers["Content-Length"]) == wheel["bytes"]
            data = response.read(wheel["bytes"] + 1)
        with (output / filename).open("xb") as stream:
            stream.write(data)
        assert len(data) == wheel["bytes"]
        assert hashlib.sha256(data).hexdigest() == wheel["sha256"]
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            unpacked = sum(member.file_size for member in entries)
            total_bytes += unpacked
            total_members += len(entries)
            assert total_bytes <= expected["maximum_unpacked_bytes"]
            assert total_members <= expected["maximum_archive_members"]
            for member in entries:
                parts = PurePosixPath(member.filename).parts
                assert parts and not member.filename.startswith("/")
                assert all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) and part not in (".", "..") for part in parts)
                assert not any(part.endswith(".data") for part in parts)
                assert not stat.S_ISLNK(member.external_attr >> 16) and not member.flag_bits & 1
                if not member.is_dir():
                    key = member.filename.casefold()
                    assert key not in seen_paths, "cross-wheel path collision"
                    seen_paths.add(key)
            metadata = [m for m in entries if m.filename.endswith(".dist-info/METADATA")]
            assert len(metadata) == 1 and metadata[0].file_size <= 131072
            headers = email.parser.BytesParser().parsebytes(archive.read(metadata[0]))
            normalize = lambda value: re.sub(r"[-_.]+", "-", value).lower()
            assert normalize(headers["Name"]) == normalize(wheel["name"])
            assert headers["Version"] == wheel["version"]
            assert sorted(headers.get_all("Requires-Dist", [])) == sorted(wheel["requires_dist"])
            licenses = [m for m in entries if ".dist-info/" in m.filename
                        and any(token in m.filename.rsplit("/", 1)[-1].upper()
                                for token in ("LICENSE", "LICENCE", "NOTICE", "COPYING", "AUTHORS"))]
            assert licenses, "license/notice material missing"
            notices = []
            for member in licenses:
                assert member.file_size <= 131072
                raw = archive.read(member)
                notices.append({"path": member.filename, "bytes": len(raw),
                                "sha256": hashlib.sha256(raw).hexdigest()})
            source_matches = []
            if wheel["name"] == "mini-swe-agent":
                for pin in pins["files"]:
                    name = pin["path"].removeprefix("src/")
                    if pin["path"] == "LICENSE.md":
                        names = [n["path"] for n in notices if n["sha256"] == pin["sha256"]]
                        assert len(names) == 1
                        name = names[0]
                    raw = archive.read(name)
                    assert len(raw) == pin["bytes"]
                    assert hashlib.sha256(raw).hexdigest() == pin["sha256"]
                    source_matches.append({"wheel_path": name, "source_path": pin["path"],
                                           "sha256": pin["sha256"]})
            rows.append({**wheel, "status": "PASS_EXACT_BYTES_METADATA",
                         "unpacked_bytes": unpacked, "members": len(entries),
                         "notices": notices, "upstream_source_matches": source_matches})
        save("PASS" if len(rows) == expected["wheel_count"] else "INCOMPLETE")
        print(json.dumps({"wheel": filename, "status": rows[-1]["status"],
                          "compressed_bytes": wheel["bytes"], "unpacked_bytes": unpacked}), flush=True)
    print(json.dumps({"result": "PASS", "wheels": len(rows), "unpacked_bytes": total_bytes,
                      "archive_members": total_members, "elapsed_seconds": time.monotonic() - began}))


if __name__ == "__main__":
    main()

