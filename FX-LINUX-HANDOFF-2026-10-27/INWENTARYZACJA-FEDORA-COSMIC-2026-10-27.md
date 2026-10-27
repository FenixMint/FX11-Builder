# Inwentaryzacja źródłowej Fedory COSMIC — wyniki OWNER

Data: 2026-10-27  
Status: **OWNER-REPORTED FINDINGS — FILE CONTENT NOT YET REVIEWED OR COPIED**  
Środowisko: Fedora COSMIC przed planowaną reinstalacją na KDE Plasma.

## Potwierdzone ścieżki

Na podstawie wklejonego odczytu z terminala użytkownika:

- `~/.config/conky/` — katalog istnieje.
- `~/.config/conky/conky.conf` — plik źródłowy znaleziony w wyszukiwaniu.
- `~/.local/bin/fenix-sensors.sh` — autorski skrypt czujników znaleziony w wyszukiwaniu.
- `~/.config/autostart/fenix-conky.desktop` — wpis autostartu znaleziony.
- `~/Pobrane/fxos-grub-background.png` — lokalna grafika GRUB znaleziona, zgodność z historycznym SHA-256 jeszcze NIE SPRAWDZONA.
- `~/.local/state/cosmic-comp/outputs.ron` — plik bieżącej konfiguracji monitora istnieje.
- `/etc/default/grub` — istnieje; zawartości nie odczytano.
- `/etc/systemd/logind.conf.d/90-thinfedora-lid.conf` — istnieje; zawartości nie odczytano.
- `/etc/tuned`, `/etc/sysctl.d`, `/etc/modprobe.d` — katalogi istnieją; nie udowodniono jeszcze, że zawierają własne zmiany OWNER.

## Brak / ograniczenie odczytu

- `~/.conkyrc` — brak według testu, nie musi być używany przy pliku `~/.config/conky/conky.conf`.
- `~/.config/systemd/user` — brak według testu, nie dowodzi braku jakichkolwiek usług `systemd --user` zainstalowanych globalnie.
- `~/.config/fenix-nightlight` i `~/.local/share/fenix-nightlight` — brak według testu; repozytorium kodu Fenix Night Light istnieje na GitHubie, ale nie oznacza to aktywnej lokalnej instalacji.
- `/boot/grub2/themes/fxos` — test `[ -e ]` zwrócił BRAK. **Status UNKNOWN**, ponieważ zwykły użytkownik może nie mieć prawa przejścia przez `/boot/grub2`. Wymaga osobnego, tylko odczytowego sprawdzenia uprawnień.

## Obecny stan pracy systemu

- `tuned-adm active` → `Current active profile: balanced-battery`.
- `swapon --show` → `/dev/zram0`, typ `partition`, rozmiar **8 GiB**, zajęte ok. **3.8 MiB**, priorytet **100**.
- Wywołanie `powerprofilesctl get` nie wyświetliło wyniku — nie ustalać przyczyny bez osobnego sprawdzenia.

Są to wyniki stanu bieżącego z raportu OWNER. **Nie dowodzą, czy i kiedy parametry TuneD/ZRAM były ręcznie zmieniane.**

## Jak zabezpieczamy

OWNER **sam ręcznie kopiuje** wybrane skrypty i ustawienia do swojego folderu na partycji **FX11**. Nie uruchamiamy automatycznego backupu, nie archiwizujemy systemu ani całego HOME, nie wymagamy szyfrowania i nie ustalamy punktu montowania.

Priorytet plików do ręcznego przeniesienia:
1. `conky.conf`, `fenix-sensors.sh`, `fenix-conky.desktop`;
2. `fxos-grub-background.png`, aktualne źródła grafiki GRUB i ewentualnie pozostałe lokalne pliki motywu;
3. `outputs.ron`, `/etc/default/grub`, `90-thinfedora-lid.conf`;
4. tylko **rzeczywiście zmodyfikowane** pliki optymalizacji TuneD / sysctl / modprobe / inne — po obejrzeniu zawartości.

Nie kopiować automatycznie całych `/etc/tuned`, `/etc/sysctl.d`, `/etc/modprobe.d` ani danych prywatnych. Poszczególne pliki należy ocenić, gdy poznamy ich nazwy i zawartość.

## Niewykonane / następny etap

- Nie wykonano kopii na partycji FX11 ani na GitHubie oryginalnych prywatnych dotfiles z Fedory.
- Nie odczytano jeszcze zawartości `conky.conf`, `fenix-sensors.sh`, `fenix-conky.desktop`, `outputs.ron` oraz własnych fragmentów TuneD.
- Nie sprawdzono praw dostępu i rzeczywistej zawartości `/boot/grub2/themes/fxos` przy użyciu tylko-odczytowego `sudo ls`.
- Nie zweryfikowano historycznego SHA-256 grafiki GRUB.
- Nie należy deklarować, że konfiguracje są już zabezpieczone do reinstalacji.

Nie usuwano ani nie nadpisywano wcześniejszych źródeł lub checkpointów FX Linux.

## Druga inwentaryzacja OWNER — rzeczywiste pliki GRUB i optymalizacji

**OWNER-REPORTED / 2026-10-27; nie jest to kopia zawartości plików.**

Po `sudo ls -la /boot/grub2/themes/fxos/` potwierdzono istnienie pełnego katalogu motywu, wcześniej błędnie oznaczonego jako BRAK zwykłym `[ -e ]` bez praw dostępu. Zawartość: `background.png`, `fxos-bold-28.pf2`, `fxos-regular-24.pf2`, `icons/`, `theme.txt` oraz `theme.txt.bak`, pikmapy `roundedsquare_*.png`, `progress_bar*.png`, pomocniczy `roundedsquare.svg` i `unifont-*.pf2`. **Należy zachować cały katalog**, nie tylko `theme.txt`. Test rozruchu był historyczny; nie uruchamiano go ponownie.

Plik `~/Pobrane/fxos-grub-background.png` ma **SHA-256 `cd06a7f64c654ca47e2a5c7879418d0e881ef50b9b221215b9803bc4f39ecc95`**. Jest to **dokładnie zgodny hash** z `ASSETS.md` historycznego prototypu. Nie dowodzi to jednak automatycznie identyczności `/boot/grub2/themes/fxos/background.png` — jego hasha jeszcze nie porównano.

Katalog `/etc/tuned/`: `active_profile`, `bootcmdline`, `post_loaded_profile`, `ppd_base_profile`, `ppd.conf`, `profile_mode`, `profiles/`, `recommend.d/`, `tuned-main.conf`. Aktywny profil z pierwszej inwentaryzacji: `balanced-battery`; **nie wiadomo, które ustawienia są autorskie**.

`/etc/sysctl.d/` zawiera symlink `99-sysctl.conf -> ../sysctl.conf`. Nie udowodniono ręcznej modyfikacji.

`/etc/modprobe.d/` zawiera plik `disable-webcam.conf` o wielkości 19 B i dacie modyfikacji z początku października. To **ważny kandydat na indywidualną zmianę**, ale nie analizowano jeszcze zawartości, zasadności ani skutków. Pozostałe wpisy to m.in. `batman-adv-blacklist.conf`, `firewalld-sysctls.conf`, `floppy-blacklist.conf`, `kvm.conf`, `l2tp_*blacklist.conf`, `lockd.conf`, `nvdimm-security.conf`, `rds-blacklist.conf`, `tuned.conf`, `vhost.conf`. Nie wnioskować z samych nazw, że wszystkie są FX-owned.

**Aktualna instrukcja OWNER:** jedno archiwum `.tar.gz` z konkretnych źródeł (Conky, sensory, autostart, GRUB kompletny, tło o potwierdzonym SHA, Fenix Night Light jeśli obecny, konfiguracja monitora/klapy, `/etc/tuned`, `/etc/sysctl.d` z `/etc/sysctl.conf`, `/etc/modprobe.d`), plus plik tekstowy z opisem modyfikacji i wynikami stanu. OWNER sam przeniesie archiwum na FX11, **bez automatycznego montowania/kopiowania, szyfrowania ani backupu systemu**. Nie wrzucać prywatnego archiwum na GitHub.

**Do potwierdzenia po wykonaniu:** rzeczywisty manifest zawartości utworzonego archiwum, rozmiar, brak błędów `tar`, fizyczny transfer na FX11. Tych zdarzeń jeszcze nie stwierdzono.
