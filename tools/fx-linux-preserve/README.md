# FX Linux — zabezpieczenie konfiguracji przed reinstalacją Fedora KDE

**Status: SOURCE TOOL / TESTED IN ISOLATED LINUX ENVIRONMENT / NOT EXECUTED ON OWNER'S THINKPAD**

Projekt FX Linux jest priorytetem P1. Ta gałąź zachowuje narzędzie przed migracją z Fedory COSMIC na Fedorę KDE Plasma. Nie jest przeznaczona do automatycznego scalenia z FX11 Builder `main`.

## Co robi skrypt

`fx-linux-preserve.sh` kopiuje **wyłącznie wskazane konfiguracje**, m.in.:
- Conky / ewentualny FenixSystem Linux i uruchamianie użytkownika;
- konfiguracje COSMIC i stan monitorów;
- Fenix Night Light;
- wybrane katalogi ikon, motywów, KDE/GTK i czcionek;
- dostępne do odczytu ustawienia `systemd`, `logind`, GRUB FX OS, BLS, `dnf`, `modprobe`, `sysctl`, `udev`, `fstab`;
- raporty pakietów `rpm`, Flatpak, usług, zram, swap, profili zasilania, montowania dysków.

Ponadto wypisuje możliwe pliki Conky/FX/Fenix poza typowymi lokalizacjami. **Lista nie jest gwarancją kompletności — trzeba ją obejrzeć ręcznie.**

**Nie wykonuje żadnych zmian w konfiguracji źródłowej, pakietach, GRUB, partycjach ani usługach. Nie używa `sudo`.**

## Krok 0 — wymagane warunki bezpieczeństwa

1. Podłączyć **fizycznie osobny, zaufany i najlepiej zaszyfrowany dysk**. Sprawdzić `lsblk -f` i rozpoznać dysk/partycję. Skrypt odrzuci zapis na tym samym *systemie plików*, ale nie potrafi dowieść, że to inny *dysk fizyczny*. Osobna partycja tego samego SSD nie wystarczy.
2. Wykonać **osobną pełną kopię danych osobistych** (dokumenty, przeglądarki, hasła/profil, poczta, projekty, SSH, zdjęcia, dyski VM itp.). Ten skrypt nie kopiuje całego `$HOME`.
3. Zidentyfikować obecny schemat partycji, ESP/UEFI oraz partycje Windows/FX11. **Nie formatować Windows/ESP bez osobnego, zweryfikowanego planu instalatora.**
4. Kopie zawierają potencjalnie prywatne adresy/identyfikatory, lokalizację i klucze w plikach konfiguracyjnych. **Nigdy nie publikować tar.gz, raportów lub dumpów w GitHubie.** W repozytorium publikujemy wyłącznie przejrzany skrypt i dokumentację.

## Użycie na Fedorze COSMIC

Uruchomić jako zwykły użytkownik (bez sudo). Przykładowa ścieżka `/run/media/$USER/MOJ_DYSK` jest **przykładem**, nie ustaloną lokalizacją.

```bash
lsblk -f
bash fx-linux-preserve.sh --dry-run "/run/media/$USER/MOJ_DYSK"
bash fx-linux-preserve.sh --capture "/run/media/$USER/MOJ_DYSK"
```

Skrypt tworzy nowy katalog `FX-LINUX-PRE-KDE-YYYYMMDDThhmmssZ-PID` z:
- `user-config.tar.gz` (gdy wykryto pasujące pliki użytkownika),
- `system-config-readable.tar.gz` (gdy wykryto czytelne pliki systemowe),
- `reports/`, w tym podsumowanie, błędy tar i nazwy możliwych dodatkowych plików,
- `SHA256SUMS` i `verification-result.txt`.

Z zewnętrznego dysku sprawdzić integralność:

```bash
bash fx-linux-preserve.sh --verify "/run/media/$USER/MOJ_DYSK/FX-LINUX-PRE-KDE-.../SHA256SUMS"
```

Jeżeli brak uprawnień do części `/boot` albo `/etc`, archiwum systemowe może być niekompletne. Skrypt zwróci błąd i zapisze szczegóły. **Nie ignorować `tar errors` i nie reinstalować systemu przed uzupełnieniem braków.** Ewentualne pliki wymagające uprawnień administratora należy zabezpieczyć osobną, świadomą operacją tylko do odczytu; nie uruchamiać całego skryptu jako root.

## Po zrobieniu kopii

- Odczytać `reports/SUMMARY.txt`, `reports/possible-extra-files.txt`, błędy i listę plików wewnątrz tar (`tar -tzf`).
- Zweryfikować SHA256 z backupu, najlepiej po ponownym podłączeniu nośnika.
- Sprawdzić, czy archiwum zawiera prawdziwe pliki GRUB FX OS, Konfigurację Conky i `logind`, a nie wyłącznie raporty. Jeśli czegoś brakuje, znaleźć źródło i dołożyć do odrębnego prywatnego backupu.
- Zabezpieczyć także **nieopublikowane grafiki GRUB PNG/PF2** — porównać z hashami w `prototypes/fx-linux-grub/ASSETS.md` na gałęzi `prototype/fx-linux-grub-theme`.
- Nie przenosić plików COSMIC wprost do KDE: traktować je jako dokumentację i źródło do adaptacji.
- Zachować możliwość powrotu do działającego GRUB/BLS/Windows i nie usuwać ręcznie wpisów EFI.

## Testy / status

Autor narzędzia zweryfikował lokalnie w izolowanym linuksowym środowisku:
- `bash -n`: OK;
- `--dry-run` jako użytkownik bez uprawnień administratora: OK;
- `--capture` na oddzielnym zamontowanym filesystemie testowym: OK;
- `--verify` dla wygenerowanych sum kontrolnych: OK.

**To nie jest test na ThinkPadzie OWNER**. Nie mamy dostępu do jego dysku i nie potwierdzamy wykonania kopii, dopóki właściciel nie uruchomi narzędzia i nie sprawdzi wyników.

## Miejsce w architekturze

Tymczasowa gałąź robocza `work/fx-linux-pre-kde-preservation-2026-10-27` w `FenixMint/FX11-Builder`. Po uzgodnieniu docelowej struktury repozytoriów narzędzie należy przenieść do FX Linux, ale **bez usuwania historycznych checkpointów**.

Zobacz [audyt zachowania na GitHub 2026-10-27](https://github.com/FenixMint/FX11-Builder/blob/main/docs/checkpoints/2026-10-27-fx-linux-github-preservation-audit.md) oraz [aktywny priorytet FX Linux](https://github.com/FenixMint/FX11-Builder/blob/main/docs/decisions/2026-10-21-FX-LINUX-FIRST-PORTFOLIO-PRIORITY.md).
