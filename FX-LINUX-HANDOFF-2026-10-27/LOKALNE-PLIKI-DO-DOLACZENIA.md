# Lokalna lista ręcznego przeniesienia — tylko własne ustawienia

OWNER skopiuje potrzebne pliki na partycję **FX11** (np. do prywatnego folderu `FX-Linux-Config/LOKALNE-Z-FEDORY/`). Bez skryptów kopiujących, dumpów systemu i rozbudowanego backupu. Zawsze używać rzeczywistych ścieżek, które istnieją.

- [ ] **Conky / FenixSystem:** `~/.config/conky/`, `~/.conkyrc`, ewentualne własne skrypty sensorów, autostart `~/.config/autostart/`.
- [ ] **GRUB:** `/boot/grub2/themes/fxos/` wraz z `background.png`, ikonami PNG, pixmapami i fontami PF2; `/etc/default/grub`, ewentualny `/etc/default/grub.fxos-backup`.
- [ ] **Monitor i klapa:** `~/.local/state/cosmic-comp/outputs.ron` oraz kopia; rzeczywisty `/etc/systemd/logind.conf.d/90-thinfedora-lid.conf`.
- [ ] **Fenix Night Light:** `~/.config/fenix-nightlight/config.ini` i własne niezacommitowane modyfikacje kodu.
- [ ] **Optymalizacje:** tylko ręcznie zmieniane konfiguracje np. `/etc/tuned/`, `/etc/sysctl.d/`, `/etc/modprobe.d/`, `/etc/udev/rules.d/`, `~/.config/systemd/user/`. Zapis *co* było zmienione i *dlaczego*.
- [ ] **Wygląd:** własne tapety, oryginalne makiety FX OS, grafiki, motywy, ikony, wybrane ustawienia GTK/KDE i autorskie skrypty.
- [ ] **Dokumentacja:** zrzuty ekranu działającego Conky, GRUB i pulpitu, notatki o błędach, zależnościach, ustawieniach energooszczędności.

Pliki COSMIC po instalacji KDE służą do analizy, **nie** do automatycznego odtwarzania. Nie publikować ich w publicznych repozytoriach. Brak wymogu kopiowania `/home`, danych osobistych, profili przeglądarek i Windows.
