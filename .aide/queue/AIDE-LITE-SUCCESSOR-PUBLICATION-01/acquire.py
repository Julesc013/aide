"""Acquire only the four frozen public release assets; no retries or clobber."""
import hashlib
import json
from pathlib import Path
import stat
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
TASK = Path(__file__).resolve().parent
DEST = ROOT / '.aide/release/acquired-aide-lite-v1.1.0.log'
HOSTS = {'github.com', 'release-assets.githubusercontent.com',
         'objects.githubusercontent.com'}


def require_url(url):
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != 'https' or parsed.hostname not in HOSTS
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        raise ValueError('release download left the approved HTTPS hosts')


class ReleaseRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        require_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def main():
    subject = json.loads((TASK / 'evidence/release-selection.json').read_text())
    expected = subject['assets']
    assert len(expected) == 4
    assert sum(item['size_bytes'] for item in expected.values()) < 4 * 1024 * 1024
    for parent in [ROOT, ROOT / '.aide', ROOT / '.aide/release']:
        info = parent.lstat()
        assert stat.S_ISDIR(info.st_mode) and not getattr(info, 'st_file_attributes', 0) & 0x400
    DEST.mkdir()  # Existing or partial acquisitions need explicit reconciliation.
    opener = urllib.request.build_opener(ReleaseRedirect())
    deadline = time.monotonic() + 180
    receipt = {'status': 'STARTED', 'assets': {}, 'credential_use': 'none'}
    receipt_path = DEST / 'acquisition.json'

    def save():
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')

    save()
    try:
        for source, identity in expected.items():
            name = Path(source).name
            assert name in {
                'aide-lite-v1.1.0.zip', 'aide-lite-v1.1.0.tar.gz',
                'aide-lite-v1.1.0.manifest.json', 'aide-lite-v1.1.0.SHA256SUMS.txt'}
            url = 'https://github.com/Julesc013/aide/releases/download/aide-lite-v1.1.0/' + name
            record = {'url': url, 'status': 'STARTED', 'bytes': 0}
            receipt['assets'][name] = record
            save()
            request = urllib.request.Request(url, headers={'User-Agent': 'AIDE-release-acquisition'})
            require_url(url)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('acquisition deadline expired')
            with opener.open(request, timeout=min(15, remaining)) as response, (DEST / name).open('xb') as out:
                require_url(response.geturl())
                assert response.status == 200
                size = identity['size_bytes']
                length = response.headers.get('Content-Length')
                assert length is None or int(length) == size
                digest = hashlib.sha256()
                while True:
                    if time.monotonic() >= deadline:
                        raise TimeoutError('acquisition deadline expired')
                    chunk = response.read(min(65536, size - record['bytes'] + 1))
                    if not chunk:
                        break
                    if record['bytes'] + len(chunk) > size:
                        raise ValueError('asset exceeds its exact size')
                    out.write(chunk)
                    digest.update(chunk)
                    record['bytes'] += len(chunk)
                assert record['bytes'] == size and digest.hexdigest() == identity['sha256']
                record.update(status='PASS', sha256=digest.hexdigest())
            save()
        receipt['status'] = 'PASS'
    except BaseException as exc:
        # Retain partial files; do not expose signed redirect URLs or credentials.
        receipt.update(status='INCOMPLETE', failure_type=type(exc).__name__)
        raise RuntimeError('asset acquisition incomplete; see retained receipt') from None
    finally:
        save()
    print('PASS: four published assets acquired with exact hashes and sizes')


if __name__ == '__main__':
    main()
