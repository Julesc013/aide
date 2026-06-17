# Test Results

Command:

```bat
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_okf_knowledge_bundle.py
```

Result:

```text
Ran 8 tests in 5.494s
OK
```

Coverage:

- frontmatter writer/parser/validator
- projection into a temporary repo root
- source artifact immutability
- required pages
- reserved `index.md` and `log.md`
- validation and lint reports
- EventRecord projection-only classification
- CLI status/project/validate/lint
- rejection of runtime/network OKF subcommands
- JSON report parsing
