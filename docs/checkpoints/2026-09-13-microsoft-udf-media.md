# Checkpoint — current Microsoft Windows 11 UDF media

Date: 2026-09-13

## Real source observed

The first genuine source used for FX11 testing is:

- file: `Win11_25H2_Polish_x64_v2.iso`
- SHA-256: `9453d410298e50c36ce31153326857848256e0980ff8fda501b4d3817540beb9`
- 7-Zip media type: `Udf`
- UDF version: `1.02`
- physical size: `8345856000` bytes
- source volume observed by xorriso: `CCCOMA_X64FRE_PL-PL_DV9`

The UDF tree contains at least:

- `sources/boot.wim` — 626224597 bytes
- `sources/install.wim` — 7437390947 bytes
- `boot/etfsboot.com` — 4096 bytes
- `efi/boot/bootx64.efi`
- `efi/microsoft/boot/efisys.bin`
- `efi/microsoft/boot/efisys_noprompt.bin`

## Failure discovered

`fx11 inspect` previously used xorriso to access `/sources/install.wim` or `/sources/install.esd` directly. On this current Microsoft image, xorriso sees only the very small ISO9660 side of the UDF bridge (`1 nodes read`) and therefore reports the Windows payload files as missing.

The El Torito entries are also hidden from xorriso's ISO filesystem tree. `xorriso -report_el_torito cmd` reports that neither the BIOS nor UEFI boot image is a normal data file that can be replayed. Therefore the old "open source ISO -> map changed files -> replay boot metadata" path is not sufficient for this source.

## Architecture decision

FX11 Builder must support current Microsoft UDF-first media rather than requiring an older or repacked source.

For a UDF source:

1. Detect UDF with `7z l -slt`.
2. Read individual WIM/ESD payloads through 7-Zip.
3. Extract the complete UDF tree to a temporary build directory.
4. Customize the extracted `boot.wim` and replace the selected install image with the single-image FX11 `install.wim`.
5. Stage FX11 provisioning, manifest, boot-manager and GParted files into the extracted tree.
6. Preserve Microsoft's `boot/etfsboot.com` as the BIOS El Torito image.
7. With GParted mainline enabled, replace the UEFI El Torito file `efi/microsoft/boot/efisys.bin` with the FX GRUB FAT image and also install FX GRUB as the filesystem fallback `efi/boot/bootx64.efi`.
8. Keep Microsoft's `efi/microsoft/boot/bootmgfw.efi` unchanged and chainload that file for the WinPE fallback. This avoids looping back into FX GRUB after `efi/boot/bootx64.efi` becomes the FX entry.
9. Rebuild a new ISO9660 level-3 image with explicit BIOS and UEFI El Torito entries. The large `install.wim` is supported by ISO level 3 rather than relying on the source UDF filesystem.

The existing xorriso replay path remains for conventional ISO9660 sources.

## Host dependency

`7z` / Debian-family package `7zip` is now a core FX11 Builder dependency because current Microsoft media can require UDF access. The Debian-family bootstrap and `fx11 doctor` were updated accordingly.

## Implementation state

Implemented in the current development line:

- `src/fx11/iso.py`: media-type detection, portable member extraction and full-tree extraction for UDF.
- `src/fx11/winpe_file.py`: customization of an already-extracted `boot.wim`.
- `src/fx11/builder.py`: UDF full-tree rebuild path while retaining the classic ISO replay path.
- `src/fx11/media_boot.py`: WinPE fallback now chainloads `efi/microsoft/boot/bootmgfw.efi` so `efi/boot/bootx64.efi` can safely become FX GRUB.
- `scripts/bootstrap-debian.sh` and `src/fx11/doctor.py`: `7zip` / `7z` dependency.
- tests updated for UDF detection and the non-looping Microsoft fallback path.

## Validation status

Do **not** yet claim a successful real UDF build. The implementation was committed after the first real-media failure and still requires:

1. CI/unit validation of the new code,
2. local `fx11 inspect` against the observed Microsoft UDF ISO,
3. the first complete FX11 build from that ISO,
4. structural `fx11 validate`,
5. UEFI QEMU/OVMF boot into both FX/GParted and Microsoft WinPE fallback,
6. later audit support for comparing a UDF source against the rebuilt FX11 output.

The earlier synthetic E2E remains valid for the conventional ISO source path and had already passed with exit code 0.
