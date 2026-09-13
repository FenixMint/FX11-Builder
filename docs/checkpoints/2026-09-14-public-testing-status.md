# Public testing status — 2026-09-14

## Decision

FX11 Builder is publicly downloadable from the GitHub repository, but it is not a stable release yet.

The public project status is:

**TESTING / PRE-RELEASE**

The `main` branch may be cloned or downloaded as source for development and testing. It must not yet be presented as production-ready.

## Why

Real hardware validation is still in progress. In particular, the current milestone is validating:

- hybrid USB/UEFI boot behavior,
- the graphical FX GRUB experience,
- FX Partition Manager / GParted handoff,
- FX11 Installer / WinPE start,
- Continue-to-installer flow,
- full installation through OOBE and FX11 provisioning.

A successful synthetic build, structural ISO validation or partial physical boot is not enough to call the project stable.

## Distribution policy

GitHub distributes the FX11 Builder source code, tests and documentation only. Generated Windows installation ISOs and Microsoft Windows binaries are not published by the project. Users provide their own Microsoft installation media.

No stable GitHub Release should be published until the real-hardware installation path reaches the agreed release milestone. If a packaged release is published earlier for testers, it must be explicitly marked as a pre-release/testing build.

## README

The repository README now carries a prominent `TESTING / PRE-RELEASE` warning near the top so users see the project status before following build instructions.
