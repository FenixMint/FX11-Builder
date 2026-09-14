from fx11.partitioning import ESP_MIB, plan_fx11_only


def test_default_esp_is_one_gib():
    assert ESP_MIB == 1024


def test_guided_layout_uses_one_gib_esp():
    plan = plan_fx11_only(256 * 1024, 1024)
    esp = plan.first("esp")
    assert esp is not None
    assert esp.size_mib == 1024
    assert esp.filesystem == "FAT32"
