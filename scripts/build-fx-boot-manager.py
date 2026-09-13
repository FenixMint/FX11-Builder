#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from fx11.bootmanager import build_unsigned_payload
from fx11.iso import BuilderError


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the current unsigned FX Boot Manager UEFI payload")
    parser.add_argument("output", type=Path, help="Directory that will receive EFI/FX11")
    parser.add_argument("--esp-uuid", help="Filesystem UUID of the ESP that contains FX11 Windows Boot Manager")
    parser.add_argument("--timeout", type=int, default=5, help="Boot-menu timeout in seconds")
    parser.add_argument("--background", type=Path, help="Optional PNG background for the FX11 GRUB theme")
    args = parser.parse_args()
    try:
        payload = build_unsigned_payload(
            args.output,
            fx11_esp_uuid=args.esp_uuid,
            timeout_seconds=args.timeout,
            background=args.background,
        )
    except BuilderError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print("FX BOOT MANAGER DEV PAYLOAD")
    print(f"EFI    : {payload.efi_binary}")
    print(f"Config : {payload.grub_config}")
    print(f"Theme  : {payload.theme_config}")
    print("Secure Boot: OFF required for this development payload")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
