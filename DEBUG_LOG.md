# DEBUG_LOG.md — Dokumentacja Architektury, Stanu Bazowego i Błędów (`Kroniki Rubieży: Horda i Ekspedycje` v6.2)

## 0. Identyfikacja stanu bazowego i zasady dla Agenta IDE (Antigravity / VS Code)
- **Repozytorium bazowe:** `https://github.com/trzesnim/AoE_Scenarios/tree/main` (stan odpowiadający wersji `v6.2` po podziale monolitu na 5 modułów `.py`).
- **Zasady nienaruszalne dla Agenta (AGY Initialization Rules):**
  1. Przed pierwszą edycją odczytaj wszystkie 5 plików `.py` z dysku i zapisz hash commitu (`git rev-parse HEAD`).
  2. Nie modyfikuj elementów oznaczonych w Sekcji 3 jako **STREFA CHRONIONA**.
  3. Nigdy nie używaj konstrukcji `try: ... except Exception: pass` wokół wywołań warunków lub efektów `AoE2ScenarioParser`.
  4. Wykonuj pracę ściśle według podetapów z `ROADMAP.md` (`Etap 0` -> `1A` -> `1B` -> `2` -> `3A` -> `3B` -> `3C` -> `4` -> `5` -> `6A` -> `6B` -> `6C` -> `7` -> `8`), weryfikując po każdym podetapie kompilację scenariusza i linter `ruff check`.

---

## 1. Struktura plików projektu i proces kompilacji

Projekt generuje 4-osobowy scenariusz kooperacyjny RPG/RTS do *Age of Empires II: Definitive Edition* przy użyciu biblioteki `AoE2ScenarioParser`. Składa się z 5 modułów Pythona oraz dokumentacji:

1. **`generate_horde_quests_scenario.py` (~35 linii) — Punkt wejścia (Runner):**
   - Wczytuje plik szablonu `INPUT_TEMPLATE` (`template.aoe2scenario`) przez `AoE2DEScenario.from_file()`.
   - Wywołuje kolejno:
     1. `populate_ingame_scenario_descriptions(scenario)` (z `horde_config.py`),
     2. `ctx = build_map_and_entities(scenario)` (z `horde_map.py`),
     3. `setup_init_aura_and_waves(scenario, ctx)` (z `horde_waves.py`),
     4. `setup_sanctuary_quests_and_victory(scenario, ctx)` (z `horde_quests.py`).
   - Zapisuje wynikowy plik do `OUTPUT_SCENARIO` (`Kroniki_Rubiezy_Horda_Coop.aoe2scenario`).
2. **`horde_config.py` — Konfiguracja, stałe ID, rejestr jednostek i definicje fal:**
   - Zawiera stałe ID obiektów, jednostek specjalnych, zasobów (`RES_*`), atrybutów silnika Genie (`ATTR_*`) oraz technologii (`TECH_*`).
   - Definiuje słownik `BALANCE` (czasy fal, progi eskalacji, statystyki 6 archetypów jednostek specjalnych, wartości nagród za Questy).
   - Definiuje funkcje: `find_scenario_folder()`, `populate_ingame_scenario_descriptions(scenario)` oraz `get_wave_definitions()`.
3. **`horde_map.py` — Silnik geometryczny mapy i spawner obiektów startowych:**
   - Zawiera klasę siatki antykolizyjnej `SafeMapGrid` oraz funkcje rzeźby terenu, biomu, lasów, rzeki, klifów, baz graczy, przełęczy, Settlementów i Sanktuarium Balansu.
   - Główna funkcja `build_map_and_entities(scenario) -> dict` buduje mapę `200x200` i zwraca słownik `ctx` z referencjami do obiektów i współrzędnych.
4. **`horde_waves.py` — Inicjalizacja AI, mutacje jednostek, Aura Maga, eskalacja i fale 1–14:**
   - Zawiera funkcje pomocnicze triggerów (`safe_call`, `safe_modify_attribute`, `add_enemy_combat_buff`, `set_as_objective`, `send_highlight_chat`, `add_player_resource`, `research_techs`, `add_guarded_camp_with_leash`, `add_spawn_and_attack_effect`, `scale_comp`).
   - Główna funkcja `setup_init_aura_and_waves(scenario, ctx)` tworzy triggery dyplomacji, technologii AI, mutacji jednostek specjalnych, garnizonów, Aury Arcymaga, 3-stopniowej eskalacji oraz 14 fal Hordy.
5. **`horde_quests.py` — Sanktuarium Balansu, Questy Q1–Q4, Settlementy G1–G3 i warunki końca gry:**
   - Główna funkcja `setup_sanctuary_quests_and_victory(scenario, ctx)` tworzy maszynę stanów Sanktuarium Balansu (`09_Diff_*`), triggery 4 Questów pobocznych (`06_Quest*`), triggery zniszczenia 6 Settlementów (`05_Settlement_Destroyed_*`) oraz triggery zwycięstwa (`07_Victory_*`) i porażki (`08_Defeat_*`).
6. **`horda.md` — Dokumentacja scenariusza dla graczy.**

### Uruchamianie kompilacji
```powershell
python generate_horde_quests_scenario.py
```

---

## 2. Konfiguracja graczy i geometria mapy (`MAP_SIZE = 200`)

### Gracze ludzcy (`human_players = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR]`)
Wszyscy 4 gracze są w sojuszu (`DiplomacyState.ALLY`), mają od `0:01` zbadaną Kartografię (`TECH_CARTOGRAPHY = 19`) i startują z zasobami `500` Food, `600` Wood, `400` Gold, `300` Stone (`BALANCE["human_start_res"]`), 6 wieśniakami i 1 skautem wewnątrz Twierdzy Sojuszu w SW części mapy (`x = 0..104, y = 100..199`):
- **`PlayerId.ONE` (Niebieski):** Town Center na `(76, 124)`. Posiada nieśmiertelnego Króla (`UnitInfo.KING.ID`) w Sanktuarium Balansu na `(6, 150)` oraz stałe obiekty `MAP_REVEALER_ID = 837` nad celami na mapie.
- **`PlayerId.TWO` (Czerwony):** Town Center na `(32, 164)`. Właściciel centralnej **Cytadeli Sojuszu** (`FEITORIA_ID = 1021` na `54, 146`, +3000 HP); w `0:01` otrzymuje `+20` do `RES_BONUS_POP_CAP = 32`, aby Feitoria nie zajmowała limitu populacji.
- **`PlayerId.THREE` (Zielony):** Town Center na `(32, 122)`. Odpowiada za umocnienia Bramy Północnej `(48, 100)`.
- **`PlayerId.FOUR` (Żółty):** Town Center na `(76, 168)`. Odpowiada za umocnienia Bramy Wschodniej `(104, 162)` i Bramy Handlowej `(104, 193)`.

### Gracze AI (`ai_players = [PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]`)
Wszyscy 4 gracze AI są w sojuszu między sobą i w stanie wojny (`DiplomacyState.ENEMY`) z `P1–P4`. Startują z `0` wszystkich surowców, bez wieśniaków i bez mobilnych jednostek na mapie w `0:00`:
- **`PlayerId.FIVE` (Turkusowy — Szturmowcy i Kamikaze):**
  - Technologie Kuźni: `TECH_SCALE_MAIL` (`8:30`), `TECH_CHAIN_MAIL` + `TECH_SQUIRES` (`18:00`), `TECH_PLATE_MAIL` (`34:30`).
  - Jednostki specjalne: Berserker Szturmowy (`ELITE_BERSERK_ID = 694`), Fanatyk Kamikaze (`PETARD_ID = 440`), Płonący Wielbłąd (`FLAMING_CAMEL_ID = 1263`).
  - Budynki: Settlement `G1_North` `(76, 72)`, Settlement `G1_East` `(132, 152)`, Quest 1 Karawanseraj `(154, 190)`.
- **`PlayerId.SIX` (Fioletowy — Artyleria i Snajperzy):**
  - Technologie Kuźni/Uniwersytetu: `TECH_FLETCHING` (`8:30`), `TECH_BODKIN_ARROW` + `TECH_BALLISTICS` (`18:00`), `TECH_BRACER` + `TECH_CHEMISTRY` + `TECH_SIEGE_ENGINEERS` (`34:30`).
  - Jednostki specjalne: Snajper Imperialny (`UnitInfo.ELITE_JANISSARY.ID = 375`), Moździerz Oblężniczy (`SIEGE_ONAGER_ID = 588`).
  - Budynki: Settlement `G2_Snipers` `(68, 34)`, Quest 2 Klif Artylerii `(28, 32)`.
- **`PlayerId.SEVEN` (Szary — Arcymagowie i Dywersja):**
  - Technologie Kuźni/Stajni: `TECH_FORGING` + `TECH_BLOODLINES` (`8:30`), `TECH_IRON_CASTING` + `TECH_HUSBANDRY` (`18:00`), `TECH_BLAST_FURNACE` (`34:30`).
  - Jednostki specjalne: Arcymag Tarczy (`IMAM_UNIT_ID = 842`), Szakal Dywersyjny (`HUSSAR_ID = 441`).
  - Budynki: Settlement `G2_Mages` `(148, 72)`, Quest 4 Krwawy Ołtarz `(105, 20)`.
- **`PlayerId.EIGHT` (Pomarańczowy — Tytani i Elita Hordy):**
  - Technologie: `TECH_FAITH` (`0:01`), `TECH_FORGING` + `TECH_SCALE_BARDING` (`8:30`), `TECH_IRON_CASTING` + `TECH_CHAIN_BARDING` (`18:00`), `TECH_BLAST_FURNACE` + `TECH_PLATE_BARDING` + `TECH_SIEGE_ENGINEERS` (`34:30`).
  - Jednostki specjalne: Taran-Żółw / Żelazny Słoń (`ELITE_BATTLE_ELEPHANT_ID = 1134`).
  - Budynki: Settlement `G3_North` `(142, 24)`, Settlement `G3_East` `(176, 56)`, Quest 3 Skarbiec Krasnoludów `(142, 118)`.

### Kluczowe strefy i współrzędne na mapie
- **Przełęcze Twierdzy Sojuszu (`build_fortified_pass_defenses`):**
  - `gate_north = (48, 100)` (`along_x=True`, Brama `789`, właściciel `P3`),
  - `gate_center = (104, 114)` (`along_x=False`, Brama `793`, właściciel `P1`),
  - `gate_east = (104, 162)` (`along_x=False`, Brama `793`, właściciel `P4`),
  - `gate_trade = (104, 193)` (`along_x=False`, Brama `793`, właściciel `P4`).
- **Punkty docelowe `attack_move` dla fal głównych (głęboko wewnątrz bazy):**
  - `deep_target_north = (48, 138)`, `deep_target_center = (54, 146)`, `deep_target_east = (68, 162)`.
- **Cele rajdów ekonomicznych Szakali (`eco_raid_targets`):**
  - `(32, 118)` (eko P3), `(76, 120)` (eko P1), `(32, 168)` (eko P2), `(76, 172)` (eko P4).
- **Korytarze wyrębu lasu przez Saperów:**
  - `north_breach_box = (75, 95, 80, 105)` (wymiar `6×11` kratek — Fala 9 w `51:00`),
  - `east_breach_box = (99, 137, 109, 142)` (wymiar `11×6` kratek — Fala 12 w `67:30`).
- **Sanktuarium Balansu:**
  - Środek komnaty: `(6, 150)` (`sanctuary_cx = 6, sanctuary_cy = 150`, obrys klifów `x = 3..9, y = 145..155`).
  - Górna flaga (`pad_up_box` — Trudniej): `(4, 146)` do `(8, 147)`.
  - Dolna flaga (`pad_down_box` — Łatwiej): `(4, 153)` do `(8, 154)`.
- **Układ Szlaku Handlowego (Południe):**
  - Plac pod Targowiska graczy w lewym dolnym rogu: `x = 2..24, y = 176..198`.
  - 10-kratkowy korytarz wzdłuż dolnej krawędzi: `x = 2..199, y = 189..199` (brukowana droga na `y = 194`).
  - Po ukończeniu Q1: pojedynczy sojuszniczy Market (`P2`) staje w prawym dolnym rogu na `(195, 194)`.

---

## 3. Co już działa i zostało potwierdzone w grze (STREFA CHRONIONA — zakaz przebudowy)

1. **Dwuwarstwowa siatka antykolizyjna `SafeMapGrid` (`horde_map.py`):**
   - Rozdział `occupied_tiles` (dokładne obrysy obiektów + spiralne szukanie wolnego pola w `place_unit`) od `no_tree_zones` (strefy ochronne sprawdzane wyłącznie przez `populate_forest_trees`).
   - Dwuprzebiegowe wygładzanie elewacji `apply_smooth_elevation(mm)` wymuszające warunek $|\Delta h| \le 1$.
2. **Szczelne lasy i przełęcze (`horde_map.py`):**
   - Fizyczne sadzenie obiektów drzew (`TREE_OAK_ID = 349`, `TREE_PINE_ID = 350`) na pełnym zakresie `0..MAP_SIZE-1`.
   - Wycinanie przełęczy prostokątem `mark_no_trees_box(gx - 6, gy - 6, gx + 6, gy + 6)` i stawianie Wzmocnionej Palisady (`FORTIFIED_PALISADE_ID = 119`) od `-7` do `+7` z `clear_trees_around=False`.
3. **Stały punktowy podgląd budynków zadań (`reveal_building_center_permanent`):**
   - Na środku każdego z 4 Questów i 6 Settlementów stoi stały obiekt `MAP_REVEALER_ID = 837` należący do `PlayerId.ONE` z zasięgiem widzenia ustawionym w `t_init` na `ATTR_LINE_OF_SIGHT = 4`.
   - W detektorach zbliżeniowych garnizonów (`add_guarded_camp_with_leash`) warunek `objects_in_area` wymaga `quantity = 2` dla `PlayerId.ONE` (1 Revealer + 1 jednostka P1) oraz `quantity = 1` dla `PlayerId.TWO..FOUR`.
4. **Ochrona przed błędem przepełnienia `uint8` (`5 + 247` ataku):**
   - Jednostki wręcz mają modyfikowany wyłącznie `armor_class = 4` (Base Melee), a jednostki strzeleckie wyłącznie `armor_class = 3` (Base Pierce).
5. **Kolejność inicjalizacji statystyk AI (`0:01` Ery -> `0:03` Mutacje):**
   - Ery AI (`TECH_FEUDAL_AGE`, `TECH_CASTLE_AGE`, `TECH_IMPERIAL_AGE`) są badane w `0:01` (`t_init`), a modyfikacje statystyk 6 klas specjalnych (`modify_attribute`) w osobnym triggerze `01b_Apply_Specialized_Unit_Archetypes` z warunkiem `timer = 3`.
6. **Komunikacja UI i Flary (`send_highlight_chat`, `set_as_objective`, `populate_ingame_scenario_descriptions`):**
   - Brak `display_timer` i `display_instructions`. Powiadomienia idą przez `send_chat` + efekt `flare` + utworzenie obiektu `FLARE_UNIT_ID = 112`. Lista zadań w prawym górnym rogu jest sortowana malejąco po `description_order`.

---

## 4. Lista znanych błędów (Bugs) z playtestów i audytu technicznego

### BUG-01 [KRYTYCZNY — WDROŻONY / NAPRAWIONY w Etapie 3A+3B]: Zwiększenie trudności o `+1` na starcie gry uruchamia Falę 14 (Endgame Endless) już w ~6. minucie gry przed Falą 1
- **Objaw w grze:** Gdy na początku meczu Gracz 1 przesunie Króla w Sanktuarium Balansu na górną flagę (`+1`), po 5,5 minuty (w ~6. minucie gry, jeszcze przed Falą 1 z `8:30`!) na bazę uderzają Huskarle, specjalni Berserkerzy, Siege Ramy, Moździerze Oblężnicze, Paladyni, Imamowie i Żelazne Słonie 1450 HP, a atak ten powtarza się cyklicznie co 5,5 minuty.
- **Miejsce w kodzie:** `setup_init_aura_and_waves()` w `horde_waves.py` oraz `wire_difficulty_transition()` w `horde_quests.py`.
- **Przyczyna techniczna:**
  1. Dla Fali 14 (`is_endless_last = True`) czas warunku `timer` został podmieniony z czasu fali (`4710s` = `78:30`) na interwał pętli Endless (`cond_time = BALANCE["wave_interval_sec"] = 330s`).
  2. Warstwy `03_W14_{s_key}_TierP1` (`enabled=False`, `looping=True`, `timer=330`) zostały dopisane do globalnej listy `tier_p1_wave_triggers`.
  3. Gdy Gracz 1 wszedł na flagę `+1` w 1. minucie gry, trigger `09_Diff_Up_0_to_P1` wykonał `activate_trigger` na wszystkich triggerach z listy `tier_p1_wave_triggers` — **włączając od razu pętlowe triggery Fali 14 (`TierP1`)**, które wybuchły po 330 sekundach!
  4. Ponadto w silniku AoE2: DE warunek `timer` w triggerze z `enabled=False` nie odlicza czasu od `0:00`, lecz startuje od `0` dopiero w momencie aktywacji triggera, a ponowne wykonanie `activate_trigger` na już wykonanych falach niepętlowych uruchamia je po raz drugi.

### BUG-02 [KRYTYCZNY — WDROŻONY / NAPRAWIONY w Etapie 1A]: Moździerze Oblężnicze (`SIEGE_ONAGER_ID = 588`) wycinają drzewa przy bramach podczas zwykłego ostrzału
- **Objaw w grze:** Moździerze Oblężnicze (`P6`) strzelając w bramy, palisady i wieże graczy niszczą sąsiednie drzewa pasa leśnego, wybijając nieplanowane dziury w lesie.
- **Miejsce w kodzie:** `01b_Apply_Specialized_Unit_Archetypes` w `horde_waves.py`.
- **Przyczyna techniczna:** Jednostka `Siege Onager` (`588`) ma w silniku Genie domyślnie `Blast Attack Level = 1` (pociski ścinają drzewa, które mają `Blast Defense Level = 1`). Aby pociski Moździerza raniły jednostki i budynki, ale nie ścinały drzew (tak jak u zwykłego Mangonela), należy ustawić atrybut **`ATTR_BLAST_ATTACK_LEVEL = 44`** na wartość **`2`** *(UWAGA: atrybut o ID `21` to `AMOUNT_OF_1ST_RESOURCE_STORAGE` — nie wolno mylić `21` z `44`!)*.

### BUG-03 [KRYTYCZNY — WDROŻONY / NAPRAWIONY w Etapie 3B+3C]: Główne warstwy Fali 14 (`Base`, `TierM1`, `Tier0`) są martwe i nigdy się nie aktywują
- **Objaw w grze:** W `78:30` (Fala 14) na domyślnym poziomie `0` główne oddziały z 6 Settlementów w ogóle się nie pojawiają (wychodzą tylko Szakale, atak na Trade Line i Saperzy).
- **Miejsce w kodzie:** `setup_init_aura_and_waves()` w `horde_waves.py` (pętla `for layer_name, l_comp, start_enabled, layer_list in layer_specs:`).
- **Przyczyna techniczna:** Dla Fali 14 `is_endless_last = True`, więc dla warstw `Base`, `TierM1` i `Tier0` ustawiane jest `start_enabled = not is_endless_last` (`False`), a warunek tworzenia triggera uzbrajającego pętlę Endless brzmi `if is_endless_last and start_enabled:` (`True and False`), przez co triggery `03_Enable_Endless_*` nigdy nie powstają.

### BUG-04 [WYSOKI — WDROŻONY / NAPRAWIONY w Etapie 2]: Błąd zaokrąglania w `scale_comp()` gubiący jednostki specjalne nawet na domyślnym Poziomie `0` (`100%`)
- **Objaw w grze:** Dla grup liczących `2` jednostki w definicji fali (np. 2 Snajperów w Fali 3, 2 Arcymagów w Falach 8–11, 2 Moździerze w Falach 8–11, 2 Żelazne Słonie w Falach 7–8) na **każdym poziomie trudności od `-2` do `+2` spawnuje się tylko 1 jednostka**. Z kolei dla `3` jednostek na poziomie `0` spawnuje się `4`.
- **Miejsce w kodzie:** `scale_comp()` w `horde_waves.py`.
- **Przyczyna techniczna:** Niezależne zaokrąglanie `round()` (ties-to-even) pięciu warstw (`0.60`, `0.20`, `0.20`, `0.25`, `0.25`). Dla `cnt = 2`: `round(1.2) = 1`, `round(0.4) = 0`, `round(0.4) = 0`, `round(0.5) = 0`, co daje w sumie `1` jednostkę zamiast `2` lub `3`.

### BUG-05 [WYSOKI — WDROŻONY / NAPRAWIONY w Etapie 5]: Błędy w cyklu Globalnej Aury Arcymaga Tarczy (`02a` / `02d`) — blokada wyłączenia przez obozowego Imama oraz ryzyko kumulacji `+60/+60` pancerza
- **Objaw w grze:**
  1. Po zabiciu Imama (`P7`) przed Bramą Centralną `(104, 114)` jednostki Hordy (`P5–P8`) nie tracą bonusu `+30/+30` pancerza, jeśli w obozie `G2_Mages` `(148, 72)` został wcześniej zespawnowany drugi Imam.
  2. Jeśli Imam z Fali 4 przeżyje pod bramą do nadejścia Fali 5, fala ponownie wykonuje `activate_trigger(t_shield_on)`, nakładając bonus `+30/+30` po raz drugi (`+60/+60` pancerza).
- **Miejsce w kodzie:** `t_shield_on` (`02a`) oraz `t_shield_off` (`02d`) w `horde_waves.py`.
- **Przyczyna techniczna:** `t_shield_off` używa globalnego warunku `own_fewer_objects(..., quantity=0)` na całą mapę zamiast sprawdzenia strefy 25 kratek wokół Bramy Centralnej (`objects_in_area` z `inverted=1`), a triggery fal bezwarunkowo wywołują `activate_trigger(t_shield_on)`.

### BUG-06 [ŚREDNI — WDROŻONY / NAPRAWIONY w Etapie 6A]: Smycz terytorialna (`Garrison_Leash_*`) i detektory nie są wyłączane po zniszczeniu Questu lub Settlementu
- **Objaw w grze:** Gdy fala Hordy przechodzi w pobliżu ruin wcześniej zniszczonego Settlementu lub Questu, działający w pętli co 3s trigger `Garrison_Leash_*` przechwytuje jednostki z fali i zawraca je rozkazem `attack_move` do środka ruin. Ponadto zburzenie budynku z daleka zostawia uzbrojony detektor.
- **Miejsce w kodzie:** `add_guarded_camp_with_leash()` w `horde_waves.py` oraz `t_q1..t_q4` i `t_destroy` w `horde_quests.py`.

### BUG-07 [ŚREDNI — WDROŻONY / NAPRAWIONY w Etapie 4]: Kumulacyjny dryf HP przy przełączaniu poziomów ujemnych (`-1`, `-2`) w Sanktuarium Balansu
- **Objaw w grze:** Kilkukrotne przejście `0 -> -1 -> 0` w Sanktuarium Balansu trwale zmienia HP jednostek wroga.
- **Miejsce w kodzie:** `apply_king_reset_and_safe_stat_shift()` w `horde_quests.py`.
- **Przyczyna techniczna:** Użycie `Operation.MULTIPLY` z `0.85` przy zejściu w dół i `1.18` przy powrocie w górę ($0.85 \times 1.18 = 1.003$ oraz obcinanie części ułamkowych po każdej operacji).

### BUG-08 [ŚREDNI — WDROŻONY / NAPRAWIONY w Etapie 4]: Opóźnienie pierwszego ticku wszystkich 3 biegów eskalacji o +5 minut
- **Objaw w grze:** Pierwszy bonus eskalacji z `20:00` wpada dopiero w `25:00`, drugi bieg z `45:00` dopiero w `50:00`, a trzeci z `55:00` dopiero w `60:00`.
- **Miejsce w kodzie:** `04a_Enable_Escalation_At_20m` .. `04f_Endgame_Horde_Escalation_Every_5m` w `horde_waves.py`.
- **Przyczyna techniczna:** Trigger włączający (`04a`, `04c`, `04e`) jedynie aktywuje trigger pętlowy (`04b`, `04d`, `04f` z `timer=300`), który odlicza swoje pierwsze 300s dopiero od momentu aktywacji.

### BUG-09 [ŚREDNI — WDROŻONY / NAPRAWIONY w Etapie 6B]: Kolizja Baszt (`KEEP`) i wież strażniczych Karawanseraju (`Q1`) ze szlakiem handlowym
- **Objaw w grze:** Po zburzeniu Targowiska Q1 `(154, 190)` dwie boczne wieże strażnicze P5 na `(149, 187)` i `(159, 187)` nadal ostrzeliwują wozy handlowe w korytarzu `y = 189..199`, a Baszty (`KEEP`) stawiane na `y = 190` wchodzą w światło drogi handlowej.
- **Miejsce w kodzie:** `06_Quest1_Build_Trade_Wall_And_Pop` w `horde_quests.py`.

### BUG-10 [NISKI — WDROŻONY / NAPRAWIONY w Etapie 1B]: Duplikacja `wave_definitions` i zanieczyszczenie słownika `ctx`
- **Miejsce w kodzie:** W `horde_waves.py` znajduje się zduplikowana tablica `wave_definitions`, a słownik `ctx` przekazuje z `horde_map.py` i `horde_waves.py` zmienne tymczasowe z pętli (`ai_p`, `h_p`, `m_id`, `r_id`, `s_key`, `sx`, `sy`, `u_id`, `wx`).

---

## 5. Definicja Bazowego HP, Centralny Rejestr Jednostek i Balans

### Definicja `base_hp` w `ENEMY_UNIT_REGISTRY`
Wartość `base_hp` w rejestrze oznacza **bazowe HP jednostki w tym scenariuszu po zastosowaniu jej archetypu specjalnego w `01b` i ulepszeń ery Imperialnej (oraz `Bloodlines` dla jednostek konnych `P7`), ale przed modyfikacją Sanktuarium Balansu, eskalacją czasową, adaptacją Questów i Furią Settlementów**.  
Na podstawie `base_hp` dla każdej jednostki ze skalowaniem HP (`scales_hp = True`) wyliczana jest stała, odwracalna delta całkowita dla poziomów ujemnych (`-1` oraz `-2`):
$$\text{hp\_delta\_down} = \max\left(2, \left\lfloor \frac{\text{base\_hp} \times 15 + 50}{100} \right\rfloor\right)$$
Dzięki temu przejście `0 -> -1` odejmuje dokładnie `hp_delta_down` (ok. 15% bazowego HP), `0 -> -2` odejmuje `2 * hp_delta_down` (ok. 30% bazowego HP), a powrót `-2 -> -1 -> 0` dodaje dokładnie te same liczby całkowite (zerowy dryf).

### Problemy balansowe i pokrycia jednostek do naprawy:
1. **Ochrona niskiego ataku Żelaznego Słonia-Tanka (`ELITE_BATTLE_ELEPHANT_ID = 1134`, P8):**
   - Żelazny Słoń ma zadawać dokładnie `3` obrażenia jednostkom (`armor_class = 4`) i `+220` budynkom (`armor_class = 11, 21`).
   - Musi mieć ustawione `attack_class = None` oraz `scales_hp = True` w `ENEMY_UNIT_REGISTRY` (aby żadne źródło — ani eskalacja, ani Sanktuarium, ani Questy, ani Furia Settlementów — nie zwiększało mu ataku w jednostki), a w triggerach Kuźni AI (`01d`, `01e`, `01f`) po zbadaniu `Forging` / `Iron Casting` / `Blast Furnace` przez `P8` jego atak w klasie `4` musi być natychmiast resetowany do `3`.
2. **Jednolita funkcja modyfikacji statystyk we wszystkich modułach:**
   - Zabrania się utrzymywania lokalnych list `enemy_melee_units` i `enemy_ranged_units` w `horde_quests.py`. Wszystkie bonusy w `horde_waves.py` i `horde_quests.py` muszą wywoływać wspólne funkcje oparte wyłącznie na `ENEMY_UNIT_REGISTRY`.
3. **Uzupełnienie list jednostek/budynków graczy (`Q2` i `Q4`) oraz stopniowanie Furii Settlementów (`Grade 1–3`):**
   - W `Q2` dopisać `ELITE_STEPPE_LANCER` (`1372`) i `HEAVY_CAMEL_RIDER` (`330`).
   - W `Q4` dopisać `BuildingInfo.SIEGE_WORKSHOP.ID` (`49`), `MILITIA` (`74`) i linię `EAGLE_WARRIOR` (`751`, `753`, `752`), a docelowe HP Imama po `Q4` ustawić na `120`.

---

## 6. Twarde reguły techniczne silnika AoE2: DE i `AoE2ScenarioParser`

1. **Zakaz efektów wywołujących crash C++ (`AoE2DE_s.exe`):**
   - **NIGDY** nie używaj `new_effect.display_timer`, `new_effect.display_instructions` ani ujemnego `new_effect.tribute`. Do zasobów i limitu populacji (`RES_BONUS_POP_CAP = 32`) używaj wyłącznie `modify_resource` z `Operation.ADD`.
2. **Zabezpieczenie przed `uint8` underflow (`5 + 247` ataku) w `modify_attribute`:**
   - Nigdy nie modyfikuj `armor_class = 4` (melee) na jednostkach strzeleckich ani `armor_class = 3` (pierce) na jednostkach wręcz.
   - Nigdy nie odejmuj ataku ani pancerza (`Operation.SUBTRACT`) poniżej wartości bazowych.
3. **Oficjalne ID atrybutów silnika Genie:**
   - `ATTR_HIT_POINTS = 0`, `ATTR_LINE_OF_SIGHT = 1`, `ATTR_MOVEMENT_SPEED = 5`, `ATTR_ARMOR = 8`, `ATTR_ATTACK = 9`, `ATTR_ATTACK_RELOAD_TIME = 10`, `ATTR_MAXIMUM_RANGE = 12`, `ATTR_WORK_RATE = 13`, `ATTR_MINIMUM_RANGE = 20`, `ATTR_BLAST_WIDTH = 22`, `ATTR_SEARCH_RADIUS = 23`, `ATTR_HERO_STATUS = 40`, **`ATTR_BLAST_ATTACK_LEVEL = 44`**, `ATTR_REGENERATION_RATE = 109`.
4. **Parametry `objects_in_area` w `AoE2ScenarioParser`:**
   - Warunek `new_condition.objects_in_area` przyjmuje `source_player`, `object_list` (ID jednostki), `area_x1`, `area_y1`, `area_x2`, `area_y2`, `quantity`, `inverted`. Nie przekazuj nieistniejącego argumentu `object_list_unit_id` do `objects_in_area`.
5. **Zgodność z linterem Ruff:**
   - Kod musi przechodzić `ruff check` bez ostrzeżeń (`I001`, `F401`, `PIE808`, `PLR1730`, `SIM102`, `RUF046`, `SIM210`, `S110`, `BLE001`).

---

## 7. Historia wdrożeń i weryfikacji binarnej

### Wdrożenie 1: Etap 0 oraz Etap 1A (`BUG-02`) [STATUS: OK]
- **Commit bazowy:** `8ed70e5a390b399aab71a059a624b7956f18bd8b`.
- **Preflight Check (Etap 0):** Serializacja `trigger_active` round-trip powiodła się (`Conds: 1 Target: True`).
- **BUG-02 (Etap 1A):** Ustawiono `ATTR_BLAST_ATTACK_LEVEL = 44` na wartość `2` dla `SIEGE_ONAGER_ID` (`PlayerId.SIX`) w triggerze `01b_Apply_Specialized_Unit_Archetypes`.
- **Weryfikacja binarna:** Potwierdzono obecność efektu `modify_attribute` (`object_attributes == 44`, `quantity == 2`) w wyjściowym pliku `.aoe2scenario`.

### Wdrożenie 2: Etap 1B (`BUG-10`, Balans), Etap 2 (`BUG-04`), Etap 6B (`BUG-09`) [STATUS: OK]
- **BUG-10 & Balans (Etap 1B):**
  - Utworzono dataclasses `WaveDefinition` i `EnemyUnitSpec` oraz `ENEMY_UNIT_REGISTRY` (26 typów jednostek wroga) w `horde_config.py`.
  - Zunifikowano funkcję `add_enemy_combat_buff` (wyłącznie `ENEMY_UNIT_REGISTRY`).
  - W triggerach Kuźni AI `01d`, `01e`, `01f` dodano natychmiastowy reset ataku Żelaznego Słonia (`1134`) do `3` (`BALANCE["tank_unit_atk"]`).
  - Usunięto 100 linii zduplikowanej tablicy `wave_definitions` z `horde_waves.py` oraz niepotrzebne klucze `enemy_melee_units` / `enemy_ranged_units` z `ctx`.
- **BUG-04 (Etap 2):**
  - Zaimplementowano deterministyczny algorytm `scale_comp_for_level` z metodą największych reszt, `HALF_UP` i gwarancją `mandatory_min_one`.
- **BUG-09 (Etap 6B):**
  - W `06_Quest1_Build_Trade_Wall_And_Pop` dodano `remove_object` dla wrogich Guard Tower P5 na `(145..165, 182..195)`.
  - Przesunięto mur na `y = 186` i baszty Keep na `y = 184`.
  - W `horde_map.py` zabezpieczono pas `x = 104..199, y = 183..188` przed spawnem drzew i nierównościami terenu.
- **Weryfikacja binarna:**
  - `01d`, `01e`, `01f`: potwierdzono reset ataku Słonia do `3`.
  - Testy jednostkowe `scale_comp_for_level`: puste składy `[]`, poziom `0` zachowany, poziom `+1` poprawnie zaokrąglony w górę, zachowanie `mandatory_min_one`.
  - `06_Quest1`: potwierdzono obecność `remove_object` (effect_type 15) dla wież P5 oraz 95 segmentów muru na `y = 186` i 6 baszt Keep na `y = 184`.
  - Analiza obiektów mapy: dokładnie 0 drzew w pasie `x = 105..199, y = 183..188`.


### Wdrożenie 4: Etap 4 (`BUG-07`, `BUG-08`), Etap 5 (`BUG-05`), Etap 6A (`BUG-06`) [STATUS: OK]
- **Etap 4 (Odwracalne delty HP i korekta 1. ticku eskalacji – naprawa `BUG-07`, `BUG-08`):**
  - W `apply_king_reset_and_safe_stat_shift` w `horde_quests.py` zastąpiono mnożenie floatami (`0.85` / `1.18`) stałymi liczbami całkowitymi `Operation.SUBTRACT` / `Operation.ADD` z `spec.hp_delta_down` z `ENEMY_UNIT_REGISTRY`.
  - W `horde_waves.py` w triggerach `04a_Enable_Escalation_At_20m`, `04c_Enable_LateGame_Escalation_At_45m` oraz `04e_Enable_Endgame_Escalation_At_55m` dodano natychmiastowe nałożenie pierwszego buffa `add_enemy_combat_buff` oraz powiadomienie czatu (punkty czasowe `20:00`, `45:00`, `55:00`).
- **Etap 5 (Dwustanowy automat Aury Arcymaga – naprawa `BUG-05`):**
  - W `horde_waves.py` triggery `02a` i `02d` przebudowano w automat skończony oparty na liście jednostek z `spec.receives_mage_shield` z `ENEMY_UNIT_REGISTRY`.
  - `02a_Mage_Global_Horde_Shield_On` ustawiono na starcie jako `enabled = True`, `looping = False`.
  - `02d_Mage_Global_Horde_Shield_Off` ustawiono na starcie jako `enabled = False`, `looping = False` z warunkiem `objects_in_area` (Imam P7 na 25 kratek wokół Bramy Centralnej) z `inverted = 1`, który po zniknięciu Imama zdejmuje pancerz i re-aktywuje `02a`.
  - Usunięto z triggerów fal jakiekolwiek aktywacje `02a`.
- **Etap 6A (Dezaktywacja garnizonów i smyczy po zniszczeniu – naprawa `BUG-06`):**
  - `add_guarded_camp_with_leash` zwraca teraz `(t_spawn, t_leash, detect_triggers)`, a uchwyty 10 obozów są przekazywane przez `ctx["camp_leash_handles"]`.
  - W `horde_quests.py` zdefiniowano `deactivate_camp_handles` i podpięto wyłączenie spawnu, smyczy oraz 4 detektorów graczy pod zniszczenie każdego z 4 Questów (`t_q1`, `t_q2`, `t_q3_unlock`, `t_q4`) oraz 6 Settlementów (`05_Settlement_Destroyed_*`).
  - Oczyszczono słownik zwracany przez `horde_map.py` ze zmiennych tymczasowych pętli.
- **Weryfikacja binarna wyjściowego `.aoe2scenario`:**
  - Przetestowano pełną symulację cyklu trudności `0 -> +1 -> +2 -> +1 -> 0 -> -1 -> -2 -> -1 -> 0` (928 efektów `modify_attribute`): dla wszystkich 26 jednostek z rejestru wykazano **dokładnie zerowy dryf statystyk ($\Delta\text{HP} == 0, \Delta\text{Atk} == 0$)**.
  - Potwierdzono obecność efektów `modify_attribute` oraz czatu w `04a`, `04c`, `04e` dla natychmiastowego pierwszego ticku eskalacji.
  - Potwierdzono stany początkowe automatu Arcymaga (`02a`: `enabled=1, looping=0`, `02d`: `enabled=0, looping=0` z `inverted=1` na obszarze Bramy Centralnej) oraz brak jakichkolwiek aktywacji `02a` z poziomu fal `03_W*`.
  - Potwierdzono deaktywację wszystkich 10 garnizonów (60 powiązań deaktywujących: 10× `Garrison_Spawn`, 10× `Garrison_Leash`, 40× `Garrison_Detect`).



### Wdrożenie 4: Etap 4 (`BUG-07`, `BUG-08`), Etap 5 (`BUG-05`), Etap 6A (`BUG-06`) [STATUS: OK]
- **Etap 4 (Odwracalne delty HP i korekta 1. ticku eskalacji – naprawa `BUG-07`, `BUG-08`):**
  - W `apply_king_reset_and_safe_stat_shift` w `horde_quests.py` zastąpiono mnożenie floatami (`0.85` / `1.18`) stałymi liczbami całkowitymi `Operation.SUBTRACT` / `Operation.ADD` z `spec.hp_delta_down` z `ENEMY_UNIT_REGISTRY`.
  - W `horde_waves.py` w triggerach `04a_Enable_Escalation_At_20m`, `04c_Enable_LateGame_Escalation_At_45m` oraz `04e_Enable_Endgame_Escalation_At_55m` dodano natychmiastowe nałożenie pierwszego buffa `add_enemy_combat_buff` oraz powiadomienie czatu (punkty czasowe `20:00`, `45:00`, `55:00`).
- **Etap 5 (Dwustanowy automat Aury Arcymaga – naprawa `BUG-05`):**
  - W `horde_waves.py` triggery `02a` i `02d` przebudowano w automat skończony oparty na liście jednostek z `spec.receives_mage_shield` z `ENEMY_UNIT_REGISTRY`.
  - `02a_Mage_Global_Horde_Shield_On` ustawiono na starcie jako `enabled = True`, `looping = False`.
  - `02d_Mage_Global_Horde_Shield_Off` ustawiono na starcie jako `enabled = False`, `looping = False` z warunkiem `objects_in_area` (Imam P7 na 25 kratek wokół Bramy Centralnej) z `inverted = 1`, który po zniknięciu Imama zdejmuje pancerz i re-aktywuje `02a`.
  - Usunięto z triggerów fal jakiekolwiek aktywacje `02a`.
- **Etap 6A (Dezaktywacja garnizonów i smyczy po zniszczeniu – naprawa `BUG-06`):**
  - `add_guarded_camp_with_leash` zwraca teraz `(t_spawn, t_leash, detect_triggers)`, a uchwyty 10 obozów są przekazywane przez `ctx["camp_leash_handles"]`.
  - W `horde_quests.py` zdefiniowano `deactivate_camp_handles` i podpięto wyłączenie spawnu, smyczy oraz 4 detektorów graczy pod zniszczenie każdego z 4 Questów (`t_q1`, `t_q2`, `t_q3_unlock`, `t_q4`) oraz 6 Settlementów (`05_Settlement_Destroyed_*`).
  - Oczyszczono słownik zwracany przez `horde_map.py` ze zmiennych tymczasowych pętli.
- **Weryfikacja binarna wyjściowego `.aoe2scenario`:**
  - Przetestowano pełną symulację cyklu trudności `0 -> +1 -> +2 -> +1 -> 0 -> -1 -> -2 -> -1 -> 0` (928 efektów `modify_attribute`): dla wszystkich 26 jednostek z rejestru wykazano **dokładnie zerowy dryf statystyk ($\Delta\text{HP} == 0, \Delta\text{Atk} == 0$)**.
  - Potwierdzono obecność efektów `modify_attribute` oraz czatu w `04a`, `04c`, `04e` dla natychmiastowego pierwszego ticku eskalacji.
  - Potwierdzono stany początkowe automatu Arcymaga (`02a`: `enabled=1, looping=0`, `02d`: `enabled=0, looping=0` z `inverted=1` na obszarze Bramy Centralnej) oraz brak jakichkolwiek aktywacji `02a` z poziomu fal `03_W*`.
  - Potwierdzono deaktywację wszystkich 10 garnizonów (60 powiązań deaktywujących: 10× `Garrison_Spawn`, 10× `Garrison_Leash`, 40× `Garrison_Detect`).