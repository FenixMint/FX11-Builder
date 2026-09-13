# Checkpoint — 2026-09-13 — project origin and wider FX roadmap

## tiny11 acknowledgement

Decision: FX11 will explicitly acknowledge NTDEV / ntdevlabs tiny11builder in public GitHub documentation.

Historical origin:

- tiny11 proved in practice that a trimmed Windows 11 can be useful on weaker hardware,
- the original FX11 need was a Linux-native builder for that general class of result,
- FX11 subsequently evolved beyond that starting point into its own architecture.

FX11 must not hide or rewrite that origin story.

## Independence and licensing boundary

FX11 is an independent implementation, not an official tiny11/NTDEV project.

As checked on this date, `ntdevlabs/tiny11builder` describes itself as open-source in the README, but a root `LICENSE` file was not available at the expected repository path.

Decision: until licensing is explicitly verified, tiny11builder is inspiration/research/reference only. Do not copy or redistribute its script source as FX11 code.

Public acknowledgement lives in:

- `README.md`,
- `ACKNOWLEDGEMENTS.md`,
- `docs/THIRD_PARTY_COMPLIANCE.md`.

## GParted consistency

The same honesty rule applies to FX Partition Manager.

Main graphical line:

**FX Partition Manager — powered by GParted**

The native FX text partition manager remains available as:

- fallback,
- recovery path,
- independent future development path.

## Linux build-host expansion

Current maintained builder hosts remain:

- Linux Mint,
- LMDE,
- Debian.

Direction: make FX11 Builder progressively distro-neutral by separating core capability checks from package-manager adapters.

Candidate next families:

- Ubuntu,
- Fedora,
- openSUSE,
- Arch-family.

No distro is declared supported until the real builder/test path is validated there.

## Future FX Linux

If FX11 proves successful/stable, explore a sibling project called **FX Linux**.

This is a future direction, not current scope.

FX Linux should inherit the FX principles:

- Your System. Your Rules.,
- transparent/reversible choices,
- visible upstream provenance,
- honest licensing,
- strong multi-OS support,
- reproducible builds,
- sensible support for weaker hardware.

No Linux base distribution is selected yet.

FX Linux should become a separate repository/product rather than expanding FX11 Builder into a mixed-purpose repository.

Detailed roadmap: `docs/ROADMAP.md`.
