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
