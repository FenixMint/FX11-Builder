from __future__ import annotations

from dataclasses import dataclass


PROTECTED_COMPONENTS = frozenset({
    "Microsoft Store",
    "Windows Update",
    "Microsoft Defender",
    "SmartScreen",
    "Windows Recovery",
    "Windows Installer",
    "PowerShell",
    ".NET",
    "WebView2",
})


@dataclass(frozen=True)
class Action:
    id: str
    kind: str
    target: str
    description: str


@dataclass(frozen=True)
class Profile:
    id: str
    description: str
    actions: tuple[Action, ...]


TINY11_SAFE = Profile(
    id="tiny11-safe",
    description="Conservative tiny11-inspired removal of optional consumer applications.",
    actions=(
        Action("remove_clipchamp", "appx_remove", "Clipchamp.Clipchamp", "Remove Clipchamp"),
        Action("remove_news", "appx_remove", "Microsoft.BingNews", "Remove News"),
        Action("remove_weather", "appx_remove", "Microsoft.BingWeather", "Remove Weather"),
        Action("remove_gethelp", "appx_remove", "Microsoft.GetHelp", "Remove Get Help"),
        Action("remove_getstarted", "appx_remove", "Microsoft.Getstarted", "Remove Get Started"),
        Action("remove_people", "appx_remove", "Microsoft.People", "Remove People"),
        Action("remove_solitaire", "appx_remove", "Microsoft.MicrosoftSolitaireCollection", "Remove Solitaire"),
        Action("remove_feedback", "appx_remove", "Microsoft.WindowsFeedbackHub", "Remove Feedback Hub"),
        Action("remove_maps", "appx_remove", "Microsoft.WindowsMaps", "Remove Maps"),
    ),
)

PRIVACY_BALANCED = Profile(
    id="privacy-balanced",
    description="Reduce advertising, suggestions and optional telemetry while preserving core Windows services.",
    actions=(
        Action("disable_ad_id", "policy", "AdvertisingID", "Disable advertising ID"),
        Action("disable_consumer_features", "policy", "ConsumerFeatures", "Disable Microsoft consumer experiences"),
        Action("disable_tailored", "policy", "TailoredExperiences", "Disable tailored experiences"),
        Action("disable_suggestions", "policy", "ContentSuggestions", "Disable suggested content and apps"),
        Action("reduce_diagnostics", "policy", "OptionalDiagnosticData", "Disable optional diagnostic data"),
    ),
)

PROFILES = {profile.id: profile for profile in (TINY11_SAFE, PRIVACY_BALANCED)}


def get_profile(profile_id: str) -> Profile:
    try:
        return PROFILES[profile_id]
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {profile_id}") from exc


def validate_profile(profile: Profile) -> None:
    for action in profile.actions:
        if action.kind == "remove_component" and action.target in PROTECTED_COMPONENTS:
            raise ValueError(f"Profile {profile.id} attempts to remove protected component: {action.target}")
