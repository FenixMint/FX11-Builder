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

## KDE FenixSystem — owner runtime read-only tests passed

OWNER wykonał `bash -n` obu pobranych skryptów, wynik: **Składnia OK**. Następnie uruchomił testowo oba skrypty przez `bash` bez instalacji do docelowych ścieżek:

- `fenix-sensors-kde.sh`: CPU TEMP **52°C**, GPU TEMP **44°C**, SSD TEMP **38°C**, FAN **3077 RPM**, APU PPT **11.0 W**; format skryptu zawiera markery Conky `\${alignr}`, co jest oczekiwane.
- `fenix-network-kde.sh`: wykrył interfejs **wlp6s0** i zwrócił dynamiczne wyrażenia Conky `\${downspeed wlp6s0}` i `\${upspeed wlp6s0}`, również oczekiwane.
- `nproc`: **12**; układ historycznych 12 wątków nie wymaga na tym sprzęcie zmiany.

**Ocena**: oba skrypty działają na aktualnym KDE bez błędów odczytu. Nie potwierdzono jeszcze działania renderowania Conky, zachowania okna pod KWin Wayland, autostartu ani zainstalowania pakietu `conky`. Następny etap: zainstalować Conky z Fedory (za decyzją OWNER), ręcznie wdrożyć profil o odrębnej nazwie `fenixsystem-kde.conf`, sprawdzić rendering bez autostartu, dopiero potem ewentualnie aktywować autostart. Nie modyfikować Night Color **5000 K**, TuneD `balanced`, ZRAM, GRUB ani rozruchu.

## Conky first live KDE Wayland test — warning BAT1/BAT2/BAT3 (OWNER terminal)

On Fedora 44 KDE Wayland, OWNER installed `imlib2-1.12.5-2.fc44` and `conky-1.22.2-3.fc44` successfully via DNF, then ran `conky -c ~/.config/conky/fenixsystem-kde.conf`.

Terminal confirmed: `FOUND: wayland`, `'KDE' wayland session running`. Conky continued running and was terminated by manual `Ctrl+C`, reporting normal signal cleanup. **Visual placement of window was NOT yet explicitly confirmed.**

Repeated warnings tried missing BAT1, BAT2, BAT3 (`/sys/class/power_supply/BAT1/uevent` and ACPI battery paths). Cause in candidate config: `${battery_percent all}` enumerates all batteries; original COSMIC configuration used `${battery_percent BAT0}`. Corrected source candidate on GitHub to target BAT0 alone. Battery name on current machine **still needs read-only verification**; original profile BAT0 was historically used on the same ThinkPad. Conky documentation: https://conky.cc/variables.

GitHub profile corrected in commit `9157ba294d3ac78a884526d12a95fd0f33bf9e5a` at `kde-adaptation/fenixsystem/fenixsystem-kde.conf`. **Source update does NOT silently change the already downloaded or installed copy on OWNER's KDE.** Minimal local action: check `/sys/class/power_supply/BAT0`, replace only `battery_percent all` with `battery_percent BAT0` in `~/.config/conky/fenixsystem-kde.conf` after creating a local single-file backup, and rerun foreground Conky. If BAT0 does not exist, identify actual battery name and adapt accordingly. No autostart changes, no TuneD or Night Color changes.

## Conky window invisible on KDE Wayland — OWNER report

OWNER confirmed BAT0 exists (also AC and a peripheral hidpp battery). Local single-file copy and replacement to `${battery_percent BAT0}` in `~/.config/conky/fenixsystem-kde.conf` succeeded. Rerunning Conky shows `FOUND: wayland`, `'KDE' wayland session running`, **no battery warnings**, terminates normally on Ctrl+C, but **NO VISIBLE CONKY WINDOW**. Thus earlier statement that Conky appears visually was incorrect. Sensor + network helper tests previously succeeded independently.

Diagnosis hypothesis, NOT confirmed: original `own_window_hints='undecorated,sticky,below,skip_taskbar,skip_pager'` with `own_window_type='normal'` may send native Wayland layer surface to a layer hidden by Plasma. The upstream Conky configuration docs show `below`/`above` translating to Wayland layer placement; KDE/KWin layer handling has known reported edge cases. See https://conky.cc/config_settings and https://github.com/brndnmtthws/conky/wiki/Configuration .

Next harmless staged test: copy the current live Conky config to an alternate test file in `~/FX-Linux-Odzysk/kde-fenixsystem/`, remove *only* the `own_window_hints` line from the alternate, keep `own_window_type='normal'`, `out_to_wayland=true`, `out_to_x=false`; run foreground Conky with alternate config and observe whether a window appears. Do NOT overwrite live file, edit GitHub candidate based on untested guesses, enable autostart or change Night Color 5000 K, tuned, GRUB, Windows. If unsuccessful, consider a second independent diagnostic with XWayland fallback only after results.

## FenixSystem KDE Wayland — first **visual** success (OWNER screenshot)

OWNER supplied a screenshot after the isolated test variant removed `own_window_hints` from `fenixsystem-kde.conf`. **The FenixSystem panel is now visibly rendered over the KDE wallpaper.** The screenshot shows functional runtime values for CPU, RAM, SSD, CPU/GPU/SSD temperatures, fan, AMD APU PPT, battery and network. Battery BAT0 fix has removed the earlier missing-BAT warnings. It is not yet known whether Conky behaves correctly across virtual desktops or with maximized windows.

A *new* visual bug was identified in the screenshot: three-column per-thread CPU rows overlap (the original `${goto 125}` spacing is not rendered as expected on this Wayland setup). The KDE candidate config in GitHub was updated to **remove `own_window_hints`** and replace the four three-column rows with **six two-column rows**, using `${alignr}` for the right side; this aligns with the other right-aligned fields in the screenshot. The updated two-column layout has **NOT** been visually tested yet.

Candidate commit: `08ef36d5316f9367a8900ab61a4c0918d97f0ad9`; path `kde-adaptation/fenixsystem/fenixsystem-kde.conf`. This change is **only in GitHub**; user's running and installed files do not update by themselves.

Next safe action: fetch the candidate config **into a separate named test file** in `~/FX-Linux-Odzysk/kde-fenixsystem`, run foreground `conky -c <test-file>`, confirm no CPU overlap and normal KWin behavior. After owner's explicit visual acceptance, optionally copy updated config to `~/.config/conky/fenixsystem-kde.conf` with a backup, then discuss KDE autostart. No other system changes, no Night Color changes (5000 K), no GRUB changes.

## FenixSystem KDE — zbyt szerokie kolumny CPU V2 i nowy wariant V3

OWNER pokazał zrzut ekranu widocznego i funkcjonalnego panelu Conky (V2) na KDE Wayland: dane czujników, SSD, RAM, bateria, sieć działają i tekst się nie nakłada. Jednak `\${alignr}` ustawia drugą kolumnę procesora przy skrajnej prawej krawędzi monitora, tworząc zbyt szeroką przerwę między dwoma wątkami. OWNER oczekuje **bardziej zwartego układu**.

Przygotowano **V3 z trzema kolumnami** i `\${offset 45}` między polami CPU, bez zależności od `\${goto}` lub `\${alignr}` w tej części. Pozostałe funkcje, brak `own_window_hints`, `BAT0`, skrypty sieci i temperatur oraz status KDE 5000K niezmienione. Zapisano w commicie `4f08721239a41aeb8d306110ea2414c03bfac130` w `kde-adaptation/fenixsystem/fenixsystem-kde.conf`.

Uzasadnienie: Conky oficjalnie dokumentuje `offset` jako poziome przesunięcie o piksele, a upstream posiada otwarte zgłoszenie niestabilności `goto` pod Waylandem: https://conky.cc/variables ; https://github.com/brndnmtthws/conky/issues/1671 .

**Nie deklarować, że V3 jest już poprawny wizualnie**: wymagany test na sesji OWNER. Pobierać tylko tę konfigurację do odrębnego pliku `fenixsystem-v3.*.conf` i uruchamiać Conky bez autostartu. Nie nadpisywać zatwierdzonych lokalnych wersji ani ustawień.

## FenixSystem KDE V3 — visual confirmation by OWNER screenshot

OWNER provided a full screenshot of V3 with three compact columns (`\${offset 45}`). All **12 CPU threads** (T01–T12) fit and no labels overlap; compared with V2, the threads are now much closer and follow a balanced three-column layout. The displayed Conky panel also renders RAM, SSD, CPU/GPU/SSD temperature, fan, APU PPT, BAT0 percentage, networking and uptime. Visually, this resolves both the original overlap of `goto` and the excessively spread `alignr` layout. The screenshot is visual evidence, not an explicit OWNER sign-off for autostart or for foreground/background window stacking across KDE activities.

**Candidate config:** `kde-adaptation/fenixsystem/fenixsystem-kde.conf`, compact three-column spacing and no `own_window_hints`; GitHub comment updated to note visual confirmation. OWNER's local live `~/.config/conky/fenixsystem-kde.conf` may still be older; V3 was launched from an independently downloaded test file.

**Next logical step (not yet run):** promote reviewed V3 to live per-user Conky config, preserving older live profile with a single-file backup, then optionally enable a **new** KDE-only desktop autostart `fenixsystem-kde.desktop` after checking no legacy `fenix-conky.desktop` or duplicate exists. Source template saved as `kde-adaptation/fenixsystem/fenixsystem-kde.desktop` with 8-second login delay. Neither new startup entry nor profile promotion has been performed on OWNER's machine. Do not change KDE Night Color 5000 K, TuneD balanced, ZRAM or boot-related files.
