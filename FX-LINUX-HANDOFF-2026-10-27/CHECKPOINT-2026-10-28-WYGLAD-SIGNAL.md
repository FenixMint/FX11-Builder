# FX Linux / Fedora KDE — checkpoint wznowienia: wygląd Plasma i Signal

**Data:** 2026-10-28  
**Rodzaj:** stan po rozmowie / checkpoint prac, **nie** `RAPORT STOP` w znaczeniu protokołu repozytorium.  
**OWNER:** „na razie tak wystarczy, ale zapisz gdzie jesteśmy”. **Pauza prac nad Signal i wizualną przebudową Plasma**; nie wykonywać kolejnych poprawek bez kontynuacji uzgodnionej z OWNER.  
**Środowisko:** Fedora 44 KDE Plasma 6.7.5 Wayland; monitor zewnętrzny 1680×1050; bieżący cel to wygodna, natywna dla KDE personalizacja FX Linux (wcześniej COSMIC).  
**Zapis:** tylko na gałęzi `handoff/fx-linux-manual-package-2026-10-27`; żadnej automatycznej zmiany lokalnego systemu ani prywatnych danych użytkownika.

## 1. Stan pulpitu / wizualny

- Kierunek tożsamości FX Linux: ciemny, nowoczesny i czytelny pulpit; docelowo górny panel, lewy dock, menu FX oraz FenixSystem; dokładne proporcje i kolory **nie zostały jeszcze zatwierdzone** jako finalna realizacja.
- Pierwsza próba utworzenia panelu doprowadziła do dwóch pełnych paneli z powielonymi ikonami — **niezaakceptowana**.
- OWNER przywrócił poprzednią konfigurację paneli z kopii `~/FX-Linux-Odzysk/kde-visual-backup-*/plasma-org.kde.plasma.desktop-appletsrc` i potwierdził „przywróciło” — **rollback PASS według OWNER**. Na przekazanych zrzutach był jeden działający górny panel. Nie uruchamiać ponownie skryptu rollback bez potrzeby.
- Tapeta FX OS i **FenixSystem KDE V3** zachowane. FenixSystem działa i ma autostart PASS; ograniczenie Conky 1.22.2: Plasma „Pokaż pulpit” może go ukrywać. OWNER zdecydował czekać na nowy pakiet w oficjalnym repo Fedory; bez ręcznej kompilacji.
- Ciemna tapeta ekranu logowania ustawiona przez OWNER; oddzielna weryfikacja po relogin nie została jednoznacznie zgłoszona. Night Color KDE **5000 K**, TuneD/tuned-ppd i ZRAM bez zmian. Konfiguracji klapy i monitorów nie ruszać — OWNER ocenia obecne działanie jako dobre.

## 2. Signal Desktop AppImage — co zrobiono i sprawdzono

- Signal jest lokalną **AppImage** w `~/.local/bin/signal-desktop.AppImage`, uruchamianą przez `~/.local/share/applications/signal-appimage.desktop`, z polami `Icon=signal-desktop` i `StartupWMClass=signal`. Ani RPM, ani Flatpak nie są źródłem tego uruchomienia.
- W menu i na przypiętej ikonie przed uruchomieniem był pusty symbol dokumentu. Z AppImage odzyskano oryginalne `signal-desktop.png` do `~/.local/share/icons/hicolor/{16,24,32,48,64,128,256,512,1024}x{16,24,32,48,64,128,256,512,1024}/apps/` (stosowne pary jednakowych wymiarów) — **dziewięć rozmiarów zainstalowanych, statyczna ikona przywrócona**.
- Zrzut GUI Signal: powiadomienia włączone, przypomnienia włączone, wyróżnianie okna włączone, dźwięki włączone, licznik ustawiony na **nieodczytane wiadomości**, wyciszone czaty nieuwzględniane. Tych ustawień nie zmienialiśmy.
- OWNER potwierdził **powiadomienia systemowe KDE PASS** przy nowej wiadomości; na ikonie chwilowo pojawia się mała nakładka przypominająca dzwonek/dźwięk. Nie utożsamiać jej z **trwałym licznikiem nieodczytanych wiadomości**.
- Syntetyczny test D-Bus `com.canonical.Unity.LauncherEntry.Update` adresowany do `application://signal-appimage.desktop` pokazał liczbę **2 natychmiast**, którą usunięto po **12 sekundach** — **Plasma Task Manager badge rendering PASS** dla obecnego identyfikatora skrótu.
- Monitor `dbus-monitor` dostarczony wcześniej przez OWNER pokazywał tylko `NameAcquired` / `NameLost`, nie było w nim uchwyconego `LauncherEntry.Update`. **Nie dowodzi to jeszcze, że rzeczywista wiadomość nie wyzwoliła takiego sygnału**, bo nie został potwierdzony jego moment podczas monitorowania.
- Potencjalna niezgodność: plik skrótu nazywa się `signal-appimage.desktop`, a obecny upstream Signal deklaruje `desktopName: signal.desktop` i korzysta z `app.setBadgeCount()` w Electron. Jest to **hipoteza**, nie potwierdzona przyczyna. **Nie zmieniać teraz nazwy pliku, nie odpinać aplikacji, nie czyścić cache Plasma ani nie reinstalować Signal.**
- **STATUS KOŃCOWY NA DZIŚ:** ikona statyczna **PASS**; powiadomienia systemowe **PASS**; chwilowy wskaźnik aktywności/powiadomienia **ZAOBSERWOWANY**; testowy licznik `2` **PASS**; **rzeczywisty trwały licznik nieodczytanych — NIEPOTWIERDZONY / na razie odłożony**. Wersja AppImage Signal nie została jeszcze odczytana.

## 3. Pozostałe tematy — nie zamykać pochopnie

- **GRUB FX OS:** wcześniej przeprowadzono audyt BLS, Windows Boot Manager, UEFI i kontrolę składni. Tło i obie ikony GRUB przeszły SHA-256 **3/3 PASS**. OWNER wcześniej zatwierdził kontrolowane przywrócenie, ale potem **zmienił priorytet i odłożył wykonanie**. Brak potwierdzenia lokalnej instalacji motywu; niczego teraz nie wykonywać przy EFI, GRUB czy partycji Windows/FX11.
- **Kamerka `blacklist uvcvideo`**: historyczny plik nieprzywrócony, potrzeba oddzielnej decyzji OWNER.
- **TuneD/sysctl/modprobe:** odczytowe porównanie wykonane; obecne TuneD `balanced` ma mapowanie baterii na `balanced-battery`, przełączanie runtime nie jest jeszcze w pełni przetestowane. `kvm.conf` ze starego COSMIC zawierał tylko komentarze; `vhost.conf` opcję dla wirtualizacji, bez uzasadnienia do automatycznego kopiowania.
- **Docelowy UX FX Linux:** szczegóły paneli, docka, menu, ikon i palety pozostają do iteracyjnego zatwierdzania po obecnej pauzie. Nie dokładać drugiego pełnego panelu ani globalnych presetów, które mogą powielić widżety.

## 4. Jak bezpiecznie wznowić

Jeżeli OWNER wróci do **Signal**: najpierw nieinwazyjny test z rzeczywistą nową, nieodczytaną wiadomością podczas monitorowania D-Bus `LauncherEntry.Update`; sprawdzić `application://...`, wersję AppImage i stan znaczników w KDE. Dopiero potwierdzony konflikt uzasadnia kopię i punktową naprawę launchera. Unikać dostępu do treści wiadomości i baz aplikacji.

Jeżeli OWNER wróci do **wyglądu Plasma**: zachować działający pojedynczy panel i backup, zacząć od małej, odwracalnej zmiany istniejącego panelu lub osobnego pustego docka po wizualnej akceptacji, bez utraty FenixSystem i powiadomień.

Jeżeli OWNER wróci do **GRUB**: ponownie zweryfikować stan przed rzeczywistym zapisem, uwzględnić wstrzymanie po zmianie priorytetu i bezpieczeństwo rozruchu.

## Dokumenty kanoniczne

- `kde-adaptation/FX-LINUX-KDE-VISUAL-V0.1-2026-10-28.md` — szczegółowy przebieg visual/Signal i odzyskanie panelu.
- `KDE-LUKI-PRZYWRACANIA-2026-10-27.md` — audyt COSMIC → KDE, GRUB, zasilanie, ekran logowania.
- `FEDORA-KDE-STAN-PO-INSTALACJI-2026-10-27.md` — bazowy stan i FenixSystem V3.

**Nie deklarować zamknięcia wszystkich prac FX Linux.** To checkpoint aktualnego stanu i świadomej pauzy.
