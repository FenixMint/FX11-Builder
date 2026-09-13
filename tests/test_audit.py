from fx11.audit import compare_inventories


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
