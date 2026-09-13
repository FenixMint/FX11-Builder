# Acknowledgements

FX11 is built in public and should be explicit about the projects that influenced it or provide components used by it.

## tiny11 / tiny11builder

The original idea for FX11 came directly from practical experience with **tiny11**: a trimmed Windows 11 installation can be noticeably more usable on weaker hardware than the stock experience.

The upstream project that inspired the first FX11 direction is:

- **tiny11builder** by **NTDEV / ntdevlabs**
- repository: `https://github.com/ntdevlabs/tiny11builder`

FX11 began from the question:

> tiny11 works; can we build a transparent, reproducible version of that idea from Linux and then take the installation experience further?

That historical relationship should remain visible in this repository.

### What FX11 took from the idea

The influence is primarily conceptual and practical:

- Windows 11 can be made lighter by removing non-essential consumer components,
- aggressive removal must be balanced against serviceability,
- the builder should let the user choose the Windows image/SKU,
- lightweight Windows is particularly valuable on older or weaker hardware,
- reproducible builder scripts are preferable to distributing opaque prebuilt Windows images.

### What FX11 changed

FX11 is not intended as a straight port of tiny11builder. It is being developed as an independent Linux-native implementation with its own architecture, including:

- Linux-hosted build pipeline,
- source/injected-file hashing and manifesting,
- conservative removal policy,
- stronger preservation of servicing/security components by default,
- separate privacy policy,
- static and runtime-audit direction,
- FX-controlled WinPE startup and direct image deployment,
- FX Partition Manager,
- GParted-based graphical partitioning line with explicit attribution,
- native FX text partition manager retained as fallback/development path,
- FX Boot Manager / GRUB multi-OS path,
- explicit unsupported-hardware warn/explain/allow policy,
- FX11 First Run and Control Center roadmap.

### Source-code licensing boundary

At the time this acknowledgement was written (2026-09-13), the upstream `ntdevlabs/tiny11builder` repository README described the project as open-source, but the repository did not expose a `LICENSE` file at the expected root path when checked.

For that reason, FX11 treats tiny11builder as an **inspiration/research reference**, not as a source-code dependency. FX11 should not copy or redistribute upstream script code unless its licensing terms are explicitly verified first.

If upstream licensing becomes explicit later, this note should be rechecked and updated rather than silently assumed.

## GParted / GParted Live

The primary graphical FX Partition Manager direction is based on GParted/GParted Live.

User-facing wording should remain clear:

**FX Partition Manager — powered by GParted**

FX branding applies to the surrounding FX installation experience. GParted remains third-party free software and its authorship, license notices and source obligations must be preserved.

See `docs/THIRD_PARTY_COMPLIANCE.md` and `docs/FX_PARTITION_MANAGER_GPARTED.md`.

## Other upstream tools

FX11 also depends on or is designed around established open-source tools such as:

- wimlib,
- xorriso,
- GRUB,
- QEMU,
- OVMF,
- GParted and its underlying storage/filesystem utilities.

These projects should remain credited in release/build documentation and are governed by their own licenses.

## Project rule

If FX11 materially benefits from another open-source project, implementation, published research or reusable component, acknowledgement should be added rather than minimized.

Good provenance is part of the product, not paperwork added at the end.
