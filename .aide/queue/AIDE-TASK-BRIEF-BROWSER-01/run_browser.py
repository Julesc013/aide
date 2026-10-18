"""One bounded observation of the already qualified, inactive task-brief page."""
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys
import time
import winreg

sys.dont_write_bytecode = True
ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-TASK-BRIEF-BROWSER-01'
PRIOR = ROOT / '.aide/queue/AIDE-TASK-BRIEF-SYMBOL-01/evidence'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def check_browser(observation):
    guards = []
    for name, hive in [('HKLM', winreg.HKEY_LOCAL_MACHINE), ('HKCU', winreg.HKEY_CURRENT_USER)]:
        for view in [winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY]:
            try:
                with winreg.OpenKey(hive, r'Software\Policies\Microsoft\Edge', 0,
                                   winreg.KEY_READ | view):
                    raise RuntimeError('Edge policy root present; profile redirection is unqualified')
            except FileNotFoundError:
                guards.append({'hive': name, 'view': view, 'policy_root_present': False})
    directory = Path(observation['version_directory'])
    executable = Path(observation['executable'])
    paths = [executable]
    for parent in [directory, *directory.parents, executable]:
        assert not parent.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT, str(parent)
    for parent, dirs, files in os.walk(directory):
        for name in dirs + files:
            path = Path(parent) / name
            assert not path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT, str(path)
        paths.extend(Path(parent) / name for name in files)
        assert len(paths) <= 1000, 'unexpected browser inventory growth'
    actual = {str(p): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in paths}
    assert actual == observation['installed_files'], 'installed browser bytes changed'
    return {'files_verified': len(actual), 'policy_guards': guards}


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.in_observation = False
        self.observations = 0
        self.json_parts = []
        self.text_parts = []
        self.title = []
        self.in_title = False
        self.csp = []
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag not in {'script', 'iframe', 'object', 'embed', 'form', 'base', 'link', 'img'}, tag
        assert not any(k.lower().startswith('on') for k in attrs), tag
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'content-security-policy':
            self.csp.append(attrs['content'])
        if tag == 'pre' and attrs.get('id') == 'observation-json':
            self.in_observation = True
            self.observations += 1
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.in_observation = False
        if tag == 'title':
            self.in_title = False

    def handle_data(self, text):
        self.text_parts.append(text)
        if self.in_observation:
            self.json_parts.append(text)
        if self.in_title:
            self.title.append(text)


def capture(label, width, observation, page, output, scratch):
    owned = scratch / label
    owned.mkdir()
    for name in ['profile', 'cache', 'crash', 'user', 'local', 'roaming', 'temp']:
        (owned / name).mkdir()
    sys.path.insert(0, str(ROOT))
    from core.runtime.continuous_worker.windows_job import sanitized_environment
    env = sanitized_environment()
    for key, name in {'USERPROFILE': 'user', 'LOCALAPPDATA': 'local', 'APPDATA': 'roaming',
                      'TEMP': 'temp', 'TMP': 'temp'}.items():
        env[key] = str(owned / name)
    screenshot = output / (label + '.png')
    command = [observation['executable'], '--headless', '--disable-gpu',
               '--force-device-scale-factor=1', '--window-size=' + str(width) + ',1800',
               '--timeout=5000', '--screenshot=' + str(screenshot), '--dump-dom',
               '--user-data-dir=' + str(owned / 'profile'), '--disk-cache-dir=' + str(owned / 'cache'),
               '--crash-dumps-dir=' + str(owned / 'crash'), '--no-first-run',
               '--no-default-browser-check', '--disable-background-networking',
               '--disable-component-update', '--disable-default-apps', '--disable-sync',
               '--disable-extensions', '--metrics-recording-only',
               '--proxy-server=http://127.0.0.1:9', '--proxy-bypass-list=<-loopback>', page.as_uri()]
    out = output / (label + '.dom'); err = output / (label + '.stderr')
    receipt = output / (label + '.invocation.json')
    record = {'command': command, 'cwd': str(owned), 'state': 'started', 'exit_code': None,
              'environment_values': 'sanitized allowlist with owned user/temp directories',
              'network_isolation': 'not_established; flags and proxy advisory only'}
    save(receipt, record)
    started = time.monotonic()
    try:
        with out.open('xb') as stdout, err.open('xb') as stderr:
            result = subprocess.run(command, cwd=owned, env=env, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=stderr, timeout=40,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
        record.update(state='completed', exit_code=result.returncode)
    except (OSError, subprocess.SubprocessError) as error:
        record.update(state='exception', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        record['elapsed_seconds'] = time.monotonic() - started
        record['files'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)}
                           for p in [out, err, screenshot] if p.is_file()}
        save(receipt, record)
    assert result.returncode == 0, label + ' browser exit'
    assert 0 < out.stat().st_size <= 512 * 1024, label + ' DOM size'
    assert 24 <= screenshot.stat().st_size <= 3 * 1024 * 1024, label + ' image size'
    with screenshot.open('rb') as stream:
        header = stream.read(24)
    assert header[:8] == b'\x89PNG\r\n\x1a\n' and header[12:16] == b'IHDR'
    dimensions = struct.unpack('>II', header[16:24])
    assert dimensions == (width, 1800), (label, dimensions)
    return {'label': label, 'dimensions': dimensions, 'dom_sha256': sha(out),
            'screenshot_sha256': sha(screenshot), 'exit_code': result.returncode}


def main():
    assert os.name == 'nt' and os.environ.get('AIDE_JOB_ID'), 'managed native job required'
    output = Path(os.environ['AIDE_JOB_OUTPUT']).resolve(strict=True)
    scratch = Path(os.environ['AIDE_JOB_TMP']).resolve(strict=True)
    assert output != scratch and output.parent == scratch.parent, 'unexpected owned roots'
    observation = json.loads((TASK / 'evidence/browser-observation.json').read_bytes())
    expected = json.loads((PRIOR / 'attempt-02-real-source-json.stdout').read_bytes())
    original = PRIOR / 'attempt-02-real-source-html.stdout'
    before_sha = sha(original)
    baseline = Page(original.read_text(encoding='ascii'))
    assert baseline.observations == 1 and json.loads(''.join(baseline.json_parts)) == expected
    assert len(baseline.csp) == 1 and "default-src 'none'" in baseline.csp[0]
    assert expected['result'] == 'PARTIAL' and expected['next_action'] == 'reconcile_records'
    page = output / 'offline-brief.html'
    page.write_bytes(original.read_bytes())
    record = {'schema': 'aide.browser-render-observation.v1', 'result': 'STARTED',
              'browser': observation['browser'], 'version': observation['version'],
              'page_sha256': before_sha, 'captures': [], 'model_requests': 0,
              'visual_review': 'PENDING', 'accessibility': 'NOT_QUALIFIED'}
    result_path = output / 'browser-result.json'
    save(result_path, record)
    try:
        record['before'] = check_browser(observation)
        for label, width in [('desktop', 1280), ('narrow', 480)]:
            row = capture(label, width, observation, page, output, scratch)
            rendered = Page((output / (label + '.dom')).read_text(encoding='utf-8'))
            assert rendered.observations == 1
            assert json.loads(''.join(rendered.json_parts)) == expected, label + ' observation changed'
            assert rendered.csp == baseline.csp and rendered.title == baseline.title
            text = ''.join(rendered.text_parts)
            for token in ['Next action', 'reconcile_records', 'PARTIAL', 'build_task_development_brief']:
                assert token in text, (label, token)
            row['complete_observation_equal'] = True
            record['captures'].append(row)
            save(result_path, record)
        record['after'] = check_browser(observation)
        assert sha(original) == before_sha == sha(page)
        record['result'] = 'CAPTURE_AND_DOM_PASS_PENDING_VISUAL_REVIEW'
    except BaseException as error:
        record.update(result='FAILED_OR_INTERRUPTED', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        save(result_path, record)
    print(json.dumps({'result': record['result'], 'captures': len(record['captures'])}))


if __name__ == '__main__':
    main()
