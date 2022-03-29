# Postgres Naming convention

Reference: [link](https://stackoverflow.com/a/4108266/7768908)

The standard names for indexes in PostgreSQL are:

`{tablename}_{columnname(s)}_{suffix}`

where the suffix is one of the following:

- `pkey` for a Primary Key constraint
- `key` for a Unique constraint
- `excl` for an Exclusion constraint
- `idx` for any other kind of index
- `fkey` for a Foreign key
- `check` for a Check constraint
- Standard suffix for sequences is `seq` for all sequences

Proof of your UNIQUE-constraint:

> NOTICE: CREATE TABLE / UNIQUE will create implicit index "example_a_b_key" for table "example"
