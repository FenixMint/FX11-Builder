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
