import shutil
import subprocess

import pytest

from fx11.iso import BuilderError
from fx11.media_efi import (
    MEDIA_GRUB_CONFIG_PATH,
    build_media_efi_payload,
    embedded_media_config,
    parse_efi_el_torito_path,
)
from fx11.media_theme import build_media_theme


def test_embedded_media_config_hands_off_to_staged_fx_grub_config():
    text = embedded_media_config()
    assert f"search --no-floppy --file --set=fxmedia {MEDIA_GRUB_CONFIG_PATH}" in text
    assert f"configfile ($fxmedia){MEDIA_GRUB_CONFIG_PATH}" in text


def test_parse_file_backed_efi_path_from_xorriso_report():
    report = "-boot_image any efi_path='/efi/microsoft/boot/efisys.bin'\n"
    assert parse_efi_el_torito_path(report) == "/efi/microsoft/boot/efisys.bin"


def test_parse_double_quoted_efi_path_from_xorriso_report():
    report = '-boot_image any efi_path="/EFI/BOOT/efiboot.img"\n'
    assert parse_efi_el_torito_path(report) == "/EFI/BOOT/efiboot.img"


def test_reject_interval_backed_efi_path_for_now():
    report = "-boot_image any efi_path=--interval:appended_partition_2:all::\n"
    with pytest.raises(BuilderError, match="interval"):
        parse_efi_el_torito_path(report)


def test_reject_missing_efi_path():
    with pytest.raises(BuilderError, match="Unable to discover"):
        parse_efi_el_torito_path("-boot_image any bin_path=/boot/etfsboot.com\n")


@pytest.mark.skipif(
    not all(shutil.which(tool) for tool in ("grub-mkstandalone", "mformat", "mmd", "mcopy", "mdir")),
    reason="GRUB/mtools not installed on this test host",
)
def test_build_media_efi_payload_contains_bootx64_and_theme(tmp_path):
    theme = build_media_theme(tmp_path / "theme")
    payload = build_media_efi_payload(tmp_path / "media-efi", theme=theme)

    assert payload.image.is_file()
    assert payload.image.stat().st_size == 16 * 1024 * 1024
    assert payload.efi_binary.is_file()
    assert len(payload.sha256) == 64

    for member in (
        "::/EFI/BOOT/BOOTX64.EFI",
        "::/EFI/FX11/theme/theme.txt",
        "::/EFI/FX11/theme/background.png",
        "::/EFI/FX11/theme/logo.png",
        "::/EFI/FX11/theme/unicode.pf2",
    ):
        proc = subprocess.run(
            ["mdir", "-i", str(payload.image), member],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr.decode("utf-8", errors="replace")
