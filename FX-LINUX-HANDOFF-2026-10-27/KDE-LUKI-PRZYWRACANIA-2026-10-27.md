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


## POWERDEVIL / KSCREEN — odczyt OWNER po reinstalacji KDE (2026-10-27)

OWNER uruchomił `systemd-inhibit --list --no-pager` oraz `kscreen-doctor -o` na Fedora 44 KDE Plasma 6.7.5 Wayland. Odczyt tylko do celów diagnozy, bez zmian systemowych.

### Rzeczywista obsługa klapy

- `PowerDevil` trzyma **block inhibitor** dla `handle-power-key:handle-suspend-key:handle-hibernate-key:handle-lid-switch`, uzasadnienie `KDE handles power events`.
- Pozostałe inhibitory `sleep` delay: ModemManager, NetworkManager, UPower, `kwin_wayland` (blokada ekranu przed uśpieniem).
- Wniosek: w bieżącej sesji **PowerDevil KDE obsługuje zdarzenie zamknięcia klapy**; odtworzenie `90-thinfedora-lid.conf` nie jest dobrym pierwszym krokiem. Brak danych o aktualnych akcjach lid-close osobno dla baterii i AC.
- Dokumentacja KDE Power Management wskazuje osobne profile *On AC Power*, *On Battery*, *On Low Battery*. Źródło: https://docs.kde.org/stable_kf6/en/powerdevil/kcontrol/powerdevil/ ; projekt KDE PowerDevil: https://github.com/KDE/powerdevil .
- Źródło konfiguracji PowerDevil w upstream ma opcję `InhibitLidActionWhenExternalMonitorPresent` (domyślnie `true` w KConfig): https://github.com/KDE/powerdevil/blob/master/PowerDevilProfileSettings.kcfg . To nie jest dowód bieżącego ustawienia OWNER.

### Rzeczywisty stan monitorów

| Output | Połączenie | Aktywność | Tryb | Położenie | Skala / priorytet |
|---|---|---|---|---|---|
| `HDMI-A-1` (zewnętrzny) | connected | **enabled** | **1680×1050 @ 59.95 Hz**, wybrany tryb | **0,0** | 1, **priority 1** |
| `eDP-1` (matryca) | connected | **disabled** | dostępny 1920×1080 @ 60.05 Hz, ale wyłączony | historycznie wyświetlane 0,0 | 1, priority 1 (nie oznacza aktywnego ekranu) |

Bieżący układ **odpowiada intencji układu monitorów z COSMIC** (zewnętrzny jako aktywny, początek pulpitu 0,0, matryca wyłączona). **Konfiguracji `outputs.ron` nie importujemy do KScreen**. Z raportu KDE: jasność HDMI 75%, eDP 100% (eDP wyłączony); nie zakładać, że jest to celowe odtworzenie poprzednich wartości.

### Brakujący test funkcjonalny

Nadal **nie wiemy**, jak PowerDevil zachowa się przy zamknięciu klapy na samej baterii i przy zasilaczu; samo `systemd-inhibit` i `kscreen-doctor` tego nie weryfikuje.

**Następny krok:** OWNER ma sprawdzić graficznie Ustawienia systemowe KDE → Zarządzanie energią: profile *Na baterii* i *Na zasilaczu* (ewentualnie Niski poziom baterii), zwłaszcza akcję `When laptop lid closed` i opcję wykonania akcji także gdy podłączony monitor zewnętrzny. W pierwszym etapie tylko odczyt, żadnego zamykania klapy ani restartowania usług podczas pracy. Potem uzgodnić oczekiwaną semantykę z poprzednim rezultatem COSMIC (zewnętrzny monitor aktywny przy zamkniętej klapie również na baterii) i zaplanować odwracalny test z zapisanymi danymi.

**Pozostałe luki nadal otwarte:** różnica TuneD `balanced` vs historyczne `balanced-battery`; motyw FX OS GRUB jeszcze nieprzywrócony; `blacklist uvcvideo` nieprzywrócone; sysctl/modprobe i ewentualne skrypty bez pełnego audytu. Night Color KDE 5000 K, Conky V3/autostart i ZRAM 8 GiB / prio 100 już potwierdzone.


## OWNER decision — lid settings are satisfactory on KDE; do not change them

OWNER potwierdził po przejrzeniu obecnego zachowania, że **ustawienia klapy na Fedora KDE są na razie poprawne i nie należy ich zmieniać**. Oznacza to świadome **ZACHOWAĆ OBECNE KDE**, a nie przywracać `/etc/systemd/logind.conf.d/90-thinfedora-lid.conf` z COSMIC. PowerDevil nadal obsługuje zdarzenia pokrywy przez inhibitor, HDMI ma aktywny układ 1680×1050 przy (0,0), eDP jest wyłączony. Nie twierdzić, że przeprowadzono formalny osobny test każdej kombinacji zasilania — decyzja jest oparta na aktualnym działaniu ocenionym przez OWNER.

Następny obszar po decyzji OWNER: TuneD i optymalizacje. KDE ma `tuned` i `tuned-ppd`, aktywny `balanced`; archiwum ze starego COSMIC raportowało `balanced-battery`. Pierwszy etap wyłącznie odczytowy: `tuned-adm list`, `tuned-adm profile_info`, odczyt aktywnego profilu starego staging `etc/tuned/active_profile`, przegląd plików `etc/tuned/profiles` i konfiguracji mapowania `ppd.conf`. Dopiero po porównaniu zdecydować, czy zachować profil `balanced`, czy potrzebna jest adaptacja, bez równoległych menedżerów energii i bez kopiowania całego `/etc/tuned`. Brak zmian w KDE/GRUB/kamerze podczas aktualizacji tego checkpointu.


## TuneD / tuned-ppd — comparison completed from OWNER read-only results

OWNER executed read-only power-profile inventory on Fedora 44 KDE after COSMIC migration.

- `tuned-adm active`: `Current active profile: balanced`.
- `tuned-adm profile_info`: `balanced`, `General non-specialized tuned profile`.
- `tuned-adm list` includes both `balanced` and `balanced-battery`, where the latter is described as a balanced profile biased toward battery savings.
- Archived old `etc/tuned/active_profile`: `balanced-battery`.
- `find ~/FX-Linux-Odzysk/etc/tuned/profiles -maxdepth 3 -type f` printed no custom profile files (scope of that command only; cannot categorically exclude other modifications).
- Current KDE `/etc/tuned/ppd.conf`:
  ```ini
  [main]
  default=balanced
  battery_detection=true
  sysfs_acpi_monitor=true
  [profiles]
  power-saver=powersave
  balanced=balanced
  performance=throughput-performance
  [battery]
  balanced=balanced-battery
  ```

**Interpretation grounded in upstream TuneD:** the KDE-facing PPD `balanced` selection maps to TuneD `balanced` on AC and TuneD `balanced-battery` on DC when battery detection is enabled. `tuned-ppd` merges the `[battery]` map with the base `[profiles]` map and chooses according to power source. Sources: https://github.com/redhat-performance/tuned/blob/master/tuned/ppd/config.py ; https://github.com/redhat-performance/tuned/blob/master/tuned/ppd/ppd.conf ; https://fedoraproject.org/wiki/Changes/TunedAsTheDefaultPowerProfileManagementDaemon .

**Recommended state:** keep default KDE integrated TuneD/`tuned-ppd` and `balanced` selection; no reason to unconditionally force the old COSMIC `balanced-battery` via `tuned-adm` or copy `/etc/tuned`. Owner's currently active `balanced` is consistent with AC mode but **we have not confirmed actual AC/charging state or runtime transitions**. Read-only verification possible: `cat /sys/class/power_supply/AC/online`, `systemctl is-active tuned-ppd`, `tuned-adm active`, and repeat in normal battery use if desired; don't require abrupt power removal.

Status: **configuration equivalence likely / runtime switching untested**. No change applied to power profiles by this analysis. Next audit target: old `/etc/sysctl.conf` and `/etc/sysctl.d`, modem/camera blacklist `uvcvideo` and GRUB theme to be addressed separately with owner permission.


## OWNER read-only comparison — sysctl.conf and tuned-main.conf

OWNER przekazał wyniki porównania z rozpakowanego COSMIC (`~/FX-Linux-Odzysk/etc`) z działającą Fedorą KDE:

- `/etc/sysctl.conf`: zarówno w archiwum COSMIC, jak i bieżącym KDE test `grep -En '^[[:space:]]*[^#;[:space:]][^=]*='` zwrócił `Brak aktywnych wpisów`. **Zakres badania: ten plik, nie wszystkie drop-in sysctl systemu.**
- `/etc/tuned/tuned-main.conf`: widoczne aktywne parametry i numery linii identyczne w obu: `daemon=1`, `dynamic_tuning=0`, `sleep_interval=1`, `update_interval=10`, `recommend_command=1`, `reapply_sysctl=1`, `default_instance_priority=0`, `udev_buffer_size=1MB`, `log_file_count=2`, `log_file_max_size=1MB`, `startup_udev_settle_wait=0`. Ten wynik nie dowodzi identyczności komentarzy ani każdego bajtu pliku; nie ma wykazanych aktywnych różnic.
- Stare `etc/sysctl.d/`: `99-sysctl.conf -> ../sysctl.conf` (symlink, nie niezależna niestandardowa reguła). Nie porównywano jeszcze wszystkich innych globalnych katalogów `sysctl.d` na działającej KDE.
- **Decyzja techniczna na podstawie dostępnych faktów:** nie odtwarzać `sysctl.conf`, `tuned-main.conf` ani starego symlinka z archiwum w ciemno. Nie wykazano utraconych dostosowań w tych konkretnych ustawieniach.

**Następny bezpieczny krok:** read-only sprawdzenie starych i nowych plików `/etc/modprobe.d`, ze szczególnym uwzględnieniem starego `disable-webcam.conf` zawierającego `blacklist uvcvideo`. Tylko OWNER decyduje, czy kamerka ma być blokowana. Potem bezpieczeństwo aktualnego GRUB/EFI/Windows przed ewentualnym przywróceniem wyglądu FX OS. Nie zmieniać działającego FenixSystem, Night Color 5000 K, klapy ani obecnego TuneD.


## OWNER read-only comparison — modprobe.d and sysctl.d results

OWNER uruchomił porównanie plików `~/FX-Linux-Odzysk/etc/modprobe.d` (archiwum Fedora COSMIC) z `/etc/modprobe.d` w działającej Fedora KDE. Wynik testu istnienia i `cmp -s`:

- **10 plików identycznych**: `batman-adv-blacklist.conf`, `firewalld-sysctls.conf`, `floppy-blacklist.conf`, `l2tp_eth-blacklist.conf`, `l2tp_netlink-blacklist.conf`, `l2tp_ppp-blacklist.conf`, `lockd.conf`, `nvdimm-security.conf`, `rds-blacklist.conf`, `tuned.conf`.
- **3 pliki obecne w archiwum COSMIC, ale nieobecne w tym samym miejscu KDE**: `disable-webcam.conf`, `kvm.conf`, `vhost.conf`. Ich nieobecność **nie dowodzi**, że są to unikalne lub potrzebne modyfikacje; `kvm.conf` i `vhost.conf` muszą zostać ocenione według zawartości. Wcześniej źródłowe `disable-webcam.conf` potwierdzono jako pojedynczy wpis `blacklist uvcvideo`, który wyłącza automatyczne ładowanie sterownika kamer UVC; OWNER musi sam zdecydować, czy kamerę ponownie blokować.
- `find /etc/sysctl.d` na KDE: `99-sysctl.conf -> ../sysctl.conf` — ten sam link co w archiwum COSMIC; brak wykazanej różnicy w tej lokalizacji.

**Wniosek:** `modprobe.d` nie przywracać hurtowo. Obejrzeć tylko tekst trzech brakujących plików, a zwłaszcza sprawdzić sens i ewentualne źródło pakietowe wpisów `kvm.conf`, `vhost.conf`. Przed jakimikolwiek zapisami do `/etc/modprobe.d` wymagana świadoma decyzja OWNER. Ocena ograniczona do porównanych ścieżek, nie do wszystkich możliwych parametrów sterowników.

**Następny krok read-only:** `for n in disable-webcam.conf kvm.conf vhost.conf; do echo "$n"; sed -n '1,120p' "$HOME/FX-Linux-Odzysk/etc/modprobe.d/$n"; done` z kontrolą istnienia pliku; ewentualnie `lsmod` / `modinfo` dla zrozumienia bieżącej obsługi sprzętu, bez zmian stanu. Następny niezależny, potencjalnie bardziej ryzykowny etap: rozpoznanie aktualnego GRUB/BLS/Windows Boot Manager przed przywracaniem wyglądu FX OS.


## OWNER verified content of three missing modprobe files

OWNER odczytał trzy brakujące względem COSMIC konfiguracje:

- `disable-webcam.conf`: dokładnie `blacklist uvcvideo` (własna decyzja o blokowaniu automatycznego ładowania UVC; stan blokady w KDE nie został włączony).
- `kvm.conf`: tylko komentarze z przykładami `#options kvm_intel nested=1` i `#options kvm_amd nested=1`. **Brak aktywnych dyrektyw**. Nie odtwarzać, nie jest wykazaną utraconą optymalizacją. Tekst odpowiada przykładom w historycznych pakietach qemu-kvm Red Hat: https://bugzilla.redhat.com/show_bug.cgi?id=1290150 .
- `vhost.conf`: dwa komentarze i **aktywne** `options vhost max_mem_regions=509`. Dotyczy maksymalnej liczby regionów pamięci dla sterownika vhost, szczególnie przy wirtualizacji QEMU/KVM; *nie* jest ogólną optymalizacją wydajności. Tekst dokładnie zgadza się z przykładowym plikiem `SOURCES/vhost.conf` w pakietach QEMU z rodziny RPM: https://git.almalinux.org/rpms/qemu/commit/001015e8674e667ac6983bb71c16e9df5d99fe06?show-outdated=&style=unified&whitespace=ignore-all . Autor dokumentacji virtio-mem mówi, że taki `max_mem_regions=509` bywa ustawiany standardowo na Fedorze przez `/etc/modprobe.d/vhost.conf`: https://virtio-mem.gitlab.io/user-guide/user-guide-qemu.html . **Nie ma dowodu**, że historyczny plik w komputerze OWNER został stworzony własnoręcznie; nie przywracać na ślepo, tylko gdy realna konfiguracja wirtualizacji tego potrzebuje.

**Ocena w tej fazie:** 10 z 13 zachowanych plików modprobe było identycznych na KDE; brakujące `kvm.conf` jest komentarzowym przykładem; `vhost.conf` jest czynną opcją specyficzną dla VM, najpewniej po pakiecie QEMU, lecz nie stwierdzono jeszcze pochodzenia RPM na starej instalacji. `disable-webcam.conf` to opcja funkcjonalna i świadoma decyzja OWNER (nie zakładać jej przywrócenia bez zgody).

**Ewentualna diagnostyka tylko do odczytu**, jeśli temat vhost będzie ważny: `modprobe -c | grep -E '^options vhost '`, `cat /sys/module/vhost/parameters/max_mem_regions` o ile ten plik istnieje, `rpm -q qemu-kvm` i lista zainstalowanych pakietów QEMU. To nic nie uruchamia ani nie ładuje modułu. W obecnym etapie nie ma uzasadnienia do zmiany `/etc/modprobe.d`.

**Następny etap migracji:** GRUB FX OS — najpierw inwentaryzacja BLS/UEFI i Windows Boot Manager oraz bezpieczna weryfikacja motywu w archiwum. Unikać zmian w bootloaderze przed audytem. 
