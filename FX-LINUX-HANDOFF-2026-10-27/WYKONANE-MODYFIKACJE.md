# Historia wykonanych i planowanych modyfikacji FX Linux

## GRUB — TESTED (2026-10-04)
Na Fedorze 44 COSMIC zadziałał prototyp `/boot/grub2/themes/fxos/`. Zachowano Fedora BLS, wpisy starszych jąder, rescue, Windows Boot Manager i UEFI Firmware Settings. Konfiguracja historyczna: `GRUB_THEME="/boot/grub2/themes/fxos/theme.txt"`, `GRUB_GFXMODE="1920x1080,1680x1050,auto"`. `grub2-script-check` wówczas przeszedł. Nadal otwarte: docelowe podświetlenie, pixmapy, nazwy wpisów odporne na aktualizacje, ikona UEFI i ponowne testy na matrycy wewnętrznej. **Nie edytować ręcznie generowanego grub.cfg**.

## Monitor i klapa — TESTED (2026-10-19)
W `~/.local/state/cosmic-comp/outputs.ron` zmodyfikowano profil HDMI tak, by zewnętrzny monitor był przy `(0,0)`, `enabled: true`, `xwayland_primary: true`, a eDP był wyłączony w profilu z zamkniętą klapą. `/etc/systemd/logind.conf.d/90-thinfedora-lid.conf` zawierał historyczne wartości zachowane w `konfiguracje-historyczne/`. Reboot na baterii, z klapą zamkniętą i monitorem HDMI-DVI: PASS. To **przykład historyczny**, nie odczyt dzisiejszego stanu. Nie importować COSMIC outputs.ron do KDE.

## Fenix Night Light — SOURCE 0.1 alpha
Zachowany kod, install/uninstall, testy, konfiguracja i timery systemd user. Aktualny backend COSMIC, nie KDE. Konfiguracja bieżącego użytkownika `~/.config/fenix-nightlight/config.ini` jest lokalna i może zawierać dane prywatne.

## FenixSystem Linux / Conky — LOKALNE, NIEPOTWIERDZONE
W historii rozmów występuje widget/monitor CPU, GPU, RAM, dysków, baterii, temperatur i sieci. Na kontrolowanych repozytoriach **nie potwierdzono kompletnego źródła i dotfiles Conky**. Dołożyć pliki ręcznie z Fedory.

## Optymalizacje Fedora COSMIC — NIEPEŁNE DANE
Znane są kierunki zasilania, usług i profilów, ale brak pełnego sprawdzonego zestawu lokalnych zmian w zram, swap, tuned, systemd, sysctl, sterownikach i skryptach. Zapisać wyłącznie to, co naprawdę jest zmienione na komputerze. Nie przedstawiać propozycji jako wykonanych zmian.

## Wygląd FX Linux KDE — PROJEKT
Priorytet P1: warstwa personalizacji Fedory KDE Plasma (później możliwe LMDE). Kierunek: dopracowany, wyrazisty pulpit, górny panel, dock, menu i monitoring. Brak gotowej odtwarzalnej konfiguracji KDE w źródłach, więc niczego takiego nie deklarujemy.

FX11 Builder Windows i FX NEXUS pozostają osobnymi projektami.
