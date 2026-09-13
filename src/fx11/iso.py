from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
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


def extract_install_image(source_iso: Path, destination: Path) -> tuple[Path, str]:
    destination.mkdir(parents=True, exist_ok=True)
    attempts = (("install.wim", "wim"), ("install.esd", "esd"))
    errors: list[str] = []
    for filename, image_format in attempts:
        out = destination / filename
        proc = subprocess.run(
            ["xorriso", "-osirrox", "on", "-indev", str(source_iso), "-extract", f"/sources/{filename}", str(out)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode == 0 and out.exists() and out.stat().st_size > 0:
            return out, image_format
        out.unlink(missing_ok=True)
        errors.append((proc.stderr or b"").decode("utf-8", errors="replace"))
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
    image, image_format = extract_install_image(source_iso, work_dir)
    editions = read_editions(image)
    return IsoInspection(
        source=source_iso,
        source_sha256=sha256_file(source_iso),
        install_image=image,
        install_format=image_format,
        editions=editions,
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
