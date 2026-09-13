import pytest

from fx11.iso import BuilderError, Edition, find_edition


EDITIONS = (
    Edition(1, "Windows 11 Home", "Home", "Core", "9"),
    Edition(6, "Windows 11 Pro", "Pro", "Professional", "9"),
    Edition(7, "Windows 11 Pro N", "Pro N", "ProfessionalN", "9"),
    Edition(10, "Windows 11 Education", "Education", "Education", "9"),
)


def test_find_edition_by_index():
    assert find_edition(EDITIONS, index=6).name == "Windows 11 Pro"


def test_find_edition_by_exact_name():
    assert find_edition(EDITIONS, query="Windows 11 Home").edition_id == "Core"


def test_find_edition_by_edition_id():
    assert find_edition(EDITIONS, query="Professional").index == 6


def test_ambiguous_partial_name_is_rejected():
    with pytest.raises(BuilderError, match="ambiguous"):
        find_edition(EDITIONS, query="Pro")


def test_unknown_index_is_rejected():
    with pytest.raises(BuilderError, match="does not exist"):
        find_edition(EDITIONS, index=99)
