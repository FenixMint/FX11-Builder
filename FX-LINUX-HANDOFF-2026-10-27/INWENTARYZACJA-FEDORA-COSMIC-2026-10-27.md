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
