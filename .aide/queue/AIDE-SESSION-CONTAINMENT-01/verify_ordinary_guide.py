"""Acceptance checks for the bounded operator-guide candidate, without writes."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--guide', type=Path, required=True)
    parser.add_argument('--prefix-sha256', required=True)
    args = parser.parse_args()
    data = args.guide.read_bytes()
    if len(data) > 65536:
        raise SystemExit('guide exceeds the declared acceptance limit')
    text = data.decode('utf-8').replace('\r\n', '\n')
    marker = '## Task workspace candidate (qualification pending)\n'
    if text.count(marker) != 1:
        raise SystemExit('retain the exact qualification-pending boundary')
    prefix, section = text.split(marker)
    if hashlib.sha256(prefix.encode('utf-8')).hexdigest() != args.prefix_sha256:
        raise SystemExit('unrelated guide content changed')
    checks = {
        'bounded_manifest': all(value in section for value in (
            'task_workspace', 'read_roots', 'max_files', 'max_input_bytes')),
        'inspect_then_run': all(value in section for value in (
            'job inspect --config <local-config> --manifest <job-json>',
            'job run --config <local-config> --manifest <job-json>')),
        'ordered_workflow': bool(re.search(r'(?m)^1\. ', section))
            and bool(re.search(r'(?m)^5\. ', section)),
        'retirement_and_no_replay': all(value in section.casefold() for value in (
            'scratch', 'reservation', 'uncertain', 'replay')),
        'candidate_review_before_integration': all(value in section.casefold()
            for value in ('candidate', 'diff', 'review', 'canonical')),
        'truthful_limits': all(value in section.casefold() for value in (
            'unrestricted', 'monitored', 'hard disk quota', 'signed-in',
            'no api billing fallback', 'actual model', 'qualification')),
    }
    if not all(checks.values()):
        print(json.dumps({'status': 'FAIL', 'checks': checks}))
        raise SystemExit(1)
    print(json.dumps({'status': 'PASS', 'checks': checks,
                      'guide_sha256': hashlib.sha256(data).hexdigest()}))


if __name__ == '__main__':
    main()
