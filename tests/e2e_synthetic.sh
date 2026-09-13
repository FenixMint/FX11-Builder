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

xorriso -indev "$ROOT/output.iso" -ls '/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd' >/dev/null 2>&1
xorriso -indev "$ROOT/output.iso" -ls '/sources/$OEM$/$$/Setup/Scripts/FX11.ps1' >/dev/null 2>&1
xorriso -indev "$ROOT/output.iso" -ls '/FX11-manifest.json' >/dev/null 2>&1

echo "FX11 synthetic end-to-end build: PASS"
