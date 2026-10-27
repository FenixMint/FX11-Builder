# FenixSystem — profil testowy Fedora 44 KDE Plasma Wayland

**Status: projekt wersji KDE, NIE uruchomiony jeszcze na komputerze OWNER.** Oryginalne pliki COSMIC pozostają w archiwum i `~/FX-Linux-Odzysk`.

## Zmiany względem odzyskanych plików

Wersja zachowuje ten sam układ z prawym górnym rogiem i dwunastoma polami obciążenia CPU. Nie włącza autostartu.

- `fenix-sensors-kde.sh`: czyta `k10temp`, `amdgpu`, `nvme`, `thinkpad` tylko gdy odpowiednie pliki istnieją i są czytelne; w pozostałych przypadkach pokazuje `--`.
- `fenix-network-kde.sh`: wykrywa interfejs domyślnej trasy IPv4/IPv6; nie zakłada starego `wlp6s0`.
- `fenixsystem-kde.conf`: zachowuje Conky Wayland i pierwotny rozkład, ale wykorzystuje nowe helpery, `nproc` w nagłówku i `battery_percent all`. Wykresy logicznych CPU 1–12 nadal bazują na historycznym układzie — sprawdzić `nproc`.
- Okno pozostaje na początek `own_window_type = 'normal'` i `below`; wygląd na KWin Wayland należy przetestować na żywo. Na Fedora 44 Conky 1.22.2 `out_to_wayland` jest poprawną opcją. Nie używamy opcji z Conky nowszych niż wersja repo Fedora 44.

## Odczyt i test bez autostartu

Zapisane pliki można pobrać z gałęzi GitHub `handoff/fx-linux-manual-package-2026-10-27` do osobnego katalogu. Przed testem przeczytać zawartość i uruchomić `bash -n` na obu skryptach. Na docelowym KDE:

```bash
sudo dnf install conky
P="$HOME/FX-Linux-Odzysk/kde-fenixsystem"
mkdir -p "$HOME/.local/bin" "$HOME/.config/conky"
install -m 755 "$P/fenix-sensors-kde.sh" "$HOME/.local/bin/fenix-sensors-kde.sh"
install -m 755 "$P/fenix-network-kde.sh" "$HOME/.local/bin/fenix-network-kde.sh"
install -m 644 "$P/fenixsystem-kde.conf" "$HOME/.config/conky/fenixsystem-kde.conf"
"$HOME/.local/bin/fenix-sensors-kde.sh"
"$HOME/.local/bin/fenix-network-kde.sh"
conky -c "$HOME/.config/conky/fenixsystem-kde.conf"
```

Test Conky odbywa się na pierwszym planie; zakończyć `Ctrl+C`. **Nie przenosić jeszcze starego `fenix-conky.desktop` do autostartu!** Obserwować czy okno jest widoczne, nie przykrywa okien, pokazuje właściwe dane i czy są błędy w terminalu.

## Stan systemu niezależnego od FenixSystem

OWNER ustawił natywny Night Color KDE na **5000 K**, TuneD na `balanced`, zram 8 GiB / priorytet 100; tego pakiet nie zmienia. Nie przywraca `logind`, GNOME/COSMIC, GRUB ani `disable-webcam.conf`.

Źródła potwierdzające wsparcie Conky Wayland w Fedora 44: https://packages.fedoraproject.org/pkgs/conky/conky/fedora-44.html ; opcje Conky: https://conky.cc/config_settings .

Nie wykonano testu w sesji użytkownika ani instalacji pakietów.

## Automatyczne pobranie trzech plików (OWNER request)

Zamiast ręcznego pobierania, OWNER może użyć terminala Fedory KDE. Pobieramy z **przypiętego commitu** `f403cb2dd9c4117f6242dce50219f5c8e4816727`, aby rezultat nie zależał od późniejszych aktualizacji gałęzi.

```bash
bash <<'BASH'
set -euo pipefail
BASE="https://raw.githubusercontent.com/FenixMint/FX11-Builder/f403cb2dd9c4117f6242dce50219f5c8e4816727/FX-LINUX-HANDOFF-2026-10-27/kde-adaptation/fenixsystem"
DEST="$HOME/FX-Linux-Odzysk/kde-fenixsystem"
mkdir -p "$DEST"
for FILE in fenix-sensors-kde.sh fenix-network-kde.sh fenixsystem-kde.conf; do
    if [[ -e "$DEST/$FILE" ]]; then
        printf 'Pomijam juz istniejacy plik: %s\n' "$FILE"
        continue
    fi
    TEMP=$(mktemp "$DEST/.download.XXXXXX")
    if curl -fLsS --retry 2 --proto '=https' "$BASE/$FILE" -o "$TEMP"; then
        mv -- "$TEMP" "$DEST/$FILE"
    else
        rm -f -- "$TEMP"
        exit 1
    fi
done
bash -n "$DEST/fenix-sensors-kde.sh"
bash -n "$DEST/fenix-network-kde.sh"
ls -lh "$DEST"
BASH
```

To tylko **pobiera pliki do staging**, nie wykonuje żadnego skryptu, nie instaluje Conky, nie aktywuje autostartu i nie zmienia konfiguracji. Istniejących plików nie nadpisuje. `bash -n` to wyłącznie sprawdzanie składni skryptów; nie testuje ich działania na czujnikach.
