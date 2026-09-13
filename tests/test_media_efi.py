import pytest

from fx11.iso import BuilderError
from fx11.media_efi import (
    MEDIA_GRUB_CONFIG_PATH,
    embedded_media_config,
    parse_efi_el_torito_path,
)


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
