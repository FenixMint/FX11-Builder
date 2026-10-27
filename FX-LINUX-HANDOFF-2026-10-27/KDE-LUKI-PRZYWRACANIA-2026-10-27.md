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
