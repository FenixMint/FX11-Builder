from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET


class BuilderError(RuntimeError):
    pass


@dataclass(frozen=True)
class Edition:
    index: int
    name: str
    description: str
    edition_id: str
    architecture: str


@dataclass(frozen=True)
class IsoInspection:
    source: Path
    source_sha256: str
    install_image: Path
    install_format: str
    editions: tuple[Edition, ...]
    media_format: str = "iso9660"


def run_checked(args: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        args,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
        check=False,
    )
    if proc.returncode != 0:
        detail = ""
        if capture_output:
            detail = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Command failed ({proc.returncode}): {' '.join(args)}" + (f"\n{detail}" if detail else ""))
    return proc


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _sevenzip() -> str | None:
    return shutil.which("7z")


def detect_media_format(source_iso: Path) -> str:
    """Detect the filesystem view exposed by the installation image.

    Current Microsoft Windows 11 media can be UDF-first. xorriso only exposes
    the ISO9660 side of such bridge images, which can contain little more than
    the primary volume descriptors. 7-Zip can read the UDF tree directly.
    """
    sevenzip = _sevenzip()
    if sevenzip is None:
        return "iso9660"
    proc = subprocess.run(
        [sevenzip, "l", "-slt", str(source_iso)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return "iso9660"
    text = proc.stdout.decode("utf-8", errors="replace")
    match = re.search(r"(?m)^Type\s*=\s*([^\r\n]+)$", text)
    if not match:
        return "iso9660"
    archive_type = match.group(1).strip().casefold()
    if archive_type == "udf":
        return "udf"
    return "iso9660"


def extract_iso_member(
    source_iso: Path,
    iso_path: str,
    destination: Path,
    *,
    media_format: str | None = None,
) -> Path:
    source_iso = source_iso.expanduser().resolve()
    destination = destination.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.unlink(missing_ok=True)
    media_format = media_format or detect_media_format(source_iso)

    if media_format == "udf":
        sevenzip = _sevenzip()
        if sevenzip is None:
            raise BuilderError(
                "This Microsoft ISO uses UDF. The '7z' command is required to read current UDF installation media. "
                "Install the Debian-family package '7zip'."
            )
        member = iso_path.lstrip("/")
        with destination.open("wb") as handle:
            proc = subprocess.run(
                [sevenzip, "x", "-so", str(source_iso), member],
                stdout=handle,
                stderr=subprocess.PIPE,
                check=False,
            )
        if proc.returncode != 0 or not destination.is_file() or destination.stat().st_size == 0:
            destination.unlink(missing_ok=True)
            detail = (proc.stderr or b"").decode("utf-8", errors="replace").strip()
            raise BuilderError(f"Unable to extract /{member} from UDF installation media.\n{detail}")
        return destination

    proc = subprocess.run(
        ["xorriso", "-osirrox", "on", "-indev", str(source_iso), "-extract", iso_path, str(destination)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0 or not destination.is_file() or destination.stat().st_size == 0:
        destination.unlink(missing_ok=True)
        detail = (proc.stderr or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Unable to extract {iso_path} from ISO installation media.\n{detail}")
    return destination


def ensure_windows_uefi_fallback(media_tree: Path) -> Path:
    """Ensure the Microsoft WinPE chainload target exists in an extracted tree.

    Some current Microsoft UDF installation media provide the signed Windows
    removable-media loader only as /efi/boot/bootx64.efi and do not also expose
    /efi/microsoft/boot/bootmgfw.efi in the UDF tree. FX11 later owns the
    removable-media path with its unsigned development GRUB loader, so preserve
    the original Microsoft bytes at the canonical Microsoft boot-manager path
    before that replacement happens.
    """
    media_tree = media_tree.expanduser().resolve()
    fallback = media_tree / "efi" / "microsoft" / "boot" / "bootmgfw.efi"
    if fallback.is_file() and fallback.stat().st_size > 0:
        return fallback

    removable = media_tree / "efi" / "boot" / "bootx64.efi"
    if not removable.is_file() or removable.stat().st_size == 0:
        raise BuilderError(
            "Extracted Microsoft media contains neither /efi/microsoft/boot/bootmgfw.efi "
            "nor /efi/boot/bootx64.efi; FX11 cannot preserve a WinPE UEFI fallback."
        )

    fallback.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(removable, fallback)
    if sha256_file(fallback) != sha256_file(removable):
        fallback.unlink(missing_ok=True)
        raise BuilderError("Microsoft UEFI fallback copy failed integrity verification.")
    return fallback


def extract_media_tree(source_iso: Path, destination: Path) -> Path:
    """Extract the complete source media tree with 7-Zip.

    This is primarily used for UDF-first Microsoft media before rebuilding a
    normal ISO9660 level-3 FX11 image. It intentionally extracts into a fresh
    temporary directory owned by the builder.
    """
    sevenzip = _sevenzip()
    if sevenzip is None:
        raise BuilderError(
            "The '7z' command is required to extract UDF installation media. "
            "Install the Debian-family package '7zip'."
        )
    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sevenzip, "x", "-y", f"-o{destination}", str(source_iso.expanduser().resolve())],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Unable to extract the Microsoft installation media tree with 7-Zip.\n{detail}")
    required = (
        destination / "sources" / "boot.wim",
        destination / "boot" / "etfsboot.com",
        destination / "efi" / "microsoft" / "boot" / "efisys.bin",
    )
    missing = [str(path.relative_to(destination)) for path in required if not path.is_file()]
    if missing:
        raise BuilderError("Extracted UDF installation media is missing required boot files: " + ", ".join(missing))
    ensure_windows_uefi_fallback(destination)
    return destination


def extract_install_image(source_iso: Path, destination: Path) -> tuple[Path, str]:
    destination.mkdir(parents=True, exist_ok=True)
    media_format = detect_media_format(source_iso)
    attempts = (("install.wim", "wim"), ("install.esd", "esd"))
    errors: list[str] = []
    for filename, image_format in attempts:
        out = destination / filename
        try:
            extract_iso_member(
                source_iso,
                f"/sources/{filename}",
                out,
                media_format=media_format,
            )
        except BuilderError as exc:
            out.unlink(missing_ok=True)
            errors.append(str(exc))
            continue
        if out.exists() and out.stat().st_size > 0:
            return out, image_format
        out.unlink(missing_ok=True)
    raise BuilderError("No /sources/install.wim or /sources/install.esd found in the ISO.\n" + "\n".join(errors[-2:]))


def read_editions(install_image: Path) -> tuple[Edition, ...]:
    proc = run_checked(["wimlib-imagex", "info", str(install_image), "--xml"], capture_output=True)
    raw = proc.stdout
    try:
        text = raw.decode("utf-16")
    except UnicodeError:
        text = raw.decode("utf-8", errors="replace")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise BuilderError(f"Unable to parse wimlib XML output: {exc}") from exc

    editions: list[Edition] = []
    for image in root.findall("IMAGE"):
        index_text = image.attrib.get("INDEX", "0")
        name = (image.findtext("NAME") or f"Image {index_text}").strip()
        description = (image.findtext("DESCRIPTION") or "").strip()
        windows = image.find("WINDOWS")
        edition_id = ""
        architecture = ""
        if windows is not None:
            edition_id = (windows.findtext("EDITIONID") or "").strip()
            architecture = (windows.findtext("ARCH") or "").strip()
        try:
            index = int(index_text)
        except ValueError:
            continue
        editions.append(Edition(index, name, description, edition_id, architecture))
    if not editions:
        raise BuilderError("No Windows editions were discovered in the installation image.")
    return tuple(editions)


def inspect_iso(source_iso: Path, work_dir: Path) -> IsoInspection:
    source_iso = source_iso.expanduser().resolve()
    if not source_iso.is_file():
        raise BuilderError(f"ISO not found: {source_iso}")
    if source_iso.suffix.lower() != ".iso":
        raise BuilderError(f"Input must be an .iso file: {source_iso}")
    media_format = detect_media_format(source_iso)
    image, image_format = extract_install_image(source_iso, work_dir)
    editions = read_editions(image)
    return IsoInspection(
        source=source_iso,
        source_sha256=sha256_file(source_iso),
        install_image=image,
        install_format=image_format,
        editions=editions,
        media_format=media_format,
    )


def find_edition(editions: tuple[Edition, ...], *, index: int | None = None, query: str | None = None) -> Edition:
    if index is not None:
        for edition in editions:
            if edition.index == index:
                return edition
        raise BuilderError(f"Image index {index} does not exist.")
    if query:
        normalized = query.casefold().strip()
        exact = [e for e in editions if e.name.casefold() == normalized or e.edition_id.casefold() == normalized]
        if len(exact) == 1:
            return exact[0]
        partial = [e for e in editions if normalized in e.name.casefold() or normalized in e.edition_id.casefold()]
        if len(partial) == 1:
            return partial[0]
        if len(partial) > 1:
            names = ", ".join(f"{e.index}:{e.name}" for e in partial)
            raise BuilderError(f"Edition query is ambiguous: {query}. Matches: {names}")
        raise BuilderError(f"Edition not found: {query}")
    raise BuilderError("No edition selected.")
