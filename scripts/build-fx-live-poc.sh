#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: sudo bash scripts/build-fx-live-poc.sh <lmde7.iso> <fx-live-poc.iso>" >&2
    exit 2
fi

SOURCE_ISO=$(readlink -f "$1")
OUTPUT_ISO=$(readlink -m "$2")
REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OVERLAY="$REPO_ROOT/live-overlay"

if [[ $EUID -ne 0 ]]; then
    echo "This prototype builder must run as root because it enters the live root filesystem." >&2
    exit 1
fi

for cmd in xorriso unsquashfs mksquashfs chroot mount umount rsync; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "Missing required command: $cmd" >&2
        exit 1
    }
done

[[ -f "$SOURCE_ISO" ]] || {
    echo "Source ISO not found: $SOURCE_ISO" >&2
    exit 1
}
[[ -d "$OVERLAY" ]] || {
    echo "FX Live overlay not found: $OVERLAY" >&2
    exit 1
}

WORK=$(mktemp -d -t fx-live-poc.XXXXXX)
ISO_TREE="$WORK/iso"
ROOTFS="$WORK/rootfs"
mkdir -p "$ISO_TREE" "$ROOTFS"

mounted=()
cleanup() {
    set +e
    for (( i=${#mounted[@]}-1; i>=0; i-- )); do
        umount -l "${mounted[$i]}" 2>/dev/null || true
    done
    rm -rf "$WORK"
}
trap cleanup EXIT INT TERM

echo "[1/7] Extracting LMDE ISO tree..."
xorriso -osirrox on -indev "$SOURCE_ISO" -extract / "$ISO_TREE" >/dev/null

SQUASH=$(find "$ISO_TREE" -type f -name filesystem.squashfs -print -quit)
if [[ -z "$SQUASH" ]]; then
    echo "Could not find filesystem.squashfs in the source ISO." >&2
    exit 1
fi
SQUASH_REL="/${SQUASH#"$ISO_TREE"/}"

echo "[2/7] Unpacking live root filesystem: $SQUASH_REL"
unsquashfs -d "$ROOTFS" "$SQUASH" >/dev/null

mount --bind /dev "$ROOTFS/dev"
mounted+=("$ROOTFS/dev")
mount -t proc proc "$ROOTFS/proc"
mounted+=("$ROOTFS/proc")
mount -t sysfs sysfs "$ROOTFS/sys"
mounted+=("$ROOTFS/sys")
mount -t devpts devpts "$ROOTFS/dev/pts"
mounted+=("$ROOTFS/dev/pts")

if [[ -e "$ROOTFS/etc/resolv.conf" || -L "$ROOTFS/etc/resolv.conf" ]]; then
    cp -a "$ROOTFS/etc/resolv.conf" "$ROOTFS/etc/resolv.conf.fx-original"
fi
rm -f "$ROOTFS/etc/resolv.conf"
cp -L /etc/resolv.conf "$ROOTFS/etc/resolv.conf"

echo "[3/7] Installing Calamares prototype dependencies inside LMDE..."
chroot "$ROOTFS" /usr/bin/env DEBIAN_FRONTEND=noninteractive bash -lc '
    set -e
    apt-get update
    apt-get install -y --no-install-recommends \
        calamares \
        calamares-settings-debian \
        zenity \
        pkexec
    apt-get clean
    rm -rf /var/lib/apt/lists/*
'

rm -f "$ROOTFS/etc/resolv.conf"
if [[ -e "$ROOTFS/etc/resolv.conf.fx-original" || -L "$ROOTFS/etc/resolv.conf.fx-original" ]]; then
    mv "$ROOTFS/etc/resolv.conf.fx-original" "$ROOTFS/etc/resolv.conf"
fi

for (( i=${#mounted[@]}-1; i>=0; i-- )); do
    umount "${mounted[$i]}"
done
mounted=()

echo "[4/7] Applying FX Live overlay..."
rsync -a "$OVERLAY/" "$ROOTFS/"
chmod 0755 "$ROOTFS/usr/local/bin/fx-live-launcher"
mkdir -p "$ROOTFS/etc/fx"
printf '%s\n' 'FX Live PoC — LMDE 7 base, Calamares profile routing, non-destructive prototype' \
    > "$ROOTFS/etc/fx/live-poc"

COMPRESSION=$(unsquashfs -s "$SQUASH" 2>/dev/null | awk 'tolower($1)=="compression" {print tolower($2); exit}')
case "$COMPRESSION" in
    xz|zstd|gzip|lzo|lz4) ;;
    *) COMPRESSION=xz ;;
esac

echo "[5/7] Rebuilding SquashFS with compression: $COMPRESSION"
NEW_SQUASH="$WORK/filesystem.squashfs"
mksquashfs "$ROOTFS" "$NEW_SQUASH" -noappend -comp "$COMPRESSION" >/dev/null

echo "[6/7] Replacing live filesystem and replaying original boot equipment..."
rm -f "$OUTPUT_ISO"
xorriso \
    -indev "$SOURCE_ISO" \
    -outdev "$OUTPUT_ISO" \
    -boot_image any replay \
    -map "$NEW_SQUASH" "$SQUASH_REL" \
    -commit >/dev/null

echo "[7/7] Basic image checks..."
xorriso -indev "$OUTPUT_ISO" -toc >/dev/null
sha256sum "$OUTPUT_ISO"

echo
echo "FX Live PoC created: $OUTPUT_ISO"
echo "Status: build artifact only; boot, Calamares profiles and physical hardware are not validated yet."
