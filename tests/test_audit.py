from fx11.audit import compare_inventories, compare_wim_inventories


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
