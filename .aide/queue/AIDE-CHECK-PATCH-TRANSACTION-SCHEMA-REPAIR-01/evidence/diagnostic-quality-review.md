# Diagnostic Quality Review

Duplicate diagnostics include:

- the collection name;
- both original conflicting values;
- the shared canonical path.

Example evidence observed:

```text
declared_changed_paths: duplicate normalized path: src/file.py from 'src//file.py' and 'src/file.py'
```

Drive-prefix diagnostics include the offending raw value and a `drive prefix`
reason.

No diagnostics exposed secrets or unrelated source content.
