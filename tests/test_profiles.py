import pytest

from os11vlin.profiles import Action, PROTECTED_COMPONENTS, PROFILES, Profile, validate_profile


def test_v1_profiles_exist():
    assert "tiny11-safe" in PROFILES
    assert "privacy-balanced" in PROFILES


def test_v1_profiles_do_not_remove_protected_components():
    for profile in PROFILES.values():
        validate_profile(profile)
        removed = {a.target for a in profile.actions if a.kind == "remove_component"}
        assert removed.isdisjoint(PROTECTED_COMPONENTS)


def test_protected_component_removal_is_blocked():
    unsafe = Profile(
        id="unsafe-test",
        description="test",
        actions=(Action("bad", "remove_component", "Windows Update", "unsafe"),),
    )
    with pytest.raises(ValueError, match="protected component"):
        validate_profile(unsafe)
