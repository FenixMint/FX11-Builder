# FX11 third-party compliance policy

This file records project rules for redistributing third-party software in FX11 installation media and releases.

## General rule

FX11 may include or redistribute third-party software only when its license permits the intended use and distribution model and when FX11 satisfies the corresponding notice/source/attribution obligations.

Do not assume that open-source means attribution-only.

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

## Release artifacts

A public release that redistributes a customized GParted Live environment should provide or reference, as legally appropriate:

- third-party notices,
- GPL text,
- corresponding source for GPL-covered distributed binaries,
- FX modifications/patches,
- exact upstream version/source provenance,
- SHA-256 hashes,
- build scripts sufficient to explain/reproduce the customization where practical.

## Supply-chain rule

Third-party boot/runtime artifacts must be pinned by version and hash. Do not silently fetch and embed mutable `latest` or branch-head binaries during a release build.

## Maintenance rule

When the upstream GParted/GParted Live version changes, review:

- license/notice changes,
- kernel/filesystem-tool changes,
- Secure Boot behavior,
- bootloader changes,
- regressions in NTFS/GPT/resize support,
- FX patch compatibility.
