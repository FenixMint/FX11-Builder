# Checkpoint — 2026-09-13 — real Windows 11 Home deep audit

## Observed local result

Source:
- `/home/hype/Pobrane/Win11_25H2_Polish_x64_v2.iso`
- Microsoft Windows 11 25H2 Polish x64 UDF media

Output:
- `/home/hype/Pobrane/FX11/FX11-25H2-PL-x64-Home-test2.iso`
- SHA-256: `4cb0b97e396441f6271c659a51245d89d8e6caaa0844f400edb90d04dc2936cd`

Before the audit:
- `pytest tests/test_audit.py`: 6 passed
- full `pytest`: 67 passed
- `fx11 validate`: VALID
- El Torito contains BIOS `/boot/etfsboot.com` and UEFI `/efi/microsoft/boot/efisys.bin`
- UEFI El Torito load size: 16 MiB
- direct `sha256sum` exactly matches the generated `.sha256` file

Deep audit completed successfully in about 3m33s:
- schema: `fx11-iso-delta-v2`
- source ISO files: 1064
- output ISO files: 1075
- ISO paths added: 11
- ISO paths removed: 0
- selected source WIM paths: 176302
- output WIM paths: 176302
- WIM paths added: 0
- WIM paths removed: 0
- WIM path inventory identical: YES

This is an important checkpoint: the selected Windows 11 Home image has the same path inventory before and after the Builder export. Current FX11 customizations are still staged outside `install.wim` for runtime provisioning, as intended.

## One audit classification issue

The first successful v2 audit reported one `unexpected_added` path:

`/efi/microsoft/boot/bootmgfw.efi`

This is not an unknown payload. It is an intentional media-preservation copy introduced by the UDF boot-fallback fix: when the Microsoft UDF source exposes the signed loader at `/efi/boot/bootx64.efi` but does not separately expose `/efi/microsoft/boot/bootmgfw.efi`, FX11 copies the original Microsoft bytes to the latter path before development GRUB takes ownership of `/efi/boot/bootx64.efi`.

The audit is being tightened so this path is classified as expected **only after proving that its SHA-256 is byte-identical to the source Microsoft `/efi/boot/bootx64.efi`**. If the bytes differ, it remains unexpected.

## CI status

The preceding audit/wimdir fix commit `d794f61b5e3e56be232dc42f8a16663c74634028` is green in GitHub Actions:
- unit: success
- Debian 13 smoke: success
- doctor: success
- synthetic E2E: success

## Next gate

Re-run the audit after the byte-identity preservation classifier lands. Desired result:
- `Unexpected added: 0`
- WIM inventory same: YES
- media preservation explicitly records `/efi/microsoft/boot/bootmgfw.efi` as byte-identical to source `/efi/boot/bootx64.efi`

After that, proceed to OVMF/QEMU runtime boot testing of FX GRUB, GParted mainline, and WinPE fallback.
