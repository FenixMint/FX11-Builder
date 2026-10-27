# FX Linux — pakiet do ręcznego zachowania przed Fedora KDE

**OWNER DECISION — 2026-10-27:** kopiujemy ręcznie **konkretne skrypty, ustawienia, materiały graficzne oraz historię modyfikacji** do wybranego folderu na partycji FX11. Nie wykonujemy automatycznego backupu, kopii systemu, archiwum całego /home, szyfrowania ani ustalania punktu montowania.

W tej paczce znajdują się zachowane na GitHubie źródła **FX OS GRUB** i **Fenix Night Light**, historycznie sprawdzone ustawienia klapy oraz dokumenty `WYKONANE-MODYFIKACJE.md`, `LOKALNE-PLIKI-DO-DOLACZENIA.md` i `ZRODLA-I-BRAKI.md`.

Wszystkie pliki w `zrodla/` są kopiami dokładnych wersji z podanych w manifeście commitów. Nie należy bez sprawdzenia wdrażać starych ustawień COSMIC w KDE, zmieniać GRUB-a ani aktywować usług. Kopiowanie ustawień z bieżącej Fedory OWNER wykona manualnie do prywatnego podfolderu na FX11. **Nie publikować lokalnych prywatnych plików na GitHubie.**

Podczas późniejszej instalacji nie wolno przypadkowo formatować partycji FX11 ani naruszać Windows Boot Managera. Sama obecność paczki nie jest dowodem wykonania lokalnego transferu.

Uwaga: poprzedni automatyczny `fx-linux-preserve.sh` to historyczny eksperyment, nie narzędzie wymagane w tym procesie.
