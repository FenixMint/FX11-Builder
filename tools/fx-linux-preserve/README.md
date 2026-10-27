# FX Linux — zachowanie ustawień przed przejściem z COSMIC na Fedora KDE

**OWNER CORRECTION — 2026-10-27.** Wcześniejszy pomysł kopii na zewnętrzny, szyfrowany nośnik i szerokich archiwów był zbyt rozbudowany. Priorytetem jest zachowanie **konkretnych konfiguracji FX Linux**, nie obrazu systemu ani całego katalogu domowego.

**Miejsce docelowe: wskazany folder na zamontowanej partycji FX11 (Windows).** Partycja FX11 może być na tym samym dysku fizycznym co Fedora. Nie wymagamy dodatkowego szyfrowania, osobnego urządzenia ani dużego archiwum systemowego.

## Co obejmujemy

- **Conky / FenixSystem Linux:** wykryte pliki konfiguracji i autostartu.
- **FX OS GRUB:** motyw `/boot/grub2/themes/fxos`, jeśli czytelny, oraz pliki `/etc/default/grub`, ustawienia BLS i opis potencjalnych źródeł lokalnych.
- **Monitory i klapa:** `~/.local/state/cosmic-comp/outputs.ron`, `/etc/systemd/logind.conf[.d]`.
- **Fenix Night Light:** ustawienia i lokalne pliki programu.
- **Wygląd:** wybrane motywy, ikony, tapety, pliki KDE/GTK i ustawienia COSMIC będące punktem odniesienia dla KDE.
- **Optymalizacje:** jawne pliki `tuned`, `sysctl.d`, `modprobe.d`, `udev/rules.d`, `dracut.conf.d`, informacyjne listy pakietów RPM/Flatpak, włączonych usług, zram/swap i aktywnego profilu zasilania.

Skrypt świadomie **nie obejmuje** Windowsa, całego Linuksa, `/home`, `/etc`, prywatnych dokumentów, poczty, profili przeglądarek, kluczy SSH ani danych użytkownika.

### Sposób pracy

1. Pod Fedorą zamontować istniejącą **partycję FX11 w trybie odczytu/zapisu**. Sprawdzić `lsblk -f` oraz `findmnt`; nie mylić Windows NTFS z partycją Linuksa czy EFI. Jeżeli Windows jest zahibernowany albo system plików NTFS jest tylko do odczytu, **nie wymuszać montowania RW** — najpierw rozwiązać przyczynę normalnymi metodami.
2. Utworzyć **jednorazowo osobny folder**, np. `/run/media/$USER/FX11/FX-Linux-Config` (ścieżka orientacyjna: użyć rzeczywistego punktu montowania).
3. Z katalogu zawierającego pobrany skrypt uruchomić jako zwykły użytkownik, bez `sudo`:

```bash
lsblk -f
findmnt
bash fx-linux-preserve.sh --dry-run "/run/media/$USER/FX11/FX-Linux-Config"
bash fx-linux-preserve.sh --capture "/run/media/$USER/FX11/FX-Linux-Config"
```

4. Skrypt tworzy niewielki folder `FX-LINUX-PRE-KDE-<data>-<pid>`, do którego trafiają **wyłącznie wybrane pliki konfiguracyjne** `user-config.tar.gz` i `system-config-readable.tar.gz`, proste raporty `reports/` oraz `SHA256SUMS`.
5. Sprawdzić integralność na tej samej partycji (najlepiej po ponownym zamontowaniu):

```bash
bash fx-linux-preserve.sh --verify "/run/media/$USER/FX11/FX-Linux-Config/FX-LINUX-PRE-KDE-.../SHA256SUMS"
```

### Granice bezpieczeństwa

- **Partycja FX11 musi pozostać nienaruszona podczas instalacji Fedory KDE.** Nie wybierać jej do formatowania ani instalacji. Zachowujemy Windows Boot Manager i istniejący rozruch.
- Sam fakt zapisania konfiguracji na FX11 **nie zabezpieczy ich przed błędnym skasowaniem tego samego dysku**; weryfikacja partycji przy instalacji pozostaje wymagana.
- Skrypt nie modyfikuje systemu, `grub.cfg`, pakietów, usług, ESP ani dysków. Nie instaluje szyfrowania.
- W archiwach mogą występować dane lokalne lub ustawienia, których nie należy publikować; **nie wysyłać ich na GitHub**. W repozytorium zachowujemy wyłącznie skrypt i ogólne wnioski.
- Archiwizacja plików wymagających roota może się nie udać; skrypt zapisze błędy. Nie uruchamiać całego skryptu jako root. Braki sprawdzić ręcznie przed reinstalacją.
- Konfiguracji COSMIC nie odtwarzać na KDE automatycznie. To materiał do adaptacji i dokumentacja wcześniejszych testów.

## Kontrola zakresu

To backup **wybranych ustawień FX**, a nie gwarancja zachowania danych osobistych. Jeżeli jakieś konkretne źródła Conky, skrypty lub grafiki leżą poza listą, wynik `reports/possible-extra-files.txt` służy do ich odnalezienia. Trzeba je skopiować osobno świadomie (bez plików prywatnych przypadkowo zawartych w katalogach).

W szczególności grafiki GRUB, czcionki PF2 i źródła Conky trzeba potwierdzić w archiwum. Ich historyczne SHA-256 są opisane w `prototypes/fx-linux-grub/ASSETS.md` na gałęzi `prototype/fx-linux-grub-theme`.

## Status wykonania

**SOURCE PREPARED / NOT RUN ON THINKPAD / NO CAPTURE VERIFIED.** Zmodyfikowano skrypt i dokumentację według aktualnego OWNER. Nie ma jeszcze potwierdzenia, że konfiguracje zostały skopiowane na FX11. Każda kontrola (np. wykonanie skryptu, test kontrolny) powinna być raportowana wyłącznie jeśli faktycznie nastąpiła.

To narzędzie znajduje się tymczasowo na gałęzi `work/fx-linux-pre-kde-preservation-2026-10-27` w repozytorium FX11 Builder i nie oznacza automatycznej integracji FX Linux z FX11.

Powiązane: [audyt zachowania FX Linux](https://github.com/FenixMint/FX11-Builder/blob/main/docs/checkpoints/2026-10-27-fx-linux-github-preservation-audit.md).
