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
    "Microsoft Edge",
    "Windows Terminal",
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
    description=(
        "Conservative tiny11-inspired removal of optional consumer applications. "
        "Windows servicing, Defender, Store, Edge/WebView2 and Terminal are preserved."
    ),
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
        Action("remove_phone", "appx_remove", "Microsoft.YourPhone", "Remove Phone Link"),
        Action("remove_xbox_app", "appx_remove", "Microsoft.XboxApp", "Remove Xbox app"),
        Action("remove_xbox_tcui", "appx_remove", "Microsoft.Xbox.TCUI", "Remove Xbox TCUI"),
        Action("remove_xbox_overlay", "appx_remove", "Microsoft.XboxGameOverlay", "Remove Xbox Game Overlay"),
        Action("remove_xbox_gaming_overlay", "appx_remove", "Microsoft.XboxGamingOverlay", "Remove Xbox Gaming Overlay"),
        Action("remove_xbox_speech", "appx_remove", "Microsoft.XboxSpeechToTextOverlay", "Remove Xbox speech overlay"),
        Action("remove_zune_music", "appx_remove", "Microsoft.ZuneMusic", "Remove legacy Media Player package"),
        Action("remove_zune_video", "appx_remove", "Microsoft.ZuneVideo", "Remove Movies & TV"),
        Action("remove_teams_consumer", "appx_remove", "MSTeams", "Remove consumer Teams package"),
        Action("remove_teams_legacy", "appx_remove", "MicrosoftTeams", "Remove legacy consumer Teams package"),
        Action("remove_family", "appx_remove", "MicrosoftCorporationII.MicrosoftFamily", "Remove Family app"),
        Action("remove_quickassist", "appx_remove", "MicrosoftCorporationII.QuickAssist", "Remove Quick Assist"),
    ),
)

PRIVACY_BALANCED = Profile(
    id="privacy-balanced",
    description=(
        "Reduce advertising, recommendations, activity upload, Recall/Copilot data collection and optional telemetry "
        "while preserving Windows Update, Defender, Store and core connectivity."
    ),
    actions=(
        Action("disable_ad_id", "policy", "AdvertisingID", "Disable advertising ID"),
        Action("disable_consumer_features", "policy", "ConsumerFeatures", "Disable Microsoft consumer experiences"),
        Action("disable_tailored", "policy", "TailoredExperiences", "Disable tailored experiences"),
        Action("disable_suggestions", "policy", "ContentSuggestions", "Disable suggested content and silent app installs"),
        Action("reduce_diagnostics", "policy", "RequiredDiagnosticData", "Limit diagnostics to required data"),
        Action("disable_activity_upload", "policy", "ActivityHistory", "Disable activity feed publishing and upload"),
        Action("disable_search_suggestions", "policy", "SearchSuggestions", "Disable web suggestions in Windows Search"),
        Action("disable_recall", "policy", "WindowsAI", "Disable Recall data analysis policy"),
        Action("disable_copilot", "policy", "WindowsCopilot", "Disable Windows Copilot policy"),
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


def appx_targets(profile_ids: list[str]) -> list[str]:
    result: list[str] = []
    for profile_id in profile_ids:
        profile = get_profile(profile_id)
        validate_profile(profile)
        for action in profile.actions:
            if action.kind == "appx_remove" and action.target not in result:
                result.append(action.target)
    return result
