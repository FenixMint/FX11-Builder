# Public documentation review required before release

Date: 2026-09-13

## Decision

Before FX11 Builder is treated as ready for public exposure, the user-facing documentation must be reviewed and rewritten separately from development/test notes.

The current root-level `FX11_BUILDER_INSTRUKCJA.txt` is a development-era working instruction, not a publication-ready end-user manual.

## Why the current instruction is not public-ready

The current document mixes several audiences and purposes:

- public end-user installation instructions,
- maintainer/developer workflow,
- local test-machine paths and examples,
- active-development status notes,
- QEMU validation workflow,
- project-internal checkpoints and implementation caveats.

It also contains environment-specific examples such as `~/Dokumenty` and `~/Pobrane`, which are useful during development but should not be presented as assumptions in a public quick-start.

## Publication structure to prepare

Public-facing documentation should be split into clear layers:

1. `README.md`
   - what FX11 Builder is,
   - what it is not,
   - supported/tested hosts,
   - legal/licensing summary,
   - minimal public quick-start,
   - links to detailed guides.

2. Public user guide / quick-start
   - path-agnostic,
   - user supplies a legitimate Windows ISO,
   - GParted acquisition/verification automated or clearly documented,
   - edition selection explained,
   - build/validate/write-to-USB workflow,
   - Secure Boot requirement stated clearly while unsigned development boot is used,
   - warnings around destructive USB writing.

3. Developer / maintainer guide
   - pytest,
   - QEMU/OVMF,
   - synthetic E2E,
   - deep audit,
   - implementation details,
   - local development workflow.

4. Internal history/checkpoints
   - keep project decision history and observed test evidence,
   - do not make checkpoint logs the primary documentation path for ordinary users.

## Release rule

Do not call the documentation publication-ready until the public README and user guide have been reviewed deliberately for:

- clarity,
- path independence,
- absence of machine-specific assumptions,
- current command accuracy,
- tested-vs-planned wording,
- licensing/provenance wording,
- Windows media redistribution policy,
- USB boot/write instructions,
- Secure Boot limitations.

The public docs review should happen after the current USB-hybrid boot fix is integrated, because USB creation instructions depend on the final output format.
