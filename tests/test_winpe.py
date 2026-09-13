from fx11.winpe import select_boot_image_index, winpe_update_commands, write_winpe_payload


def test_winpe_payload_runs_wpeinit_before_fx11_launcher(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.startnet.read_text(encoding="ascii")
    assert "wpeinit" in text.lower()
    assert "X:\\FX11\\fx11-launch.cmd" in text


def test_winpeshl_forces_fx11_startnet_as_shell(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.winpeshl.read_text(encoding="ascii")
    assert "[LaunchApps]" in text
    assert "cmd.exe" in text
    assert "startnet.cmd" in text


def test_winpe_launcher_enters_partition_manager_and_keeps_setup_fallback(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.launcher.read_text(encoding="ascii")
    assert "Start FX Partition Manager" in text
    assert "X:\\FX11\\fx11-partition.cmd" in text
    assert "stock Windows Setup fallback" in text
    assert "clean" not in text.lower()
    assert "format " not in text.lower()
    assert "wpeutil reboot" in text.lower()


def test_text_partition_manager_requires_confirmation_and_can_continue_to_installer(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.partition_manager.read_text(encoding="ascii")
    lower = text.lower()
    assert "fx11 only" in lower
    assert "fx11 + other os" in lower
    assert "custom / manual" in lower
    assert "all partitions and data" in lower
    assert "clean" in lower
    assert "create partition efi size=300" in lower
    assert "create partition msr size=16" in lower
    assert "shrink desired=1024 minimum=1024" in lower
    assert "continue directly to fx11 installation" in lower
    assert "x:\\fx11\\fx11-install.cmd" in lower


def test_fx11_installer_applies_image_and_creates_boot_files(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.installer.read_text(encoding="ascii")
    lower = text.lower()
    assert "dism /apply-image" in lower
    assert "/index:1" in lower
    assert "/applydir:w:\\" in lower
    assert "bcdboot w:\\windows /s s: /f uefi" in lower
    assert "setupcomplete.cmd" in lower
    assert "fx11.ps1" in lower
    assert "fx11-manifest.json" in lower
    assert "s:\\efi\\fx11" in lower
    assert "reagentc /setreimage" in lower
    assert "automatic firmware-default activation" in lower


def test_boot_wim_declared_boot_index_wins():
    xml = """<WIM><IMAGE INDEX='1'/><IMAGE INDEX='2'/><BOOT INDEX='1'/></WIM>"""
    assert select_boot_image_index(xml) == 1


def test_boot_wim_falls_back_to_setup_index_two():
    xml = """<WIM><IMAGE INDEX='1'/><IMAGE INDEX='2'/></WIM>"""
    assert select_boot_image_index(xml) == 2


def test_winpe_update_plan_replaces_shell_and_adds_fx11_payload(tmp_path):
    payload = write_winpe_payload(tmp_path)
    commands = winpe_update_commands(payload)
    assert "/Windows/System32/startnet.cmd" in commands
    assert "/Windows/System32/winpeshl.ini" in commands
    assert "/FX11/fx11-launch.cmd" in commands
    assert "/FX11/fx11-partition.cmd" in commands
    assert "/FX11/fx11-install.cmd" in commands
    assert "/FX11/README.txt" in commands
