import pytest

from fx11.gparted import GPARTED_LIVE
from fx11.iso import BuilderError
from fx11.media_boot import (
    MEDIA_CONTINUE_MARKER_PATH,
    MEDIA_THEME_ESP_DIR,
    build_media_grub_config,
)
from fx11.media_efi import MEDIA_WINPE_READY_PATH
from fx11.media_theme import (
    MEDIA_THEME_BACKGROUND_ISO_PATH,
    MEDIA_THEME_CONFIG_ISO_PATH,
    MEDIA_THEME_FONT_ISO_PATH,
)


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
    assert "hooks=medium" in text
    assert "locales=pl_PL.UTF-8" in text
    assert "keyboard-layouts=pl" in text


def test_media_boot_uses_real_grub_file_search_module_name():
    text = build_media_grub_config().grub_config

    assert "insmod search_fs_file" in text
    assert "insmod search_file" not in text


def test_media_boot_prefers_efi_theme_and_keeps_iso_fallback():
    text = build_media_grub_config().grub_config

    assert "insmod gfxterm" in text
    assert "insmod gfxterm_background" in text
    assert "insmod gfxmenu" in text
    assert "insmod png" in text
    assert "set gfxmode=auto" in text
    assert "set gfxpayload=keep" in text
    assert f"{MEDIA_THEME_ESP_DIR}/unicode.pf2" in text
    assert f"{MEDIA_THEME_ESP_DIR}/theme.txt" in text
    assert f"{MEDIA_THEME_ESP_DIR}/background.png" in text
    assert MEDIA_THEME_FONT_ISO_PATH in text
    assert MEDIA_THEME_CONFIG_ISO_PATH in text
    assert MEDIA_THEME_BACKGROUND_ISO_PATH in text
    assert "terminal_output gfxterm" in text
    assert "background_image" in text
    assert "set theme=" in text


def test_media_boot_uses_fat_resident_winpe_loader():
    text = build_media_grub_config().grub_config

    assert "menuentry 'FX11 Installer'" in text
    assert "WinPE fallback" not in text
    assert MEDIA_WINPE_READY_PATH in text
    assert "/EFI/Microsoft/Boot/bootmgfw.efi" in text
    assert "/bootmgr.efi" not in text
    assert "chainloader ($winboot)/EFI/Microsoft/Boot/bootmgfw.efi" in text
    assert "chainloader ($winmedia)" not in text


def test_media_boot_supports_continue_marker():
    text = build_media_grub_config().grub_config

    assert MEDIA_CONTINUE_MARKER_PATH in text
    assert "set default='fx11-winpe'" in text
    assert "set timeout=3" in text


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
