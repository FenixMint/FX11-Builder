from pathlib import Path

from fx11.media_theme import default_media_theme, write_media_background


def test_media_theme_uses_fenix_branding_and_fx11_identity():
    text = default_media_theme()

    assert 'text = "FX11"' in text
    assert 'text = "Fenix"' in text
    assert 'desktop-image: "background.png"' in text
    assert 'selected_item_color = "#69efa2"' in text
    assert "FenixMint" not in text


def test_media_background_is_valid_png(tmp_path):
    background = write_media_background(tmp_path / "background.png", width=640, height=360)
    data = background.read_bytes()

    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    assert len(data) > 1024
