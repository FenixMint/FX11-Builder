import pytest

from fx11.gparted import GPARTED_LIVE
from fx11.iso import BuilderError
from fx11.media_boot import build_media_grub_config


def test_media_boot_defaults_to_gparted_partition_manager():
    config = build_media_grub_config()
    text = config.grub_config

    assert "set timeout=5" in text
    assert "set default='fx-partition-manager'" in text
    assert "FX Partition Manager — powered by GParted" in text
    assert GPARTED_LIVE.filename in text
    assert "loopback loop" in text
    assert "(loop)/live/vmlinuz" in text
    assert "findiso=$isofile" in text


def test_media_boot_keeps_winpe_fallback_without_looping_to_fx_grub():
    text = build_media_grub_config().grub_config

    assert "FX11 Installer / WinPE fallback" in text
    assert "/efi/microsoft/boot/bootmgfw.efi" in text
    assert "chainloader" in text
    assert "chainloader ($winmedia)/efi/boot/bootx64.efi" not in text


def test_media_boot_rejects_negative_timeout():
    with pytest.raises(BuilderError, match="timeout"):
        build_media_grub_config(timeout_seconds=-1)


def test_media_boot_requires_absolute_windows_boot_path():
    with pytest.raises(BuilderError, match="absolute"):
        build_media_grub_config(windows_boot_path="efi/boot/bootx64.efi")
