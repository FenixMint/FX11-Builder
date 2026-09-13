#!/usr/bin/env bash
set -euo pipefail

ROOT="$(mktemp -d)"
trap 'rm -rf "$ROOT"' EXIT

mkdir -p "$ROOT/home/Windows" "$ROOT/pro/Windows"
mkdir -p "$ROOT/iso/sources" "$ROOT/iso/boot" "$ROOT/iso/efi/microsoft/boot"
printf 'synthetic-home\n' > "$ROOT/home/Windows/edition.txt"
printf 'synthetic-pro\n' > "$ROOT/pro/Windows/edition.txt"

wimlib-imagex capture \
  "$ROOT/home" "$ROOT/iso/sources/install.wim" \
  "Windows 11 Home" "Synthetic Windows 11 Home" \
  --compress=XPRESS --no-acls \
  --image-property=WINDOWS/EDITIONID=Core \
  --image-property=WINDOWS/ARCH=9

wimlib-imagex append \
  "$ROOT/pro" "$ROOT/iso/sources/install.wim" \
  "Windows 11 Pro" "Synthetic Windows 11 Pro" \
  --compress=XPRESS --no-acls \
  --image-property=WINDOWS/EDITIONID=Professional \
  --image-property=WINDOWS/ARCH=9

cp "$ROOT/iso/sources/install.wim" "$ROOT/iso/sources/boot.wim"
dd if=/dev/zero of="$ROOT/iso/boot/etfsboot.com" bs=2048 count=1 status=none
dd if=/dev/zero of="$ROOT/iso/efi/microsoft/boot/efisys.bin" bs=1M count=1 status=none

xorriso -as mkisofs \
  -iso-level 3 \
  -V SYNTHWIN11 \
  -b boot/etfsboot.com -no-emul-boot -boot-load-size 4 \
  -eltorito-alt-boot \
  -e efi/microsoft/boot/efisys.bin -no-emul-boot \
  -o "$ROOT/source.iso" \
  "$ROOT/iso" >/dev/null 2>&1

fx11 inspect "$ROOT/source.iso" | tee "$ROOT/inspect.txt"
grep -q "Windows 11 Home" "$ROOT/inspect.txt"
grep -q "Windows 11 Pro" "$ROOT/inspect.txt"

fx11 build "$ROOT/source.iso" --index 2 -o "$ROOT/output.iso"
fx11 validate "$ROOT/output.iso"
test -s "$ROOT/output.iso.sha256"

xorriso -osirrox on -indev "$ROOT/output.iso" -extract /sources/install.wim "$ROOT/output-install.wim" >/dev/null 2>&1
wimlib-imagex info "$ROOT/output-install.wim" --xml > "$ROOT/output.xml"

python3 - "$ROOT/output.xml" <<'PY'
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

raw = Path(sys.argv[1]).read_bytes()
text = raw.decode("utf-16")
root = ET.fromstring(text)
images = root.findall("IMAGE")
assert len(images) == 1, f"expected one exported image, got {len(images)}"
assert images[0].findtext("NAME") == "Windows 11 Pro"
assert images[0].findtext("WINDOWS/EDITIONID") == "Professional"
PY

xorriso -osirrox on -indev "$ROOT/output.iso" -extract /sources/boot.wim "$ROOT/output-boot.wim" >/dev/null 2>&1
mkdir -p "$ROOT/boot-check"
wimlib-imagex extract "$ROOT/output-boot.wim" 2 \
  /Windows/System32/startnet.cmd \
  /Windows/System32/winpeshl.ini \
  /FX11/fx11-launch.cmd \
  /FX11/fx11-partition.cmd \
  /FX11/fx11-install.cmd \
  --dest-dir="$ROOT/boot-check" --no-acls >/dev/null

# WIM paths are Windows-case-insensitive, while Debian's filesystem is not.
# Resolve extracted names case-insensitively so this validates the payload,
# not wimlib's preserved filename casing on the Linux host.
find_one() {
  local name="$1"
  local found
  found="$(find "$ROOT/boot-check" -type f -iname "$name" -print -quit)"
  if [ -z "$found" ]; then
    echo "Missing extracted WinPE payload file: $name" >&2
    find "$ROOT/boot-check" -type f -print >&2 || true
    exit 2
  fi
  printf '%s\n' "$found"
}

assert_contains_ci() {
  local file="$1"
  local literal="$2"
  local label="$3"
  if ! grep -Fqi -- "$literal" "$file"; then
    echo "WinPE payload assertion failed: $label" >&2
    echo "Expected literal: $literal" >&2
    echo "File: $file" >&2
    echo "----- file contents -----" >&2
    cat "$file" >&2 || true
    echo "-------------------------" >&2
    exit 3
  fi
}

STARTNET_FILE="$(find_one startnet.cmd)"
WINPESHL_FILE="$(find_one winpeshl.ini)"
LAUNCHER_FILE="$(find_one fx11-launch.cmd)"
PARTITION_FILE="$(find_one fx11-partition.cmd)"
INSTALL_FILE="$(find_one fx11-install.cmd)"

assert_contains_ci "$STARTNET_FILE" 'wpeinit' 'startnet initializes WinPE'
assert_contains_ci "$STARTNET_FILE" 'FX11\fx11-launch.cmd' 'startnet hands off to FX11 launcher'
assert_contains_ci "$WINPESHL_FILE" 'startnet.cmd' 'winpeshl starts startnet'
assert_contains_ci "$LAUNCHER_FILE" 'Start FX Partition Manager' 'launcher exposes FX Partition Manager'
assert_contains_ci "$PARTITION_FILE" 'Continue directly to FX11 installation' 'partition manager can hand off to installer'
assert_contains_ci "$INSTALL_FILE" 'dism /Apply-Image' 'installer applies the Windows image'
assert_contains_ci "$INSTALL_FILE" 'bcdboot W:\Windows /s S: /f UEFI' 'installer writes Windows UEFI boot files'

xorriso -indev "$ROOT/output.iso" -ls '/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd' >/dev/null 2>&1
xorriso -indev "$ROOT/output.iso" -ls '/sources/$OEM$/$$/Setup/Scripts/FX11.ps1' >/dev/null 2>&1
xorriso -indev "$ROOT/output.iso" -ls '/FX11-manifest.json' >/dev/null 2>&1

echo "FX11 synthetic end-to-end build with partition-to-installer handoff: PASS"
