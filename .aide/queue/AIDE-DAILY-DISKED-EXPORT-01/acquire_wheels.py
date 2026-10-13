"""One bounded acquisition of exact public native test wheels; execute no wheel."""
import sys
sys.dont_write_bytecode = True
import email.parser
import hashlib
import io
import json
import os
from pathlib import Path
import time
import urllib.parse
import urllib.request
import zipfile

TASK = Path(__file__).resolve().parent


class RefuseRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Unreviewed wheel redirect refused')


def main():
    expected = json.loads((TASK / 'evidence/wheel-inputs.json').read_text(encoding='utf-8'))
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    rows = []
    opener = urllib.request.build_opener(RefuseRedirect())
    assert len(expected['wheels']) == 7
    assert sum(w['bytes'] for w in expected['wheels']) == 631366
    for wheel in expected['wheels']:
        url = urllib.parse.urlsplit(wheel['url'])
        assert url.scheme == 'https' and url.netloc == 'files.pythonhosted.org'
        assert url.path.startswith('/packages/') and not url.query and not url.fragment
        filename = wheel['filename']
        assert Path(filename).name == filename and filename.endswith('.whl')
        assert filename == urllib.parse.unquote(url.path.rsplit('/', 1)[1])
        started = time.monotonic()
        with opener.open(wheel['url'], timeout=20) as response:
            if response.headers.get('Content-Length') is not None:
                assert int(response.headers['Content-Length']) == wheel['bytes']
            data = response.read(wheel['bytes'] + 1)
        with (output / filename).open('xb') as stream:
            stream.write(data)
        assert len(data) == wheel['bytes']
        assert hashlib.sha256(data).hexdigest() == wheel['sha256']
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            assert len(entries) < 1000 and sum(e.file_size for e in entries) < 16 * 1024 * 1024
            metadata = [e for e in entries if e.filename.endswith('.dist-info/METADATA')]
            assert len(metadata) == 1
            headers = email.parser.BytesParser().parsebytes(archive.read(metadata[0]))
            normalize = lambda value: value.lower().replace('_', '-').replace('.', '-')
            assert normalize(headers['Name']) == normalize(wheel['name'])
            assert headers['Version'] == wheel['version']
        rows.append({**wheel, 'status': 'PASS_EXACT_BYTES_METADATA',
                     'elapsed_seconds': time.monotonic() - started})
        (output / 'acquisition.json').write_text(json.dumps({
            'schema': 'aide.native-test-wheel-acquisition.v1',
            'status': 'PASS' if len(rows) == 7 else 'PARTIAL', 'wheels': rows,
            'downloaded_code_executed': False, 'global_installation': False,
            'target_mutated': False, 'authenticity_qualification': 'not_claimed'
        }, indent=2) + '\n', encoding='utf-8', newline='\n')
        print(json.dumps({'filename': filename, 'bytes': len(data), 'status': rows[-1]['status']}), flush=True)


if __name__ == '__main__':
    main()
