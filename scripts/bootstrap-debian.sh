#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This bootstrap script supports Debian-family hosts (Debian, LMDE, Linux Mint)." >&2
  exit 2
fi

sudo apt-get update
sudo apt-get install -y \
  python3 \
  python3-venv \
  python3-pip \
  wimtools \
  xorriso \
  grub-efi-amd64-bin \
  mtools \
  qemu-system-x86 \
  ovmf

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

printf '\nFX11 Builder installed in %s/.venv\n' "$PWD"
printf 'Activate with: . .venv/bin/activate\n'
printf 'Then run: fx11 doctor\n'
