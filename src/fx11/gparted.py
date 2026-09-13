from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .iso import BuilderError, sha256_file


@dataclass(frozen=True)
class GPartedLiveSpec:
    version: str
    gparted_version: str
    architecture: str
    filename: str
    sha256: str
    kernel: str
    release_page: str
    project_home: str


@dataclass(frozen=True)
class VerifiedGPartedLive:
    path: Path
    spec: GPartedLiveSpec
    sha256: str


GPARTED_LIVE = GPartedLiveSpec(
    version="1.8.1-6",
    gparted_version="1.8.1",
    architecture="amd64",
    filename="gparted-live-1.8.1-6-amd64.iso",
    sha256="d789c38779f0d6f7026c12f44c2c52a04f66e28a1aea7d51f3045ad1bbf28411",
    kernel="7.1.12-1",
    release_page="https://sourceforge.net/projects/gparted/files/gparted-live-stable/1.8.1-6/",
    project_home="https://gparted.org/",
)


def verify_gparted_live(path: Path, spec: GPartedLiveSpec = GPARTED_LIVE) -> VerifiedGPartedLive:
    source = path.expanduser().resolve()
    if not source.is_file():
        raise BuilderError(f"GParted Live image not found: {source}")
    if source.stat().st_size == 0:
        raise BuilderError(f"GParted Live image is empty: {source}")

    actual = sha256_file(source)
    if actual.casefold() != spec.sha256.casefold():
        raise BuilderError(
            "GParted Live SHA-256 mismatch. "
            f"Expected {spec.sha256}, got {actual}. "
            "Refusing to import an unpinned third-party image."
        )

    return VerifiedGPartedLive(path=source, spec=spec, sha256=actual)
