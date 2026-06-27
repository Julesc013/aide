# Validation Commands

Planned and executed validation:

- `py -3 -m compileall -q core\protocol\update_plan.py .aide\scripts\tests\test_aide_update_plan_v1.py .aide\scripts\aide_lite.py`
- `py -3 -m unittest discover -s .aide\scripts\tests -p test_aide_update_plan_v1.py`
- `py -3 .aide\scripts\aide_lite.py update-plan status`
- `py -3 .aide\scripts\aide_lite.py update-plan project`
- `py -3 .aide\scripts\aide_lite.py update-plan validate`
- predecessor regression validators
- Q43-Q48 no-apply/no-publish validators
- `py -3 .aide\scripts\aide_lite.py validate`
- task inspect/evidence
- path, secret-like, and source-output misuse scans
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide\scripts\aide_lite.py commit check --latest`
