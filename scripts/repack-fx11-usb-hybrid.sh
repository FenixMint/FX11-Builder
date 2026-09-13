#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/repack-fx11-usb-hybrid.sh INPUT_FX11.iso OUTPUT_HYBRID.iso

Rebuilds an already-generated FX11 ISO with a GPT EFI System Partition view of
the current FX11 UEFI media image. During repack it refreshes the staged FX11
GRUB configuration, graphical theme and BOOTX64.EFI so boot changes can be
tested without rebuilding install.wim or boot.wim.
EOF
}

if [[ $# -ne 2 ]]; then
  usage
  exit 2
fi

INPUT=$1
OUTPUT=$2

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: input ISO does not exist: $INPUT" >&2
  exit 1
fi

if [[ -e "$OUTPUT" ]]; then
  echo "ERROR: output already exists: $OUTPUT" >&2
  echo "Choose a new output filename." >&2
  exit 1
fi

for tool in 7z xorriso sha256sum grub-mkstandalone mformat mmd mcopy mdir; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "ERROR: required tool is missing: $tool" >&2
    exit 1
  fi
done

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
PYTHON="$REPO_ROOT/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  PYTHON=$(command -v python3 || true)
fi
if [[ -z "$PYTHON" ]]; then
  echo "ERROR: Python 3 is required to refresh the FX11 media boot payload." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
TMP=$(mktemp -d -t fx11-usb-hybrid-XXXXXX)
trap 'rm -rf "$TMP"' EXIT
TREE="$TMP/tree"
mkdir -p "$TREE"

echo "=== FX11 USB HYBRID REPACK ==="
echo "Input : $INPUT"
echo "Output: $OUTPUT"
echo

echo "=== 1. Extracting ISO filesystem ==="
7z x -y "-o$TREE" "$INPUT"

BIOS="$TREE/boot/etfsboot.com"
UEFI="$TREE/efi/microsoft/boot/efisys.bin"
WIN_FALLBACK="$TREE/efi/microsoft/boot/bootmgfw.efi"
REMOVABLE_EFI="$TREE/efi/boot/bootx64.efi"
MEDIA_GRUB="$TREE/FX11/media/grub.cfg"
MEDIA_EFI_STAGED="$TREE/FX11/media/efiboot.img"
MEDIA_THEME_DIR="$TREE/FX11/media/theme"

if [[ ! -f "$BIOS" ]]; then
  echo "ERROR: missing BIOS El Torito image after extraction: $BIOS" >&2
  exit 1
fi
if [[ ! -f "$UEFI" ]]; then
  echo "ERROR: missing UEFI El Torito image after extraction: $UEFI" >&2
  exit 1
fi
if [[ ! -s "$WIN_FALLBACK" ]]; then
  echo "ERROR: preserved Microsoft WinPE EFI loader is missing: $WIN_FALLBACK" >&2
  exit 1
fi
if [[ ! -f "$MEDIA_GRUB" ]]; then
  echo "ERROR: missing staged FX11 media GRUB config after extraction: $MEDIA_GRUB" >&2
  exit 1
fi

echo
echo "=== 2. Refreshing FX11 media menu, theme and EFI image ==="
PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" \
  "$PYTHON" - "$MEDIA_GRUB" "$MEDIA_THEME_DIR" "$TMP/media-efi" "$UEFI" "$REMOVABLE_EFI" "$MEDIA_EFI_STAGED" <<'PY'
from pathlib import Path
import shutil
import sys

from fx11.media_boot import build_media_grub_config
from fx11.media_efi import build_media_efi_payload
from fx11.media_theme import build_media_theme

grub_path = Path(sys.argv[1])
theme_dir = Path(sys.argv[2])
efi_work = Path(sys.argv[3])
uefi_path = Path(sys.argv[4])
removable_path = Path(sys.argv[5])
staged_path = Path(sys.argv[6])

grub_path.write_text(build_media_grub_config().grub_config, encoding="utf-8")
theme = build_media_theme(theme_dir)
efi = build_media_efi_payload(efi_work, theme=theme)

uefi_path.parent.mkdir(parents=True, exist_ok=True)
removable_path.parent.mkdir(parents=True, exist_ok=True)
staged_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(efi.image, uefi_path)
shutil.copy2(efi.efi_binary, removable_path)
shutil.copy2(efi.image, staged_path)

print(f"Updated menu : {grub_path}")
print(f"Theme config : {theme.theme_config}")
print(f"Background   : {theme.background}")
print(f"FX11 logo    : {theme.logo}")
print(f"GRUB font    : {theme.font}")
print(f"EFI image    : {uefi_path}")
print(f"BOOTX64.EFI  : {removable_path}")
PY

THEME_CONFIG="$MEDIA_THEME_DIR/theme.txt"
THEME_BACKGROUND="$MEDIA_THEME_DIR/background.png"
THEME_LOGO="$MEDIA_THEME_DIR/logo.png"
THEME_FONT="$MEDIA_THEME_DIR/unicode.pf2"
for required in "$THEME_CONFIG" "$THEME_BACKGROUND" "$THEME_LOGO" "$THEME_FONT" "$UEFI" "$REMOVABLE_EFI"; do
  if [[ ! -s "$required" ]]; then
    echo "ERROR: refreshed FX11 media asset missing: $required" >&2
    exit 1
  fi
done

# The same theme is embedded in the EFI FAT partition so GRUB does not depend
# on ISO-relative theme loading on real firmware.
for efi_asset in \
  ::/EFI/BOOT/BOOTX64.EFI \
  ::/EFI/FX11/theme/theme.txt \
  ::/EFI/FX11/theme/background.png \
  ::/EFI/FX11/theme/logo.png \
  ::/EFI/FX11/theme/unicode.pf2; do
  if ! mdir -i "$UEFI" "$efi_asset" >/dev/null 2>&1; then
    echo "ERROR: refreshed EFI image is missing $efi_asset" >&2
    exit 1
  fi
done

echo
echo "=== 3. Rebuilding with GPT EFI System Partition metadata ==="
xorriso \
  -as mkisofs \
  -iso-level 3 \
  -J \
  -joliet-long \
  -V FX11 \
  -c boot/boot.cat \
  -b boot/etfsboot.com \
  -no-emul-boot \
  -boot-load-size 8 \
  -eltorito-alt-boot \
  -e efi/microsoft/boot/efisys.bin \
  -no-emul-boot \
  -efi-boot-part --efi-boot-image \
  -o "$OUTPUT" \
  "$TREE"

echo
echo "=== 4. Verifying System Area ==="
SYSTEM_REPORT="$TMP/system-area.txt"
xorriso -indev "$OUTPUT" -report_system_area plain 2>&1 | tee "$SYSTEM_REPORT"

if ! grep -qi "GPT" "$SYSTEM_REPORT"; then
  echo "ERROR: rebuilt ISO does not report GPT metadata." >&2
  exit 1
fi

if ! grep -Eqi "EFI|ESP|System Partition" "$SYSTEM_REPORT"; then
  echo "ERROR: rebuilt ISO does not report an EFI partition." >&2
  exit 1
fi

echo
echo "=== 5. Verifying El Torito ==="
xorriso -indev "$OUTPUT" -report_el_torito plain

echo
echo "=== 6. Verifying refreshed FX boot menu and theme ==="
if ! grep -q "gl_batch" "$MEDIA_GRUB"; then
  echo "ERROR: refreshed media GRUB config does not enable GParted batch graphics mode." >&2
  exit 1
fi
if ! grep -q "chainloader .*bootmgfw.efi" "$MEDIA_GRUB"; then
  echo "ERROR: refreshed media GRUB config does not target the preserved Microsoft EFI loader." >&2
  exit 1
fi
if ! grep -q "background_image" "$MEDIA_GRUB"; then
  echo "ERROR: refreshed media GRUB config has no graphical background fallback." >&2
  exit 1
fi
if ! grep -q "EFI/FX11/theme/theme.txt" "$MEDIA_GRUB"; then
  echo "ERROR: refreshed media GRUB config does not prefer the EFI-resident FX11 theme." >&2
  exit 1
fi
if ! grep -q 'file = "logo.png"' "$THEME_CONFIG"; then
  echo "ERROR: FX11 logo is not wired into the GRUB theme." >&2
  exit 1
fi
if ! grep -q 'text = "Fenix"' "$THEME_CONFIG"; then
  echo "ERROR: FX11 theme author mark is missing." >&2
  exit 1
fi

echo
echo "=== 7. SHA-256 ==="
sha256sum "$OUTPUT" | tee "$OUTPUT.sha256"

echo
echo "USB-HYBRID REPACK VALID"
echo "ISO: $OUTPUT"
echo "SUM: $OUTPUT.sha256"
echo
echo "Next: raw-write this ISO to USB, verify the copy byte-for-byte, then test UEFI boot."
