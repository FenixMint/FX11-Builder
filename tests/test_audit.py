from pathlib import Path
from types import SimpleNamespace

from fx11 import audit as audit_module
from fx11.audit import compare_inventories, compare_wim_inventories, list_wim_files, parse_7z_slt_files


def test_compare_inventories_reports_added_removed_and_common():
    source = ("/bootmgr", "/sources/boot.wim", "/sources/install.wim")
    output = (
        "/bootmgr",
        "/sources/boot.wim",
        "/sources/install.wim",
        "/FX11-manifest.json",
        "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1",
    )

    delta = compare_inventories(source, output)

    assert delta.added == (
        "/FX11-manifest.json",
        "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1",
    )
    assert delta.removed == ()
    assert delta.common_count == 3


def test_compare_inventories_detects_removed_source_file():
    delta = compare_inventories(("/a", "/b"), ("/b", "/c"))
    assert delta.added == ("/c",)
    assert delta.removed == ("/a",)
    assert delta.common_count == 1


def test_compare_wim_inventories_can_prove_path_inventory_is_unchanged():
    files = ("/Windows/System32/kernel32.dll", "/Windows/explorer.exe", "/Users/Default/NTUSER.DAT")
    delta = compare_wim_inventories(files, files)
    assert delta.added == ()
    assert delta.removed == ()
    assert delta.common_count == 3


def test_compare_wim_inventories_flags_unexpected_offline_change():
    delta = compare_wim_inventories(("/Windows/a.dll", "/Windows/b.dll"), ("/Windows/a.dll", "/Windows/evil.dll"))
    assert delta.added == ("/Windows/evil.dll",)
    assert delta.removed == ("/Windows/b.dll",)


def test_parse_7z_slt_files_ignores_archive_header_and_directories():
    listing = """Path = /tmp/Win11.iso
Type = Udf
Physical Size = 1234

Path = sources
Folder = +
Attributes = D

Path = sources/boot.wim
Size = 626224597
Folder = -
Attributes = A

Path = sources/install.wim
Size = 7437390947
Folder = -
Attributes = A

Path = efi/boot/bootx64.efi
Size = 3008968
Folder = -
Attributes = A
"""

    assert parse_7z_slt_files(listing) == (
        "/efi/boot/bootx64.efi",
        "/sources/boot.wim",
        "/sources/install.wim",
    )


def test_list_wim_files_uses_supported_wimdir_syntax_and_preserves_spaces(monkeypatch, tmp_path: Path):
    wim = tmp_path / "install.wim"
    wim.write_bytes(b"wim")
    captured: dict[str, object] = {}

    def fake_run(args: list[str], label: str):
        captured["args"] = args
        captured["label"] = label
        return SimpleNamespace(
            stdout=(
                b"/Windows\n"
                b"/Windows/System32/kernel32.dll\n"
                b"/Program Files/Common Files/example.dll\n"
            ),
            stderr=b"",
            returncode=0,
        )

    monkeypatch.setattr(audit_module, "_run", fake_run)

    assert list_wim_files(wim, 1) == (
        "/Program Files/Common Files/example.dll",
        "/Windows",
        "/Windows/System32/kernel32.dll",
    )
    assert captured["args"] == ["wimlib-imagex", "dir", str(wim), "1"]
