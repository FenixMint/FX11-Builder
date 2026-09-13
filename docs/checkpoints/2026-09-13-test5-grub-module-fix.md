# Test5 GRUB module compatibility fix — 2026-09-13

## Observed on Linux Mint host

The test5 preparation stopped before producing a valid ISO. Focused tests reported 15 passed / 1 failed, and the repack then failed at the same point while rebuilding the FX11 media BOOTX64.EFI.

Exact failure:

`grub-mkstandalone: cannot open /usr/lib/grub/x86_64-efi/search_file.mod: No such file or directory`

The physical USB still contained test4 at that moment; test5 was not written to USB.

## Cause

The explicit GRUB module list used the non-existent module name `search_file`. On the Mint/Ubuntu GRUB packaging used by the test host, file-based `search --file` support is provided by `search_fs_file.mod`.

## Fix

- Replaced `search_file` with `search_fs_file` in the standalone EFI module list.
- Replaced `insmod search_file` with `insmod search_fs_file` in the staged media GRUB configuration.
- Added regression tests that reject the old module name.
- Kept all other test5 changes unchanged: graphical theme in FX11BOOT, preserved Microsoft `bootmgfw.efi` WinPE target, and the GParted Continue-to-Installer handoff hook.

## Status

Code fix is committed. Runtime/build confirmation is still required on the Mint host. Do not call test5 valid until the focused tests pass and `repack-fx11-usb-hybrid.sh` reaches `USB-HYBRID REPACK VALID`.
