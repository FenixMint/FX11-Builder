# FenixSystem — profil testowy Fedora 44 KDE Plasma Wayland

**Status: podstawowe czujniki, sieć i widoczność Conky na KDE Wayland POTWIERDZONE przez OWNER; wariant V3: kompaktowy trzykolumnowy układ CPU pokazany na zrzucie OWNER i wizualnie potwierdzony.** Oryginalne pliki COSMIC pozostają w archiwum i `~/FX-Linux-Odzysk`.

## Zmiany względem odzyskanych plików

Wersja zachowuje ten sam układ z prawym górnym rogiem i dwunastoma polami obciążenia CPU. Nie włącza autostartu.

- `fenix-sensors-kde.sh`: czyta `k10temp`, `amdgpu`, `nvme`, `thinkpad` tylko gdy odpowiednie pliki istnieją i są czytelne; w pozostałych przypadkach pokazuje `--`.
- `fenix-network-kde.sh`: wykrywa interfejs domyślnej trasy IPv4/IPv6; nie zakłada starego `wlp6s0`.
- `fenixsystem-kde.conf`: zachowuje Conky Wayland i pierwotny rozkład, ale wykorzystuje nowe helpery, `nproc` w nagłówku i **`battery_percent BAT0`** (potwierdzono obecność BAT0). Wątki CPU 1–12 przedstawiono w V3 w **trzech zwartych kolumnach** z `${offset 45}`; `nproc` wynosi **12**.
- Na KWin Wayland `own_window_type = 'normal'` jest zachowany, ale usunięto `own_window_hints` zawierające `below`: OWNER potwierdził, że dopiero usunięcie wskazówek pozwoliło zobaczyć widżet na pulpicie. Na Fedora 44 Conky 1.22.2 `out_to_wayland` jest poprawną opcją. Nie używamy opcji z Conky nowszych niż wersja repo Fedora 44.

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

OWNER zainstalował oficjalny `conky-1.22.2-3.fc44`, uruchomił FenixSystem na KDE Wayland i pokazał zrzut ekranu po usunięciu `own_window_hints`. W zrzucie działały CPU, RAM, dysk, czujniki, bateria i sieć, ale etykiety CPU w **pierwotnym układzie trzykolumnowym nachodziły na siebie**. Dwukolumnowa poprawka z GitHuba jest nadal kandydatem do testów.

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

## Drugi etap: test widocznej wersji z poprawionymi kolumnami CPU

Pobierz **tylko nową konfigurację**, przypiętą do commitu `08ef36d5316f9367a8900ab61a4c0918d97f0ad9`. Użyj osobnej nazwy, **nie nadpisuj** `~/.config/conky/fenixsystem-kde.conf` ani poprzednich wersji w staging.

```bash
DIR="$HOME/FX-Linux-Odzysk/kde-fenixsystem"
mkdir -p "$DIR"
TARGET="$DIR/fenixsystem-kde-v2.conf"
URL="https://raw.githubusercontent.com/FenixMint/FX11-Builder/08ef36d5316f9367a8900ab61a4c0918d97f0ad9/FX-LINUX-HANDOFF-2026-10-27/kde-adaptation/fenixsystem/fenixsystem-kde.conf"
curl -fLsS --proto '=https' "$URL" -o "$TARGET" &&
  conky -c "$TARGET"
```

Jeśli w tym katalogu plik `fenixsystem-kde-v2.conf` już istnieje, zastosuj inną nazwę lub najpierw sprawdź zawartość, żeby nie utracić ręcznych zmian. Poprawka nie zakłada aktywacji autostartu.

## CPU: poprawka V3 — kompaktny układ (2026-10-27)

OWNER potwierdził obrazem, że V2 z `${alignr}` nie nakłada wątków na siebie, ale zbyt szeroko rozsuwa je po całej szerokości Conky. V3 wraca do 3 kolumn bez problematycznego na KDE Wayland `${goto}`, używając względnych `${offset 45}`.

Test bez nadpisywania lokalnej konfiguracji:

```bash
DIR="$HOME/FX-Linux-Odzysk/kde-fenixsystem"
mkdir -p "$DIR"
TEST=$(mktemp "$DIR/fenixsystem-v3.XXXXXX.conf")
URL="https://raw.githubusercontent.com/FenixMint/FX11-Builder/4f08721239a41aeb8d306110ea2414c03bfac130/FX-LINUX-HANDOFF-2026-10-27/kde-adaptation/fenixsystem/fenixsystem-kde.conf"
if curl -fLsS --proto '=https' "$URL" -o "$TEST"; then
    conky -c "$TEST"
else
    rm -f -- "$TEST"
fi
```

OWNER przesłał zrzut działającej V3: trzy zwarte kolumny CPU nie nachodzą na siebie i widżet pokazuje wszystkie główne pomiary. Autostart pozostaje nieuruchomiony do chwili świadomego włączenia na komputerze.

## Wdrożenie wersji V3 i opcjonalny autostart KDE

Po wizualnej weryfikacji V3 na zrzucie OWNER można zastąpić **tylko** plik `~/.config/conky/fenixsystem-kde.conf`, zachowując jego poprzednią wersję z datą. Stary autostart COSMIC `fenix-conky.desktop` pozostaje wyłączony; nie nadpisywać go, bo może tworzyć duplikaty. Nowy `fenixsystem-kde.desktop` został przygotowany w tym katalogu GitHub, ale w systemie OWNER jeszcze go nie instalowano.

Na komputerze potwierdzić, czy istnieją już wpisy `~/.config/autostart/fenix-conky.desktop` lub `~/.config/autostart/fenixsystem-kde.desktop`. Jeżeli pierwszy istnieje, najpierw przejrzeć jego cel i wyłączyć go świadomie, nie usuwać na ślepo. Używać nowego profilu dla KDE tylko gdy oba skrypty `~/.local/bin/fenix-sensors-kde.sh` i `~/.local/bin/fenix-network-kde.sh` działają (OWNER je przetestował).

Autostart KDE odczekuje 8 sekund i wywołuje `conky -c ~/.config/conky/fenixsystem-kde.conf`. W sesji Wayland nie ma autostart COSMIC; Night Color 5000 K pozostaje natywny KDE. Działania w GitHubie nie instalują zmian na komputerze OWNER.
