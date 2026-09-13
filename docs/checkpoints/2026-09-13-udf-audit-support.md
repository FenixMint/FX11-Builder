# Checkpoint — UDF-aware FX11 audit

Date: 2026-09-13

The real Microsoft Windows 11 25H2 source used by the project is UDF-first. `fx11 inspect` and the Builder already gained UDF support through 7-Zip, but the deep audit still inventoried ISO paths only through xorriso.

That mismatch would make a genuine-source audit incomplete even when the build itself succeeded.

## Change

`src/fx11/audit.py` now:

- detects UDF source media,
- inventories UDF file paths through `7z l -slt`,
- keeps xorriso inventory for normal ISO9660 output media,
- extracts audited paths through the shared UDF/ISO-aware `extract_iso_member()` helper,
- derives expected FX11 additions from the generated manifest,
- recognises declared GParted and FX media boot payloads as expected additions rather than false-positive unexpected files.

A parser regression test was added for 7-Zip technical-list output.

## Status wording

The code and tests have been committed, but no claim is made here that the new audit path has already been observed against the user's full real UDF source and generated FX11 output. That must be verified after the first genuine Windows 11 Home build completes.
