# FX11 third-party compliance policy

This file records project rules for third-party code, software, ideas and redistributed components used by or materially influencing FX11.

## General rule

FX11 may include or redistribute third-party software only when its license permits the intended use and distribution model and when FX11 satisfies the corresponding notice/source/attribution obligations.

Do not assume that:

- public repository = permission to copy,
- open-source wording = complete licensing terms,
- attribution alone satisfies a copyleft license,
- branding a component makes it ours.

When licensing is unclear, use the project as research/inspiration only and do not import its source code until the license is verified.

## tiny11 / tiny11builder

FX11 should permanently acknowledge **NTDEV / ntdevlabs tiny11builder** as the inspiration that triggered the project.

Historical project origin:

- tiny11 demonstrated that a trimmed Windows 11 can remain useful and can perform better on weaker hardware,
- the initial FX11 problem statement was to build a transparent/reproducible equivalent direction from Linux,
- FX11 then expanded into its own partitioning, WinPE deployment, boot, privacy, audit and first-run architecture.

Upstream reference:

`https://github.com/ntdevlabs/tiny11builder`

### Licensing boundary

As checked on 2026-09-13, the upstream README describes tiny11builder as open-source, but the repository did not expose a root `LICENSE` file at the expected path.

Therefore, until upstream licensing is explicitly verified:

- do not copy tiny11builder PowerShell code into FX11,
- do not redistribute tiny11builder scripts as FX11 components,
- do not claim that tiny11 code is licensed for reuse merely because the repository is public,
- treat tiny11builder as inspiration, behavioral reference and comparison material,
- keep the acknowledgement visible in `README.md` and `ACKNOWLEDGEMENTS.md`.

If licensing later becomes explicit, re-audit before changing this boundary.

### FX11 independence

FX11 is not an official tiny11/NTDEV project and should never imply endorsement or affiliation.

The `tiny11-safe` FX11 profile name is historical acknowledgement of the direction that inspired it; its policy is maintained independently and intentionally differs from upstream tiny11builder.

## GParted / GParted Live

GParted is licensed under GNU GPL v2 or, at the user's option, any later version.

For a redistributed FX-branded GParted-based environment:

- retain applicable copyright notices,
- include the relevant GPL license text,
- make corresponding source available in a GPL-compliant way,
- publish FX patches/build scripts for GPL-covered modified components where required,
- preserve notices/licenses for bundled Debian/GParted Live packages,
- keep upstream GParted attribution visible,
- do not imply that upstream GParted authors endorse FX11,
- record the exact upstream version and hashes in the build/release manifest.

Preferred product wording:

**FX Partition Manager — powered by GParted**

The FX brand applies to the overall partitioning experience and surrounding integration. The underlying GParted application remains identified as third-party free software.

## Other redistributed/open-source components

FX11 builds on established tools including or potentially including:

- wimlib,
- xorriso,
- GRUB,
- QEMU,
- OVMF,
- GParted Live and its bundled storage/filesystem tools.

Each release/build path should record the component version and applicable license/provenance information. When binaries are redistributed, release packaging must satisfy the exact obligations of the corresponding license rather than applying a one-size-fits-all notice.

## Release artifacts

A public release that redistributes a customized GParted Live environment or other third-party binaries should provide or reference, as legally appropriate:

- third-party notices,
- applicable license texts,
- corresponding source where required,
- FX modifications/patches,
- exact upstream version/source provenance,
- SHA-256 hashes,
- build scripts sufficient to explain/reproduce the customization where practical.

## Supply-chain rule

Third-party boot/runtime artifacts must be pinned by version and hash. Do not silently fetch and embed mutable `latest` or branch-head binaries during a release build.

Research-only references should also be pinned in documentation when a particular upstream revision materially influenced an FX11 implementation decision.

## Branding rule

FX11 may brand the overall user experience, integration layer and original FX components. It must not remove attribution or make upstream third-party software appear to have been authored by FX11.

Preferred phrasing is explicit, e.g.:

- `FX Partition Manager — powered by GParted`
- `FX Boot Manager — based on GRUB`

## Maintenance rule

When an upstream third-party version changes, review:

- license/notice changes,
- source-distribution obligations,
- security advisories,
- bootloader/kernel/filesystem behavior,
- Secure Boot behavior,
- regressions relevant to FX11,
- FX patch compatibility.

## Documentation rule

If an upstream project materially influenced FX11, it belongs in `ACKNOWLEDGEMENTS.md` even when no source code is copied.

Honest provenance is part of the project's engineering standard.
