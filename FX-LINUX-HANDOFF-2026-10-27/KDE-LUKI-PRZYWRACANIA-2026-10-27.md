# FX Linux — audyt luk po przejściu Fedora COSMIC → Fedora KDE

**Data:** 2026-10-27  
**Status:** dokumentacja i plan porównania, nie raport pełnego przywrócenia  
**Podstawa:** historia w `WYKONANE-MODYFIKACJE.md`, `INWENTARYZACJA-FEDORA-COSMIC-2026-10-27.md` i checkpoint KDE `FEDORA-KDE-STAN-PO-INSTALACJI-2026-10-27.md`. Wnioski źródłowe tylko z tych zapisów; brak nowych odczytów sprzętu poza wynikami przekazanymi przez OWNER.

## OWNER: Nadal nie wszystko z COSMIC przywrócono

Owner słusznie wskazał, że ukończenie FenixSystem nie oznacza ukończenia całej migracji. Nie zamykać przywracania FX Linux. Zachować działający profil KDE i iteracyjnie porównać pozostałe funkcje, bez masowego importu starej konfiguracji.

| Obszar | Stan historyczny Fedora COSMIC | Potwierdzony stan Fedora KDE | Następne działanie |
|---|---|---|---|
| FenixSystem | Conky + `fenix-sensors.sh`, `fenix-conky.desktop` | **PASS**: port KDE V3 działa, GPU/CPU/SSD/FAN/APU/bateria/NET, 12 wątków, autostart po zalogowaniu | Pozostawić; znane znikanie po Show Desktop w Conky 1.22.2, czekać na nowszy oficjalny pakiet Fedory według decyzji OWNER |
| Night Light | Fenix Night Light alfa ma backend COSMIC, projektowa temperatura 4000 K noc | **PASS odpowiednik KDE:** natywny Night Color **5000 K** wybrany przez OWNER | Nie włączać COSMIC backendu ani zmieniać na 4000 K |
| ZRAM | 8 GiB, priorytet 100 | **PASS wartości**: 8 GiB, priorytet 100 | Nie zmieniać domyślnie |
| Zasilanie | TuneD `balanced-battery` | **RÓŻNICA**: TuneD 2.28 z `tuned-ppd`, profil `balanced`; brak `power-profiles-daemon` | Porównać profil i wybory KDE/PowerDevil; nie wymuszać profilu w ciemno |
| Klapa | `/etc/systemd/logind.conf.d/90-thinfedora-lid.conf`, historycznie `suspend` na baterii, `ignore` z zewnętrznym zasilaniem/docked; test z zamkniętą klapą i HDMI na baterii zaliczony | **NIEZWERYFIKOWANE** | Sprawdzić aktualny logind i obsługę w PowerDevil; dopasować docelową funkcję, bez automatycznego odtwarzania starych plików |
| Monitory | COSMIC `outputs.ron`, HDMI (0,0), eDP off w profilu zamkniętej klapy | **NIEZWERYFIKOWANE** | Skonfigurować natywnie w KDE/KScreen, nie importować `outputs.ron` |
| GRUB FX OS | Kompletny motyw `/boot/grub2/themes/fxos`, historia testu Fedora BLS/Windows Boot Manager/UEFI | **NIEZWERYFIKOWANE / NIEODTWORZONE** | Sprawdzić boot i obecność Windows, ścieżki EFI/BLS, dopiero potem rozważać przywrócenie motywu; nigdy nie dotykać ręcznie generowanego `grub.cfg` |
| Webcam blacklist | `/etc/modprobe.d/disable-webcam.conf` 19 B; cel i treść nieprzebadane | **NIEZWERYFIKOWANE** | Obejrzeć tylko konkretny plik; osobna decyzja OWNER o blokowaniu kamery |
| sysctl / modprobe / udev / systemd | Zarchiwizowano wybrane konfiguracje, nie udowodniono wszystkich ręcznych modyfikacji | **NIEZWERYFIKOWANE** | Porównać wyłącznie rzeczywiste lokalne zmiany z domyślną Fedorą KDE, nie kopiować całych katalogów systemowych |
| Wygląd Plasma | Kierunek FX Linux: panel górny, dock, menu, motywy, grafiki i komfortowy pulpit | **CZĘŚCIOWO / PROJEKT**: FenixSystem wizualny działa; pozostałych personalizacji nie potwierdzono | Iteracyjnie ustalić docelowy wygląd natywnie dla KDE |
| Inne skrypty/aplikacje | Pełna lista poza zachowanym archiwum i źródłami nie jest udowodniona | **NIEZWERYFIKOWANE** | Zebrać *manifest* dostępnych źródeł i opisać rzeczywiste personalizacje, nie wymyślać brakujących zmian |

## Priorytet dalszego audytu

1. Wykonać wyłącznie odczytowe porównanie starego folderu `~/FX-Linux-Odzysk` z bieżącymi konfiguracjami: logind/klapa, aktywny TuneD, obecność pełnego motywu GRUB, wpisów GRUB, `disable-webcam.conf` oraz plików ekranu KDE.
2. Podjąć po kolei decyzje w kategoriach: **zachować obecne KDE / zaadaptować / odtworzyć / świadomie pominąć**.
3. Szczególną ostrożność zachować wobec zamkniętej klapy i monitorów oraz `/etc/default/grub`, UEFI, Windows Boot Manager i partycji FX11. Każda zmiana systemowa musi być celowa i odwracalna.
4. Nie powielać zakończonych prac z Conky ani nie wymuszać projektowego Fenix Night Light dla COSMIC. Nie publikować prywatnego archiwum.

## Co WIEMY, czego NIE WIEMY

Archiwum `FX-Linux-Config-20261027-115021.tar.gz` zostało zweryfikowane na KDE tym samym SHA-256 co wcześniej i rozpakowane do odrębnego `~/FX-Linux-Odzysk`. Potwierdzono trzy własne pliki FenixSystem, pełny lokalny katalog źródeł GRUB był obecny na COSMIC przed migracją, ale jego obecność w obecnym katalogu staging KDE ani stan systemowego GRUB po migracji nie były odrębnie zweryfikowane. Nie twierdzić, że wszystko z COSMIC zostało odtworzone. Nie rekonstruować hipotetycznych optymalizacji z samej nazwy folderu.


## Wynik pierwszego porównania archiwum COSMIC z działającą KDE — OWNER

OWNER przekazał odczyt **tylko do odczytu** z nowej Fedory KDE (2026-10-27):

| Sprawdzono | COSMIC w `~/FX-Linux-Odzysk` | KDE obecnie | Interpretacja |
|---|---|---|---|
| Klapa | `HandleLidSwitch=suspend`, `HandleLidSwitchExternalPower=ignore`, `HandleLidSwitchDocked=ignore` | brak pliku `/etc/systemd/logind.conf.d/90-thinfedora-lid.conf` | stare własne ustawienia nieprzeniesione; **nie dowodzi to jeszcze aktualnej akcji zamknięcia klapy**, bo PowerDevil/KDE może przejąć obsługę |
| TuneD | aktywny `balanced-battery` przed reinstalacją | `Current active profile: balanced` | potwierdzona zmiana profilu, niekoniecznie błąd; potrzebna decyzja funkcjonalna |
| GRUB FX OS | `theme.txt` obecny w archiwum | systemowy `/boot/grub2/themes/fxos/theme.txt` nieobecny przy sprawdzeniu sudo | motyw zachowany, ale **nieprzywrócony** |
| GRUB settings | historycznie `GRUB_THEME` i `GRUB_GFXMODE` | `grep '^GRUB_(THEME|GFXMODE)='` nic nie zwrócił | brak tych aktywnych linii w `/etc/default/grub`; **nie wyciągać wniosku o stanie wszystkich mechanizmów rozruchu** |
| Webcam | w archiwum dokładnie `blacklist uvcvideo` | brak `/etc/modprobe.d/disable-webcam.conf` | poprzednia indywidualna blokada modułu nieprzeniesiona; brak pliku nie dowodzi pełnej aktywności kamerki |

**Dodatkowy kontekst techniczny zweryfikowany w dokumentacji:** systemd-logind stosuje różne akcje dla zasilania zewnętrznego i dock/multi-display, ale powłoka graficzna może przejąć zdarzenia pokrywy przez inhibitor `handle-lid-switch`. KDE PowerDevil zarządza akcją zamknięcia pokrywy i odrębnie profilami na baterii/AC. Źródła: https://www.freedesktop.org/software/systemd/man/latest/logind.conf.html oraz https://docs.kde.org/stable_kf6/en/powerdevil/kcontrol/powerdevil/ .

**Kolejność i bezpieczeństwo:**
1. Odczytowo: `systemd-inhibit --list` (czy KDE przejmuje obsługę klapy), `kscreen-doctor -o` (faktyczny układ monitorów), a w GUI KDE sprawdzić Ustawienia systemowe → Zarządzanie energią, osobno zasilanie sieciowe i bateria. Nie testować zamknięcia klapy przed weryfikacją, jeśli może to przerwać pracę.
2. Dalej porównać TuneD `balanced` i historyczny `balanced-battery`; nie instalować konkurujących daemona ani nie wymuszać profilu bez pomiarów.
3. Webcam: zapytać OWNER, czy zachować intencjonalne wyłączenie; **nie przywracać `blacklist uvcvideo` w ciemno**.
4. GRUB: zweryfikować konfigurację i wpis Windows Boot Manager/UEFI oraz BLS przed jakimikolwiek zapisami w `/boot`, `/etc/default/grub`, EFI lub generowanym `grub.cfg`.
5. Nie przenosić całego `/etc/tuned`, `/etc/sysctl.d`, `/etc/modprobe.d` ani `outputs.ron` z COSMIC do KDE.

To jest aktualizacja audytu. **Żadnych ustawień na komputerze OWNER nie zmieniono przez tę operację GitHub.**
