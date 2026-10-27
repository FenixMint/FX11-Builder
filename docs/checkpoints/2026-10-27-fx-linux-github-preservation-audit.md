# FX Linux — audit zachowania konfiguracji i optymalizacji na GitHubie

Data: **2026-10-27**  
Status: **READ-ONLY REMOTE AUDIT / DOCUMENTED CHECKPOINT**  
Priorytet: **P1 FX Linux** (według OWNER: [2026-10-21](../decisions/2026-10-21-FX-LINUX-FIRST-PORTFOLIO-PRIORITY.md))

## Cel i granice weryfikacji

OWNER poprosił o sprawdzenie, czy historyczne materiały służące optymalizacji Linuksa i customizacji wyglądu są zachowane na GitHubie. Audyt dotyczy **stanu zdalnych repozytoriów i ich gałęzi**, nie działającego systemu operacyjnego.

Sprawdzono listę repozytoriów dostępnych połączonemu kontu GitHub, zdalne drzewa plików oraz istotne pliki i checkpointy:

- `FenixMint/FX11-Builder` / `main` — drzewo przy audycie: `ed61d3ad8af314ea867b6b17ea0bf19cec57168f`;
- `FenixMint/FX11-Builder` / `prototype/fx-linux-grub-theme` — drzewo: `1d04ac8127874dfc4bdbe6c5ad9be3a980ae4ee7`;
- `FenixMint/FX11-Builder` / `prototype/fxos-grub-theme` — drzewo: `07ced4fcc46e1d97c9d37c169d929562788ed2b5`;
- `FenixMint/fenix-nightlight` / `main` — drzewo: `9ff669e8a55fa0cd302680bcdf42d346e73f006e`;
- `FenixMint/FenixMint-FX11-legacy` / `main` — drzewo: `6c65e29ee41bf4d251b276f8be706599ab1fbc29` (głównie historia Windows, nie źródła linuksowego Conky).

W dostępnej liście repozytoriów `FenixMint` **nie było dedykowanego `FX-Linux`**. To nie dowodzi braku lokalnych plików, nieprzesłanych commitów, innych kont czy prywatnych źródeł poza dostępną instalacją konektora.

Nie było dostępu do lokalnych konfiguracji Fedory, wyników `systemctl`, kopii `~/.config` ani uruchomionych na maszynie procesów. Nie wykonywano instalacji, testów ani operacji zmieniających konfigurację.

## Stan potwierdzony

| Obszar | Stan zdalny | Co potwierdzono / ograniczenie |
| --- | --- | --- |
| Motyw **FX OS GRUB** | **SOURCE + DOCUMENTATION / PROTOTYPE BRANCH** | Działający szkic `theme.txt` na `prototype/fx-linux-grub-theme`. [README](https://github.com/FenixMint/FX11-Builder/blob/prototype/fx-linux-grub-theme/prototypes/fx-linux-grub/README.md), [theme.txt](https://github.com/FenixMint/FX11-Builder/blob/prototype/fx-linux-grub-theme/prototypes/fx-linux-grub/theme.txt). Nie na `main`. |
| GRUB — test sprzętowy | **HISTORICALLY TESTED / DOCUMENTED** | [Checkpoint 2026-10-04](https://github.com/FenixMint/FX11-Builder/blob/prototype/fx-linux-grub-theme/prototypes/fx-linux-grub/CHECKPOINT-2026-10-04.md): motyw wystartował, wpisy Fedory BLS, starsze kernele, rescue, Windows i UEFI zachowane. Nie oznacza to końcowego ukończenia motywu. |
| Źródła ikon GRUB | **EDITABLE SVG / OTHER PROTOTYPE BRANCH** | `experiments/fxos-grub/icons-src/{fedora,windows,firmware,os}.svg` na `prototype/fxos-grub-theme`. [README źródeł](https://github.com/FenixMint/FX11-Builder/blob/prototype/fxos-grub-theme/experiments/fxos-grub/icons-src/README.md). |
| Grafiki tła, gotowe PNG i fonty PF2 GRUB | **NOT FOUND IN INSPECTED REMOTE TREES** | [ASSETS.md](https://github.com/FenixMint/FX11-Builder/blob/prototype/fx-linux-grub-theme/prototypes/fx-linux-grub/ASSETS.md) dokumentuje pliki i hashe SHA-256, ale wskazuje, że binaria zostały lokalnie. Konieczne odzyskanie i weryfikacja z maszyny, nie regenerowanie na ślepo. |
| Obsługa ekranu zewnętrznego / klapy / uśpienia | **HISTORICALLY TESTED / DOCUMENTED SETTINGS** | [Checkpoint 2026-10-19](https://github.com/FenixMint/FX11-Builder/blob/prototype/fx-linux-grub-theme/prototypes/fx-linux-grub/CHECKPOINT-2026-10-19-DISPLAY-LID.md): opis kopii i korekty `outputs.ron`, drop-in `systemd-logind`, test HDMI, baterii i zamkniętej klapy. **Brak automatycznego, przenośnego instalatora tych ustawień w sprawdzonym drzewie.** |
| **Fenix Night Light** | **SOURCE + INSTALL/UNINSTALL + TESTS** | [Repo](https://github.com/FenixMint/fenix-nightlight): `src/`, `install.sh`, `uninstall.sh`, timery `systemd --user`, testy; deklarowany status **0.1 alpha**. |
| Fenix Night Light na KDE Plasma | **PLANNED / NOT FOUND IN CURRENT SOURCE** | Obecny zaimplementowany backend to `src/fenix_nightlight/backends/cosmic.py`. Nie znaleziono backendu KDE/KWin. |
| FX Linux — koncepcja profili, FX Base i konfiguracji dystrybucji | **DOCUMENTED DIRECTION + SOME LIVE/INSTALLER CODE** | [Profile i edycje](2026-09-14-fx-linux-profiles-vs-editions.md), [FX Base readiness](2026-09-15-fx-base-build-readiness.md), `scripts/build-fx-live-poc.sh`, `live-overlay/`. To starsza linia live/installera i nie jest równoważne obecnemu instalowalnemu profilowi Fedora KDE. |
| **FenixSystem Linux / Conky** | **NOT FOUND AS COMPLETE SOURCE/CONFIGURATION** | Nie stwierdzono zdalnego repozytorium z pełnym plikiem Conky, skryptami pobierania metryk i odtwarzalną konfiguracją pulpitu FX Linux. W `FX11 Legacy` jest dokumentacja Fenix System **Windows**, ale nie jest to program Conky dla Linuksa. |
| **Optymalizacja Fedora COSMIC** (CPU/RAM/dysk/zram/usługi/zasilanie) | **NOT FOUND AS COMPLETE PROFILE** | Nie znaleziono kompletnego, przetestowanego, wersjonowanego zestawu ustawień Fedory i skryptu ich zastosowania/rollback. Pojedynczy checkpoint ekranu i `logind` nie zastępuje profilu optymalizacyjnego. |
| **FX Linux KDE Plasma Visual** | **DECISION / CONCEPT; REPRODUCIBLE CONFIG NOT FOUND** | [Priorytet P1](../decisions/2026-10-21-FX-LINUX-FIRST-PORTFOLIO-PRIORITY.md) i opis założeń zachowane; brak zestawu `plasmashell`/KWin, układu paneli, widgetów, kolorów, ikon, menu i skryptu wdrożenia zgodnego z projektem OWNER. |
| Gotowy obraz makiety pulpitu FX OS z rozmowy | **NOT CONFIRMED ON GITHUB** | Makieta pokazana w rozmowie nie występuje jako widoczny, wersjonowany plik w sprawdzonych drzewach. Nie wnioskuj, że lokalny oryginał został utracony. |

## Istotny kontekst historyczny

Dokumenty z września opisywały także dalekosiężną ideę `FX Base` / LMDE/Cinnamon / Live/Calamares i profilów. **Nie usuwamy tej historii.** Wiążący, późniejszy kierunek OWNER z października nadaje pierwszeństwo **modułowym modyfikacjom istniejącej Fedory KDE** i późniejszej możliwości adaptacji na LMDE, a **nie** utrzymywaniu od razu własnej dystrybucji.

Motyw GRUB jest rozdzielony na **dwie odrębne gałęzie prototypowe**, z plikami źródłowymi nieobecnymi w `main`. Nie scalać automatycznie ani nie zastępować historycznego prototypu bez zatwierdzonego planu.

## Luki do zamknięcia przed bezpiecznym odtworzeniem FX Linux

1. **Read-only lokalny inwentarz na źródłowym komputerze Fedora/COSMIC**: ustalić aktualne pliki Conky, autostart i skrypty sensorów; dotychczasowe modyfikacje usług, ustawienia zasilania, procesora, zram, grafiki, dysku, aktualizacji oraz różnice od pakietów bazowych. Nie zakładać, że coś z historycznej rozmowy nadal obowiązuje.
2. **Odzyskanie GRUB assets** na podstawie nazw i SHA-256 z `ASSETS.md`, z zachowaniem dotychczasowego GRUB/BLS i rollback Breeze. Nie publikować binarnych grafik zanim źródło, uprawnienia i zgodność nie zostaną sprawdzone.
3. **Zachowanie makiety oraz identyfikacji wizualnej FX OS** jako materiału projektowego. Tworzyć odrębny od GRUB manifest wyglądu KDE Plasma, bez wrzucania prywatnych ustawień sesji na GitHub.
4. **Przenośny profil FX Linux dla Fedora KDE**: repozytorium/dotfiles, jawne zależności, dry-run, zastosowanie, weryfikacja, rollback, dokumentacja wersji Fedory/KDE. LMDE otrzyma odrębny adapter dopiero po sprawdzeniu zgodności.
5. **Fenix Night Light**: osobno zaprojektować/zweryfikować backend zgodny z KDE Plasma/Wayland; obecny COSMIC helper nie zapewnia tej funkcji na KDE.
6. **Sformalizować źródła monitoringu** (Conky/FenixSystem), projekt paneli, menu i widgetów z zachowaniem możliwości ręcznej zmiany przez użytkownika.

**Bezpieczny następny krok:** lokalny, nieinwazyjny odczyt stanu i kopia źródeł na komputerze bazowym; potem oddzielne, kontrolowane zapisanie wyłącznie przejrzanych i pozbawionych danych prywatnych konfiguracji do GitHub. Nie wykonywać bez kopii ani bez osobnego planu zmian usług, dysków, UEFI lub bootloadera.

## Wynik

**Częściowo zabezpieczone**: istnieją źródła/ustalenia GRUB, działający kod Fenix Night Light, szczegółowy checkpoint konfiguracji ekranu/klapy i architektura FX Linux. **Niepotwierdzone na GitHubie**: kompletne optymalizacje Linuksa, gotowy Conky/FenixSystem Linux, odtwarzalna konfiguracja KDE i finalne graficzne binaria GRUB.

Ten dokument utrwala **ustalenia audytu**, bez modyfikowania istniejących modułów. Poza utworzeniem samego checkpointu na GitHubie żadnych zmian kodu ani działań na systemach nie wykonywano.

## Update 2026-10-27 — przygotowano narzędzie backupu przed Fedora KDE

**SOURCE TOOL PREPARED / LOCAL BACKUP NOT EXECUTED.** OWNER zdecydował o zabezpieczeniu konfiguracji przed reinstalacją środowiska z COSMIC na KDE. Powstała odrębna gałąź robocza `work/fx-linux-pre-kde-preservation-2026-10-27` z nieinwazyjnym skryptem do wykonania prywatnej kopii na zewnętrznym nośniku:

- [fx-linux-preserve.sh](https://github.com/FenixMint/FX11-Builder/blob/work/fx-linux-pre-kde-preservation-2026-10-27/tools/fx-linux-preserve/fx-linux-preserve.sh)
- [Instrukcja i bramki bezpieczeństwa](https://github.com/FenixMint/FX11-Builder/blob/work/fx-linux-pre-kde-preservation-2026-10-27/tools/fx-linux-preserve/README.md)

Skrypt przechodzi `bash -n`, syntetyczny dry-run, lokalny test archiwizacji i kontrolę `sha256sum --check` w oddzielonym środowisku Linux, **ale nie był uruchomiony na ThinkPadzie OWNER**. Nie mamy jeszcze rzeczywistych archiwów ani potwierdzonego wyniku odczytu `/boot/grub2/themes/fxos`, lokalnego Conky czy plików graficznych. Fizycznie oddzielny nośnik oraz osobna pełna kopia danych osobistych pozostają warunkami przed reinstalacją. Prywatnych dumpów nie wysyłać do publicznego GitHub. Dokumentacja tego procesu nie stanowi zgody na formatowanie partycji Windows/ESP lub innych dysków.

## OWNER correction — 2026-10-27: only selected FX Linux settings on FX11 partition

**OWNER DECISION — supersedes the destination/scope instructions of the immediately preceding backup-tool update, not the historical audit:**

> Nie kopiujemy systemu. Zabezpieczamy ustawienia. Konkretne konfiguracje trafią na partycję FX11. Bez rozbudowanego szyfrowania.

Implementation update in temporary branch `work/fx-linux-pre-kde-preservation-2026-10-27`:
- Config-only allowlist, no image, no complete home, no broad system archive. Preserve FX Linux Conky/FenixSystem, GRUB visuals, COSMIC display config, Fenix Night Light, relevant KDE/GTK visuals, logind and tuning config, simple package/service diagnostic lists.
- OWNER-chosen target: a separate folder on mounted, writable **FX11 partition**, including when on same physical disk as Fedora. No requirement for an external disk, BitLocker, archive encryption, or a full-system image.
- No system mutation or installation; operation writes only the selected archive folder on FX11.
- Explicit safety condition: FX11 Windows/NTFS partition and boot entries **must not be formatted** during Fedora KDE installation. If Windows NTFS is hibernated, unclean or mounted read-only, do not force write access.
- Local config tar files remain private; GitHub retains only public tooling / non-private documentation.

Source: [skrypt](https://github.com/FenixMint/FX11-Builder/blob/work/fx-linux-pre-kde-preservation-2026-10-27/tools/fx-linux-preserve/fx-linux-preserve.sh) and [current instructions](https://github.com/FenixMint/FX11-Builder/blob/work/fx-linux-pre-kde-preservation-2026-10-27/tools/fx-linux-preserve/README.md).

**Test**: source file Git blob SHA `f076672f538d9c97dc4745503c5f2bdaa0b26794` verified against local copy; `bash -n`, synthetic `--dry-run`, synthetic `--capture` to separately mounted Linux tmpfs, and `--verify` SHA-256 passed as non-root user. NOT tested on actual FX11 NTFS, NOT run on ThinkPad, and no real settings capture yet verified.
