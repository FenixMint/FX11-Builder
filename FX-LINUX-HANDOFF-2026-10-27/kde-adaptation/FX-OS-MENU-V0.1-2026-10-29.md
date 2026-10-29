# FX OS Menu v0.1 — visual and functional contract — 2026-10-29

Status: **OWNER wants menu implementation now; design and installation preparation only; not yet installed**.
Repository context: FenixMint/FX11-Builder, branch `handoff/fx-linux-manual-package-2026-10-27`.
Related rolling checkpoint: `FX-LINUX-KDE-VISUAL-V0.1-2026-10-28.md`.

## Explicit OWNER decisions

- **Menu button:** one **round glowing FX logo at the extreme LEFT end of the EXISTING top horizontal panel**, replacing the icon of the working KDE Application Launcher. **NOT on the left dock**.
- **Menu geometry:** large popup **below that upper-left menu button**, never full-screen; dark, glossy/blue-black with cyan edge/glow and rounded corners, consistent with current OWNER-approved **Oxygen** Plasma Style and FX OS space wallpaper.
- **Main visual reference:** OWNER-selected **original third FX OS reference image** from prior conversation; its custom menu and dark sci-fi gloss are reference, **not** its compact telemetry card. Keep full detailed **FenixSystem V3** as is at upper right, never replace/resize it.
- **Content layout:** generous search field at top; **two principal columns** (favorites/quick apps on left, categories/app browser on right), with accessible navigation to Places/Files, Settings, recent items, and clearly separated session/power actions at bottom. Search across actual installed apps (including Flatpak/AppImage when present), usable by keyboard as well as pointer. Labels in Polish.
- **Two future distinct right-click actions on app entries:** `Dodaj do panelu` targets the **TOP** panel, `Dodaj do docka` targets the **LEFT** dock. The latter must be implemented only after deciding the final dynamic-dock technology; do NOT silently route both commands to the same task manager. Provide removal and reordering through natural GUI. These actions are **NOT implemented yet**.
- **Appearance direction:** FX OS Gloss inspired by Windows XP Luna, Windows 7 Aero, Mandriva Powerpack 2008 (Ia Ora) and KDE Plastik/Keramik/Oxygen: vibrant app icons, tactile highlights, dark navy glossy layers, subtle bevels and electric-blue focus. Avoid washed-out minimalist Windows 10/11 look.

## Current proven KDE baseline

- Fedora 44 KDE Plasma **6.7.5**, Kirigami **6.31.0**, Plasma Style **Oxygen** (applied and OWNER visually approved), icons previously `breeze-dark`.
- Existing top panel **55** contains **`org.kde.plasma.kickoff` widget 56** at upper-left; task manager 58, pager 57, systray 60, clock 75 and Show Desktop 76 are working. Do not remove or re-create panel 55.
- Existing genuine left panel **85**, 64 px thick, `lengthMode='fit'`, `hiding='none'`, contains user-owned Quicklaunch with selected app icons and is not covered by normal maximized windows (OWNER PASS). Keep as reliable fallback while future dock is researched.
- Important upstream source (verified KDE v6.7.5): https://github.com/KDE/plasma-desktop/tree/v6.7.5/applets/kickoff . Stock Kickoff `ConfigGeneral.qml` exposes its **custom icon**, app/favorite layout options, category behavior and menu settings; `main.qml` uses the QML icon config and imports the native application model. **The exact requested two-column simultaneous favorites + app categories, bespoke appearance and two custom pin-target actions are NOT guaranteed by merely changing the stock icon/theme.** A custom user-local plasmoid/fork or equivalent supported implementation may be needed.

## Staged work and safeguards

1. **Capture current open-menu screenshot** of existing Kickoff at the intended 1680x1050 workspace; inspect actual Favorites, Applications, Places, Search, Power/actions, dimensions, and FX OS wallpaper clearance. Read current widget 56 configuration through safe GUI/read-only Plasma scripting as needed. Before *any* mutation, snapshot `~/.config/plasma-org.kde.plasma.desktop-appletsrc` and `~/.config/plasmashellrc` in `~/FX-Linux-Odzysk/` (never commit private files to public GitHub).
2. **Icon/branding step:** obtain an OWNER-approved round FX emblem (user-supplied asset or approved new user-local vector) and configure **only icon of existing Kickoff widget 56**, keeping a clear revert path to its current icon. Do not assume any screenshot/wallpaper contains a reusable clean icon.
3. **Menu functional baseline:** use KDE native application search/category/favorites and power action models. If a separate menu plasmoid is necessary, install it **user-locally** (not into `/usr/share`) as a separately testable alternative; do not remove native Kickoff before new widget fully works, retains keyboard/favorites/Flatpak/AppImage/Signal support and is OWNER-accepted. No new duplicate launcher on the permanent top bar until test plan.
4. **FX OS Gloss layout/polish:** two-column popup below left top button, cyan focus/hover borders, selective blue glow, icon readability, session buttons, optional blur and animation, should never obscure right FenixSystem V3.
5. **Dock integration later:** add distinct pin-to-left action only after final dynamic dock design/provider and safe API have been selected; current Quicklaunch supports chosen fixed launchers but does not display unrelated running apps.
6. **Validation:** open, close, keyboard search, launch Firefox/Thunderbird/LibreWolf/Signal/Dolphin, installed app categories, favorites reordering, places and power actions, Wayland compatibility, screenshot, logout/login persistence, no changes to tray/clock/top manager/left dock/FenixSystem.

## OWNER's separate new dock decision — DO NOT implement as part of menu work

Owner on 2026-10-29 explicitly **reopened dock choice**: final dock should be **"żywy"**, displaying currently **running applications**, not merely a static curated launcher strip. **Cairo-Dock** is an **idea to evaluate**, not a selected/approved install; verify Fedora 44 / Plasma 6.7.5 / Wayland integration, icon pinning/reordering, task deduplication, notifications (notably Signal), app IDs, window reserve/auto-hide, and maintenance. Native KDE task-manager or a custom applet are alternatives. **Keep current working panel 85/Quicklaunch untouched for now** and focus exclusively on the FX OS menu.

## Status and next input

MENU phase STARTED; existing Kickoff is functional. **Not yet installed:** custom FX icon, new menu popup, two contextual add-to-panel/dock actions. Next screen needed for grounded UI work: existing top-left Kickoff menu **opened** at current Plasma+Oxygen screenshot. Do not presume current contents/geometry without viewing.
