# Local checkpoint — GParted payload verified

Date: 2026-09-13

This checkpoint records the user's local validation state before the first real FX11 ISO build with the GParted mainline path.

## Confirmed locally

Host:

- Linux Mint 22.3
- x86_64
- kernel 7.0.0-31-generic

On repository state `38cf18d` the user ran the current unit suite and observed:

- focused GParted/media tests: 8 passed
- full unit suite: 53 passed
- `fx11 doctor`: READY

The pinned GParted Live image was downloaded successfully:

- file: `gparted-live-1.8.1-6-amd64.iso`
- size reported by the download: 720371712 bytes
- SHA-256 observed locally: `d789c38779f0d6f7026c12f44c2c52a04f66e28a1aea7d51f3045ad1bbf28411`

This exactly matches the FX11 pinned input.

`mtools` was already installed locally.

## Important incomplete item

The later pull containing the first FX UEFI/El Torito takeover work did **not** complete because the user's local `scripts/bootstrap-debian.sh` had uncommitted changes. Git correctly refused to overwrite them.

Therefore:

- `tests/test_media_efi.py` was not present in the user's checkout yet,
- the subsequent 53-test run still tested the older local checkout,
- the new FX UEFI media-boot code must not yet be considered locally validated.

Next action: preserve/stash the local bootstrap change, fast-forward to current `main`, rerun the focused media EFI/GParted tests and then the full suite.
