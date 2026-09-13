from fx11.bootmanager import BootEntry, WINDOWS_BOOT_PATH, grub_config


def test_fx11_entry_chainloads_windows_boot_manager():
    config = grub_config(fx11_esp_uuid="ABCD-1234")
    assert "menuentry 'FX11' --id 'fx11'" in config
    assert "search --no-floppy --fs-uuid --set=fxesp ABCD-1234" in config
    assert f"chainloader ($fxesp){WINDOWS_BOOT_PATH}" in config
    assert "set timeout=5" in config


def test_detected_loader_is_preserved_as_chainload_entry():
    config = grub_config(
        fx11_esp_uuid="FX11-ESP",
        detected_entries=(
            BootEntry("Fedora", "/EFI/fedora/shimx64.efi", "FEDORA-ESP", "fedora"),
            BootEntry("FreeBSD", "/EFI/BOOT/BOOTX64.EFI", "BSD-ESP", "freebsd"),
        ),
    )
    assert "menuentry 'Fedora' --id 'fedora'" in config
    assert "chainloader ($os1)/EFI/fedora/shimx64.efi" in config
    assert "menuentry 'FreeBSD' --id 'freebsd'" in config
    assert "chainloader ($os2)/EFI/BOOT/BOOTX64.EFI" in config


def test_duplicate_fx11_windows_loader_is_not_added_twice():
    config = grub_config(
        fx11_esp_uuid="SAME-ESP",
        detected_entries=(BootEntry("Windows Boot Manager", WINDOWS_BOOT_PATH, "SAME-ESP", "windows"),),
    )
    assert config.count(WINDOWS_BOOT_PATH) == 1


def test_missing_uuid_falls_back_to_loader_file_search():
    config = grub_config()
    assert f"search --no-floppy --file --set=fxesp {WINDOWS_BOOT_PATH}" in config


def test_uefi_firmware_escape_hatch_is_present():
    config = grub_config()
    assert "menuentry 'UEFI Firmware Settings'" in config
    assert "fwsetup" in config
