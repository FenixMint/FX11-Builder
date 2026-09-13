from pathlib import Path
from types import SimpleNamespace

import pytest

from fx11 import iso as iso_module
from fx11.iso import BuilderError, Edition, detect_media_format, find_edition


EDITIONS = (
    Edition(1, "Windows 11 Home", "Home", "Core", "9"),
    Edition(6, "Windows 11 Pro", "Pro", "Professional", "9"),
    Edition(7, "Windows 11 Pro N", "Pro N", "ProfessionalN", "9"),
    Edition(10, "Windows 11 Education", "Education", "Education", "9"),
)


def test_find_edition_by_index():
    assert find_edition(EDITIONS, index=6).name == "Windows 11 Pro"


def test_find_edition_by_exact_name():
    assert find_edition(EDITIONS, query="Windows 11 Home").edition_id == "Core"


def test_find_edition_by_edition_id():
    assert find_edition(EDITIONS, query="Professional").index == 6


def test_ambiguous_partial_name_is_rejected():
    with pytest.raises(BuilderError, match="ambiguous"):
        find_edition(EDITIONS, query="Pro")


def test_unknown_index_is_rejected():
    with pytest.raises(BuilderError, match="does not exist"):
        find_edition(EDITIONS, index=99)


def test_detect_media_format_recognizes_udf(monkeypatch, tmp_path: Path):
    source = tmp_path / "windows.iso"
    source.write_bytes(b"iso")
    monkeypatch.setattr(iso_module, "_sevenzip", lambda: "/usr/bin/7z")
    monkeypatch.setattr(
        iso_module.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=b"Path = windows.iso\nType = Udf\n", stderr=b""),
    )
    assert detect_media_format(source) == "udf"


def test_detect_media_format_defaults_non_udf_to_iso9660(monkeypatch, tmp_path: Path):
    source = tmp_path / "windows.iso"
    source.write_bytes(b"iso")
    monkeypatch.setattr(iso_module, "_sevenzip", lambda: "/usr/bin/7z")
    monkeypatch.setattr(
        iso_module.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=b"Path = windows.iso\nType = Iso\n", stderr=b""),
    )
    assert detect_media_format(source) == "iso9660"
