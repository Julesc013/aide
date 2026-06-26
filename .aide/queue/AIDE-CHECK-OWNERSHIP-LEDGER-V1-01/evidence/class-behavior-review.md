# Class Behavior Review

All eleven requested ownership classes are present in the taxonomy and at least
one record exists for each class.

The current records set `apply_allowed`, `overwrite_allowed`, and
`delete_allowed` to `false`. Unknown and never-touch records block apply in the
generated projection.

Material gaps are not class enumeration gaps. They are missing semantic record
fields, missing Q43 migration, and missing conflict checks needed for downstream
install/update planning.
