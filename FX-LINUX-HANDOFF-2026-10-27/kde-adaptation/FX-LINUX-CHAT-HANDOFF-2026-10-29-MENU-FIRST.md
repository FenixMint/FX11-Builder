# FX Linux / FX OS — przekazanie do nowej rozmowy (2026-10-29)

**OWNER priorytet: TERAZ MENU FX OS.** Dock zostaje na obecnym, działającym rozwiązaniu tymczasowym. Nie zaczynać nowej rozmowy od zmiany docka ani odtwarzania już zrobionych kroków.

## Przeczytaj na starcie

1. `AGENTS.md`, `README.md` oraz właściwe zasady repozytorium `FenixMint/FX11-Builder`.
2. Aktywna gałąź: `handoff/fx-linux-manual-package-2026-10-27`.
3. Szczegółowy projekt menu: `FX-LINUX-HANDOFF-2026-10-27/kde-adaptation/FX-OS-MENU-V0.1-2026-10-29.md`.
4. Narastający, historyczny checkpoint: `FX-LINUX-HANDOFF-2026-10-27/kde-adaptation/FX-LINUX-KDE-VISUAL-V0.1-2026-10-28.md` — **nowsze decyzje OWNER nadpisują wczesne plany**, bez usuwania historii.

## Ostatnie świadome decyzje OWNER

- **Menu:** opracować teraz własne duże menu FX OS, otwierane z **okrągłego, podświetlonego przycisku FX w lewym GÓRNYM rogu poziomego panelu** (nigdy na lewym docku). Menu pod przyciskiem, nie pełnoekranowe; wyszukiwarka, dwie kolumny: ulubione i kategorie/aplikacje; miejsca/pliki, ustawienia, ostatnie, wylogowanie/zasilanie; soczyste ikony, Oxygen/FX OS Gloss, język polski. Inspiracje: koncept OWNER nr 3, Windows XP Luna, Windows 7 Aero, Mandriva Powerpack 2008 Ia Ora, Plastik/Keramik/Oxygen.
- **Dwa odrębne polecenia docelowe menu:** `Dodaj do panelu` = GÓRNY panel; `Dodaj do docka` = LEWY dock. Nie implementować tego drugiego przez zgadywanie dopóki finalny dock nie jest wybrany; obie funkcje są **NIEZAIMPLEMENTOWANE**.
- **Dock:** OWNER zmienił koncepcję docelową. Chce **żywy dock, reagujący na uruchomione aplikacje**, z przypinaniem i dowolną kolejnością. **Cairo-Dock to tylko pomysł do porównania**, nie zatwierdzona technologia ani zgoda na instalację. Sprawdzić później rzeczywistą kompatybilność Fedora 44 / KDE Plasma 6.7.5 / Wayland, zadania, Signal, autoukrywanie/rezerwację miejsca i stabilność. **Dock research i migracja odłożone — najpierw menu.**

## Faktyczny działający pulpit — NIE PSUĆ

- Fedora 44, **KDE Plasma 6.7.5, Wayland**, Kirigami 6.31.0; motyw ikon `breeze-dark`; **Oxygen Plasma Style** aktualnie zastosowany i zaakceptowany przez OWNER (pełniejsze kolory, szklana krawędź).
- **Górny panel ID 55**: menu Kickoff `56`, Pager `57`, menedżer ikon-zadań `58`, separator `59`, zasobnik `60`, zegar `75`, Pokaż pulpit `76`. Na górze mają zostać na stałe **Ustawienia systemowe, Discover, Dolphin** oraz pojawiać się uruchomione aplikacje; zasobnik i zegar po prawej. Wcześniejsze usunięcie widgetu 58 przesunęło zegar i zasobnik w lewo; zostało wycofane. **Nie usuwać 58 ani panelu 55.**
- **Lewy prawdziwy panel ID 85** z jednym `org.kde.plasma.quicklaunch` (nowy widget ID nieustalony po ręcznej migracji). Szerokość **64 px**, `lengthMode='fit'`, `minimumLength=64`, `maximumLength=820`, położenie `left`, wyrównanie `center`, `hiding='none'`. Kolorowe ulubione w jednej kolumnie. OWNER potwierdził test **maksymalizowane okno NIE ZASŁANIA docka**. To **działająca baza tymczasowa**, nie finalny dynamiczny dock.
- Oryginalna ciemna tapeta FX OS oraz **pełny, szczegółowy FenixSystem V3** po prawej pozostają nietknięte. Nie podmieniać FenixSystem na mini-widget.
- Signal AppImage ma działającą ikonę i natywne powiadomienia KDE; stały licznik nieprzeczytanych nie został potwierdzony.
- Błędy z przeszłości: masowe nadpisanie `[General] launchers` popsuło ikony i wymagało rollbacku; skrypty gdbus miały też błędy parsowania. **Nie powtarzać bulk-edit, nie zakładać identyfikatorów bez kontroli, robić kopie i pojedyncze testy.**
- Ostatnia potwierdzona lokalna kopia przed auto-fit: `~/FX-Linux-Odzysk/fx-dock-autofit-20261029-185024-Amsh`. Kopie są prywatne i nie trafiają do repo.

## Następna rozmowa — pierwszy ruch

**Nie instalować jeszcze nowego menu.** Najpierw poprosić OWNER o **zrzut obecnego menu Kickoff OTWARTEGO** z przycisku w lewym górnym rogu; porównać z kontraktem `FX-OS-MENU-V0.1-2026-10-29.md`. Następnie dobrać etapową, odwracalną implementację: ikona FX dla istniejącego Kickoff `56` jako bezpieczny pierwszy etap (wyłącznie po uzyskaniu zaakceptowanego materiału graficznego) vs osobny testowany użytkownikowy plasmoid dla docelowego dużego menu. Zawsze zachować działające Kickoff, górny panel, Quicklaunch, Oxygen i FenixSystem do chwili weryfikacji.

**Status:** Menu DESIGN/PLANNING, nie wdrożone. Dock live RESEARCH LATER. Pulpit i oba panele teraz działają. Ostatni test docka OWNER PASS. Formalne `RAPORT START/STOP` tylko na wyraźny sygnał OWNER zgodnie z AGENTS.md.