# OS11vLIN

Linux-native Windows 11 image builder inspired by the tiny11maker approach.

The goal is to build reproducible and auditable Windows 11 installation media on Linux while keeping the source ISO untouched.

## V1 scope

V1 uses a conservative `tiny11-safe + privacy-balanced` profile:

- inspect the Linux host and required tools,
- inspect a Windows 11 ISO before making changes,
- preview planned changes with a dry run,
- remove only explicitly allowed consumer/bloat packages,
- apply privacy settings without disabling Windows Update, Defender, Microsoft Store, SmartScreen or core servicing,
- rebuild and validate bootable media,
- test generated images in QEMU/UEFI,
- support Linux Mint, LMDE and Debian as first-class hosts.

## Safety principles

1. The source ISO is never modified in place.
2. Every modification is declared in a profile and recorded in a build manifest.
3. Protected Windows components are blocked from removal by policy.
4. V1 uses a conservative profile rather than aggressive debloating.
5. Every build stage should be independently testable.

## Current status

Initial V1 foundation. Host diagnostics and profile planning are implemented first. WIM/ISO mutation follows only after the baseline pipeline is covered by tests.

## Development

Python 3.11+ is required.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'

os11vlin doctor
os11vlin profiles
os11vlin plan --profile tiny11-safe --profile privacy-balanced
pytest
```

## Planned external tools

Core build path:

- `wimlib-imagex` (`wimtools` on Debian-family distributions)
- `xorriso`
- `7z`
- `rsync`
- `sha256sum`

VM validation:

- `qemu-system-x86_64`
- OVMF/UEFI firmware

## Legal note

No Microsoft binaries are distributed by this project. Users must provide their own Windows installation media and comply with the applicable Microsoft license terms.
