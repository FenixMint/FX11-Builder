#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from fx11.gparted import GPARTED_LIVE, verify_gparted_live
from fx11.iso import BuilderError


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the pinned GParted Live input for FX11 Builder")
    parser.add_argument("iso", type=Path, help=f"Expected file: {GPARTED_LIVE.filename}")
    args = parser.parse_args()

    try:
        verified = verify_gparted_live(args.iso)
    except BuilderError as exc:
        parser.exit(2, f"ERROR: {exc}\n")

    print("GParted Live input verified")
    print(f"Version : {verified.spec.version}")
    print(f"GParted : {verified.spec.gparted_version}")
    print(f"Arch    : {verified.spec.architecture}")
    print(f"Kernel  : {verified.spec.kernel}")
    print(f"File    : {verified.path}")
    print(f"SHA256  : {verified.sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
