from pathlib import Path

from fx11.doctor import detect_distribution


def test_detect_distribution(tmp_path: Path):
    os_release = tmp_path / "os-release"
    os_release.write_text('ID=debian\nPRETTY_NAME="Debian GNU/Linux 13 (trixie)"\n', encoding="utf-8")
    distro_id, distro_name = detect_distribution(os_release)
    assert distro_id == "debian"
    assert distro_name == "Debian GNU/Linux 13 (trixie)"


def test_unknown_distribution_for_missing_file(tmp_path: Path):
    distro_id, distro_name = detect_distribution(tmp_path / "missing")
    assert distro_id == "unknown"
    assert distro_name == "Unknown Linux"
