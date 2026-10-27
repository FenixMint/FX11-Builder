# FX Linux / Fedora KDE — przywracanie funkcji przez adaptację, nie kopiowanie 1:1

Date: 2026-10-27  
Status: **OWNER ARCHITECTURAL DIRECTION / IMPLEMENTATION PENDING**

## OWNER statement

OWNER rozpoczyna przywracanie wcześniej zabezpieczonych ustawień na Fedora KDE i wyraźnie wskazuje, że na KDE filtr światła niebieskiego działa inaczej niż w COSMIC. Nie wykonujemy zero-jedynkowego odtwarzania starej konfiguracji.

**KONTRAKT: odtworzyć zamierzone zachowanie, nie przepisane w ciemno pliki z poprzedniego środowiska.**

## Dane źródłowe

OWNER zgłosił lokalne utworzenie `FX-Linux-Config-20261027-115021.tar.gz` (6,5M; 293 wpisy), SHA256: `bda592a6cc782c72a57282e9c4f81ebe222b613cbb8b9342c5ec8851e41b7e0b`.
Weryfikacja `tar -tzf` była pozytywna na źródłowej Fedorze. **Transfer archiwum na FX11 i jego stan na KDE nie zostały jeszcze w tej rozmowie zweryfikowane.** Archiwum jest prywatne, nie publikować go na GitHubie.

Istnieją także źródła Fenix Night Light 0.1 alpha (backend COSMIC), oryginalne źródła GRUB oraz historycznie testowane informacje o monitorze/zamykaniu klapy. Historyczne wartości to nie automatyczne polecenie ich zastosowania.

## Matryca wdrożenia

| Obszar | Strategia | Najpierw |
| --- | --- | --- |
| Nocne kolory / światło niebieskie | **NATYWNE KDE:** KWin/Plasma Night Color; Fenix Night Light 0.1 COSMIC nie instalować jako regulatora barw na KDE | Włączyć ręcznie Night Color w Ustawieniach systemowych, wybór harmonogramu i temperatury wg preferencji |
| Fenix Night Light | **PORT/PROJECT:** zasada prywatności, lokalizacja ręczna, cel 4500 K dzień / 4000 K noc / łagodne przejście jako źródłowe preferencje; nie twierdzić, że mechanizm KDE ma identyczne możliwości | Nie uruchamiać równoległego harmonogramu COSMIC |
| Conky / FenixSystem | **PORT + REVIEW:** zachować `conky.conf`, `fenix-sensors.sh`, `fenix-conky.desktop`; sprawdzić ścieżki, zależności, zachowanie na Wayland, sensory i uprawnienia | Odtworzyć do staging, przejrzeć i testowo uruchomić ręcznie, dopiero potem autostart |
| COSMIC monitors | **REPLACE WITH KDE KScreen:** `outputs.ron` wyłącznie jako dokumentacja historyczna | Skonfigurować ekran(y) w KDE, testować HDMI, zamkniętą klapę i zasilanie z akumulatora |
| Klapa / `systemd-logind` | **REVIEW BOTH STACKS:** historyczne `HandleLidSwitch*=...` to punkt odniesienia, a nie dowód potrzeby zmiany | Porównać bieżące PowerDevil/KDE i `logind`; zmieniać tylko rzeczywisty konflikt |
| TuneD / power | **RECONCILE:** historyczny `balanced-battery` nie musi być właściwy domyślnie w nowej konfiguracji | Sprawdzić `tuned-adm active`, `tuned-ppd` i profil GUI KDE; nie uruchamiać dwóch konkurujących menedżerów |
| zram | **VERIFY:** poprzednio 8 GiB, priorytet 100 | Sprawdzić `swapon --show`, bez wymuszania rozmiaru bez potrzeby |
| Modprobe `disable-webcam.conf` | **OWNER CHOICE / SECURITY REVIEW:** nie importować wszystkich plików `modprobe.d` | Sprawdzić cel blokady kamery i jej skutki; decyzja osobna |
| GRUB FX OS | **LATER & BOOT SAFE:** poprzedni motyw zachowany, ale nowa instalacja może używać innych ścieżek/układów | Najpierw zweryfikować boot, BLS, Windows Boot Manager, UEFI i plan rollback; dopiero potem motyw bez ręcznej edycji `grub.cfg` |
| Plasma visual | **NATIVE KDE:** panele, dock, menu, widgety, kolory, motywy | Budować profil odtwarzalny specyficznie dla KDE |

## Zasada kolejności

1. Przegląd wynikowego środowiska KDE i prywatnego archiwum **tylko do odczytu**; zweryfikować SHA256 archiwum po przeniesieniu.
2. Wyodrębnić pliki archiwum do nowego katalogu staging, **nie** bezpośrednio na `/`, `/etc`, `/boot` ani w istniejący katalog domowy. Nie uruchamiać skryptów z archiwum bez ich obejrzenia.
3. Natywne Night Color KDE można skonfigurować osobno przez GUI. Użytkownik wybiera harmonogram, ręczną lokalizację lub godziny; nie włączać automatycznego pobierania lokalizacji bez zgody.
4. Przejrzeć pojedynczo Conky/skrypt czujników, zależności i autostart; przetestować manualnie, nie włączać w ciemno.
5. Ocenić monitory, lid, zasilanie, TuneD i zram wg obecnego zachowania; dopiero uzasadnione ustawienia systemowe z rollback.
6. GRUB/boot i blokadę kamery pozostawić na później. Niczego nie zmieniać w EFI/Windows bez osobnej weryfikacji i zgody.

## Read-only baseline commands (adapt to actual KDE installation)

```bash
printf 'Desktop=%s Session=%s\n' "$XDG_CURRENT_DESKTOP" "$XDG_SESSION_TYPE"
plasmashell --version 2>/dev/null || true
cat /etc/fedora-release
command -v conky || true
command -v tuned-adm && tuned-adm active || true
swapon --show
rpm -q conky tuned tuned-ppd power-profiles-daemon 2>/dev/null || true
```

Nie wykonywać `sudo tar -xzf ... -C /`. Nie nadpisywać istniejących plików `~/.config` bez rozpoznania konfliktów.

## Sources of KDE behavior, distinct from project history

- KDE System Settings docs, Night Color under Display and Monitor: https://docs.kde.org/trunk_kf6/en/systemsettings/systemsettings/general.html
- KDE UserBase, Night Color manual location/custom schedule/temperature: https://userbase.kde.org/Tips/How_to_customize_Night_Color_on_KDE_Plasma
- Fedora `tuned-ppd` integration design: https://fedoraproject.org/wiki/Changes/TunedAsTheDefaultPowerProfileManagementDaemon

**No actual restoration performed on OWNER's KDE by this documentation.**
