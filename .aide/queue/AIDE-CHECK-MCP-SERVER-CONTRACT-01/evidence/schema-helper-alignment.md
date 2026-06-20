# Schema Helper Alignment

The schema parses and the projected contract retains the expected AIDE envelope
shape. The build helper reports schema/helper alignment as `PASS`.

Independent fixture checks found two material defects that helper validation
does not catch:

- null cursor fields in list fixtures;
- wrong resource-not-found error code.

No helper, schema, or test repair was performed.
