from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from . import __version__
from .audit import write_delta_report
from .builder import build_iso, inspect_source, validate_output_iso
from .doctor import host_report
from .iso import BuilderError, Edition, find_edition
from .profiles import PROFILES, get_profile, validate_profile
from .vm import launch_qemu


DEFAULT_PROFILES = ["tiny11-safe", "privacy-balanced"]


def command_doctor() -> int:
    report = host_report()
    print("FX11 Builder Host Check")
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
        profile_ids = DEFAULT_PROFILES.copy()
    print("FX11 BUILD PLAN\n")
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


def _print_editions(editions: tuple[Edition, ...]) -> None:
    print("\nAvailable Windows images:")
    for edition in editions:
        extra = f" [{edition.edition_id}]" if edition.edition_id else ""
        arch = f" arch={edition.architecture}" if edition.architecture else ""
        print(f"  {edition.index:>2}. {edition.name}{extra}{arch}")


def command_inspect(source: Path) -> int:
    inspection, temp = inspect_source(source)
    try:
        print(f"Source : {inspection.source}")
        print(f"SHA256 : {inspection.source_sha256}")
        print(f"Image  : {inspection.install_format.upper()}")
        _print_editions(inspection.editions)
        return 0
    finally:
        temp.cleanup()


def _choose_edition(editions: tuple[Edition, ...], index: int | None, query: str | None) -> Edition:
    if index is not None or query:
        return find_edition(editions, index=index, query=query)
    if not sys.stdin.isatty():
        raise BuilderError("No edition selected. Use --index N or --edition NAME in non-interactive mode.")
    _print_editions(editions)
    while True:
        try:
            value = input("\nSelect Windows image index > ").strip()
        except EOFError as exc:
            raise BuilderError("No edition selected.") from exc
        if value.isdigit():
            try:
                return find_edition(editions, index=int(value))
            except BuilderError as exc:
                print(exc)
                continue
        print("Enter one of the numeric image indexes shown above.")


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return slug or "Windows11"


def command_build(args: argparse.Namespace) -> int:
    profiles = args.profiles or DEFAULT_PROFILES.copy()
    inspection, temp = inspect_source(args.source)
    try:
        edition = _choose_edition(inspection.editions, args.index, args.edition)
        print(f"\nSelected: {edition.index}. {edition.name}")
        print(f"Source SHA256: {inspection.source_sha256}")
        command_plan(profiles)
        if args.dry_run:
            print("\nBuild not started because --dry-run was specified.")
            return 0
        output = args.output
        if output is None:
            output = Path.cwd() / f"{inspection.source.stem}-FX11-{_slug(edition.name)}.iso"
        print(f"\nBuilding: {output}")
        result = build_iso(inspection, edition, output, profiles, force=args.force)
        print("\nBUILD VALID")
        print(f"ISO    : {result.output_iso}")
        print(f"SHA256 : {result.output_sha256}")
        print(f"SUM    : {result.checksum_file}")
        print(f"Edition: {result.edition.name}")
        print(f"Profiles: {', '.join(result.profiles)}")
        return 0
    finally:
        temp.cleanup()


def command_validate(iso: Path) -> int:
    validate_output_iso(iso.expanduser().resolve())
    print(f"VALID: {iso}")
    return 0


def command_audit(args: argparse.Namespace) -> int:
    report_path = args.output
    if report_path is None:
        report_path = args.fx11_iso.with_name(args.fx11_iso.name + ".delta.json")
    report = write_delta_report(args.source_iso, args.fx11_iso, report_path)
    delta = report["delta"]
    print("FX11 ISO DELTA AUDIT")
    print(f"Source          : {report['source']['path']}")
    print(f"FX11 ISO        : {report['output']['path']}")
    print(f"Added paths     : {len(delta['added'])}")
    print(f"Removed paths   : {len(delta['removed'])}")
    print(f"Unexpected added: {len(delta['unexpected_added'])}")
    print(f"Report          : {report_path.expanduser().resolve()}")
    return 0


def command_test(args: argparse.Namespace) -> int:
    return launch_qemu(
        args.iso,
        memory_mb=args.memory,
        cpus=args.cpus,
        disk_gb=args.disk,
        uefi=not args.bios,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fx11", description="Build custom Windows 11 installation images on Linux")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check host compatibility and external tools")
    sub.add_parser("profiles", help="List available build profiles")

    plan = sub.add_parser("plan", help="Preview profile actions without modifying an image")
    plan.add_argument("--profile", action="append", default=[], dest="profiles", choices=sorted(PROFILES))

    inspect = sub.add_parser("inspect", help="Inspect a Windows ISO and list all Home/Pro/Enterprise/etc. images")
    inspect.add_argument("source", type=Path)

    build = sub.add_parser("build", help="Build a selected Windows 11 edition")
    build.add_argument("source", type=Path, help="Original Microsoft Windows 11 ISO")
    select = build.add_mutually_exclusive_group()
    select.add_argument("--index", type=int, help="WIM/ESD image index from 'fx11 inspect'")
    select.add_argument("--edition", help="Edition name or EditionID, e.g. 'Windows 11 Pro' or Professional")
    build.add_argument("-o", "--output", type=Path)
    build.add_argument("--profile", action="append", default=[], dest="profiles", choices=sorted(PROFILES))
    build.add_argument("--dry-run", action="store_true")
    build.add_argument("--force", action="store_true")

    validate = sub.add_parser("validate", help="Validate a generated FX11 ISO")
    validate.add_argument("iso", type=Path)

    audit = sub.add_parser("audit", help="Compare an FX11 ISO against its source ISO and write a delta report")
    audit.add_argument("source_iso", type=Path, help="Original source Windows ISO")
    audit.add_argument("fx11_iso", type=Path, help="Generated FX11 ISO")
    audit.add_argument("-o", "--output", type=Path, help="Output JSON report path")

    test = sub.add_parser("test", help="Boot an ISO in a temporary QEMU VM")
    test.add_argument("iso", type=Path)
    test.add_argument("--memory", type=int, default=4096, help="VM memory in MiB")
    test.add_argument("--cpus", type=int, default=2)
    test.add_argument("--disk", type=int, default=64, help="Temporary disk size in GiB")
    test.add_argument("--bios", action="store_true", help="Use legacy BIOS instead of OVMF/UEFI")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "doctor":
            return command_doctor()
        if args.command == "profiles":
            return command_profiles()
        if args.command == "plan":
            return command_plan(args.profiles)
        if args.command == "inspect":
            return command_inspect(args.source)
        if args.command == "build":
            return command_build(args)
        if args.command == "validate":
            return command_validate(args.iso)
        if args.command == "audit":
            return command_audit(args)
        if args.command == "test":
            return command_test(args)
        return 1
    except (BuilderError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
