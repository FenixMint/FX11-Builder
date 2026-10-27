# FX Linux — Fedora KDE: odczyt stanu po instalacji i preferencje OWNER

Date: 2026-10-27  
Status: **OWNER-REPORTED CURRENT KDE BASELINE / CONFIGURATION ADAPTATION NOT YET EXECUTED BY ASSISTANT**

## Zweryfikowane przez OWNER w terminalu

- Distro: **Fedora release 44 (Forty Four)**.
- `XDG_CURRENT_DESKTOP=KDE`, `XDG_SESSION_TYPE=wayland`.
- `plasmashell 6.7.5`.
- `conky`: **pakiet nie jest zainstalowany**.
- `lm_sensors-3.6.0-24.fc44.x86_64`: zainstalowany.
- `tuned-2.28.0-1.fc44.noarch`: zainstalowany.
- `tuned-ppd-2.28.0-1.fc44.noarch`: zainstalowany.
- `power-profiles-daemon`: **pakiet nie jest zainstalowany**.
- `tuned-adm active`: **Current active profile: balanced**.
- `swapon --show`: `/dev/zram0`, partition, **8 GiB**, in use **344 MiB** during report, priority **100**.

### Night Color — NOWA DECYZJA OWNER

OWNER: "**ustawiłem 5000K bo na kde ta temperatura lepsza**".

**Wiążące dla aktualnej instalacji Fedora KDE: Night Color 5000 K**, ustawione ręcznie w natywnych ustawieniach KDE i preferowane wizualnie przez OWNER. Nie przywracać automatycznie starego celu 4000 K z COSMIC/Fenix Night Light. Parametry harmonogramu **nie zostały podane**, nie zgadywać. Fenix Night Light v0.1 alpha ma wyłącznie backend COSMIC — nie uruchamiać go równolegle do KDE Night Color.

## Porównanie z poprzednim systemem COSMIC

| Obszar | Historyczna Fedora COSMIC | Nowa Fedora KDE | Decyzja |
| --- | --- | --- | --- |
| Filtr barwy | wcześniejsze cele projektu 4500/4000 K | **5000 K**, OWNER już wybrał | **zachować aktualne KDE 5000 K** |
| FenixSystem | Conky i `fenix-sensors.sh` na starej instalacji | Conky brak, `lm_sensors` jest | zainstalować `conky` z Fedory; najpierw analiza istniejących dotfiles; autostart na koniec |
| TuneD | `balanced-battery` | `balanced`, `tuned` i `tuned-ppd` | nie wymuszać profilu historycznego bez oceny, unikać konfliktów z drugim menedżerem |
| ZRAM | 8 GiB, priorytet 100 | 8 GiB, priorytet 100 | nie zmieniać bez potrzeby |
| Inne | `outputs.ron`, `logind`, FX GRUB | bieżącej konfiguracji po instalacji nie sprawdzono | ocenić osobno po ustabilizowaniu KDE |

## Conky — uwagi kompatybilności

Pakiet `conky` istnieje w oficjalnym repozytorium Fedora 44 (w czasie sprawdzenia portal Fedora Packages podawał `1.22.2-3.fc44`). Źródło: https://packages.fedoraproject.org/pkgs/conky/conky/ .

Conky pod Wayland/KWin może wymagać odmiennego ustawienia okna/rysowania (natywne Wayland vs XWayland); nie zakładać, że stare `conky.conf` z COSMIC działa natychmiast. Źródła: https://conky.cc/config_settings , https://discuss.cachyos.org/t/conky-on-kde-plasma-wayland/35498 . Zewnętrzne uwagi nie są testem w instalacji OWNER.

## Bezpieczny następny etap

1. OWNER wskazuje archiwum `FX-Linux-Config-20261027-115021.tar.gz` na swoim systemie; zweryfikować SHA-256 `bda592a6cc782c72a57282e9c4f81ebe222b613cbb8b9342c5ec8851e41b7e0b`. Nadal nie ma w rozmowie potwierdzenia, czy został przeniesiony na FX11.
2. Archiwum czytać/rozpakować **do osobnego katalogu roboczego**, nie do `/`, `/etc`, `/boot` ani istniejącego `~/.config`. Nie kopiować na ślepo plików COSMIC.
3. W pierwszej kolejności obejrzeć oryginalne: `conky.conf`, `fenix-sensors.sh`, `fenix-conky.desktop`. Sprawdzić odwołania do starych ścieżek, dostępność czujników, zależności i ustawienia X11/Wayland.
4. Za zgodą OWNER można zainstalować `conky` z oficjalnego repo Fedory przez DNF; skonfigurować i uruchomić ręcznie, dopiero po teście włączyć autostart.
5. Pozostałe optymalizacje, blokadę kamery i motyw GRUB ocenić oddzielnie; nie zmieniać rozruchu ani partycji Windows/FX11 bez osobnej weryfikacji.

**Ten dokument utrwala informacje otrzymane od OWNER. Nie instaluje pakietów ani nie zmienia bieżącego KDE.**

## Owner check — archive verified and FenixSystem staging extracted

OWNER ran `sha256sum -c -` on `~/Pobrane/FX-Linux-Config-20261027-115021.tar.gz` under Fedora KDE, obtaining `DOBRZE` (PASS) against historical checksum `bda592a6cc782c72a57282e9c4f81ebe222b613cbb8b9342c5ec8851e41b7e0b`.

OWNER then extracted this archive into `~/FX-Linux-Odzysk` (separate staging folder). `find` confirmed the following recovered files:

- `~/FX-Linux-Odzysk/home/<local-user>/.config/conky/conky.conf`
- `~/FX-Linux-Odzysk/home/<local-user>/.local/bin/fenix-sensors.sh`
- `~/FX-Linux-Odzysk/home/<local-user>/.config/autostart/fenix-conky.desktop`

**Confirmed:** correct archive and FenixSystem source files exist on Fedora KDE in staging. **Not yet done:** inspect actual contents, install Conky, test sensors and XWayland window behavior, activate autostart, restore any config into live `~/.config`. Do not automatically import COSMIC configs. Keep KDE native Night Color at OWNER-preferred 5000 K.

Next: inspect three source files as read-only text (after OWNER redacts any secrets) to identify runtime dependencies, actual Conky window settings and autostart commands before planning a minimally invasive KDE-specific restore.

## FenixSystem source inspected and KDE candidate profile prepared

OWNER displayed the **actual contents** of three recovered files from archived Fedora COSMIC:

- `conky.conf` (93 lines) already uses `out_to_wayland = true`, `out_to_x = false`, a top-right window, a detailed 12-thread CPU table, RAM/SSD, external sensor script, battery BAT0 and fixed network interface `wlp6s0`.
- `fenix-sensors.sh` (19 lines) reads `k10temp`, `amdgpu`, `nvme` and `thinkpad` via hwmon without missing-sensor guards.
- `fenix-conky.desktop` (8 lines) runs `sleep 3; exec conky -c ~/.config/conky/conky.conf`, `TryExec=/usr/bin/conky`.

All three source files were recovered to staging; not yet active under KDE. Fedora 44 official `conky-1.22.2-3.fc44` was confirmed externally as built with Wayland support: https://packages.fedoraproject.org/pkgs/conky/conky/fedora-44.html .

Prepared isolated **KDE test candidate**, preserving original behavior but not copied to OWNER's running system:
- `kde-adaptation/fenixsystem/fenix-sensors-kde.sh` — guarded hwmon reads, `--` fallback;
- `kde-adaptation/fenixsystem/fenix-network-kde.sh` — default-route network interface, no hardcoded `wlp6s0`;
- `kde-adaptation/fenixsystem/fenixsystem-kde.conf` — Wayland profile with 12-thread layout, helpers, battery `all`; no autostart;
- `kde-adaptation/fenixsystem/README.md` — testing instructions.

**Still required**: install Conky on actual Fedora KDE, execute `bash -n` on downloaded helper scripts, test window layering under KWin/Wayland, verify hardware sensors and then decide whether to enable a KDE autostart. This is NOT yet completed or accepted by OWNER. Preserve KDE Night Color 5000 K and existing TuneD `balanced` and ZRAM.

## Pobranie plikow FenixSystem KDE - 2026-10-27 18:15

OWNER potwierdzil udany automatyczny download do ~/FX-Linux-Odzysk/kde-fenixsystem/: fenix-network-kde.sh (672 B), fenix-sensors-kde.sh (995 B), fenixsystem-kde.conf (ok. 2.1 KiB). Pliki maja tryb -rw-------, dlatego na etapie diagnostyki skrypty uruchamiamy przez bash. Poprzedni skrypt pobierajacy zakonczyl sprawdzanie skladni obu skryptow bez bledu. To jeszcze nie instalacja Conky, test czujnikow ani uruchomienie autostartu. Nastepny krok: sprawdzenie output obu skryptow oraz nproc, pozniej test manualny Conky bez autostartu.
