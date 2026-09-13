#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/repack-fx11-usb-hybrid.sh INPUT_FX11.iso OUTPUT_HYBRID.iso

Rebuilds an already-generated FX11 ISO with a GPT EFI System Partition view of
the existing UEFI El Torito image. During repack it refreshes the staged FX11
media GRUB configuration from the current checkout, so boot-menu fixes can be
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

for tool in 7z xorriso sha256sum; do
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
  echo "ERROR: Python 3 is required to refresh the FX11 media GRUB configuration." >&2
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
MEDIA_GRUB="$TREE/FX11/media/grub.cfg"

if [[ ! -f "$BIOS" ]]; then
  echo "ERROR: missing BIOS El Torito image after extraction: $BIOS" >&2
  exit 1
fi
if [[ ! -f "$UEFI" ]]; then
  echo "ERROR: missing UEFI El Torito image after extraction: $UEFI" >&2
  exit 1
fi
if [[ ! -f "$MEDIA_GRUB" ]]; then
  echo "ERROR: missing staged FX11 media GRUB config after extraction: $MEDIA_GRUB" >&2
  exit 1
fi

echo
echo "=== 2. Refreshing FX11 media boot menu ==="
PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" \
  "$PYTHON" - "$MEDIA_GRUB" <<'PY'
from pathlib import Path
import sys

from fx11.media_boot import build_media_grub_config

path = Path(sys.argv[1])
path.write_text(build_media_grub_config().grub_config, encoding="utf-8")
print(f"Updated: {path}")
PY

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
echo "=== 6. Verifying refreshed FX boot menu ==="
if ! grep -q "gl_batch" "$MEDIA_GRUB"; then
  echo "ERROR: refreshed media GRUB config does not enable GParted batch graphics mode." >&2
  exit 1
fi
if ! grep -q "chainloader .*bootmgr.efi" "$MEDIA_GRUB"; then
  echo "ERROR: refreshed media GRUB config does not target /bootmgr.efi for WinPE fallback." >&2
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
