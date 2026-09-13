import pytest

from fx11.gparted import GPARTED_LIVE
from fx11.iso import BuilderError
from fx11.media_boot import build_media_grub_config
from fx11.media_theme import MEDIA_THEME_CONFIG_ISO_PATH, MEDIA_THEME_FONT_ISO_PATH


def test_media_boot_defaults_to_gparted_partition_manager():
    config = build_media_grub_config()
    text = config.grub_config

    assert "set timeout=5" in text
    assert "set default='fx-partition-manager'" in text
    assert "FX Partition Manager" in text
    assert "powered by GParted" not in text
    assert GPARTED_LIVE.filename in text
    assert "loopback loop" in text
    assert "(loop)/live/vmlinuz" in text
    assert "findiso=$isofile" in text
    assert "gl_batch" in text
    assert "locales=pl_PL.UTF-8" in text
    assert "keyboard-layouts=pl" in text


def test_media_boot_loads_graphical_fx11_theme_with_text_fallback():
    text = build_media_grub_config().grub_config

    assert "insmod gfxterm" in text
    assert "insmod png" in text
    assert "set gfxmode=auto" in text
    assert "set gfxpayload=keep" in text
    assert MEDIA_THEME_FONT_ISO_PATH in text
    assert MEDIA_THEME_CONFIG_ISO_PATH in text
    assert "terminal_output gfxterm" in text
    assert "set theme=" in text


def test_media_boot_keeps_winpe_entry_without_looping_to_fx_grub():
    text = build_media_grub_config().grub_config

    assert "menuentry 'FX11 Installer'" in text
    assert "WinPE fallback" not in text
    assert "/bootmgr.efi" in text
    assert "chainloader" in text
    assert "chainloader ($winmedia)/efi/boot/bootx64.efi" not in text


def test_media_boot_rejects_negative_timeout():
    with pytest.raises(BuilderError, match="timeout"):
        build_media_grub_config(timeout_seconds=-1)


def test_media_boot_requires_absolute_windows_boot_path():
    with pytest.raises(BuilderError, match="absolute"):
        build_media_grub_config(windows_boot_path="efi/boot/bootx64.efi")


def test_media_boot_rejects_empty_gparted_locale_or_keyboard():
    with pytest.raises(BuilderError, match="locale"):
        build_media_grub_config(gparted_locale="")
    with pytest.raises(BuilderError, match="keyboard"):
        build_media_grub_config(gparted_keyboard_layout="")
