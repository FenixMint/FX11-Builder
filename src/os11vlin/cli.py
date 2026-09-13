from __future__ import annotations

import argparse

from . import __version__
from .doctor import host_report
from .profiles import PROFILES, get_profile, validate_profile


def command_doctor() -> int:
    report = host_report()
    print("OS11vLIN Host Check")
    print(f"Distribution : {report['distribution']}")
    print(f"Architecture : {report['architecture']}")
    print(f"Kernel       : {report['kernel']}")
    print("\nTOOLS")
    for tool in report["tools"]:
        status = "OK" if tool.found else ("MISSING" if tool.required else "OPTIONAL")
        print(f"[{status}] {tool.name} ({tool.command})")
    print(f"\nSTATUS: {'READY' if report['ready'] else 'NOT READY'}")
    return 0 if report["ready"] else 2


def command_profiles() -> int:
    for profile in PROFILES.values():
        print(f"{profile.id}: {profile.description}")
    return 0


def command_plan(profile_ids: list[str]) -> int:
    if not profile_ids:
        profile_ids = ["tiny11-safe", "privacy-balanced"]
    print("OS11vLIN BUILD PLAN\n")
    for profile_id in profile_ids:
        profile = get_profile(profile_id)
        validate_profile(profile)
        print(f"[{profile.id}] {profile.description}")
        for action in profile.actions:
            print(f"  - {action.description} ({action.kind}: {action.target})")
        print()
    print("PROTECTED CORE COMPONENTS REMAIN UNCHANGED.")
    print("Dry run only: no ISO or WIM files were modified.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="os11vlin", description="Build conservative Windows 11 images on Linux")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Check host compatibility and external tools")
    sub.add_parser("profiles", help="List available build profiles")
    plan = sub.add_parser("plan", help="Preview profile actions without modifying an image")
    plan.add_argument("--profile", action="append", default=[], dest="profiles")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "doctor":
        return command_doctor()
    if args.command == "profiles":
        return command_profiles()
    if args.command == "plan":
        return command_plan(args.profiles)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
