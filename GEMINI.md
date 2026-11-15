# GEMINI.md — Instrukcja Architektoniczna i Środowiskowa (`Kroniki Rubieży: Horda` v6.6+)

## 1. Środowisko i Weryfikacja (Nie szukaj Pythona po systemie!)
- Interpreter `python` oraz linter `ruff` są dostępne bezpośrednio w bieżącym środowisku. Nie wykonuj komend diagnostycznych szukających `python.exe` (`where`, `reg query`, przeszukiwanie `AppData`).
- **Kolejność weryfikacji po edycji kodu:**
  1. `python -m ruff check .` — szybka kontrola składni i importów (<1 s).
  2. `python test_horde_scenario.py -v` — automatycznie kompiluje świeży plik `.aoe2scenario` przez `build_horde_scenario()` i uruchamia 26 testów jednostkowych oraz walidację binarną (~35 s). Nie musisz uruchamiać `generate_horde_quests_scenario.py` osobno przed testami.

## 2. Zasada Pełnego Kontekstu i Dokumentacji (`horda.md`, `DEBUG_LOG.md`, `ROADMAP.md`)
- **Pełny odczyt przed edycją:** Przed modyfikacją kodu przeczytaj w całości modyfikowane moduły `.py`, `horda.md` oraz `DEBUG_LOG.md`, aby zachować spójność całego systemu i uniknąć regresji.
- **Kiedy aktualizować dokumentację:** Aktualizuj pliki `.md` wyłącznie po wdrożeniu zmian w kodzie i przejściu testów. **Nie modyfikuj** ich podczas zadań czysto analitycznych, audytów ani podczas generowania `SCENARIO_DOSSIER.md`.
- **`horda.md` oraz opisy w grze (`populate_ingame_scenario_descriptions` w `horde_config.py`):** Każda zmiana wpływająca na rozgrywkę (składy i czasy fal, statystyki jednostek, limity technologii AI, warunki i nagrody Questów/Settlementów, progi eskalacji, geometria bazy/bram) **musi** zostać odzwierciedlona zarówno w odpowiednich sekcjach `horda.md`, jak i w `populate_ingame_scenario_descriptions()` (wraz z podbiciem numeru wersji). Nie wolno zostawiać w `horda.md` opisów mechanik, które zostały zmienione w kodzie.
- **`DEBUG_LOG.md` (dziennik techniczny):** Po każdym udanym wdrożeniu dopisz nowy wpis na końcu Sekcji 7 (historia wdrożeń) zawierający: numer wersji/iteracji, listę zmodyfikowanych plików, opis przyczyny i rozwiązania oraz konkretny wynik weryfikacji binarnej (`test_horde_scenario.py` + sprawdzone metryki). Jeśli naprawiono nowy błąd, dopisz go również do listy w Sekcji 4.
- **`ROADMAP.md` (plan i backlog):** Oznaczaj ukończone zadania statusem `[DONE / WDROŻONE]`. Nowe pomysły, uwagi z playtestów oraz zadania odłożone na później dopisuj w sekcji planowanych prac na końcu pliku (bez kasowania historii wcześniejszych etapów).
- **Spójność `SCENARIO_DOSSIER.md`:** Jeśli zmiana dotyczyła zasad rozgrywki i w katalogu istnieje plik `SCENARIO_DOSSIER.md`, zaktualizuj go lub zaznacz w raporcie końcowym, że wymaga odświeżenia przed kolejnym audytem zewnętrznym.
- **Zakaz cichych wyjątków:** Nigdy nie używaj konstrukcji `try: ... except Exception: pass` wokół wywołań `AoE2ScenarioParser`. Używaj jawnego `safe_call` weryfikującego sygnatury przez `inspect.signature`.

## 3. Architektura Modułów Projektu
- `generate_horde_quests_scenario.py` — punkt wejścia (Runner).
- `horde_config.py` — stałe ID, słownik `BALANCE`, `ENEMY_UNIT_REGISTRY` (jedyne źródło prawdy o statystykach i skalowaniu 26 jednostek wroga), listy `PLAYER_*`, `get_wave_definitions()` oraz opisy w grze (`populate_ingame_scenario_descriptions`).
- `horde_map.py` — generator mapy `200×200`, dwuwarstwowa siatka antykolizyjna `SafeMapGrid` (`occupied_tiles` vs `no_tree_zones`), wygładzanie elewacji $|\Delta h| \le 1$, bazy `P1–P4`, 6 Settlementów, 4 Questy i Sanktuarium Balansu `(6, 150)`.
- `horde_waves.py` — inicjalizacja dyplomacji i technologii AI (`01_Init`, `01b`, `01d–01f` z `enforce_specialized_unit_caps`), garnizony (`add_garrison_spawn_effect` + `add_guarded_camp_with_leash`), Aura Arcymaga (`02a–02d`), przepychanie bram (`02e`), eskalacja czasowa (`04a–04f`) oraz fale 1–14 i Tryb Endless (`03_*`).
- `horde_quests.py` — Zegar Fali (`00_Wave_Timer_*`), Sanktuarium Balansu (`09_Diff_*`), Questy `Q1–Q4` (`06_*`), zniszczenie Settlementów (`05_*` z `collapse_camp_buildings`) i warunki zwycięstwa/porażki (`07_*`, `08_*`).
- `test_horde_scenario.py` — zestaw 26 testów (algorytmy skalowania, zerowy dryf HP/Atk, brak kolizji jednostek i budynków z wodą/drzewami/smyczami, struktura binarna triggerów).

## 4. Nienaruszalne Reguły Silnika Genie (AoE2: DE)
1. **Zakaz efektów wywołujących crash C++:** Nigdy nie używaj `display_timer`, `display_instructions` ani ujemnego `tribute`. Do zasobów i limitu populacji (`RES_BONUS_POP_CAP = 32`) używaj wyłącznie `modify_resource` z `Operation.ADD`.
2. **Ochrona przed `uint8` underflow (`5 + 247` ataku):** Jednostkom wręcz modyfikuj wyłącznie `armor_class = 4` (Base Melee), a strzeleckim `armor_class = 3` (Base Pierce). Wszystkie grupowe buffy Hordy muszą przechodzić przez `ENEMY_UNIT_REGISTRY`.
3. **Sanktuarium Balansu bez blokad czasowych:** Nie twórz triggerów zamrażających Sanktuarium (`State_Sanctuary_Unlocked`, `Close_Window`, `Relay2s`). Ochronę przed podwójnym przeskokiem poziomu w jednym ticku zapewnia odwrócony porządek topologiczny rejestracji triggerów `09_Diff_*` (`id(P1->P2) < id(0->P1) < id(M1->0) < id(M2->M1)` dla pada górnego i analogicznie dla dolnego).
4. **Ruch Szakali (`PlayerId.SEVEN`) i separacja rozkazów:**
   - Do ruchu ignorującego walkę na froncie używaj `trigger.new_effect.task_object(..., action_type=ActionType.MOVE)` (nie istnieje efekt `.move`).
   - `PlayerId.SEVEN` w triggerze `02e_Push_Gate_Units_Deep_Into_Base` może być obsługiwany wyłącznie w strefie Bramy Centralnej `(104, 114)`, aby nie nadpisywać rozkazów `MOVE` Szakali na flankach północnej i wschodniej.
5. **Geometria spawnów i smyczy (`Garrison_Leash_*`):**
   - Spawny fal używają siatki 11-kolumnowej (`dx = (idx % 11) - 5`, `dy = (idx // 11) - 5`). Każdy punkt spawnu fali lub odwetu (wraz z rozrzutem `±5`) musi leżeć poza `ring_outer = 20` wszystkich obozów tego samego gracza AI oraz poza kafelkami `TERRAIN_WATER = 1`, drzewami i budynkami.
   - Spawny garnizonów obozowych muszą korzystać z `add_garrison_spawn_effect` omijającego `ctx["occupied_tiles"]`.
6. **Pułapy statystyk jednostek specjalnych AI (`enforce_specialized_unit_caps`):**
   - Po każdym badaniu technologii przez AI (`01d`, `01e`, `01f`) wymuszaj stałe pułapy dla 6 archetypów: `ATTR_BLAST_ATTACK_LEVEL = 44` ustawione na `2` dla `SIEGE_ONAGER_ID = 588` oraz zasięg `21` i prędkość `0.58`; atak `3`, pancerz `10/12` i prędkość `0.72` dla Żelaznego Słonia `1134`; atak `2`, pancerz `0/6` i prędkość `1.62` dla Szakala `441`; zasięg `19` dla Snajpera `557`; prędkość `0.78` dla Arcymaga `842`; pancerz strzelecki `0` dla Berserkera `694` (`1.40`) i Kamikaze `440`/`1263` (`1.50`), oraz korektę `-20 HP` dla Słonia i Szakala po `TECH_BLOODLINES` w `01d`.