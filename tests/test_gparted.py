from hashlib import sha256

import pytest

from fx11.gparted import GPartedLiveSpec, GPARTED_LIVE, verify_gparted_live
from fx11.iso import BuilderError


def _spec_for(data: bytes) -> GPartedLiveSpec:
    return GPartedLiveSpec(
        version="test",
        gparted_version="test",
        architecture="amd64",
        filename="gparted-live-test.iso",
        sha256=sha256(data).hexdigest(),
        kernel="test",
        release_page="https://example.invalid/release",
        project_home="https://example.invalid/",
    )


def test_pinned_gparted_release_metadata():
    assert GPARTED_LIVE.version == "1.8.1-6"
    assert GPARTED_LIVE.filename == "gparted-live-1.8.1-6-amd64.iso"
    assert GPARTED_LIVE.sha256 == "d789c38779f0d6f7026c12f44c2c52a04f66e28a1aea7d51f3045ad1bbf28411"


def test_verify_gparted_live_accepts_exact_hash(tmp_path):
    data = b"synthetic-gparted-live-image\n"
    image = tmp_path / "gparted.iso"
    image.write_bytes(data)

    verified = verify_gparted_live(image, _spec_for(data))

    assert verified.path == image.resolve()
    assert verified.sha256 == sha256(data).hexdigest()


def test_verify_gparted_live_rejects_hash_mismatch(tmp_path):
    image = tmp_path / "gparted.iso"
    image.write_bytes(b"unexpected image")
    expected = _spec_for(b"expected image")

    with pytest.raises(BuilderError, match="SHA-256 mismatch"):
        verify_gparted_live(image, expected)


def test_verify_gparted_live_rejects_missing_file(tmp_path):
    with pytest.raises(BuilderError, match="not found"):
        verify_gparted_live(tmp_path / "missing.iso")
