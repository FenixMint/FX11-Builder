# FX Linux — KDE Plasma Visual v0.1 (Fedora 44)

**Data:** 2026-10-28  
**Status:** PLAN WDROŻENIOWY / KONTRAKT WIZUALNY V0.1. Decyzja OWNER: można rozpocząć poprawki wizualne zgodnie z przyjętym kierunkiem. Żadnych zmian pulpitu OWNER jeszcze nie wykonał w tym checkpoincie.

## Źródła i zakres zatwierdzenia

- `docs/decisions/2026-10-21-FX-OS-FAMILY-AND-FX11-BUILDER.md`: własna tożsamość FX OS, atrakcyjnie, nie nazbyt płasko, praktycznie; kontrola użytkownika, audyt i odwracalność; Fedora KDE pierwsza, później możliwe LMDE; zarys: górny panel, lewy dock, menu i monitoring.
- `docs/decisions/2026-10-21-FX-LINUX-FIRST-PORTFOLIO-PRIORITY.md`: FX Linux jest priorytetem P1, adaptacja istniejącej dystrybucji.
- `FX-LINUX-HANDOFF-2026-10-27/WYKONANE-MODYFIKACJE.md`: wygląd FX Linux KDE dotąd tylko projektowy; żadna odtwarzalna konfiguracja Plasma nie została zweryfikowana.
- `FX-LINUX-HANDOFF-2026-10-27/FEDORA-KDE-STAN-PO-INSTALACJI-2026-10-27.md`: Fedora 44, Plasma 6.7.5, Wayland; OWNER wybrał Night Color **5000 K**.
- `FX-LINUX-HANDOFF-2026-10-27/KDE-LUKI-PRZYWRACANIA-2026-10-27.md`: działają FenixSystem KDE V3/autostart, monitory HDMI 1680×1050 i eDP off, TuneD, ZRAM; ciemne tło menedżera logowania ustawione według OWNER. GRUB FX OS mimo wcześniejszej zgody pozostaje wstrzymany po zmianie priorytetu.
- KDE official: https://userbase.kde.org/Plasma/Panels (panele, pozycje, zadania, ustawienia), https://develop.kde.org/docs/plasma/scripting/api/ (przyszła odtwarzalna automatyzacja).
  
**Granice:** profil wizualny tylko na poziomie użytkownika KDE; nie modyfikować GRUB, EFI, partycji, PAM, menedżera logowania, klapy, zasilania, TuneD, kamerki, systemowych usług, Conky autostartu ani konfiguracji monitorów.

## Założenia przyjęte vs propozycje do testu

**Wiążący kierunek:**
1. Własna, rozpoznawalna tożsamość **FX Linux**, bez podszywania się pod inną dystrybucję.
2. Nowoczesny, przestrzenny, czytelny pulpit, nie agresywnie jasny i nie nadmiernie płaski.
3. **Górny panel**, **lewy dock**, menu uruchamiania aplikacji, czytelny stan systemu, istniejący **FenixSystem**.
4. Konfiguracja natywna dla KDE Plasma/Wayland; wszystkie istotne zmiany etapowane, audytowalne i odwracalne.

**Proponowane, jeszcze NIE zatwierdzone jako dokładny projekt:**
- Ciemny granat/grafit i chłodny błękit FX, z subtelnym ciepłym akcentem; nie przypisywać źródłom obowiązującej palety HEX dla pulpitu.
- Górny panel o wysokości ok. 38–42 px na monitorze 1680×1050; po lewej menu, po prawej zasobnik/system i zegar. Panel może być lekko przezroczysty i niezasłaniający FenixSystem.
- Lewy, wyśrodkowany pionowy dock z ikonami zadań/aplikacji; szerokość ok. 54–64 px, bez trzeciego managera docka.
- Istniejący Conky V3 na prawym górnym obszarze (`gap_x=30`, `gap_y=90`) zachować bez zmian, aby nie wywołać regresji Wayland.

Dokładny układ, ikony, tapeta, kolor akcentu, autoukrywanie i wymiary zależą od potwierdzenia wzrokowego przez OWNER, nie wolno ich przedstawiać jako zrealizowanych.

## Kolejność wdrażania — zmiany małymi partiami

### 0. Snapshot tylko konfiguracji użytkownika (przed pierwszą zmianą)

Należy zachować kopię `~/.config/plasma-org.kde.plasma.desktop-appletsrc`, jeśli istnieje. Można to zrobić w osobnym folderze `~/FX-Linux-Odzysk/kde-visual-backup-YYYYMMDD-HHMMSS` wraz z manifestem. Nie kopiować całego home ani materiałów prywatnych na GitHub. Pliki źródłowe użytkownika pozostają nietknięte.

### 1. Szkielet na obecnym pulpicie — pierwszy etap teraz

1. W KDE na pulpicie: prawy przycisk myszy → **Wejdź w tryb edycji** → **Dodaj panel** → **Pusty panel**.
2. Umieść go przy **górnej krawędzi**, na razie bez usuwania bieżącego dolnego panela. Zacznij od wysokości ok. 40 px, preferuj czytelną, neutralną przezroczystość.
3. Dodaj tylko widżety: menu aplikacji po lewej, element elastycznego odstępu, po prawej zasobnik systemowy i zegar; upewnij się, że nie powiela aktywnych kontrolek w stopniu mylącym. W trakcie edycji można przenosić widgety przez GUI.
4. Zachowaj panel dolny jako drogę powrotu do czasu oceny stabilności i wygody.

### 2. Dock po lewej — kolejny etap po akceptacji etapu 1

Dodać drugi **pusty panel**, przesuń do lewej krawędzi; ustawić ~58 px szerokości, długość dobraną do liczby aplikacji, zadania jako ikony bez tekstu. Nie instalować Latte Dock ani pobocznych skryptów bez potrzeby. Zostawić awaryjny panel do czasu oceny działania docka.

### 3. Kolory i tapeta

Ocenić obecną tapetę i preferowany motyw Plasma; proponować ciemne, miękkie barwy i powiązanie ze stylistyką FX OS GRUB, ale nie przenosić bez zgody grafiki ze starego bootloadera jako domyślnej tapety. Nie wykonywać zbiorowego "Global Theme" zmieniającego układ paneli bez kontroli poszczególnych sekcji. Ekran logowania już zmieniony przez OWNER; niezależny od tapety pulpitu.

### 4. Detale i odtwarzalność

Własna ikona menu FX (źródło i prawa autorskie), akcenty, typografia, spójna tapeta, układ statusu, ergonomia przy 1680×1050/1920×1080. Dopiero po ręcznej akceptacji spisać profil Plasma możliwy do odtworzenia na kolejnej Fedorze bez kopiowania ślepo całej starej konfiguracji; osobny przyszły adapter LMDE.

## Bramki jakości

- Po każdej zmianie screenshot z monitora zewnętrznego; nic nie zasłania FenixSystem. Sprawdzenie zegara, Wi-Fi, głośności, baterii, powiadomień i menu.
- Panel i dock działają po wylogowaniu i zalogowaniu, nie zaburzają Conky V3 ani jasności/Night Color 5000 K.
- Użytkownik zawsze może cofnąć zmiany w trybie edycji; kopia oryginalnego `plasma-org.kde.plasma.desktop-appletsrc` jest dostępna.
- Wersja V0.1 **nie znaczy**, że skonfigurowano już pulpit. Dotychczas wdrożone: wyłącznie poprzednie FenixSystem oraz login-screen dark; panele/dock niepotwierdzone.

## Następny wkład OWNER

Po ustawieniu górnego panelu w GUI przesłać zrzut aktualnego pulpitu. Wówczas dobrać właściwe rozmieszczenie i rozmiary, uwzględniając FenixSystem po prawej. Niebieski/bursztynowy kolor pulpitu pozostaje propozycją do oceny.


## 2026-10-28 — visual verification: two overcrowded panels, restore a single panel first

OWNER pokazał zrzut pulpitu Fedora KDE Plasma Wayland po ręcznej próbie dodania górnego panelu. **Stan wizualny niezaakceptowany:** dwa pełnoszerokie panele (górny i dolny), każdy z powielonymi zestawami ikon i kontrolek; w tym stanie nie jest to docelowy górny panel + lewy dock. Conky FenixSystem V3 jest widoczny po prawej, tapeta FX OS pozostaje bez zmian. Sam screenshot nie dowodzi czy powtarzalność pochodzi z kilku widgetów Task Manager, przypiętych aplikacji czy innych osobnych widżetów — najpierw inspekcja w trybie edycji.

**Plan naprawczy bezpieczną metodą natywnego KDE GUI:** (1) skopiować bieżący `~/.config/plasma-org.kde.plasma.desktop-appletsrc` do prywatnego folderu odzysku, bez zapisu prywatnych dotfiles do GitHub; (2) usunąć wyłącznie nowo dodany górny panel przez `Wejdź w tryb edycji` → konfiguracja tego panelu → `Usuń panel`, zostawić oryginalny dolny jako drogę powrotu; (3) sprawdzić wygląd dolnego, ocenić powielone elementy; (4) następnie usuwać tylko rozpoznane zbędne widżety (np. duplikaty Menedżera zadań) w GUI, zachowując jedno menu, jedno miejsce na zadania, jedną tackę i zegar; (5) dopiero po działającym jednym panelu zmienić jego położenie i ewentualnie dodać *pusty* lewy dock. Nie wykonywać równoczesnego usuwania obu paneli, kasowania appletsrc, `plasmashell --replace`, globalnego resetu Plasma ani instalowania Latte Dock.

**Status:** rozpoznano problem wyłącznie wizualnie na zrzucie OWNER; nie potwierdzono jeszcze usunięcia panelu ani testu wylogowania. Dokumentację wolno aktualizować, ale nie twierdzić, że fizycznie naprawiono konfigurację użytkownika. GRUB pozostaje odłożony; Night Color 5000 K i Conky pozostają niezmienione.

## OWNER correction: restore pre-change Plasma backup instead of manually removing panels

2026-10-28: OWNER explicitly requests restoration of **existing pre-change configuration backup** rather than GUI deletion of the newly created top panel. This supersedes the immediately preceding GUI-based repair suggestion. Use `~/FX-Linux-Odzysk/kde-visual-backup-*/plasma-org.kde.plasma.desktop-appletsrc`, if present and unambiguously identifiable as the baseline copied before visual changes; **do not restore** `~/FX-Linux-Odzysk/kde-panel-backup/`, which could have been created only after both panels were already broken. Back up the current broken layout to a different timestamped folder for rollback. Stop only the user Plasma shell service, replace the layout file, and start the same shell service; do not stop KWin or display manager. If no unique original baseline file or missing `plasma-plasmashell.service`, halt and inspect without destructive commands. Verify restored single panel visually before any additional changes. **No on-device restore yet confirmed**; this checkpoint records the owner's instruction and safe plan. GRUB remains paused.


## OWNER verification — Plasma panel configuration restored

2026-10-28: OWNER reported `przywróciło` after running the rollback command that selects a single original `~/FX-Linux-Odzysk/kde-visual-backup-*/plasma-org.kde.plasma.desktop-appletsrc`, stores the current two-panel layout separately, and restarts only the Plasma user shell service. **RESTORE PASS according to OWNER** — the prior Plasma panel arrangement was restored. No claim is made of an independently reviewed post-restore screenshot or fresh-login test. Avoid running the same restore again unnecessarily.

The failed visual first iteration exposed two full-width panels with duplicate app icons. Next iteration: **do not add another full panel or apply global theme presets blindly**. Start by inspecting the restored single-panel arrangement and its individual widgets in KDE edit mode; modify one controlled component at a time, preserving the current working layout and backup. Conky FenixSystem KDE V3, FX wallpaper, login wallpaper, Night Color 5000 K and the paused GRUB restore are outside scope.


## OWNER screenshots — single panel recovered, Signal launcher icon missing until running

2026-10-28. OWNER supplied two screenshots of restored Fedora KDE desktop. The duplicated two-panel state is gone. **One full-width top panel** is visible with application launchers on the left and tray/clock on the right; FenixSystem V3 remains visible at the upper right of FX OS wallpaper.

New defect reported: **Signal Desktop icon missing in the pinned top panel and the application menu while Signal is not running**. The launcher shows a generic blank document icon, but after Signal is launched the correct blue Signal icon becomes visible. OWNER states the same symptom is present in the app menu before launch. This is **not evidence that Signal itself is broken**; a stale or incorrect icon name/path in a `.desktop` entry, duplicated launchers, Flatpak/AppImage export, or Plasma application identification/icon caching are possible explanations, unconfirmed.

First diagnostic must be read-only: detect Signal installation type, inspect exact `.desktop` entries in the user's application directory, system application directory and Flatpak export locations; capture only Name, Icon, Exec, StartupWMClass, X-Flatpak and desktop file paths. Do not reset Plasma, purge cache, reinstall Signal, remove pinned applications, or overwrite desktop files until root cause is identified. Official Signal Linux documentation includes AppImage launchers with `Icon=signal-desktop` and `StartupWMClass=signal`: https://support.signal.org/hc/pl/articles/360008216551-Instalacja-aplikacji-Signal .

**No on-device Signal icon fix has been applied or verified in this checkpoint**.


## Signal Desktop AppImage — identified launcher and icon lookup

OWNER confirmed Signal uses AppImage rather than Fedora RPM or Flatpak. Read-only scan found only the user's launcher at `~/.local/share/applications/signal-appimage.desktop`.

Launcher fields: `Name=Signal Desktop`, `Exec=~/.local/bin/signal-desktop.AppImage %U` (repo anonymized: actual desktop file uses absolute home path), `Icon=signal-desktop`, `StartupWMClass=signal`.

Important: `Icon=signal-desktop` and `StartupWMClass=signal` match current official Signal AppImage launcher guidance: https://support.signal.org/hc/en-us/articles/360008216551-Installing-Signal . Do NOT assume that this icon name is incorrect. Test whether a matching `signal-desktop` icon is actually available in XDG icon directories, including user icon themes. The AppImage format includes its main icon under `.DirIcon` / root icon or `usr/share/icons`: https://docs.appimage.org/reference/appdir.html .

Behavior from OWNER screenshot: generic blank-paper icon in launcher and app menu while Signal is not running; actual blue Signal icon appears after launching. Missing installed icon is a plausible cause, **not yet verified**.

Next step: read-only lookup of icon in user and system theme paths and AppImage executable. If no icon is registered, extract from the existing AppImage and install only the image in user icon theme, without rewriting the working launcher, resetting Plasma, removing favorites, or reinstalling Signal. No on-device fix was made in this documentation update.


## Signal AppImage — missing installed icon confirmed by OWNER

OWNER confirmed read-only diagnostic on 2026-10-28: Signal AppImage exists as executable `~/.local/bin/signal-desktop.AppImage` (~138 MB); `rpm -q signal-desktop` returned not installed; icon lookup produced **no matches** for `signal-desktop.*` or `signal.png` under the checked user and system icon directories.

Together with previously verified `~/.local/share/applications/signal-appimage.desktop` containing `Icon=signal-desktop` and `StartupWMClass=signal`, this supports a missing icon-registration diagnosis. The AppImage's embedded graphic has not yet been extracted or inspected, so no on-device fix can be claimed.

Safe user-level repair planned: run the already-owned AppImage with `--appimage-extract` inside an isolated folder under `~/FX-Linux-Odzysk`, locate authentic `signal-desktop.png` under `usr/share/icons/hicolor/*/apps` or AppDir root, validate PNG MIME and copy to matching `~/.local/share/icons/hicolor/<size>/apps/signal-desktop.png`. No `sudo`, no edits to the desktop entry, no reset of Plasma and no Signal reinstall. Official AppImage docs: https://docs.appimage.org/user-guide/run-appimages.html and https://docs.appimage.org/reference/appdir.html. After user action, confirm icon in menu and pinned panel while Signal is closed; only then mark PASS.

Private user's absolute home path and private AppImage contents are not committed to GitHub.


## Signal AppImage — original icon restored; unread badge and notifications still required

**2026-10-28 — OWNER terminal confirmation**: the original Signal icon was extracted from the trusted local AppImage and installed as `signal-desktop.png` in the user's `~/.local/share/icons/hicolor/` at **nine** sizes: 16, 24, 32, 48, 64, 128, 256, 512, 1024 px. Installation finished successfully. OWNER reports the icon is now present; this is **static icon restoration PASS**, not proof of unread badge behavior or desktop notifications.

**New OWNER functional requirement / regression from prior Linux Mint with Debian package**: on new unread Signal messages, the Signal application icon should visibly change/show badge, and KDE desktop notifications must appear; changes should clear with reading. User emphasizes both functions as important. On Fedora 44 KDE Wayland Signal is distributed as AppImage and launched from `~/.local/share/applications/signal-appimage.desktop`. Do not treat installing a PNG as implementing dynamic badges.

Distinct mechanisms to test:
1. Signal Settings > Notifications: enable notifications, configure new App Badge section (unread messages or unread chats where supported). Signal desktop added configurable App Badge counts around v8.27 (September 2026). Source: https://aboutsignal.com/de/news/signal-introduces-new-notification-settings/ and https://fossies.org/diffs/Signal-Desktop/8.26.0_vs_8.27.0/_locales/en/messages.json-diff.html . Check actual installed Signal version in Help > About rather than assuming it has this feature.
2. Plasma System Settings > Notifications: enable 'Notification badges: Show in task manager' and per-app Signal notification popups/history/badges. Official KDE docs: https://docs.kde.org/stable_kf6/en/plasma-workspace/kcontrol/notifications/ . Check DND and notification filtering.
3. Signal's notification-area (tray/statusnotifier) icon is **separate** from the task-manager launcher badge. Recent Signal/Electron regression around versions 8.24-8.25 affected tray icon on Linux, and some AppImage builds had continued trouble around 8.26. Source: https://github.com/signalapp/Signal-Desktop/issues/7992 and https://github.com/signalapp/Signal-Desktop/issues/8034 . Check actual version and configured minimize-to-tray behavior before any workarounds.
4. Potential but UNCONFIRMED desktop-id mismatch: current Signal source package.json declares `desktopName: signal.desktop` (https://github.com/signalapp/Signal-Desktop/blob/main/package.json), whereas OWNER launcher is `signal-appimage.desktop`. Electron's app.setBadgeCount links badges to desktop file IDs via LauncherEntry D-Bus API: https://www.electronjs.org/docs/latest/api/app . The current AppImage's actual embedded app version/config was not checked; do not rename launchers or repin without testing and backup.

**Safe next step**: inspect GUI notification settings, Signal version, tray setting, and conduct an ordinary self-chosen incoming message test with Signal minimized. Only observe badges and notifications; do not ask for private message content. Do not change Signal database/profile, reinstall into .deb on Fedora, downgrade Signal, clear Plasma state, or install third-party notification daemons. No unread/status notification test is confirmed yet.


## Signal notification preferences — OWNER screenshot reviewed

2026-10-28: OWNER supplied a screenshot of Signal Desktop's own **Powiadomienia** settings, read only (the image is private and not stored in GitHub). Confirmed UI values:
- `Włącz powiadomienia` ON; display level `Imię, treść i działania`; muted notification class allows calls/mentions/replies.
- `Powiadomienia o reakcjach` ON, `Przypomnienia o nieprzeczytanych` ON, `Wyróżnij okno aplikacji Signal, gdy pojawi się powiadomienie` ON.
- Both push-notification sounds and in-chat sounds ON.
- `Licznik nieodczytanych wiadomości` configured as `Nieodczytane wiadomości`; including muted chats in application count OFF.

**Signal-side preferences set / reported, but no incoming-message delivery test performed yet.** Window highlighting is not proof of a badge counter. KDE Plasma has an independent `System Settings → Notifications → Application Progress and Badges → Notification badges → Show in task manager` setting and per-app badge/popups/notification-history permissions, per official KDE documentation: https://docs.kde.org/trunk_kf6/en/plasma-workspace/kcontrol/notifications/index.html .

Electron's Linux API `app.setBadgeCount()` requires a launcher matching the app `.desktop` identification: https://www.electronjs.org/docs/latest/api/app . Current launcher is `signal-appimage.desktop` (official Signal AppImage integration instructions also suggest that filename: https://support.signal.org/hc/en-us/articles/360008216551-Installing-Signal). A possible mismatch is a **hypothesis only**: do not rename the launcher, clear Plasma cache, or alter pinned tasks before testing whether a badge fails with the KDE setting enabled.

**Next:** OWNER inspect KDE's global and Signal-specific badge/popups settings; send an unread test message to Signal while minimized, look for (a) notification popup, (b) numbered badge on the pinned task icon, (c) tray behavior if enabled, and (d) clearance on reading. Do not disclose message contents. If notifications work but badges do not, check actual AppImage desktop name and test narrow reversible desktop-ID adjustment. No fix beyond static icon installation yet.


## Signal unread test — internal notification visible, Plasma icon unchanged

OWNER reports after receiving a message: Signal shows an unread indication **inside the application**, but the KDE task-manager icon **does not change**. Do not equate internal UI indication with a successful KDE notification popup or with D-Bus badge delivery; those two behaviors have not yet been verified by OWNER. The icon installed in nine `hicolor` sizes is a static asset, not an unread indicator.

Potential integration mismatch: user launcher file `signal-appimage.desktop` follows Signal's AppImage installation instructions, but upstream Signal Desktop `package.json` currently specifies `desktopName: signal.desktop`; Electron documents that Linux `app.setBadgeCount()` emits LauncherEntry D-Bus updates and requires the actual `.desktop` filename to match `app.setDesktopName` / `desktopName`. Sources: https://www.electronjs.org/docs/latest/api/app and https://github.com/signalapp/Signal-Desktop/blob/main/package.json . Signal 8.27 added `set-badge-count` use (https://fossies.org/diffs/Signal-Desktop/8.26.0_vs_8.27.0/app/main.main.ts-diff.html). Version of OWNER AppImage is still unknown, and behavior may differ; **mismatch is a hypothesis, not a confirmed cause**.

Next noninvasive test: KDE System Settings → Notifications → Notification badges → Show in task manager; Signal app-specific notification badges and popups; separately observe whether a Signal incoming unread triggers `com.canonical.Unity.LauncherEntry.Update` with `dbus-monitor --session "type='signal',interface='com.canonical.Unity.LauncherEntry',member='Update'"`. This generally reveals the launcher URI and numeric badge count, not message text. If it produces `application://signal.desktop` while the pinned icon points to `signal-appimage.desktop`, design a narrow reversible launcher-ID correction *with backup and careful repinning*, no duplicate panels or global reset. If no signal is emitted, diagnose Signal/Electron runtime before making launcher changes.

Nothing about this test involves reading Signal message contents or touching its encrypted profile database. No on-device badge fix has been performed at this stage.


## Signal KDE badge — D-Bus monitor contained no LauncherEntry.Update during observation

2026-10-28: OWNER executed `dbus-monitor --session "type='signal',interface='com.canonical.Unity.LauncherEntry',member='Update'"` and supplied output showing only D-Bus service bookkeeping `NameAcquired` and `NameLost`. **No `com.canonical.Unity.LauncherEntry.Update` was captured in the shown observation.** There is no explicit confirmation that a fresh unread event occurred while this monitor was running, so absence of messages must not be claimed as proof Signal never emits them.

Electron documents `app.setBadgeCount` on Linux for desktops supporting LauncherEntry and requires the `.desktop` file name to match `app.setDesktopName`/package `desktopName`: https://www.electronjs.org/docs/latest/api/app . Current Signal source declares `desktopName=signal.desktop` (https://github.com/signalapp/Signal-Desktop/blob/main/package.json); official AppImage instructions use `signal-appimage.desktop` (https://support.signal.org/hc/en-us/articles/360008216551-Installing-Signal). **Potential ID mismatch**, not confirmed as actual runtime blocker. KDE explicitly provides `Notification badges → Show in task manager`: https://docs.kde.org/trunk_kf6/en/plasma-workspace/kcontrol/notifications/index.html .

**Next safe diagnostic:** inject one temporary **synthetic badge signal** via `gdbus emit` for the existing launcher ID `application://signal-appimage.desktop`, show a test count briefly then clear it; this does not create Signal messages or edit user config. If Plasma displays it, taskbar badge pipeline is functional for that ID; then retest with an actual new unread message while D-Bus monitor is already running. If no badge, inspect KDE global toggle and pinned launcher/task-manager app type. Do NOT rename `.desktop`, reinstall Signal, or clear Plasma configs yet.

Static Signal PNG icon install in nine sizes remains PASS; Signal in-app notification/unread settings screenshot reviewed; system popup appearance and real external badge delivery are still unverified.


## Signal unread badge — synthetic LauncherEntry test PASS

OWNER confirmed on Fedora KDE: `gdbus emit --session --object-path /com/canonical/unity/launcherentry --signal com.canonical.Unity.LauncherEntry.Update 'application://signal-appimage.desktop' "{'count-visible': <true>, 'count': <2>}"` produced the number **2 instantly on the pinned Signal icon**, and clearing the same identifier after the 12-second test removed the badge. **KDE launcher badge display and existing pin ID PASS**. No changes to Signal profile, launcher or panels from this test; it generated only a synthetic D-Bus signal.

Upstream Signal Desktop (as checked 2026-10-28): `package.json` has `desktopName: signal.desktop`; `app/main.main.ts` invokes `app.setBadgeCount(badgeCount)` when handling `set-badge-count`. Electron documentation explicitly requires Linux desktopName and installed `.desktop` filename to match. Current OWNER launcher basename is `signal-appimage.desktop`, and a synthetic message addressed to that basename displayed correctly. This mismatch is a **strong hypothesis**, not yet proof of actual Signal IPC or incoming-message badge behavior. Source: https://www.electronjs.org/docs/latest/api/app ; Signal repository main `package.json` and `app/main.main.ts`.

Next minimal diagnostic: run `dbus-monitor --session "type='signal',interface='com.canonical.Unity.LauncherEntry',member='Update'"` **before an actual new unread Signal message arrives** and record whether it emits `application://signal.desktop`, `application://signal-appimage.desktop`, or nothing. Previous monitor output showed only D-Bus NameAcquired/NameLost, with no explicit confirmation a new unread event happened during monitoring. Do not rename desktop file, repin or reset panel before this observation. If actual message emits `application://signal.desktop`, repair launcher mismatch with a backup and targeted unpin/repin. If no emission, investigate exact installed Signal AppImage version and runtime badge behavior instead. Do not read or store message content.


## Signal — KDE popups now seen and transient overlay on pinned icon

2026-10-28: After the synthetic LauncherEntry badge test and a further real Signal notification test, OWNER reports that **KDE system notifications appeared** and a **small transient bell/sound-like overlay** appeared on the Signal icon. This is positive evidence that Signal can deliver KDE desktop notifications and that the pinned icon reacts visually to an event.

Do **not** misclassify this overlay as a persistent numerical unread badge. It may indicate application attention or playback of a notification sound (Plasma task manager shows audio activity overlays). The OWNER has not reported a lasting unread count, nor provided LauncherEntry D-Bus `Update` output from the new message. On the prior synthetic badge test, number `2` appeared immediately and cleared correctly after 12 seconds, so Plasma's LauncherEntry target `application://signal-appimage.desktop` works.

Remaining acceptance criteria: a badge should reflect real unread message count and clear after reading, not only flash during playback of a notification sound; no need to change already working Signal notification settings. If monitoring was active during the real event, inspect any `com.canonical.Unity.LauncherEntry.Update` line and reported `application://...` identifier. If no update appears despite a confirmed new unread event, diagnose Signal's Electron badge emission or launcher desktop-name mismatch (Signal source identifies `signal.desktop` while the user installed official AppImage launcher `signal-appimage.desktop`). Do not reset Plasma, rename a working launcher or repin prematurely.

Source context: https://www.electronjs.org/docs/latest/api/app (setBadgeCount Linux LauncherEntry desktop ID) and https://api.kde.org/kstatusnotifieritem.html (NeedsAttention status may indicate a received IM).

Status: system notification popups **PASS** by OWNER report; reactive transient icon overlay **OBSERVED**; persistent unread badge **NOT VERIFIED**.


## 2026-10-29 — OWNER resumes FX Linux Plasma redesign

OWNER explicitly resumed redesign of FX Linux KDE desktop, panels and dock on 2026-10-29, requesting the previously documented visual direction, replacing the pause recorded in `../CHECKPOINT-2026-10-28-WYGLAD-SIGNAL.md` **only for visual/layout work**. Signal real persistent unread badge remains paused, whereas working menu icon, notifications and synthetic icon badge must be preserved.

Verified project direction: one slim **existing top panel** for FX launcher, tray/status/clock; one **separate, native Plasma empty left-side dock panel** initially; keep FenixSystem Conky at upper right and current FX OS wallpaper. Suggested exploratory geometry: top ~40 px, left dock panel ~58 px thick, centered vertically, fixed/custom modest length initially; exact appearance must be OWNER-accepted by screenshot. The prior failure was a duplicated full-width panel with repeated widgets; never use `Default Panel` for the dock, clone the populated top panel, or remove/replace both panels in one action.

Execution plan: (0) OWNER creates new private timestamped snapshot of existing `~/.config/plasma-org.kde.plasma.desktop-appletsrc` under `~/FX-Linux-Odzysk/kde-visual-backup-*` and checks hash; (1) preserve existing working top panel unchanged while adding *only* a blank left panel through native KDE GUI, position left, align center, set ~58 px thickness and custom short length (not full-height); (2) obtain new screenshot / OWNER verification of blank dock skeleton before adding any applets; (3) add exactly one Icons-only Task Manager to the dock with controlled pinned apps, verify each app, then **only afterward** remove the corresponding old top-panel task manager / launchers; (4) refine existing top panel to menu left, spacer, systray and clock right with ~40 px height; (5) revisit typography/FX icon/color/opacity as separate reversible phases.

Only permission to guide/user-apply desktop changes is implied; **no remote device access** and nothing on the OWNER desktop is changed by this GitHub documentation write. No commands for EFI, GRUB, login manager, power, system services, monitor geometry, Night Color or Conky. Do not install third-party docks / layout packages. Do not interpret the proposed measurements as previously OWNER-approved exact values.

Status: **plan resumed; backup/new dock construction not yet run or verified by OWNER**.


## 2026-10-29 — three OWNER-supplied original FX OS visual references

OWNER supplied three original FX OS desktop design reference images following an inaccurate newly generated alternative. **Do not treat the generated mountain/weather/calendar concept as the approved visual contract.** The actual visual direction is present in these three supplied screenshots. Images are not copied to the public GitHub repository; descriptions below are the approved-source visual audit, with selection as a reasoned recommendation pending direct OWNER confirmation.

**Reference 1 (image 1):** Dark FX OS original cosmic/blue-ring wallpaper and very dark glass-like interface with glowing blue borders. Very narrow vertical dock at left, FX button top, icons below; **bottom horizontal taskbar** with FX logo, pinned apps, systray/date; large three-column FX OS start menu (left categories, center favorites and all apps, right Places/Settings/Recent/Power). This bottom-taskbar variation **differs from** the previously agreed top-panel direction, but its rich menu and dock aesthetics are useful reference.

**Reference 2 (image 2, recommended layout baseline because matches documented concept):** Compact full-width **top panel** with FX app/menu button and a few launchers on left and system icons/time on right; separate thin **left vertical dock** with circular glowing FX icon, app launchers and bottom recycle bin; large dark, blue-border-glow **FX OS menu** below top bar with search row, left category column, favorites/recently used middle area and Places/System/Power right area; original FX OS wallpaper with luminous arc centered; detailed classic **FenixSystem monitoring** on the right. On displayed 1680x/approx 1050 screenshot, FenixSystem remains visible to right of opened menu. This best embodies **top panel + left dock + menu + FenixSystem**.

**Reference 3 (image 3):** Compact top bar with numbered desktop/workspace switcher `1 2 3 4` and systray to right; left full-height dock; alternate two-column FX OS start menu with favorites left, app categories right; right-side compact three-ring monitoring card rather than full classic FenixSystem. Useful optional inspiration for virtual desktop switcher and simpler launcher layout but not mandatory features.

**Distinguishing effects:** Black/dark-navy surfaces, electric blue/cyan neon edge lighting and subtle translucent/blur layers, rounded corners, FX-branded iconography and menu heading, original space-lit FX OS wallpaper. Reproduce these visually in KDE insofar as native widgets allow. Do not promise the custom, multi-column FX menu can be obtained merely by applying a built-in Application Launcher theme; that is a separate widget/launcher UI implementation or customization task requiring design/technical feasibility evaluation.

**Best next implementation step remains safe and incremental:** Make fresh user-only copy of `plasma-org.kde.plasma.desktop-appletsrc`; preserve existing upper panel, wallpaper, FenixSystem and working Signal notifications; add one `Pusty panel` to left edge only, ~58px, centered, no widgets yet; verify screenshot. Later add icons-only task manager and reorganize existing top panel. Never use `Default Panel` or copy a populated panel. Owner has not yet confirmed running these steps in the resumed session.

Status: visual references reviewed, reference 2 recommended as starting architecture; **no additional local Plasma modification is verified**.


## 2026-10-29 — OWNER selects reference 3 as principal FX OS visual target

OWNER showed the third original mockup again (original cosmic FX OS wallpaper, upper bar with desktops 1–4, slim glowing FX icon dock to left, large FX OS menu on left and compact telemetry card at upper right) and explicitly stated this is **the best reference**. The previously newly generated (mountain/weather/calendar) mockup was described as decent, but **not preferred**. This explicit OWNER choice **supersedes the previous assistant's recommendation to use reference 2 as principal**. Preserve the 3 original images as conceptual reference; images are in chat only and were not committed to the public repo.

**Selected target components**, visually faithful to supplied reference:
- Top slim translucent dark panel, workspace switcher `1 2 3 4` left, tray/status + date/time right; no bottom full-width taskbar.
- Left vertical dock integrated into layout: round glowing FX mark/menu launcher on top, apps down the left with blue highlight and subtle separators, trash icon near bottom; should work as native Plasma panel/Icons-only Task Manager where practical.
- Large **FX OS** custom-look launcher with cyan edge glow, dark/glass background, rounded edges, top search field, favorites list in left column, app categories/places/actions in right column, logout/restart/shutdown buttons near bottom. **Do not claim exact custom menu is available through native Application Launcher appearance alone**; investigate separate custom Plasma launcher design/implementation after safe panel foundation.
- Original FX OS wallpaper with blue luminous halo, central FX OS branding.
- Compact dark-glass FenixSystem card at upper right with circular CPU/RAM/disk values, network activity and uptime. Current detailed Conky FenixSystem is functioning, must be **preserved until a separately tested replacement** is accepted. Numeric values in reference image are illustrative, not current machine measurements.

**Design status:** OWNER selected visual target; not proof of a working Plasma layout or approval of system-level changes. Next action: ensure an actual fresh local backup exists, then create one *empty left panel* in native KDE edit mode, without changing existing upper panel or working FenixSystem. Follow with screenshot for geometry review; add applets and custom menu incrementally. Previous duplicate-panel failure is a prohibited repeat pattern.

**Status precedence:** this note supersedes only the earlier reference 2 preference, not the rollback safeguards, Signal pause, KDE user-level scope, or no-GRUB/EFI/PowerDevil modifications.


## 2026-10-29 — OWNER final correction: existing FenixSystem V3 is immutable in visual redesign

**Wiążąca decyzja OWNER (korekta nadrzędna wobec poprzedniej sekcji):** „panel FenixSystem ma być taki jak jest, nie robimy go kompaktowego”. **Zachować bieżący, rozbudowany FenixSystem V3 dokładnie w istniejącej formie** — bez zmniejszania do karty, bez zamiany na trzy wskaźniki kołowe, bez zmiany wymiarów, położenia, układu metryk, wyglądu, konfiguracji Conky, autostartu ani skryptów monitorujących.

Zdjęcie nr 3 pozostaje **głównym wzorem jedynie dla paneli, docka, menu FX OS, tapety/kolorystyki i subtelnych podświetleń**. Przedstawiony na nim **kompaktowy panel monitoringu jest wyraźnie WYŁĄCZONY z zakresu** — nie wolno odtwarzać go ani traktować jako planowanego zamiennika. FenixSystem V3 ma zachować dotychczasowe miejsce u góry po prawej; nowe elementy KDE należy rozmieścić tak, aby go nie zasłaniały.

Zakres implementacji: nowy lewy dock, uporządkowany górny panel, docelowe menu FX OS i estetyka/efekty w natywnym KDE. Każda zmiana odwracalna, snapshot konfiguracji Plasma przed edycją. Żadna lokalna zmiana nie została wykonana przez sam ten zapis na GitHubie.


## 2026-10-29 — OWNER screenshot: empty left panel built; FX launcher must remain top-left

OWNER supplied an actual Fedora KDE screenshot after the first native-Panel step. **Confirmed visually**: the original horizontal top panel survives with its current KDE application launcher at far upper-left, multiple application icons and functional system tray/clock at right. A second **blank vertical panel** exists at left beneath/along the upper panel; it is currently **almost full screen height**, appears dark gray and has a plus/handle around mid-height, **not yet a compact floating dock**. Wallpaper FX OS and full existing detailed FenixSystem V3 at upper-right remain unaffected. No duplicates of a populated second horizontal bar are visible. Existence of a fresh backup from this resumed phase was not confirmed in OWNER terminal.

**Explicit OWNER correction / binding:** 'przycisk menu (okrągły FX) ma być w lewym rogu górnego panelu (tam gdzie jest obecny przycisk menu)'. Therefore: the **round glowing FX icon / FX OS application launcher goes exclusively at the FAR LEFT OF TOP PANEL**, replacing the current KDE launcher icon in the existing widget; **NOT on top of left dock**. Keep left dock for pinned/running applications and optionally trash, with no second FX launcher. This supersedes layout elements from the chosen concept art that depict a large FX emblem atop the vertical dock.

Implementation recommendation for the next small change: preserve current top Application Launcher widget and configure its icon in place (right click menu → Configure Application Launcher → click icon → choose approved local round FX icon; user-owned icon asset not yet provided/extracted, so do not invent one or alter launcher if the asset is absent). Independently adjust the left empty panel's length, centering, floating and thickness in panel edit mode; only after screenshot validation add Icons-only Task Manager. **Do not remove or re-add working launcher** while changing icon; desktop's Signal pinned-task and notification integration should remain intact. No scripts to modify `appletsrc`, restart Plasma or reinstall docks.

Status: empty left panel creation **OBSERVED**, FX launcher placement **OWNER APPROVED**, dock compact geometry and actual FX menu/icon visual **PENDING**. FenixSystem V3 is outside scope, unchanged.


## 2026-10-29 — OWNER requests terminal-only precise left-dock geometry

OWNER reports that dragging sliders in Plasma GUI to set the current *empty* left panel's vertical position and height is inconvenient; asks to set it **from the terminal**. The latest cropped screenshot shows a tall dark left panel and an edit plus marker, with the upper-left application launcher still appearing at its top.

Confirmed supported Plasma Desktop scripting API via KDE official documentation: enumerate `panels()`, select the unique panel with `location === 'left'`, use `lengthMode='custom'`, `height` (vertical panel width), `minimumLength`, `maximumLength`, `length`, `alignment='center'`, and `offset=0`. Read-only `widgetIds.length` allows refusing to touch populated unexpected panels. Official sources: https://develop.kde.org/docs/plasma/scripting/api/ and https://develop.kde.org/docs/plasma/scripting/ ; programmatic call D-Bus `org.kde.PlasmaShell.evaluateScript` on `org.kde.plasmashell /PlasmaShell`.

Proposed **OWNER-run**, user-level, one-shot terminal edit, not yet executed or confirmed: before any D-Bus mutation copy **both** `~/.config/plasma-org.kde.plasma.desktop-appletsrc` and `~/.config/plasmashellrc` to a unique timestamped private backup under `~/FX-Linux-Odzysk/`. In JS assert precisely one `left` panel, exactly one existing `top` panel, and `left.widgetIds.length===0` (still empty), otherwise abort. Then set only left `p.lengthMode='custom'; p.minimumLength=450; p.maximumLength=450; p.length=450; p.alignment='center'; p.offset=0; p.height=58; p.hiding='none'` and enable `p.floating=true` only if exposed by the runtime API. Do not alter any top-panel widget, remove/create panels, modify Conky, or restart Plasma. After execution, visually check and verify on the next login, recording actual result only upon OWNER confirmation.

Exact pixel values remain **working proposal**, not fixed product standard. The desired round FX launcher remains at far left of the **top** panel, not left dock. FenixSystem V3 unchanged.


## 2026-10-29 — left dock geometry PASS (OWNER terminal and screenshot)

**Verified by OWNER terminal output and fresh screenshot**: the native Plasma Desktop Scripting interface successfully configured the **existing empty left panel ID 81** with `p.location='left'`, `p.alignment='center'`, `p.length=450`, `p.height=58`, while preserving the populated top bar and its launcher/widgets. Terminal output: `FX DOCK: ID=81`, `Położenie: left`, `Wyrównanie: center`, `Wymiary: 58 x 450`. Visual screenshot now shows a dark ~58px wide vertically centered dock at the left rather than a full-height strip; an editing plus icon appears within it and no app icons have been installed. Do not claim this verifies FenixSystem visually from the cropped screenshot, although the script only modified the left panel.

OWNER copied `plasma-org.kde.plasma.desktop-appletsrc` and `plasmashellrc` into their private timestamped backup `~/FX-Linux-Odzysk/kde-dock-backup-20261029-152555`. **Geometry configuration: PASS**. No Plasma restart or reinstall was required.

**Next single step suggested**: add precisely one `org.kde.plasma.icontasks` (`Menedżer zadań tylko z ikonami`) widget to the **current left panel ID 81**, preferably via the supported native Plasma scripting API (`panel.addWidget`) to match OWNER preference for precise console configuration. Before mutation back up both Plasma config files to another unique private timestamped folder. Guard: require exactly one left panel ID 81 with zero existing widgets, and `knownWidgetTypes.includes('org.kde.plasma.icontasks')`. Stop if those conditions fail; never create a new panel or add a task manager to the top. Verification: visually inspect dock and running app buttons; the existing top panel remains intact, so running-app icons may temporarily be shown in both places until deliberate migration after acceptance. Do not unpin/repin Signal or alter its working notification integration in this step.

Sources: KDE API https://develop.kde.org/docs/plasma/scripting/api/ documents `Containment.addWidget(string)` and `widgetIds`, and KDE's own Unity-like panel example https://userbase.kde.org/Plasma/How_to_create_a_Unity-like_look_and_feel_theme_using_Plasma%E2%80%99s_Desktop_Scripting_API uses `leftpanel.addWidget('org.kde.plasma.icontasks')`. **No widget installation executed or verified yet.**


## 2026-10-29 — left dock Icons-only Task Manager now populated (visual PASS)

OWNER supplied new full 1680×1050 KDE screenshot after instruction to add `org.kde.plasma.icontasks` to the existing left panel ID 81. **VISUAL PASS:** a ~58px dark vertical dock is present at left, vertically centered, populated by application icons including Firefox, Plasma Settings, Dolphin, Discover, Signal, Konsole, and another pinned/running app. The original full-width **top panel** still displays application icons and a launcher plus tray/time at right, so duplicate icons across panels are **currently expected temporary state**. The original blue-ring FX OS wallpaper remains, and the complete **FenixSystem V3 detailed telemetry remains visibly present** in its existing upper-right place. No blank extra top panel or duplicate menu observed.

User did not provide terminal stdout for the widget insertion, but screenshot is strong visual evidence the icons-only task manager was added and functioning at least for icon rendering. Do not claim task activation, Signal live unread badge, persistence after login, or click handling as tested yet. Do not assume all icons currently visible in upper task manager are replicated in left dock.

**Next safe step:** prior to changing the upper panel, read-only inventory of each panel's `id`, `location`, and each `widget.id`, `widget.type` via KDE Plasma Scripting `panels()` / `panel.widgetIds` / `panel.widgetById(id)`. The current left dock geometry was set on panel ID 81, but inspect runtime IDs rather than assuming unverified top IDs. KDE official API: https://develop.kde.org/docs/plasma/scripting/api/ . No changes to the top panel until confirmed widget topology; then use another timestamped home-only backup and remove **only the identified top task manager** after confirming the left dock accepts needed pinned apps. Preserve the existing top launcher widget (future round FX icon), systray, clock and working Signal notification state. Keep FX V3 exactly as is.

Status: **Left dock populated VISUAL PASS**; dock runtime/feature/after-relogin test not yet recorded; clean top bar, FX menu icon, workspace switcher and FX OS custom launcher still pending.


## 2026-10-29 — OWNER final left dock application order and running-task overflow

**Binding OWNER correction superseding the immediately preceding provisional order and any screenshot-default pin order.** The **native Plasma left dock** is to show the following pinned apps **top to bottom, exactly in this order**:

1. Firefox
2. Thunderbird
3. LibreWolf
4. Signal
5. Terminal (on current KDE installation, identify actual terminal desktop entry; likely Konsole but do not assume without read-only validation)
6. RustDesk
7. Ustawienia systemowe (KDE System Settings)
8. Discover
9. KWrite
10. and after: **other currently running applications**, automatically appearing below the nine pinned items; apps already pinned at positions 1–9 must **not** appear a second time when running.

Implementation: one `org.kde.plasma.icontasks` widget already visually confirmed on left panel ID 81. Its pins are independent of upper panel's pins, so **only configure the left task-manager widget**, leaving top panel intact until later deliberate cleanup. Verify installed `.desktop` identifiers for Thunderbird, LibreWolf, Signal AppImage (`signal-appimage.desktop`), Terminal/Konsole, RustDesk, Discover, KWrite by read-only audit before writing pinned-launcher URLs. Do not invent app IDs or implicitly install missing apps. Confirm whether runtime task manager correctly groups existing pinned and running windows under one icon; specifically preserve Signal window identification/notifications.

**Geometry caveat:** previous dock was deliberately fixed to length 450px and thickness 58px. Nine pinned icons plus additional running apps **may exceed this capacity** and create clipping/overflow. Later adapt length mode / constraints to content and available monitor height, or adjust icon sizing while preserving legibility; do not silently truncate desired apps. Keep dock vertically aligned, dark/floating. Before any Plasma widget change take new private backup of `~/.config/plasma-org.kde.plasma.desktop-appletsrc` and `~/.config/plasmashellrc`.

Unchanged OWNER decisions: glowing circular FX launch icon belongs only at **far-left of the top panel**, not the dock; existing complete FenixSystem V3 is not to be changed, resized, moved or made compact; wallpaper/Signal notifications preserved. **This GitHub record does not claim the pin order was applied locally**.


## 2026-10-29 — OWNER definitive flexible left-dock pin order (10 apps)

**Latest and definitive OWNER specification**, superseding earlier provisional 7-, 9- and other 10-item pin orders: current requested top-to-bottom initial pinned launcher sequence is:

1. Firefox
2. Thunderbird
3. LibreWolf
4. Signal
5. Dolphin
6. Terminal (Konsole; use existing system terminal launcher, verify desktop ID)
7. RustDesk
8. KDE System Settings (Ustawienia systemowe)
9. Discover
10. KWrite
11. and later: all OTHER **currently running** apps only, not in 1–10.

**Crucial OWNER flexibility requirement:** this is the STARTING order, **not a permanently fixed/locked policy**. OWNER must be able to drag/rearrange the ten pinned launchers freely at any time, and to change future pinned apps without editing source code or running a reinstall script. There must be only one representation of each pinned app when running (launcher becomes task); unpinned running apps follow the pinned group. Keep `Menedżer zadań tylko z ikonami` (`org.kde.plasma.icontasks`) as **one widget** within left panel ID 81, `Sort=Manually` and grouping by app where supported. Do not construct ten separate KDE launcher widgets or create fixed per-app panel components, since then item reordering and identity become error-prone.

Upstream KDE evidence: task manager model substitutes running task for matching pinned launcher and keeps pinned launchers separate, with unpinned running tasks afterward (https://api.kde.org/legacy/plasma/plasma-workspace/html/classTaskManager_1_1TasksModel.html). KDE Discussions confirms Icons-only Task Manager allows drag-to-reorder pinned icons among themselves, and running unpinned tasks among themselves, but not interleaving those categories, as desired (https://www.mail-archive.com/kde-bugs-dist%40kde.org/msg1186594.html). This is expected native behavior, not evidence of failure.

**Geometry warning:** existing left panel ID 81 is 58px thick and 450px long, which may be insufficient for 10 pinned app slots plus running tasks. KDE Plasma native scripting API supports `lengthMode='fit'` to adapt panel to content (https://develop.kde.org/docs/plasma/scripting/api/). Change geometry as a separate user-verified step, possibly Fit content with sensible maximum length, preserving FenixSystem and upper bar. Do not assume exact icon pixel size, density or number of rows without seeing the result.

**Next safe step:** inspect current Icons-only Task Manager widget ID/config and find matching app `.desktop` IDs (including AppImage Signal and possibly RustDesk/LibreWolf). Work within the single existing widget: pin missing apps, reorder by mouse in manual sort, test opening a pinned app keeps exactly one button, test another unpinned app is appended. Prefer existing working GUI pinning/reordering; if scripting launchers, back up before change, do not invent `applications:` URLs or reset whole Plasma configuration.

**Status:** ORDER DESIGN / OWNER REQUIREMENT CONFIRMED, not yet applied to actual pinned order. No launcher or panel configuration was modified by this GitHub-only documentation update. Existing Signal notification integration and full FenixSystem V3 remain outside scope.


## 2026-10-29 — OWNER requires menu action to add any application to left dock

**Explicit OWNER requirement (follows flexible 10-app pin order):** when choosing **any application from the application menu**, the OWNER wants to right-click it and choose **"Dodaj do panelu"**, causing the application to be permanently pinned in the **left FX OS dock**, not the existing top bar. This should remain fully user-editable: new pin joins the pinned group (after the initial ten / any user-rearranged pins, before transient unpinned running apps), can be freely reordered by dragging, unpinned via menu, survives relogin, and does not duplicate a running instance of that app. This is a long-term **functional acceptance criterion**, not merely a GUI label preference.

**Important Plasma 6 distinction:** the stock context action `Add to Panel` can create a distinct launcher widget or target another panel; it is NOT equivalent to pinning into an Icons-only Task Manager and may cause a duplicate running-app icon. Native stock actions usually include `Pin to Task Manager` / `Przypnij do menedżera zadań` and drag-drop to task manager. KDE evidence: https://discuss.kde.org/t/cannot-rearrange-all-taskmanager-icons/20135 and https://discuss.kde.org/t/application-menu-doesnt-show-add-to-panel-widget-option/46468 .

**Implementation plan/contract:** keep a single `org.kde.plasma.icontasks` widget on left panel ID 81. Remove or disable only the old top-panel task manager *after reviewing panel/widget inventory and snapshot*, leaving top FX launcher, workspace pager, systray, clock. Test native right-click **Pin to Task Manager** from the application menu once there is a single task-manager target. For the future dedicated FX OS menu, explicitly expose a user-facing **"Dodaj do panelu"** action that programmatically pins to the left `icontasks` widget, not Plasma containment `addWidget`/separate shortcut widgets. Implement and verify only once actual widget API and target selection are confirmed; this behavior **does not exist yet and must not be promised as already working**.

Original top bar and the complete detailed FenixSystem V3 are outside modifications at this stage. Signal AppImage integration is preserved; future pin operations need a test for its application-ID pairing. No local system edits occurred with this documentation-only update.


## 2026-10-29 — OWNER correction: separate Add to Panel vs Add to Dock actions

**OWNER explicit correction superseding immediately previous add-to-panel routing requirement:** The future FX OS application-menu context menu **must expose TWO DISTINCT commands** (both user-visible in Polish):

- **`Dodaj do panelu`** → add/create a persistent application launcher on the **TOP horizontal Plasma panel**. This must NOT silently redirect to the left dock.
- **`Dodaj do docka`** → pin the application to the **LEFT vertical dock**, implemented with the existing single `org.kde.plasma.icontasks` widget, so an already-pinned and running app shows only once within this dock.

Both actions should retain user configurability (remove, rearrange, persistence across restarts) and target the explicitly named destination. Top panel and left dock are separate targets; a launcher intentionally added to both can reasonably appear in both places (that is not a defect). The starting 10 dock pins and freedom to rearrange/pin more remain valid.

**Status:** functional design contract explicitly decided by OWNER. The two-command context menu is **not yet implemented or tested**. Standard Plasma `Dodaj do panelu` might choose panel depending on its normal menu and current topology; custom FX OS menu must implement unambiguous routing instead of claiming current stock menu already does it. The first goal is preserving working existing top panel, left dock ID 81, current FenixSystem V3 and Signal notifications while continuing staged desktop changes.

Earlier paragraph stating `Dodaj do panelu` should always pin to left dock is historical and **superseded by this note**. Do not rewrite historical screenshots or undo previous records.


## 2026-10-29 — start dock pin application: adaptive length and real desktop IDs

OWNER says `to jedziemy` after approving the two independent future menu actions (Add to Top Panel; Add to Left Dock). Begin the native KDE dock implementation, **not the custom FX menu widget yet**.

Execution sequence adapted to the actual setup: panel ID 81 is a 58px left panel, currently 450px long with one Icons-only Task Manager; 10 fixed-height pinned icons plus extra active tasks are too many for 450px. First user-run controlled geometry change: make `lengthMode='fit'`, `minimumLength=240`, `maximumLength=850`, alignment center, leave width 58; before writing snapshot `plasma-org.kde.plasma.desktop-appletsrc` and `plasmashellrc` to timestamped `~/FX-Linux-Odzysk` directory. Guard unique left panel ID 81 and unique Icons-only Task Manager widget; inspect existing launchers and manually-sorted state. List matching actual `.desktop` basenames from XDG application directories for Firefox, Thunderbird, LibreWolf, Signal, Dolphin, Konsole, RustDesk, System Settings, Discover, and KWrite. Do not guess desktop IDs because AppImages/Flatpaks may have distinctive names.

After OWNER runtime output, safely rewrite **only the left icontasks widget** initial pinned launcher list in exact confirmed 10-app order, preserving drag-to-reorder and dynamic unpinned running applications below. This is a one-time initial preference, not a daemon/script continuously enforcing order. Verify GUI drag + unpin/re-pin behavior and Signal icon identity; do not rewrite the top bar. KDE docs for Plasma Desktop Scripting: https://develop.kde.org/docs/plasma/scripting/api/ and config reference: https://develop.kde.org/docs/plasma/scripting/keys/ ; source for KDE TaskManager pinned task integration: https://github.com/KDE/plasma-workspace/blob/master/libtaskmanager/tasksmodel.h .

**No local changes from this note**. Signal notifications working; FenixSystem V3 strictly unchanged; bespoke menu 'Dodaj do panelu' top vs 'Dodaj do docka' left remains an unimplemented requirement.


## 2026-10-29 — auto-fit dock applied; exact launcher IDs inventory (8/10)

OWNER executed the safe one-shot script and supplied the runtime output plus the screenshot:
- **Backup PASS** saved to a timestamped private directory `~/FX-Linux-Odzysk/kde-dock-fit-20261029-155309-*`, preserving `plasma-org.kde.plasma.desktop-appletsrc` and `plasmashellrc`.
- **Plasma script succeeded:** left panel ID **81**, single `org.kde.plasma.icontasks` widget ID **82**. The original icon task manager `[General] launchers` field contains exactly **four pinned launchers**: `preferred://browser,applications:systemsettings.desktop,preferred://filemanager,applications:org.kde.discover.desktop`. `sortingStrategy=1`, `groupingStrategy=1` from runtime reads; do not claim semantic meaning without verifying KDE enum.
- Set `minimumLength=240`, `maximumLength=850`, `lengthMode='fit'`, alignment center. Runtime returned `Nowy tryb długości: fit` and screenshot shows dock automatically lengthened and centered with additional icons; upper panel and full original FenixSystem V3 both remain visible and unchanged. **AUTO-FIT PASS (OWNER)**.
- Read-only application discovery in XDG application dirs identified: `org.mozilla.firefox.desktop`, `net.thunderbird.Thunderbird.desktop`, `signal-appimage.desktop`, `org.kde.dolphin.desktop`, `org.kde.konsole.desktop`, `systemsettings.desktop`, `org.kde.discover.desktop`, `org.kde.kwrite.desktop` (8 of 10 target applications). Other discovered variants: `kdesystemsettings.desktop` and Discover notifier/URL-handler/flatpak desktop files; prefer actual launch targets, not helpers.
- **LibreWolf and RustDesk entries were not found in the directories scanned by that one-level discovery.** Do not infer that apps are uninstalled: inspect other XDG data dirs, Flatpak application lists, `command -v`, AppImage desktop integration etc. Do not fabricate launcher URIs or alter their install methods.
- The screenshot currently has icons in both top bar and left dock. Do not confuse temporary running tasks with persistent pins: only four are confirmed as pinned in the left dock.

**Next safe step:** diagnostic search for actual LibreWolf and RustDesk launchers; then (only after verified valid desktop IDs / presence) apply exact ten initial pinned launchers as the comma-separated `[General] launchers` value in widget ID 82 using KDE's `writeConfig` / `reloadConfig`, with new backup. Keep manual drag-order enabled and allow additional non-pinned running apps below pinned group. Do not change top bar, FenixSystem, Signal notification handling or GRUB. Sources: https://develop.kde.org/docs/plasma/scripting/api/ and KDE discuss launchers stored in `appletsrc`: https://discuss.kde.org/t/how-to-know-what-broken-apps-pinned-to-the-task-bar-used-to-point-to/45035 .

State: **geometry fit PASS**, static 10-pin order **NOT YET APPLIED**, 8 valid .desktop IDs known, 2 unverified. The custom FX OS menu with separate `Dodaj do panelu` and `Dodaj do docka` remains a future implementation requirement.


## Dock FX OS — wszystkie dziesiec identyfikatorow aplikacji potwierdzone

OWNER potwierdzil instalacje Flatpak: LibreWolf jako `io.gitlab.librewolf-community.desktop` oraz RustDesk jako `com.rustdesk.RustDesk.desktop`. Oba skroty istnieja w eksporterze Flatpak. Wraz z osmioma wczesniej sprawdzonymi skrotami daje to komplet 10/10. Nastepny etap to jednorazowa zmiana listy `launchers` w lewym widzecie `org.kde.plasma.icontasks` ID 82, panel ID 81, z osobnym backupem i zachowaniem `sortingStrategy=1` (recznie). Kolejnosc OWNER: Firefox, Thunderbird, LibreWolf, Signal, Dolphin, Konsole, RustDesk, Ustawienia systemowe, Discover, KWrite; pozostale uruchomione aplikacje po nich. Gorny panel i FenixSystem bez zmian. Status: konfiguracja dziesieciu przypiec jeszcze niewykonana przez OWNER.


## 2026-10-29 — failed 10-launcher replacement; rollback needed

OWNER ran the previously instructed Plasma scripting update on left panel ID 81 / Icons-only Task Manager widget ID 82: set `General/launchers` to all 10 desktop URLs, then `w.reloadConfig()`. Script returned success and echoed all 10 entries, but the actual screenshot **shows a broken dock**: a generic blank-document icon, fewer than 10 icons shown, and incorrect order. This is a verified regression following our instruction; **10-pin application FAIL**. DO NOT present a successful config write as a successful UI result or retry the same script.

Crucial preserved safe point: user reported that the problematic run created `~/FX-Linux-Odzysk/kde-dock-pins-20261029-160408-TpaZ`, containing pre-change copies of `plasma-org.kde.plasma.desktop-appletsrc` and `plasmashellrc`. This is the most appropriate restore source, because it was saved immediately before the faulty pin operation (and after the successful left dock `fit` geometry update). Do not use a much older pre-dock backup: that would lose working geometry and panel work.

Next OWNER-run recovery: validate both backup files and `plasma-plasmashell.service` availability; make a separate timestamped snapshot of the current broken layout; stop **only the user Plasma Shell service**; restore both configuration files from the immediate pre-change backup; restart Plasma Shell. Previous similar restore procedure was confirmed working on this host. No GRUB/EFI/system services changes. **Restore success is not verified until OWNER's terminal and screenshot feedback.**

After successful restore, investigate why 10 pinned entries were not rendered correctly. A likely issue could be KDE internal task-manager config formats or launcher resolution/update semantics, but **root cause has not been established**. Safer path: add/pin one application at a time via native icon task manager, confirm visual and deduplication before proceeding. Preserve live top panel, full FenixSystem V3 and Signal notification settings.

**Status: regression documented, safe rollback planned, not yet OWNER-confirmed.**


## 2026-10-29 — pre-10-pin backup restore PASS after bad pinned-list change

OWNER ran rollback and supplied full terminal output plus post-rollback screenshot. Restore source was the correctly selected **immediately preceding layout backup** at `~/FX-Linux-Odzysk/kde-dock-pins-20261029-160408-TpaZ`. Before restoring, OWNER preserved bad layout in private `~/FX-Linux-Odzysk/kde-dock-broken-20261029-160659-MtSq`. Verified both `plasma-org.kde.plasma.desktop-appletsrc` and `plasmashellrc` were copied from pre-change backup while only `plasma-plasmashell.service` was stopped, started, and checked active. Terminal printed **PRZYWRACANIE ZAKOŃCZONE**. Screenshot confirms normal-looking left dock with original application icons, the top panel intact, full detailed FenixSystem V3 on right, and original FX OS wallpaper.

**ROLLBACK PASS by terminal + screenshot; the last 10-launcher script FAILED UI acceptance and remains prohibited to rerun.** The native left dock and `fit` geometry survived. No on-device GRUB/EFI or login settings changes were performed. Do not imply exact original icon count/order tested after rollback; visuals support recovery of prior usable state.

**Next safe incremental approach:** do not replace the entire `General/launchers` string via KDE Plasma scripting. Use the **existing left dock** Icons-only Task Manager's native menu: launch first missing app (e.g., Thunderbird) using original application launcher, locate its icon **in left dock**, right-click **that left-dock icon** and choose **Przypnij do menedżera zadań**; close it to confirm pin persists and icon renders correctly. Add remaining required apps one at a time, verify immediately, then adjust order using drag & drop (manual sorting). Leave upper panel unmodified until the dock's pinned list works, and keep FenixSystem V3 untouched. If missing icons or duplicates appear, stop and inspect; no bulk state writes or reinstall.

**OWNER-requested target sequence (remains unchanged):** Firefox, Thunderbird, LibreWolf, Signal, Dolphin, Konsole, RustDesk, Ustawienia systemowe, Discover, KWrite; below: unpinned currently running apps, no duplicates. Future FX menu dual actions Add to Panel (top) / Add to Dock (left) still separate, not yet implemented.

Status now: usable left dock restored, desired 10-pin list NOT yet applied or tested. Previous icon/status integrations are not proven broken by the rollback.


## 2026-10-29 — Thunderbird manually placed second after rollback

OWNER supplied an updated full desktop screenshot after the instruction to pin Thunderbird via the native Icons-only Task Manager. **Visual confirmation:** left dock shows Firefox in first position, Thunderbird in second position with its usual blue bird/envelope logo. Remaining icons are not yet ordered as requested; top panel and full detailed FenixSystem V3 remain present. The screenshot alone does not prove Thunderbird stays pinned after exiting (OWNER has not supplied a closed-app persistence check), so classify this as **second-position VISUAL PASS**, persistence pending.

**Next one-app-at-a-time step:** use existing LibreWolf icon, if present as a running task on left dock, right-click and choose native `Przypnij do menedżera zadań`, then move to third position under Thunderbird by drag-and-drop; if LibreWolf not running, launch from menu first. Avoid changing other pinned tasks and do not use the previously failing bulk `General/launchers` overwrite. Check its icon remains after exit and no duplicate task when reopened. Preserve Signal icon, top launcher, FenixSystem and the user's free rearrangement requirement.

Current target list remains Firefox, Thunderbird, LibreWolf, Signal, Dolphin, Konsole, RustDesk, System Settings, Discover, KWrite; all other running apps afterward. Full widget control and menu's `Dodaj do panelu` vs `Dodaj do docka` remain future tasks. User has not yet confirmed persistence of Thunderbird after closing.


## 2026-10-29 — OWNER manually arranged dock icons after rollback

OWNER wrote: `mam. ustawiłem kolejnosc` after instruction to manually pin and reorder the icons via the native KDE Icons-only Task Manager. Treat this as **OWNER-reported manual ordering completed**; the exact set and persistence of all ten pinned icons have not been independently inspected.

The attached screenshot is a 1680x1-pixel strip; it does **not** contain a legible dock, so no visual verification is possible from this image. Avoid asserting precise resulting pin order or after-restart persistence as verified. Prior full screenshots confirmed left panel ID 81 and Icons-only Task Manager widget ID 82 and the upper panel + full FenixSystem V3 intact.

Binding target remains, as an editable initial order: Firefox, Thunderbird, LibreWolf, Signal, Dolphin, Konsole, RustDesk, System Settings, Discover, KWrite; unpinned running applications follow without duplicates. Do not again overwrite `General/launchers` in bulk because this was proven to break icon rendering. Best next action is an optional **read-only** `widget.readConfig('launchers', '')` for left widget 82, plus a correctly-sized screenshot (or OWNER confirmation that all 10 appear) and later a persistence test. Keep the layout as OWNER arranged; do not force an order or touch FenixSystem V3.

Status: manual arrangement **OWNER REPORTED**; visual verification not possible from current narrow attachment. No device changes made by the GitHub record.


## 2026-10-29 — full-screen manual dock status: first four ordered, remainder pending

OWNER supplied a readable full desktop screenshot after stating that icon order was adjusted manually. Actual observed dock (top to bottom): 1 Firefox, 2 Thunderbird, 3 LibreWolf, 4 Signal, 5 Konsole/terminal, 6 unidentified white-blue icon, 7 Discover, 8 KDE System Settings, 9 Dolphin. There is **no clearly visible KWrite launcher**; exact identity of the white-blue icon cannot be asserted from screenshot alone, and neither running state nor permanence of pins can be proven from a still image. Do not declare all 10 ordered or a persistent pin test PASS yet.

The **first four icons are visually aligned with OWNER's target**, however Dolphin should move to position 5, Konsole to 6, RustDesk 7, System Settings 8, Discover 9, KWrite 10. Before changing other icons, perform **one native drag only**: move Dolphin from the bottom of the visible dock directly below Signal so it becomes the fifth item, preserving first four. Then ask for screenshot/confirmation of result. Do not repeat bulk rewriting the task manager launchers list or restart Plasma. Keep manually editable sorting and other dynamic running apps.

Full top panel remains populated, systray and clock visible. Original full-sized detailed FenixSystem V3 remains on right. The saved screenshot is in the conversation, **not uploaded to the public repo**.

Current status: manual dock arrangement **PARTIAL VISUAL PASS (positions 1-4)**; remaining order and pin permanence **PENDING**. No local device changes from this GitHub documentation write.


## 2026-10-29 — OWNER wants vivid full-color icons in left dock

**OWNER visual requirement:** user reports that icons inside left vertical dock seem slightly washed out / greyed compared with the original full-color app icons and wants **fully saturated/legible application icons**. This is an additional visual acceptance requirement, not merely a description of running state.

From full-resolution screenshot: dock icons still contain their correct recognizable colors (Firefox orange, Thunderbird blue, LibreWolf cyan, Signal violet, Discover blue), but dark gray square task backgrounds and inactive/active state differences may affect perceived contrast. **The exact cause is not confirmed**. Prior 10-launcher bulk replacement and rollback were unrelated to icon appearance and must not be repeated. Upstream Plasma task manager highlights launched/active tasks using theme-dependent visual states; docs: https://userbase.kde.org/Plasma/Tasks and https://forum.manjaro.org/t/task-manager-pinned-app-behavior-plasma-6/161944 . Current KDE source Task.qml binds icon directly to task model `decoration`, with state `IsLauncher` and `IsMinimized`; avoid claiming a configurable universal 'icon saturation' checkbox without evidence.

**Next non-destructive diagnostic:** compare one left-dock app icon while closed versus running and when hovered; distinguish actual desaturation of graphic from dark item background/highlight state. Only then tune left dock **appearance**, not the icon assets, global icon theme, Signal AppImage or entire Plasma shell; prioritize adjustments that can be tested and undone. Keep top panel and FenixSystem V3 unchanged. No on-device changes made from this documentation update.

Status: **visual polish issue OPEN**; no claim that icons are repaired or recolored.


## 2026-10-29 — LibreWolf screenshot: no obvious brightness change; task tile appearance remains

OWNER provided a full 1680x1050 screenshot as follow-up to the requested LibreWolf launch test for washed-out left-dock icons. The left dock shows recognizably colored Firefox, Thunderbird, LibreWolf, Signal, Konsole, Dolphin, RustDesk/other apps; each occupies a dark gray task tile. **No clear change in LibreWolf icon brightness is discernible from this single screenshot** compared with earlier screen captures. It cannot prove icon saturation, hover effect, running-state effect, or app activity status alone. Upper panel and original full FenixSystem V3 continue visually intact.

Source check: KDE upstream `plasma-desktop/applets/taskmanager/qml/Task.qml` renders tasks via `Kirigami.Icon { enabled: true; source: task.model.decoration; active: task.highlighted }` and background via `KSvg.FrameSvgItem` with task-state and hover prefixes. Thus launchers and running app task tiles can look different by theme/hover even without replacing icon image data. Source: https://github.com/KDE/plasma-desktop/blob/master/applets/taskmanager/qml/Task.qml . Upstream `master` is a reference, not independently verified to be exact version 6.7.5 on OWNER.

Safe next observation: compare the LEFT dock's same LibreWolf icon at rest and while pointer is hovering over it, with the mouse cursor away from other elements; report whether icon itself brightens or only dark gray task tile/highlight changes. If only the tile changes, pursue a reversible **dock-only style / Plasma look** experiment rather than editing individual application icons, app shortcuts, FenixSystem scripts, top panel pinned task list, KDE system QML, or Signal. Do not claim a 'saturation slider' exists in stock Icons-only Task Manager. Avoid another bulk launcher-list edit after verified regression.

Status: visual polish issue unresolved, all ongoing changes on installed desktop remain OWNER-driven. No new on-device modification from this note.


## 2026-10-29 — OWNER confirms hover slightly brightens but icons remain washed out

OWNER explicitly reports: 'lekko rozjasnia po najechaniu ale wciaz takie przygaszenie jest. brakuje pełnokrwistego koloru'. Therefore hovering changes the icon appearance only a little, but the **actual visual defect is persistent perceived lack of vibrancy when idle**; reproducing the hovered state alone may not completely meet OWNER expectations.

Verified technical evidence from upstream KDE: Plasma's Icons-only Task Manager QML uses `Kirigami.Icon` with `active: task.highlighted`, `enabled: true` and `source: task.model.decoration` in `plasma-desktop/applets/taskmanager/qml/Task.qml` (checked against current main, NOT proven byte-for-byte identical to Fedora's Plasma 6.7.5). Kirigami API confirms `active` uses QIcon Active rendering/effects for hover: https://api.kde.org/qml-org-kde-kirigami-primitives-icon.html . Plasma task manager `ConfigAppearance.qml` does NOT expose a saturation slider: https://github.com/KDE/plasma-desktop/blob/master/applets/taskmanager/qml/ConfigAppearance.qml .

**Scope-safe plan:** do not rewrite pinned launchers or remove the current working left panel (ID 81 / `icontasks` 82). Prefer a future user-local, separately testable FX-themed rendering layer / native compatible variant that boosts default-state icon vibrancy, uses dark task frames and soft blue active accents while retaining task management, drag-to-reorder, notifications and deduplication. Do not change global icon theme, system KDE QML files or the complete detailed FenixSystem V3 merely to improve dock colors. Avoid claiming that customizing tasks.svg alone increases raw bitmap icon saturation; task theme background can improve perceived contrast but rendering effects may require a widget change.

Immediate read-only next step: identify active icon theme (`kreadconfig6 --file kdeglobals --group Icons --key Theme`), Plasma theme (`kreadconfig6 --file plasmarc --group Theme --key name`), and installed Plasma/Frameworks versions (`plasmashell --version`, `rpm -q plasma-desktop plasma-workspace kf6-kirigami`), without any system changes. The OWNER has not yet approved an applet replacement, and no fix for icon saturation has been applied or tested.

**Status:** hover response CONFIRMED, full-color requirement UNMET, further implementation gated by safe compatibility audit and OWNER's visual acceptance.


## 2026-10-29 — KDE theme/version confirmed; color-rich dock requires targeted visual design

OWNER read-only output on running Fedora 44 KDE Wayland:

- Icon theme in `kdeglobals`: **`breeze-dark`**.
- Plasma desktop style: **`default`**.
- `plasmashell --version`: **6.7.5**.
- RPM: `plasma-desktop-6.7.5-1.fc44.x86_64`, `plasma-workspace-6.7.5-1.fc44.x86_64`, `kf6-kirigami-6.31.0-1.fc44.x86_64`.

Owner reports that hovered icon brightens slightly but retains a washed-out look and wants vivid fully colorful dock icons. KDE upstream `plasma-desktop/applets/taskmanager/qml/Task.qml` binds `Kirigami.Icon.active` to `task.highlighted` and sources icon from `task.model.decoration`; KDE Kirigami Icon documentation confirms Active mode adds an icon effect. KDE KIconThemes current implementation applies `KIconEffect::toActive` (gamma) for Active state and keeps Default state unmodified, so avoid asserting that default KDE task icon is deliberately grayscale or that changing `kdeglobals [DesktopIcons] DefaultEffect` will reliably fix it in KF6. Source: https://api.kde.org/qml-org-kde-kirigami-primitives-icon.html and https://github.com/KDE/kiconthemes/blob/master/src/kiconloader.cpp .

**Diagnosis:** stock Breeze Dark/default Plasma style, no evidence of missing package or misconfigured icon theme. Stronger colors may require a targeted user-local design of task-item backgrounds/visual emphasis and potentially custom icon rendering, rather than a nonexistent stock 'saturation' control. Changing global icon themes, application files, or system QML is not authorized as a dock-only adjustment. Changing `widgets/tasks.svg` can alter task buttons' visual contrast but does NOT inherently increase icon bitmap color saturation. A custom task-manager plasmoid would require independent compatibility tests before replacing the working current one.

**Safe next phase:** explore the actual source icon appearance and user-local Plasma theme task frame options without changing existing left widget `82` or pinned launchers. Since the previous bulk launcher mutation failed, do not repeat any replacement/reset of icon task manager. Preserve upper panel, Signal notifications and the existing detailed FenixSystem V3. Current state is diagnostic only; no full-color fix applied.


## 2026-10-29 — located the stock Plasma task button background SVG

OWNER ran a read-only filesystem search and found exactly `/usr/share/plasma/desktoptheme/default/widgets/tasks.svgz`. No user-local `tasks.svg`/`tasks.svgz` was found in the searched user Plasma theme tree. This identifies the **stock task-item background artwork**, but not an override or proven cause of icon color attenuation.

Official KDE docs state `widgets/tasks.svg[z]` supplies Task Manager background frames by states (normal, focus, hover etc.), **not the underlying application icon pixels**, and a Plasma Style selected for the desktop can affect **all** Task Manager instances; https://develop.kde.org/docs/plasma/theme/theme-elements/ and https://develop.kde.org/docs/plasma/theme/theme-details/ . Both left and top panels currently have task items, so do not replace `/usr/share/plasma/desktoptheme/default/widgets/tasks.svgz` or place an unmanaged global theme override just to fix the left dock, as that would cause wider visual changes and would not inherently increase saturation.

Next scope-safe step: an isolated and reversible **per-left-panel opacity/background contrast** test via the built-in Plasma panel configuration (opaque vs adaptive/translucent), only after preserving current appearance and leaving task-manager widget and pins untouched. Explicitly state that this may change perceived vividness/contrast but will **not** directly increase icon saturation; if insufficient, source-backed design work for a user-local dock-specific task rendering variant will be necessary. Do not claim an icon-saturation control exists in stock Plasma 6.7.5.

STATUS: file discovery PASS; full-color icon issue still OPEN; no modifications to user's system made by this checkpoint update. FenixSystem V3 and Signal remain untouched.


## 2026-10-29 — OWNER expands glossy FX OS style to both top panel and left dock

**New explicit OWNER design direction and scope:** both the *upper horizontal panel* and the *left vertical dock* may be restyled together. OWNER strongly prefers the lively, saturated, layered, dimensional design languages remembered from **Windows XP and Windows 7**, and explicitly dislikes the flat, under-emphasized aesthetic associated with Windows 10/11. This supersedes the previous plan to consider adjusting only the left dock's visual background.

**FX OS Gloss direction:** preserve the original dark blue FX wallpaper, existing circular FX launcher placement at the far upper-left (when implemented), icons-only draggable/pinnable app dock, notifications and full detailed FenixSystem V3. Aim for strong colorful app icons, dark navy/graphite surfaces, tasteful blue/cyan highlights, reflective gradients, light bevels and bright borders, distinct pressed/hover/active states, high contrast and a high-quality glass/Aero-like visual depth. XP/7 are **design references**, not a requirement to copy Windows assets or reproduce OS trademarks. Avoid both minimalist gray-on-gray and excessive glowing UI.

**Verified implementation facts:** KDE Plasma style controls visual backgrounds of panels and task items, and is generally shared across both panels, which is now acceptable. Official KDE docs https://develop.kde.org/docs/plasma/theme/theme-details/ and https://develop.kde.org/docs/plasma/theme/theme-elements/ identify the user-local style path `~/.local/share/plasma/desktoptheme/<theme>` and `widgets/tasks.svg[z]`, `widgets/panel-background.svg[z]`. **An SVG Plasma style alone cannot directly increase actual icon bitmap saturation**; source icon render is handled by `Kirigami.Icon` inside Task Manager. Standard stock applet has no color saturation slider. Avoid claiming style preview alone fixes this. A custom dock-only applet would be a separate later project if truly necessary.

**Optional compatibility avenue:** the official Fedora 44 repository contains `plasma-oxygen` version 6.7.5-1.fc44, a dimensional Qt/Plasma style and window-decoration package (https://packages.fedoraproject.org/pkgs/plasma-oxygen/plasma-oxygen/). It might be useful as a reversible reference, **not a committed user system installation or a guaranteed exact visual match**. Prefer first checking `rpm -q plasma-oxygen` and available installed `~/.local/share/plasma/desktoptheme` plus system theme directories, without changing a theme or installing packages.

**Safe next staged plan:** preserve panel layout and pin list; collect/confirm baseline style and theme inventory, create private snapshots of Plasma style and relevant user settings, then design a **user-local FX OS Gloss Plasma style** with appropriate panel backgrounds and task frames to be tried on both panels while retaining the ability to return to `default` style. Do NOT select/install any *Global Theme* that may reset the panels or menus; do not modify `tasks.svgz` in `/usr/share/`, Plasma task-manager widget, Signal config, or FenixSystem V3. The custom menu will remain a separate development stage.

**Status:** concept/scope approved, technical implementation of a glossy fully-colored theme NOT YET made or tested on the machine.


## 2026-10-29 — OWNER adds Mandriva Powerpack 2008, Oxygen, Plastik and Keramik inspiration

**Explicit OWNER design addition:** Mandriva Powerpack 2008 joins the XP Luna / Windows 7 Aero visual inspirations for the *FX OS Gloss* design direction. OWNER specifically recalls **Oxygen, Plastik, Keramik**. This adds a historically rich KDE/Mandriva reference for vivid icons, glossy/skeuomorphic contours, depth, gradients and colored focus/hover/active states rather than flat Windows 10/11-like surfaces. Full detailed FenixSystem V3 remains untouched, as do current icon task manager pins and Signal.

**Historical verification, important to avoid conflation:** Mandriva Powerpack **2008.0** was shipped with **KDE 3.5.7** and used **Ia Ora** by default; a contemporary Powerpack review describes switching to **Plastik** (https://www.osnews.com/story/18757/review-mandriva-linux-powerpack-20080/). **Keramik** and **Plastik** belong to the KDE 3 style heritage, while **Oxygen** was introduced as the primary KDE **4** theme around **2008** (https://kde.org/anniversaries/30/; https://github.com/KDE/oxygen); do NOT claim all three were Mandriva Powerpack 2008.0 default styles. Treat them as stylistic sources, not as guaranteed binary drop-in themes for Plasma 6.

**Verified OWNER read-only Fedora 44 inventory:** `rpm -q plasma-oxygen plasma-oxygen-qt6` reports both not installed; `find ... -name metadata.json` shows only `/usr/share/plasma/desktoptheme/breeze-dark`, `/usr/share/plasma/desktoptheme/breeze-light`, `/usr/share/plasma/desktoptheme/default`; user-local theme inventory produced no matches. Actual earlier active icon theme: `breeze-dark`; Plasma theme `default`; Plasma 6.7.5 / Kirigami 6.31.0.

**Current availability**: Official Fedora 44 repository offers **`plasma-oxygen` and its `plasma-oxygen-qt6` subpackage** at KDE 6.7.5 (https://packages.fedoraproject.org/pkgs/plasma-oxygen/plasma-oxygen/; https://packages.fedoraproject.org/pkgs/plasma-oxygen/plasma-oxygen-qt6/). KDE Plasma 6.7 release notes say classic Oxygen, Air themes have been renewed for Plasma 6.7 including adaptive opacity and panel positions (https://kde.org/announcements/plasma/6/6.7.0/). This is a **potential reversible comparison**, NOT an installation already authorized or performed. Historic Plastik/Keramik are design references; no claim they are native package options on Fedora Plasma 6.7.5.

**Visual direction:** FX OS Glass/Gloss combines rich electric-blue edges and dark navy with tactile glossy task buttons, fine highlight reflection/bevel, soft shadows/gradients, legible hover/pressed/active state, vivid colorful application iconography. Apply to **both top panel and left dock** when implementing a *Plasma Style*; do not apply a global theme that resets panel layouts, and do not overwrite `/usr/share/plasma/desktoptheme/default/widgets/tasks.svgz`. A Plasma theme may modify panel/task-frame appearance but cannot by itself guarantee changing source app icon saturation; keep that distinction in acceptance tests.

**Next safe sequence:** (1) preserve backup of working panel layout, current desktop style, and icons; (2) consider a scoped, explicitly approved official Oxygen 6.7.5 trial *style-only* with immediate rollback, or an isolated user-local FX OS Gloss Plasma Style; (3) assess brightness/contrast on both panels while keeping pinned list and FenixSystem intact; (4) avoid system QML changes or untested GTK theme hacks. No local system modification performed during this documentation update.


## 2026-10-29 — OWNER approves official Oxygen install and reversible Plasma Style-only trial

**Explicit OWNER authorization:** `tak, testujemy ale ten oxygen tez warto miec na podoredziu`. Install official Oxygen in Fedora 44 and **keep it installed as an optional available style**, even if the final FX OS Gloss design selects a different theme. Test its appearance on **both** left dock and top bar, maintaining editable icon task manager and the existing full FenixSystem V3.

Verified in official Fedora Packages: `plasma-oxygen-6.7.5-1.fc44` is available and contains Plasma Styles `/usr/share/plasma/desktoptheme/oxygen` and `/usr/share/plasma/desktoptheme/air`, plus Oxygen Qt6 application style and window decorations. `plasma-oxygen` pulls in `plasma-oxygen-qt6` and other official dependencies. Sources: https://packages.fedoraproject.org/pkgs/plasma-oxygen/plasma-oxygen/fedora-44-updates.html ; https://packages.fedoraproject.org/pkgs/plasma-oxygen/plasma-oxygen-qt6/fedora-44-updates.html . KDE Plasma 6.7 explicitly reintroduced an updated Oxygen and Air style: https://kde.org/announcements/plasma/6/6.7.0/ .

**Proposed user-run safe workflow, not yet executed or verified on workstation:**
1. Save private timestamped backups under `~/FX-Linux-Odzysk/` of `plasmarc`, `kdeglobals`, `plasma-org.kde.plasma.desktop-appletsrc`, `plasmashellrc` before applying anything; baseline previously read: Plasma Style `default`, icon theme `breeze-dark`.
2. Run `sudo dnf install plasma-oxygen` through the official Fedora repositories, reviewing the DNF transaction. Keep installed; do not remove after test unless OWNER explicitly decides to.
3. Verify `rpm -q plasma-oxygen plasma-oxygen-qt6` and list styles through `plasma-apply-desktoptheme --list-themes`.
4. Apply **only Plasma Style `oxygen`** via `plasma-apply-desktoptheme oxygen` or KDE System Settings → Colors & Themes → Plasma Style → Oxygen → Apply. **Do not select Global Theme Oxygen**, which may offer changing the desktop/panel layout; keep top/left panel widgets, wallpaper, existing Breeze Dark icons and application style unchanged initially.
5. Visual comparison of vividness, button depth, glossy highlights on both top panel/dock and full existing FenixSystem visibility. If unsatisfactory, restore only Plasma Style `default` via `plasma-apply-desktoptheme default` or GUI, leaving Oxygen installed. Never restore the old appletsrc over working pins merely to roll back a style-only trial.

**Scope and status:** authorization for install and style-only trial granted, no on-machine package install or theme switch confirmed yet, no additional UI change claimed. The main FX OS Gloss contract remains inspired by XP/Win7 Aero and Mandriva 2008 Ia Ora / KDE Plastik, Keramik and Oxygen, not a requirement to use Oxygen permanently.


## 2026-10-29 — OWNER visually approves Oxygen on both panels

OWNER supplied screenshot following the approved Oxygen-only Plasma Style test and explicitly wrote **`odrazu lepiej`** ('immediately better'). Treat this as an **OWNER subjective visual PASS** for Oxygen on both the top panel and the left vertical dock. Observations from the screenshot: dock task buttons now sit on dark almost-black background without the prominent stock gray square tiles, edges of both panels have fine outlined/shiny border; colored app icons appear clearer and contrast better against FX OS dark wallpaper. Aesthetic direction consistent with gloss/dimension requirement.

**Continuity verified visually:** left task-manager dock still exists with its colorful application icons; horizontal top panel still exists with icons, systray and clock; unchanged original detailed **FenixSystem V3** visible on right with its CPU, RAM, SSD, thermal, battery, network and uptime sections. Screenshot does not establish launcher pin persistence or that every icon reached the desired target order. Do not modify those in this checkpoint.

**Status:** Oxygen **applied visually on user's system** (inferred from screenshot immediately after switch, as corroborated by user), user **likes result**. Exact RPM installation state beyond prior requested installation not independently returned by terminal, but Oxygen appearing and styling panels strongly supports that the Plasma Oxygen theme is installed. OWNER earlier approved keeping it installed as a choice; **keep Oxygen active for now**, do not switch back to `default` or remove package. The visual brief remains FX OS Gloss inspired by Aero XP/7, Mandriva 2008 Ia Ora, Plastik/Keramik/Oxygen. Next scope: safe, user-local refinements, no edits to `/usr/share/...`, preserve ability to switch back and preserve the original FX wallpaper and full FenixSystem. Important note: changing Plasma Style improves contrast/background, not proven to alter source bitmap saturation.

No user-device action performed by this documentation update. Future actions require owner-driven implementation steps.


## 2026-10-29 — OWNER moves to upper panel cleanup after Oxygen acceptance

OWNER explicitly requests **`teraz porzadek z górnym panelem`** after visually accepting the Oxygen-only Plasma Style test. The new work phase is TOP HORIZONTAL PANEL cleanup. Keep Oxygen active, original wallpaper, detailed FenixSystem V3, and left vertical dock with its manually arranged icons and working Signal integration. No boot/login/power/Night Color edits.

**Desired upper-bar UI (OWNER previously agreed):** round FX application-menu logo at extreme upper-left (custom FX menu later), KDE virtual desktop pager 1 2 3 4 adjacent, optional **intentionally pinned** upper-panel shortcuts, stretch/spacer, system tray and clock at upper-right, existing Show Desktop at right if useful. Remove automatic duplicated task entries from the upper bar so left dock is primary application task manager. Future custom menu must keep distinct actions `Dodaj do panelu` (upper panel persistent shortcut) and `Dodaj do docka` (left `icontasks` pin). Neither future FX icon/FX menu nor two routing commands are implemented yet; do not claim otherwise.

**Safety gate:** previous destructive bulk left-dock launcher change caused broken icons; restore succeeded. Therefore before removing anything on upper panel, save private timestamped backups under `~/FX-Linux-Odzysk/` of `plasma-org.kde.plasma.desktop-appletsrc`, `plasmashellrc`, `plasmarc`; use a **read-only** Plasma scripting audit to list each panel and widget type/id via `panels()`, `p.widgetIds`, `p.widgetById(id).type`. This must establish whether the many icons on upper left are an `org.kde.plasma.icontasks`/`org.kde.plasma.taskmanager` instance or many separate launcher widgets. Left panel 81 and widget 82 must remain untouched.

**Next action after OWNER sends live readout:** identify TOP panel id and precise widget to edit, remove **only** the top task-manager widget (if indeed one), never the containing panel, launcher, system tray, spacer or clock. For individual launcher widgets use GUI one at a time. Add native KDE `Pager` widget then configure four virtual desktops and display desktop number rather than thumbnails; use KDE System Settings for number of virtual desktops if needed. Test everything visibly before attempting bespoke menu logo. Use reversible, incremental actions and preserve all other applications.

Official KDE refs: https://develop.kde.org/docs/plasma/scripting/api/ ; https://docs.kde.org/stable_kf6/en/plasma-desktop/plasma-desktop/panel.html ; https://docs.kde.org/stable_kf6/en/kwin/kcontrol/desktop/index.html .

**Status:** new work phase agreed, no on-machine changes made as of this documentation commit. GitHub branch HEAD inspected via API: 3ff6c7b7c9cee16a8beed4f28705ff4617d2a55c. User-local working tree unavailable to remote assistant.


## 2026-10-29 — read-only inventory confirms exact upper panel task manager widget 58

**OWNER runtime read-only script and verified user-local backup.** Backup directory: `~/FX-Linux-Odzysk/kde-top-before-20261029-173646-ILI5` (only store path relative to home; user reported local copy of `plasma-org.kde.plasma.desktop-appletsrc`, `plasmashellrc`, `plasmarc`). The `gdbus` Plasma script yielded:

```text
PANEL 55 | location=top
  WIDGET 56 | org.kde.plasma.kickoff
  WIDGET 57 | org.kde.plasma.pager
  WIDGET 58 | org.kde.plasma.icontasks
  WIDGET 59 | org.kde.plasma.marginsseparator
  WIDGET 60 | org.kde.plasma.systemtray
  WIDGET 75 | org.kde.plasma.digitalclock
  WIDGET 76 | org.kde.plasma.showdesktop
PANEL 81 | location=left
  WIDGET 82 | org.kde.plasma.icontasks
```

**Updated conclusion / important correction:** The native **Pager ALREADY EXISTS** as widget 57 on upper panel 55; do not add another one. Extra upper left app icons are rendered by top `icontasks` widget **58**. The separate left dock `icontasks` widget **82** lives in panel **81** and must be left intact. The kickoff widget 56 is stock app menu (not the future bespoke FX OS menu).

**NEXT authorized, narrow operation:** remove ONLY `org.kde.plasma.icontasks` widget ID `58` from verified TOP panel ID `55`, never delete panel 55 or panel 81 or widget 82; preserve kickoff 56, pager 57, separator 59, system tray 60, clock 75, Show Desktop 76. The official Plasma scripting API documents `Widget.remove()` (https://develop.kde.org/docs/plasma/scripting/api/). Precondition: exact backup of appletsrc still exists and read-only guard confirms panel/widget identity/type and the left dock target, then one user-run guarded call `w.remove()`. Stop if topology/IDs mismatch. Afterward verify a new read-only enumeration (top has 56/57/59/60/75/76; left remains 81/82) and screenshot, **do not assume removal succeeded until runtime output**.

Later stage: configure already-present Pager to display desktops 1-4; inspect virtual-desktop count before setting to 4. Keep FX OS Gloss Oxygen style and full detailed FenixSystem V3. Custom round FX menu, direct top shortcut action vs dock pin action remain future functionality.

**Status:** inventory PASS, exact target identified, **removal not yet performed or verified**.


## 2026-10-29 — upper task icons removed; tray jumped left because no flexible spacer

OWNER shared an updated full 1536x960 desktop screenshot after running the proposed removal of TOP task manager `org.kde.plasma.icontasks` widget 58 from top panel 55. **Visual confirmation**: the duplicated app task icons disappeared from the top bar. **Layout regression observed**: the system tray (widget 60), clock (75) and Show Desktop button (76), formerly at the far right, have slid immediately beside the top-left Kickoff launcher (56). The bar remains full width, with a wide blank region to the right. Left vertical dock ID 81 / widget 82, original wallpaper, Oxygen look and full detailed FenixSystem V3 all remain visibly intact. The runtime output of the deletion call has not yet been provided; do not claim a read-only post-delete API audit.

**Root cause:** Plasma panel items left-align by default; the previous top task manager took up expanding width. `org.kde.plasma.marginsseparator` widget 59 is not a full expanding spacer. KDE documentation confirms an **elastic/flexible Panel Spacer** is used to separate left/right groups (https://userbase.kde.org/Plasma/Panels and Plasma 6 clarification https://discuss.kde.org/t/solved-plasma-panel-spacer-and-flexible-space-widgets-gone/45581).

**Immediate safe correction:** GUI-only, **do not restore deleted top task manager**. Right-click the horizontal top panel -> Enter Edit Mode / Show Panel Configuration; use the **panel configuration tool's `Add Spacer` / `Dodaj odstęp`** control (in Plasma 6 not necessarily found in the regular Add Widgets search). Drag its blue editable stripe **between the existing Pager 57 and system tray 60** (i.e. after Kickoff / pager group and before margins separator 59/system tray); ensure `Set flexible size` is ON. This should expand to fill the middle, shifting the system tray, clock and Show Desktop to the far right. Leave the right group widget order intact. Exit Edit Mode and verify visually.

**Do not touch**: top launcher 56, Pager 57, widget 59, tray 60, clock 75, Show Desktop 76, whole panel 55, left panel 81/widget 82, Signal icon/notifications, FenixSystem, oxygen style; do not repeat deletion or add a new task manager. Later inspect why Pager 57 currently not visibly showing digits; 4 desktops and `1 2 3 4` remain separate next stage. If edit UI cannot locate Add Spacer, stop and request a screenshot of panel Edit Mode rather than guess or write undocumented scripting mutations. Backups remain in `~/FX-Linux-Odzysk/kde-top-before-20261029-173646-ILI5`.

Status: top task duplication **VISUAL PASS**, right-side alignment **REGRESSION OPEN**, simple flexible spacer correction planned but not applied yet.


## 2026-10-29 — OWNER requests immediate rollback of top task manager removal

**OWNER explicitly ordered**: `poczekaj. wrócmy do stanu sprzed usuniecia na górny panelu` ('Wait. Return to state before deletion on the top panel'). This **supersedes** the flexible spacer correction plan for now. Stop additional panel edits, do not add spacer yet. OWNER wants the exact previous top task-manager state back, including its icons and the right aligned system tray/clock.

Known safe rollback snapshot from **immediately before deletion**: `~/FX-Linux-Odzysk/kde-top-before-20261029-173646-ILI5` which contains `plasma-org.kde.plasma.desktop-appletsrc`, `plasmashellrc`, `plasmarc`. Restore only appletsrc + plasmashellrc from it; **do not overwrite plasmarc**, as Oxygen Plasma Style should remain active. Snapshot the current post-deletion config into a new timestamped `~/FX-Linux-Odzysk/kde-top-before-rollback-*` directory first.

Suggested OWNER-run guarded shell procedure: check both source files exist/nonempty; save current configs to new directory; `systemctl --user stop plasma-plasmashell.service`; set EXIT trap that restarts shell if failure; copy both backed-up config files into `~/.config/`; `systemctl --user start plasma-plasmashell.service`; clear trap; confirm shell active. The prior dock rollback used the same stop/copy/start pattern and was successful. This should restore upper panel widget 58 and right alignment, as well as restore left dock to the pre-deletion snapshot (which was taken after manual ordering). **No rollback performed by assistant**; wait for OWNER terminal result and full screenshot, validate visually and optionally read-only enumerate panels/wigets afterwards.

Important: OWNER requests revert, NOT a fresh removal/addition; no upper panel 'spacer' changes until OWNER re-authorizes. Preserve original wallpaper, Oxygen, Signal and FenixSystem V3.


## 2026-10-29 — OWNER revises upper panel concept: fixed system apps + dynamic running tasks

OWNER reports successful prior restoration ('super') after reverting upper task manager deletion and **explicitly changes the upper panel functional contract**: starting from left, **application menu → System Settings → Discover → Dolphin → icons for other running applications**. The **left vertical dock remains an independently curated OWNER-selected pinned app collection**, fully manually customizable (drag/reorder/pin/unpin). The right end of the upper panel must keep the system tray, clock and Show Desktop button. This supersedes the prior concept of deleting the top task manager to remove all application task icons. Retain top `org.kde.plasma.icontasks` widget **58** because it is needed for pinned launchers plus dynamic running tasks and was filling the space that kept the right-side widgets at the right.

Previously confirmed top panel ID **55**: Kickoff menu 56, existing Pager 57, Icons-only Task Manager 58, margins separator 59, system tray 60, clock 75, Show Desktop 76. Left panel ID 81, independent Icons-only Task Manager 82. The successful restoration is OWNER-reported only in text; no post-rollback tool enumeration has yet been provided. Don't alter/remove Pager 57 yet; virtual desktops 1-4 are DEFERRED because new specified top order omits pager; do not silently insert a new pager.

**Exact intended top pinned order:** (1) `systemsettings.desktop`, (2) `org.kde.discover.desktop`, (3) `org.kde.dolphin.desktop` following the top application menu (which is a separate widget, not a task item). All other running applications then appear in the same top `icontasks` dynamically. Unpin old fixed top icons (Firefox, Thunderbird, etc.) **only from the TOP manager** after verifying each is pinned, not from the LEFT dock. Applications running simultaneously may appear in both top and side panels by OWNER choice; this is intentional distinct task views, not an error. The upper three fixed apps remain pinned even when closed. Separate future FX menu context actions retained: `Dodaj do panelu` adds shortcut to TOP and `Dodaj do docka` pins to LEFT; they are not yet implemented.

**Safe next step:** no script to bulk modify `launchers` (one such edit previously broke left dock). With saved snapshot at `~/FX-Linux-Odzysk/kde-top-before-20261029-173646-ILI5` and rollback checkpoint, perform **ONE native GUI unpin test** on a non-core TOP launcher (e.g. Firefox) when it is closed: right-click its icon on the TOP horizontal task manager -> `Odepnij od menedżera zadań` if present; verify TOP Firefox icon disappears when closed, LEFT Firefox remains pinned and functioning, right tray/clock stay right. If icon is currently running, unpin should keep it shown until application exits. If the action menu does not show Unpin, do not guess; inspect GUI/screenshot. Only after validating single-item isolation, unpin additional top non-core icons one by one and rearrange/verify top three fixed pins, leaving left dock untouched. No restarts, no delete of widget 58, no edit to system Plasma QML or FenixSystem V3, keep Oxygen active.

**Status:** new top-vs-left behavioral contract AUTHORITATIVELY OWNER APPROVED; no new on-device changes performed by documentation entry.


## 2026-10-29 — OWNER requires left dock show ONLY explicitly selected applications

OWNER reports unpinning old app pins from TOP panel and requests the next behavior: `teraz trzeba ustawic by w bocznym były tylko wybrane` — the **LEFT dock should show ONLY explicitly chosen/pinned apps** and **must not automatically add any merely running unselected app**. The top `org.kde.plasma.icontasks` widget 58 continues to show dynamic running tasks (plus the intentional top 3 pins). Oxygen stays.

**Confirmed technical blocker, version-matched KDE 6.7.5 source:** Plasma's built-in `org.kde.plasma.icontasks` uses `TasksModel` and supports filters current desktop/activity/screen/minimized but has **NO option to display pinned launchers only**. See https://github.com/KDE/plasma-desktop/blob/v6.7.5/applets/taskmanager/qml/ConfigBehavior.qml and https://github.com/KDE/plasma-desktop/blob/v6.7.5/applets/taskmanager/qml/main.qml . Do not claim unpinning existing apps or enabling any filter will suppress all other running tasks; do not write an unverified `showOnlyLaunchers` config key.

**Suitable official widget:** KDE Plasma 6.7.5 `org.kde.plasma.quicklaunch` (Quicklaunch, Polish `Szybkie uruchamianie`) in `kdeplasma-addons` package; Fedora 44 offers `kdeplasma-addons-6.7.5-1.fc44` (https://packages.fedoraproject.org/pkgs/kdeplasma-addons/kdeplasma-addons/). KDE source https://github.com/KDE/kdeplasma-addons/tree/v6.7.5/applets/quicklaunch documents drag and drop, reordering and removal of chosen launcher URLs; it does NOT dynamically display unrelated running tasks. The official widget is for panel use and works with vertical layouts. **Trade-off:** Quicklaunch is an app launcher, not a task manager; active-window indicators, SmartLauncher/Unity notification count overlays (esp. Signal AppImage) and window manipulation may not be identical to current `icontasks`. Preserve independent Signal notification flow and test this before considering completed.

**Safe migration plan (no destructive changes yet):**
1. Check availability read-only: `rpm -q kdeplasma-addons` and `test -f /usr/share/plasma/plasmoids/org.kde.plasma.quicklaunch/metadata.json && echo QUICKLAUNCH_OK || echo QUICKLAUNCH_MISSING`. (The path should be verified in live output.) If missing, ask OWNER to approve/install `sudo dnf install kdeplasma-addons` rather than assume.
2. Take timestamped private backup of current `~/.config/plasma-org.kde.plasma.desktop-appletsrc` and `plasmashellrc` before changes; ensure exact left panel 81, widget 82.
3. Add one Quicklaunch widget into **existing left panel 81** using Edit Mode > Add Widgets; do NOT remove panel 81 or current `icontasks` 82 yet. Populate a small trial (Firefox, Thunderbird, LibreWolf, Signal etc.) by dragging apps from menu or Quicklaunch context-menu. Verify visually icon identities, drag reorder and absence of auto-added running apps when launch unrelated app.
4. After all chosen apps work and OWNER accepts Signal badge behavior, remove **only original left `icontasks` widget 82** from panel 81 via GUI, leaving new Quicklaunch and top task manager 58 untouched. Otherwise remove trial Quicklaunch and original dock remains as before.

**Status:** design requirement OWNER-stated; technical analysis complete; no changes to user's machine executed; next is read-only plugin availability check. No automatic launchers list rewrites, script-based panel reset, modifications to Signal shortcuts, or global theme changes.


## 2026-10-29 — Quicklaunch 6.7.5 already installed; former path test was a false negative

OWNER ran:
```text
rpm -q kdeplasma-addons
kdeplasma-addons-6.7.5-1.fc44.x86_64
rpm -ql kdeplasma-addons | grep '/org.kde.plasma.quicklaunch/' | head -n 10
(no matching lines)
```

**Correction to previous instructions:** the grep assumed a **directory** `/org.kde.plasma.quicklaunch/`, but Fedora 44 `kdeplasma-addons` ships the Quicklaunch **compiled native plugin** `org.kde.plasma.quicklaunch.so` under the Plasma applet plugin path. No `.../org.kde.plasma.quicklaunch/` directory is required. The empty grep is thus a *false negative*. Verified from Fedora 44 package file listing: https://packages.fedoraproject.org/pkgs/kdeplasma-addons/kdeplasma-addons/fedora-44-updates.html . Follow-up read-only proof on device: `rpm -ql kdeplasma-addons | grep 'org.kde.plasma.quicklaunch.so'`.

**Next user-run steps (not yet completed):** back up `plasma-org.kde.plasma.desktop-appletsrc` and `plasmashellrc` under `~/FX-Linux-Odzysk/dock-quicklaunch-before-*`; then enter editing mode of **existing LEFT panel 81**, Add Widgets, find `Szybkie uruchamianie` / `Quicklaunch` and add alongside existing icons-only Task Manager `82` — **do not remove 82 yet**. Add one or two chosen apps to Quicklaunch, test icon, vertical arrangement, reordering, test an unrelated app launching and remaining absent from Quicklaunch, and check Signal notification badge compatibility. Only after OWNER approves full working curated icon list should 82 be removed from the left panel while preserving the TOP task manager `58`.

Current goal remains left panel **selected apps only**, top panel 3 system pins + dynamic running tasks, preserving Oxygen, top right tray/clock, wallpaper, and detailed FenixSystem V3. No user device modifications have been performed by this checkpoint write.


## 2026-10-29 — Quicklaunch appears as small 3-column box; stage formatting into 1 vertical column

OWNER shared full-screen screenshot of active Oxygen FX OS desktop at 18:07: TOP system launcher and application running-icons arrangement remains intact, with right systray/clock and full detailed FenixSystem V3 visibly unaffected. LEFT panel now shows a **small dark rectangle with Quicklaunch app icons arranged roughly three per row across several rows**, icons much too small. OWNER explicitly asks to **`teraz trzeba go sformatować`** (format/rework this widget's presentation). No read-only post-migration widget enumeration yet, so screenshot suggests but does not prove prior `icontasks` ID 82 was removed; do not identify its current ID without live API check.

**Source-backed fix:** KDE's `kdeplasma-addons` **v6.7.5** `applets/quicklaunch/ConfigGeneral.qml` offers `Maximum columns` in vertical form factor with config `maxSectionCount`, plus `Show launcher names` and `Enable popup` checkboxes. `layout.js` computes `cols()=Math.min(grid.count,maxSectionCount)` and `rows()=ceil(grid.count/maxSectionCount)`, so changing maximum columns to **1** makes one vertical list instead of three columns: https://github.com/KDE/kdeplasma-addons/blob/v6.7.5/applets/quicklaunch/ConfigGeneral.qml and https://github.com/KDE/kdeplasma-addons/blob/v6.7.5/applets/quicklaunch/layout.js .

**Proposed OWNER GUI steps**: right-click the Quicklaunch applet (or use Edit Mode → configure specific widget), set `Maximum columns: 1`, `Show launcher names: off`, `Enable popup: off`, Apply. Assess resulting vertical icon size, panel height and alignment from screenshot **BEFORE** adjusting panel width (known original 58 px), geometry, custom panel background or icon list. Do not edit applets configuration files in bulk, remove the left panel, or change the top task manager. Preserve Quicklaunch's curated launcher URLs and verify Signal icon and launcher works. A screenshot alone does not prove that Quicklaunch Signal notification badges work like Icons-only Task Manager; that remains a tradeoff.

**Status:** Quicklaunch visual presentation needs formatting, first GUI configuration proposal SOURCE VERIFIED, not yet executed. The longer-term dock must remain single-column (unless OWNER changes mind), choose-only apps, freely reordered, colorful, dark Oxygen gloss. Top dynamic app taskbar and full detailed FenixSystem unaffected.
