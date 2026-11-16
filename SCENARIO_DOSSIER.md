# SCENARIO DOSSIER — Kroniki Rubieży: Horda i Ekspedycje (v7.0.3)

- **Plik wynikowy:** `Kroniki_Rubiezy_Horda_Coop.aoe2scenario` (`243 043` B, `969` triggerów, `5350` obiektów startowych: `P0=5142, P1=37, P2=18, P3=26, P4=39, P5=13, P6=12, P7=10, P8=53`) | **Rozmiar mapy:** `200×200` (Olbrzymia) | **Horyzont rozgrywki:** 60–90 min
- **Struktura drużyn:** 8 graczy aktywnych — Drużyna 1 (`P1–P4` Ludzie, `human=True`, `lock_civ=False`, `allied_victory=True`) vs Drużyna 2 (`P5–P8` AI, `human=False`, `lock_civ=True`, `allied_victory=True`, zasoby startowe `0/0/0/0`)
- **Wymagane ustawienia lobby:**
  - Tryb: `Custom Scenario` | AI Difficulty: **`Extreme`** (wymagane dla poprawnego wyboru celów przez jednostki AI po skryptowym rozkazie)
  - Widoczność: `Normal` | Limit populacji: `200` (dynamicznie rośnie do `230` po Q1 i `250` po Q3) | Zasoby/Wiek startowy: `Standard`
  - `Lock Teams = Off` (wymagane dla `01_Init_Diplomacy_And_Cartography`), `Lock Speed = On`, `All Techs = Off`, `Allow Cheats = Off`
- **Warunek zwycięstwa (Czterofazowy Boss Fight `07a -> 07b -> 07c -> 07d` + Tarcza Gwardii Słoni):**
  - **`07a_All_Settlements_Destroyed_Boss_Warning` (`enabled=True`):** zniszczenie wszystkich 6 głównych budynków Settlementów (`G1_North`, `G1_East`, `G2_Snipers`, `G2_Mages`, `G3_North`, `G3_East`) dezaktywuje eskalację (`04a–04f`), wszystkie triggery Trybu Endless oraz wszystkie triggery Zegara Fal (`00_Wave_Timer_UI_*` / `Tick_*`), aktywuje nagłówek `00_Wave_Timer_Boss_Banner`, czyści `kill_object` (`ObjectType.BUILDING`) budynki `P1–P4` na polanie `(110..124, 108..128)`, stawia `MAP_REVEALER` dla `P1–P4` na `(104, 114)` i `(116, 114)`, odtwarza dźwięk i flarę `(116, 114)`, ogłasza 60-sekundowe ostrzeżenie na odwrót armii i aktywuje `07b`
  - **`07b_Spawn_Final_Boss_Wave` (`enabled=False`):** po upływie `timer=60s` spawnuje szturm na **3 bramy**: przed Bramą Centralną `(116, 114) -> (54, 146)` armię `P8` (`1x Wielki Chan Subotai [698]`, `6x Iron Elephant`, `16x Paladin`, `4x Siege Ram`) oraz `(118, 122) -> (54, 146)` `2x Imam` `P7`, na Bramę Północną `(68, 60) -> (48, 136)` `P8` (`10x Paladin`, `10x Heavy Cav Archer`, `2x Siege Ram`) i na Bramę Wschodnią `(116, 162) -> (68, 152)` `P8` (`10x Paladin`, `10x Heavy Cav Archer`, `2x Siege Ram`), puszcza flarę `(116, 114)` i aktywuje `07c`, `07b_Boss_Elephant_Guard_Heal` oraz `07b_Boss_Elephants_Slain_Disable_Heal`
  - **`07b_Boss_Elephant_Guard_Heal` (`enabled=False, looping=True`) / `07b_Boss_Elephants_Slain_Disable_Heal` (`enabled=False, looping=False`):** co `3s` leczy `FINAL_BOSS_HERO_ID` (`P8`) o **`+180 HP`**, dopóki w strefie bitwy **`(40, 90, 135, 175)`** żyje `≥1` `ELITE_BATTLE_ELEPHANT_ID` (`P8`); po wybiciu Żelaznych Słoni ze strefy `(40, 90, 135, 175)` (`timer=10` + `inverted=True`) wyłącza regenerację i ogłasza to na czacie z flarą `(104, 114)`
  - **`07c_Confirm_Boss_Spawned` (`enabled=False`):** warunek `objects_in_area` (`0..199`, `P8`, `FINAL_BOSS_HERO_ID`, `ObjectState.ALIVE`, `quantity=1`, bez inwersji) potwierdza fizyczną obecność żywego Chana na mapie i aktywuje `07d`
  - **`07d_Victory_Final_Boss_Defeated` (`enabled=False`, `order=99`):** po upływie `5s` od potwierdzenia i braku żywego `FINAL_BOSS_HERO_ID` (`P8`, `ObjectState.ALIVE`, `inverted=1`) na całej mapie `0..199` wyłącza pętlę leczenia gwardii, `07b_Boss_Elephants_Slain_Disable_Heal`, `00_Wave_Timer_Boss_Banner` i ogłasza `declare_victory` dla `P1–P4`
- **Warunek porażki (`08_Defeat_Citadel_Lost`):** zniszczenie Cytadeli Sojuszu `P2` (`Feitoria` na `(54, 146)`) -> `declare_victory` dla `P5–P8`
- **Interfejs panelu Celów (`Objectives`):**
  - `order=210..207`: **Skrót zasad `TL;DR` w oknie `Objectives`** (`00_TLDR_Modal_1_Cel` [`header=1, order=210`], `00_TLDR_Modal_2_Role` [`209`], `00_TLDR_Modal_3_Wyprawy` [`208`], `00_TLDR_Modal_4_Wrogowie` [`207`]) — `display_as_objective=1, display_on_screen=0, timer=999999` (widoczne po kliknięciu zakładki `Objectives`, bez zaśmiecania stałego HUD-u podczas rozgrywki; to samo `TL;DR` umieszczone też na początku zakładki `Hints`)
  - `order=110`: Zegar Fali (`00_Wave_Timer_UI_000..168`) — statyczne banery (`timer=999999`) przełączane co `30s` od `0:00` do `84:00` (`5040s`) oraz `00_Wave_Timer_Boss_Banner` aktywowany w `07a`; alerty na czacie na `-60s` przed każdą z Fal 1–14 i startem Endless (`84:00`) oraz dodatkowy alert `-30s` przed Falą 1 (`8:00`)
  - `order=109`: Poziom Trudności (`State_Diff_Lvl_M2..P2`, lokalizacja `(4,138)`) aktualizowany na żywo przez Sanktuarium Balansu
  - `order=100..96`: Nagłówek Questów (`100`) i 4 Questy (`Q1=99`, `Q2=98`, `Q3=97`, `Q4=96` z etapami `Stage1 -> Stage2`)
  - `order=99` *(aktywowany w `07c`)*: Finałowy cel zgładzenia Wielkiego Chana Subotaia (`07d_Victory_Final_Boss_Defeated`)
  - `order=90..84`: Nagłówek Settlementów (`90`) i 6 Settlementów (`G1_N=89`, `G1_E=88`, `G2_S=87`, `G2_M=86`, `G3_N=85`, `G3_E=84`)

---

## A. Mapa i układ przestrzenny (200×200)

### 1. Konstrukcja i bariery Twierdzy Sojuszu (SW: `x=0..104, y=100..199`)
- **System antykolizyjny generacji:** dwuwarstwowy rozkład obiektów (`occupied_tiles` dla budynków/wody/murów/drzew/jednostek oraz `no_tree_zones` wokół dróg, klifów, baz i stref spawnu); wygładzanie elewacji całej mapy gwarantuje $|\Delta h| \le 1$ między sąsiednimi kafelkami
- **Bariera północna (`y=100`):** wzgórza (`flat_radius=4, height=3`) co `8` kratek dla `x=0, 8, ..., 104` z przerwą dla `72 <= x <= 84`; pas lasu `FOREST_PINE` na `(0..108, 95..105)`
- **Bariera wschodnia (`x=104`):** wzgórza (`flat_radius=4, height=3`) co `8` kratek dla `y=100, 108, ..., 180` z przerwą dla `134 <= y <= 146`; pas lasu `FOREST_PINE` na `(99..109, 95..199)`
- **Cytadela Sojuszu (`P2`):** `Feitoria` (`5×5`, ID `1021`) na `(54, 146)` z buforem bez drzew `r=3`; w `0:00` dostaje `+3000 HP` oraz `+20` `RES_BONUS_POP_CAP` (`id=32`) dla `P2`
- **Sanktuarium Balansu (`(4, 138)` — pełna izolacja na zachodniej krawędzi):** szczelna komnata `7×11` (`x=1..7, y=133..143`, wnętrze `x=2..6, y=134..142` `ROAD`, `elev=0`, strefa bez drzew `r=6`):
  - Szczelny obwód klifów `ROCK_CLIFF_ID` (`623`) na podłożu `DIRT_3` (bez luk: `x in {1,7}` dla `y=133..143` oraz `y in {133,143}` dla `x=1..7`); flaga górna `FLAG_A` `(4, 135)` + pochodnie `(3/5, 135)`; flaga dolna `FLAG_B` `(4, 141)` + pochodnie `(3/5, 141)`
  - W środku `(4, 138)` stoi Król `P1` (`9999 HP`, regeneracja `5000/min` ≈ `83.3 HP/s`) + stałe `MAP_REVEALER` dla `P1–P4` na `(4.5, 138.5)`
- **Plac Targowy graczy (SW):** czysty płaski plac `x=2..24, y=176..198` (`elev=0`, bez drzew w `x=2..24, y=177..198`, `DIRT_1` na `x=3..23, y=177..198`) pod Markety `P1–P4`
- **Korytarz handlowy:** pas `y=189..199` (`x=2..199`, `elev=0`, bez drzew) z drogą (`ROAD`, `width=1`) na `y=194` (`x=3..198`) oraz pasem `y=183..188` (`x=104..199`, `elev=0`, bez drzew) zarezerwowanym pod Mur Handlowy Q1
- **Puszcza Zaplecza, bufor leśny i zagajniki wewnętrzne:** nieprzebrany pas dębowy `FOREST_OAK` (`TREE_OAK_ID`) na każdym wolnym kafelku w `x=8..13, y=128..176` i pomiędzy komnatami `x=1..13, y=144..158` (a także `(0..13, 106..132)` i `(0..13, 170..175)`), oddzielający komnaty `(4, 138)` i `(4, 164)` od baz `P1–P4`; `FOREST_PINE` na `(26..98, 180..188)`; zagajniki w Twierdzy na `(54, 122)` (`r=5.5`, Oak) i `(54, 172)` (`r=4.5`, Pine); zarezerwowany plac `(58, 152)` (`mark_footprint(3, no_tree_margin=1)` + `mark_no_trees(r=4)` + `2x TORCH` na `(56, 150), (60, 154)`) pod Klasztor nagrody `Q4`
- **Posterunek Kwatermistrza Twierdzy `P2` (`(4, 164)` — pełna izolacja na zachodniej krawędzi, odblokowywany w `10:00`, 3-poziomowe skalowanie):** szczelna komnata `7×11` (`x=1..7, y=159..169`, wnętrze `x=2..6, y=160..168` `ROAD`, `elev=0`, obwód z klifów `ROCK_CLIFF_ID` na `DIRT_3`); Kwatermistrz `UnitInfo.KING.ID` (`P2`) na `(4, 164)` (9999 HP, regen 5000/min) + stałe `MAP_REVEALER` dla `P1–P4` na `(4.5, 164.5)`; dwie flagi `GAIA`: północna `FLAG_A (600)` na `(4, 161)` + pochodnie `(3/5, 161)` oraz południowa `FLAG_B (601)` na `(4, 167)` + pochodnie `(3/5, 167)`. Gracz `P2` aktywuje rozkaz wchodząc **wyłącznie Królem (`UnitInfo.KING.ID`)** w `pad_x±2, pad_y±2` (Król jest teleportowany na `(4, 164)` i zatrzymywany przez `stop_object` w `(2..6, 160..168)`):
  - **Poziom 1 (`10:00–20:00`, odblokowany przez `06d_Unlock_Quartermaster_And_PoI1_10m` `timer=600`):** `06d_P2_QM_Mil_T1` = `4x Conquistador` `(52,149),(53,149),(55,149),(56,149)` + `1x Mangonel` `(54,150)` dla `P2`; `06d_P2_QM_Eco_T1` = `+125 Food, +125 Wood, +100 Gold` dla `P1–P4` (**bez naprawy murów**). Cooldown: `06d_P2_QM_Cooldown_T1_240s`.
  - **Poziom 2 (`20:00–30:00`, przełączany przez `06d_Upgrade_Quartermaster_Tier2_20m` `timer=1200`):** `06d_P2_QM_Mil_T2` = `4x Conquistador` `(52..53/55..56, 149)` + `2x Bombard Cannon` `(53/55, 150)`; `06d_P2_QM_Eco_T2` = `+200 F/W/G` dla `P1–P4` + naprawa Twierdzy (`0..110, 95..199`) i Muru `Q1` (`111..199, 183..187`) o **`+250 HP`**. Cooldown: `06d_P2_QM_Cooldown_T2_240s`.
  - **Poziom 3 (`od 30:00+`, przełączany przez `06d_Upgrade_Quartermaster_Tier3_30m` `timer=1800`):** `06d_P2_QM_Mil_T3` = `6x Elite Conquistador` `(51..53/55..57, 149)` + `2x Bombard Cannon` `(53/55, 150)` + `2x Siege Ram` `(52/56, 150)`; `06d_P2_QM_Eco_T3` = `+300 F/W/G` dla `P1–P4` + naprawa Twierdzy (`0..110, 95..199`) i Muru `Q1` (`111..199, 183..187`) o **`+500 HP`**. Cooldown: `06d_P2_QM_Cooldown_T3_240s`.
  - **Wspólny czas odnowienia (`240s` / 4 minuty):** w każdym z 3 progów wybór flagi wyłącza obie flagi (`State_P2_QM_Ready` -> `06d_P2_QM_Cooldown_T*_240s` z `looping=True` i autodezaktywacją), a po `240s` resetuje licznik i przywraca gotowość.
- **Zdarzenia Eksploracyjne na Mapie (`Map PoI`, `06e_PoI*`, promień detektora `r=3` — 100% rozłączne od wszystkich detektorów garnizonów):**
  - **PoI 1 — Opuszczony Obóz Inżynierów (`(30, 76)`, `enabled=False`, odblokowywany w `10:00` przez `06d_Unlock_Quartermaster_And_PoI1_10m`):** strefa bez drzew `r=4` przed lasem NW, `OUTPOST` `GAIA` na `(30, 75)` + `2x TORCH` `(28/32, 76)`; pierwszy odkrywca z `P1–P4` w `27..33, 73..79` otrzymuje `2x Capped Ram` `(29/31, 76)` + `2x Petard` `(29/31, 77)` oraz `+200W/+200G` dla wszystkich `P1–P4` (wzajemna dezaktywacja 4 triggerów)
  - **PoI 2 — Zaginiona Karawana (`(124, 178)`, `enabled=True`):** strefa bez drzew `r=4`, `DIRT_1` `r=3`, `GOLD_MINE` `GAIA` na `(124, 178)` + `2x TORCH` `(122/126, 178)`; pierwszy odkrywca w `121..127, 175..181` przyznaje `+350F/+350G` dla `P1–P4` oraz stawia `MAP_REVEALER` dla `P1–P4` nad `Q1 (154, 190)`
  - **PoI 3 — Kamień Wędrowca i Zwiadowcy (`(50, 90)`, `enabled=True`):** strefa bez drzew `r=4`, `DIRT_2` `r=3`, `OUTPOST` `GAIA` na `(50, 89)` + `2x TORCH` `(48/52, 90)`; pierwszy odkrywca z `P1–P4` w `47..53, 87..93` (`06e_PoI3_Scout_P1..P4`) otrzymuje `2x Light Cavalry` `(49, 90)` i `(51, 90)`, przyznaje `+150 Stone, +150 Gold` dla `P1–P4` oraz stawia `MAP_REVEALER` dla `P1–P4` nad brodem `(122, 62)`

### 2. Bazy graczy P1–P4
- **Wspólne zasoby i technologie startowe (`0:00`):** `500 Food, 600 Wood, 400 Gold, 300 Stone`, `TECH_CARTOGRAPHY` dla `P1–P4`, `6x Villager Male` (`(-3,-2)..(-1,-3)`), `1x Scout Cavalry` (`(+4,0)`), `MAP_REVEALER` (`LOS=4`, `P1`) nad każdym z 10 obozów AI oraz dla `P1–P4` nad `(4, 138)` i `(4, 164)`
- **Symetryczne zasoby wokół każdego TC `(cx, cy)` (promień bez lasu `r=11`):**
  - `6x` Drzewo dębowe: `(-5,-3), (4,-4), (-4,4), (4,3), (-5,1), (3,-5)` | `6x` Owca: `(-3,2)..(-2,3)`
  - `2x` Dzik: `(-9,-1)` i `(+1,+9)` | `4x` Jeleń: `(-7..-8, -7..-8)`
  - `6x` Krzak jagód: `(-8,-4)` | `8x` Złoto: `(+7,-6)` | `6x` Złoto: `(+7,+5)` | `6x` Kamień: `(-8,+5)`
  - `2` organiczne zagajniki leśne (`r=4.8`): `(-14, 0)` (`FOREST_OAK`) oraz `(0, +14)` (`FOREST_PINE`)

| Gracz | Pozycja TC (`4×4`) | Sektor obrony | Domki startowe (`2×2`, offset od `(cx, cy)`) | Rekomendowane cywilizacje (`horda.md`) |
| :--- | :--- | :--- | :--- | :--- |
| **P1 (Niebieski)** | `(76, 124)` | Brama Centralna `(104, 114)` + Król `(4, 138)` | 2 domki: `(0,-7), (3,-7)` | Bizancjum, Brytowie, Teutoni, Czesi |
| **P2 (Czerwony)** | `(32, 164)` | Cytadela `(54, 146)` + Plac Targowy SW | 6 domków: `(-3,-7),(0,-7),(3,-7),(-3,-10),(0,-10),(3,-10)` | **Hiszpanie** (+25% złota z handlu), Portugalczycy, Frankowie, Burgundczycy |
| **P3 (Zielony)** | `(32, 122)` | Brama Północna `(48, 100)` + dostęp do Q2 | 2 domki: `(0,-7), (3,-7)` | Celtowie, Goci, Polacy, Rzymianie |
| **P4 (Żółty)** | `(76, 168)` | Brama Wschodnia `(104, 162)` i Handlowa `(104, 193)` + Q1 | 2 domki: `(0,-7), (3,-7)` | Litwini, Hindustańczycy, Węgrzy, Saraceni |

### 3. Cztery Bramy, przeszkody terenowe i obiekty na rubieżach

| Obiekt / Strefa | Współrzędne | Właściciel / Typ | Szczegóły geometryczne i umocnienia |
| :--- | :--- | :--- | :--- |
| **Brama Północna** | `(48, 100)` | `P3` (wzdłuż X) | Strefa płaska `13×13` (`DIRT_1`), brama `789` (`x=46..49`, `+600 HP`), mur `FORTIFIED_PALISADE` (`119`, `+600 HP`) na `x=41..55`, `2x Guard Tower` na `(44, 104)` i `(52, 104)` |
| **Brama Centralna** | `(104, 114)` | `P1` (wzdłuż Y) | Strefa `13×13`, brama `793` (`y=112..115`, `+600 HP`), mur na `y=107..121`, `2x Guard Tower` na `(100, 110)` i `(100, 118)`, krąg `8` pochodni (promień `10` wokół `(116, 114)`) |
| **Brama Wschodnia** | `(104, 162)` | `P4` (wzdłuż Y) | Strefa `13×13`, brama `793` (`y=160..163`, `+600 HP`), mur na `y=155..169`, `2x Guard Tower` na `(100, 158)` i `(100, 166)` |
| **Brama Handlowa** | `(104, 193)` | `P4` (wzdłuż Y) | Strefa `13×13`, brama `793` (`y=191..194`, `+600 HP`), mur na `y=186..199`, `2x Guard Tower` na `(100, 189)` i `(100, 197)` |
| **Rzeka i 3 brody** | `rx=62+0.9t, ry=8+0.8t+3sin(0.08t)` (`t=0..139`) | `TERRAIN_WATER=1` (`r=2`) | Warunek omijający Twierdzę: `rx>112 or ry<90`; 3 brody (`TERRAIN_SHALLOWS=4, r=5`): `(84, 30)`, `(122, 62)`, `(154, 92)` |
| **Grzbiety skalne** | `(16,48)->(44,48)` i `(124,134)->(158,134)` | `GAIA` (`ROCK_CLIFF_ID`) | Grzbiet NW: `height=3`, łuk `curve=3sin(t*pi)`; grzbiet E: `height=2`; pas `DIRT_3` (`r=2`), bez drzew |
| **Przesieka Północna** | `(75..80, 95..105)` | Wyłom `6×11` | Zablokowana drzewami (`north_breach_trees`), wycinana w Fali 9 (`51:00`) |
| **Przesieka Wschodnia** | `(99..109, 137..142)` | Wyłom `11×6` | Zablokowana drzewami (`east_breach_trees`), wycinana w Fali 12 (`67:30`) |
| **Relikty + Złoto** | `(54,62), (116,88), (168,128), (92,44)` | `GAIA` | Po `1x Relic` (`285`) w punkcie oraz `6x Gold Mine` na `(rx+3, ry+3)` |
| **Stałe odsłaniacze** | Centra 10 obozów (4Q + 6S) | `P1` (`MAP_REVEALER=837`) | `LOS = 4` (ustawione w `01_Init`), zapewnia stałą widoczność i podgląd opisów pod Mgłą Wojny |

- **Drogi (`ROAD`, `width=1`, bufor bez drzew `2`):** `G1_North (76,72) -> (48,100)`, `G1_East (132,152) -> (104,162)`, `G2_Mages (148,72) -> (104,114)`, `G3_East (176,56) -> G2_Mages (148,72)`
- **11 organicznych lasów na rubieżach (`paint_organic_forest`):**
  - `FOREST_PINE`: `(20, 74)` `r=7.0`, `(16, 12)` `r=7.5`, `(126, 94)` `r=6.5`, `(184, 136)` `r=7.5`, `(184, 22)` `r=7.0`
  - `FOREST_OAK`: `(48, 74)` `r=5.5`, `(68, 12)` `r=6.5`, `(108, 56)` `r=6.0`, `(172, 96)` `r=7.0`, `(184, 158)` `r=5.0`, `(126, 172)` `r=5.0`
- **20 polan spawnu i odwetu (`no_trees`, `r=7`):** `(48,86), (52,86), (68,60), (78,87), (105,34), (106,72), (116,114), (118,122), (116,162), (117,140), (117,178), (156,152), (162,180), (68,48), (76,84), (120,152), (120,162), (128,36), (134,78), (160,62)`

---

## B. Frakcje AI (P5–P8) i 6 Archetypów Specjalnych

### 1. Cywilizacje i harmonogram technologii AI (`01_Init`, `01b`, `01d–01f`)
- **P5 (Turkusowy — Wikingowie, `lock_civ=True`):** kontroluje `G1_North`, `G1_East`, `Q1`.
- **P6 (Fioletowy — Turcy, `lock_civ=True`):** kontroluje `G2_Snipers`, `Q2` oraz wyłomy Saperów.
- **P7 (Szary — Saraceni, `lock_civ=True`):** kontroluje `G2_Mages`, `Q4`, Arcymagów i Szakale.
- **P8 (Pomarańczowy — Persowie, `lock_civ=True`):** kontroluje `G3_North`, `G3_East`, `Q3`, `Trade_Line_Attack`, wszystkie kontrataki Settlementów oraz Finałowego Bossa **Wielkiego Chana Subotaia (`698`)**.
- **`01_Init` (`0:00`):** dla `P5–P8` bada `Feudal Age (101)`, `Castle Age (102)`, `Imperial Age (103)`; dla `P8` dodatkowo `TECH_FAITH (45)`; dla `P1–P4` dodaje **`+600 HP`** do `FORTIFIED_PALISADE_ID (119)` oraz wszystkich bram palisadowych (`789, 792, 793, 797, 801`).
- **`01b` (`0:03`):** zeruje `ATTR_MAXIMUM_RANGE=0` i `ATTR_WORK_RATE=0` dla `IMAM (842)`, `MISSIONARY`, `MONK` dla `P5–P8` (brak konwersji przez AI), aplikuje statystyki 6 archetypów oraz Bossa (`FINAL_BOSS_HERO_ID = 698` `P8`: `4500 HP`, `Hero=1`, pancerz `8/10`, atak `cl=3: 45`, prędkość `0.85`).
- **`01d` (`8:30` / `510s`):** bada dla `P5–P8`: `Forging (67)`, `Scale Mail (74)`, `Scale Barding (81)`, `Fletching (199)`, `Bloodlines (435)`; następnie odejmuje `-20 HP` dla `HUSSAR_ID` i `ELITE_BATTLE_ELEPHANT_ID` (neutralizacja Bloodlines) i wywołuje `enforce_specialized_unit_caps`.
- **`01e` (`18:00` / `1080s`):** bada dla `P5–P8`: `Iron Casting (68)`, `Chain Mail (76)`, `Squires (215)`, `Chain Barding (82)`, `Bodkin Arrow (200)`, `Ballistics (93)`, `Husbandry (39)`, **`TECH_FAITH (45)`** + `enforce_specialized_unit_caps`.
- **`01f` (`34:30` / `2070s`):** bada dla `P5–P8`: `Blast Furnace (75)`, `Plate Mail (77)`, `Plate Barding (80)`, `Bracer (201)`, `Chemistry (47)`, `Siege Engineers (377)` + `enforce_specialized_unit_caps`.

### 2. Sześć Archetypów Specjalnych (statystyki w `01b` oraz pułapy `enforce_specialized_unit_caps`)

| Archetyp (ID / Gracz) | Bazowe HP (Skala?) | Prędkość (Cap) | Atak bazowy / bonus (Skala?) | Pancerz M/P (Cap) | Zasięg / Reload / Blast / Poświata / Uwagi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Żelazny Słoń (`1134`, `P8`)** | `1450` (Tak; `-20` w `8:30`) | `0.72` (Cap) | `3` melee `cl=4` (Cap; **Nie skaluje**) + `+140` vs budynki (`cl=11, 21`) | `10 / 12` (Cap `cl=4, 3`) | `Hero Status=1` (odporny na konwersję), `receives_mage_shield=False`, `mandatory_min_one=True` |
| **2. Szakal Dywersyjny (`441`, `P7`)** | `95` (Tak; `-20` w `8:30`) | `1.62` (Cap) | `7` melee `cl=4` (Cap; **Nie skaluje**) | `0 / 6` (Cap `cl=4, 3`) | `receives_mage_shield=False`, `mandatory_min_one=False` |
| **3. Arcymag Tarczy (`842`, `P7`)** | `240` (Nie; `Q4 -> 120`) | `0.78` (Cap) | Brak (`range=0, work_rate=0`) | `3 / 4` (z `01b`) | `Hero Status=1`, regen `300/min` (`5 HP/s`), `receives_mage_shield=False`, `mandatory_min_one=True` |
| **4. Moździerz Oblężniczy (`588`, `P6`)** | `350` (Tak) | `0.58` (Cap) | `+75` bonus `cl=4` (Tak `cl=4`) | Bazowy + Kuźnia | `Hero Status=1`, Range `21` (Cap), `min_range=6`, `LOS/Search=23`, Reload `10.0s`, `Blast Width=2.6`, `Blast Attack Level=2` (nie ścina drzew), `receives_mage_shield=False`, `mandatory_min_one=True` |
| **5. Snajper Imperialny (`557`, `P6`)** | `90` (Tak) | Bazowy + Squires | `+85` bonus `cl=3` (Tak `cl=3`) | Bazowy + Kuźnia | `Hero Status=1`, Range `19` (Cap), `LOS/Search=21`, Reload `6.5s`, `receives_mage_shield=False`, `mandatory_min_one=True` |
| **6a. Berserker Szturmowy (`694`, `P5`)** | `185` (Tak) | `1.40` (Cap) | `+12` bonus `cl=4` (Tak `cl=4`) | Pierce `0` (Cap `cl=3`) | `receives_mage_shield=True`, `mandatory_min_one=True` |
| **6b. Petard (`440`) / Pł. Wielbłąd (`1263`, `P5`)** | `115` (Nie) | `1.50` (Cap) | `+95` bonus `cl=4` (**Nie skaluje**) | Pierce `0` (Cap `cl=3`) | `Blast Width=2.4`, `receives_mage_shield=False`, `mandatory_min_one=True` |

### 3. Mechanika Aury Arcymaga, ruch Szakali i popychanie bram (`02a–02e`)
- **Strefa Aury Arcymaga (`02a–02d`):** kwadrat `±18` wokół `(110, 114)`, czyli `(92, 96)..(128, 132)` (`37×37` kratek) przed Bramą Centralną:
  - **`02a_Mage_Global_Horde_Shield_On`:** aktywuje się przy `≥1` `IMAM_UNIT_ID` (`P7`) w strefie; nakłada **globalnie wszystkim graczom `P5–P8`** **`+8/+8` pancerza** (`cl=3, 4`) dla **`20` jednostek** z `receives_mage_shield=True` (6 typów piechoty, 6 jazdy, 4 łuczników, `Capped Ram`, `Siege Ram`, `Heavy Camel Rider`, `Elite Mameluke`)
  - **Wykluczenia z Tarczy Maga (`10` jednostek):** `Snajper Imperialny`, `Mangonel`, `Moździerz Oblężniczy`, `Żelazny Słoń`, `Szakal`, `Arcymag`, `Petard`, `Płonący Wielbłąd`, `Battering Ram`, `Wielki Chan Subotai`
  - **`02b_Mage_AoE_Heal_Pulse_3s`:** co `3s` (gdy Imam `P7` w strefie) leczy wszystkie jednostki `P5–P8` w `(92..128, 96..132)` o **`+15 HP`**
  - **`02c_Mage_Visual_Flare_Beacon_8s`:** co **`20s`** (`timer=20`, gdy Imam `P7` w strefie) wysyła ostrzeżenie na czacie i flarę na `(114, 114)`
  - **`02d_Mage_Global_Horde_Shield_Off`:** gdy brak Imama `P7` w strefie (`inverted=1`), odejmuje `-8/-8` pancerza tym samym `20` typom jednostek, wyłącza `02b/02c/02d` i reaktywuje `02a`
- **Zachowanie Szakali (`ActionType.MOVE`):**
  - Spawnowane w Falach 3–14 z `G2_Mages` (`P7`) rozkazem `task_object(..., ActionType.MOVE)` na obszar `±8` wokół spawnu — ignorują jednostki na przedpolu aż do celu pod TC
  - Fale nieparzyste (`3,5,7,9,11,13`): spawn Brama Północna `(52, 86)`; fale parzyste (`4,6,8,10,12,14`): spawn Brama Wschodnia `(116, 162)`
  - Cele cykliczne `eco_raid_targets[w_num % 4]`: `w%4==0 -> (32, 118)` (P3), `w%4==1 -> (76, 120)` (P1), `w%4==2 -> (32, 168)` (P2), `w%4==3 -> (76, 172)` (P4)
  - Tryb Endless: łączna liczba skalowana jak dla F14 (`17` bazowo), dzielona na dwie grupy: `(n+1)//2` z `(52, 86)` na `(32, 118)` oraz `n//2` z `(116, 162)` na `(76, 172)`
- **Popychanie bram (`02e_Push_Gate_Units_Deep_Into_Base`):** pętla co `15s` wysyłająca `attack_move` w 5 strefach:
  - Brama Północna `(40..56, 96..108)` -> `(48, 138)` dla **`P5, P6, P8`** (wyklucza `P7`, aby nie nadpisywać `MOVE` Szakali)
  - Brama Centralna `(96..108, 106..122)` -> `(54, 146)` dla **`P5, P6, P7, P8`**
  - Brama Wschodnia `(96..108, 154..170)` -> `(68, 162)` dla **`P5, P6, P8`** (wyklucza `P7`)
  - Przesieka Północna `(74..82, 94..108)` -> `(68, 130)` dla **`P5, P6, P8`**
  - Przesieka Wschodnia `(98..112, 135..144)` -> `(68, 146)` dla **`P5, P6, P8`**

---

## C. Tabela Fal 1–14 i Trybu Endless

### 1. Punkty spawnu, czyszczenie polan i cele (siatka 11-kolumnowa `dx=(i%11)-5, dy=(i//11)-5`, obszar rozkazu `±8`)
- **Ochrona polan spawnu przed zamurowaniem (`add_spawn_and_attack_effect`):** dla zewnętrznych spawnów (`spawn_x > 105 or spawn_y < 96`) przed `create_object` wywołuje `kill_object` (`ObjectType.BUILDING`) dla `P1–P4` w obszarze `spawn_x ± 6, spawn_y ± 6` (z ograniczeniem `area_y2 <= 182` dla `spawn_x > 105 and spawn_y >= 172`, chroniącym baszty i Mur Handlowy Q1 na `y=183..186`)
- **`G1_North` (`P5`):** spawn `(48, 86)` -> `attack_move` `(48, 138)` (Brama Północna)
- **`G1_East` (`P5`):** spawn `(117, 178)` -> `attack_move` `(68, 162)` (Brama Wschodnia)
- **`G2_Snipers` (`P6`):** spawn `(68, 60)` -> `attack_move` `(48, 138)` (Brama Północna)
- **`G2_Mages` (`P7`):** główna armia spawn `(116, 114)` -> `attack_move` `(54, 146)` (Brama Centralna); Szakale osobno
- **`G3_North` (`P8`):** spawn `(106, 72)` -> `attack_move` `(54, 146)` (Brama Centralna)
- **`G3_East` (`P8`):** główna armia spawn `(156, 152)` -> `attack_move` `(68, 162)` (Brama Wschodnia); `Trade_Line_Attack` osobno na `(162, 180)` -> `(96, 194)`

### 2. Harmonogram i składy fal na Poziomie 0 (Domyślny)

| Fala / Czas | `G1_North` (`P5`) | `G1_East` (`P5`) | `G2_Snipers` (`P6`) | `G2_Mages` (`P7`) + Szakale | `G3_North` (`P8`) | `G3_East` (`P8`) + Wydarzenia Specjalne |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **F1** `8:30` (`510s`) | 6 MAA, 5 Arch | 6 MAA, 5 Scout | — | — | — | — |
| **F2** `13:00` (`780s`) | 8 MAA, 6 Arch, 1 B.Ram | 8 Spear, 6 Scout, 1 Mang | — | 5 Scout, 6 Arch | — | — |
| **F3** `18:00` (`1080s`) | 11 Pike, 3 Bers, 1 Pet, 1 B.Ram | 8 Husk, 5 Kni, 1 F.Cam | 10 Xbow, 2 Jan | 6 Kni, 1 B.Ram + **5 Szakali** `(52,86)->(76,172)` | — | — |
| **F4** `23:30` (`1410s`) | 14 Pike, 4 Bers, 2 B.Ram | 10 Husk, 6 Kni, 2 F.Cam | 12 Xbow, 3 Jan | **1 Imam**, 10 Kni, 2 B.Ram + **6 Szakali** `(116,162)->(32,118)` | — | — |
| **F5** `29:00` (`1740s`) | 16 Pike, 4 Bers, 2 Pet, 2 C.Ram | 12 Husk, 2 F.Cam, 2 C.Ram | 14 Xbow, 3 Jan, **1 S.Onag** | 1 Imam, 12 Kni + **7 Szakali** `(52,86)->(76,120)` | 8 Kni, 10 Pike | — |
| **F6** `34:30` (`2070s`) | 18 Pike, 5 Bers, 2 C.Ram | 14 Husk, 3 F.Cam, 2 C.Ram | 16 Xbow, 3 Jan, 1 S.Onag | 1 Imam, 12 Cav, 2 C.Ram + **8 Szakali** `(116,162)->(32,168)` | **1 Ele**, 10 Kni, 12 Pike | 14 Xbow, 8 Kni |
| **F7** `40:00` (`2400s`) | 20 Halb, 5 Bers, 3 Pet, 3 C.Ram | 16 Husk, 3 F.Cam, 2 C.Ram | 18 Arb, 4 Jan, 1 S.Onag | 1 Imam, **18 Cav** + 9 Szakali `(52,86)->(76,172)` | 2 Ele, **16 Cav**, 12 Halb, **2 S.Ram** | 1 Ele, 16 Arb *(Signature: Pancerna Szarża)* |
| **F8** `45:30` (`2730s`) | 22 Halb, 6 Bers, 3 S.Ram | 18 Husk, 3 F.Cam, 3 S.Ram | 20 Arb, 4 Jan, 2 S.Onag | 2 Imam, 16 Cav, 3 S.Ram + **10 Szakali** `(116,162)->(32,118)` | 2 Ele, 14 Cav, 14 Halb | 2 Ele, 18 Arb, 1 S.Onag + **Trade Raid** (`3 SR, 10 Pal, 10 HCA`) |
| **F9** `51:00` (`3060s`) | 25 Halb, 7 Bers, 3 Pet, 3 S.Ram | 20 Husk, 4 F.Cam, 3 S.Ram | 22 Arb, 4 Jan, 2 S.Onag | 2 Imam, 16 Pal, 3 S.Ram + **12 Szakali** `(52,86)->(76,120)` | 3 Ele, 15 Pal, 16 Halb | 2 Ele, 20 Arb, 2 S.Onag + **Wyłom Płn. (`G2_Snipers`)** |
| **F10** `56:30` (`3390s`) | 28 Halb, 8 Bers, 3 Pet, 4 S.Ram | 23 Husk, 3 F.Cam, 4 S.Ram | 25 Arb, 4 Jan, 2 S.Onag | 2 Imam, 19 Pal, 4 S.Ram + **22 Szakali** `(116,162)->(32,168)` | 3 Ele, 19 Pal, 18 Halb | 3 Ele, 23 Arb, 2 S.Onag + **Trade Raid** (`3 SR, 14 Pal, 14 HCA`) *(Signature: Noc Szakali)* |
| **F11** `62:00` (`3720s`) | 31 Halb, 9 Bers, 4 Pet, 4 S.Ram | 26 Husk, 4 F.Cam, 4 S.Ram | 28 Arb, **8 Jan**, **4 S.Onag** | 2 Imam, 22 Pal, 4 S.Ram + **14 Szakali** `(52,86)->(76,172)` | 4 Ele, 22 Pal, 20 Halb | 4 Ele, 26 Arb, **4 S.Onag** *(Signature: Nawałnica Artylerii i Snajperów)* |
| **F12** `67:30` (`4050s`) | 34 Halb, 10 Bers, 4 Pet, 4 S.Ram | 29 Husk, 4 F.Cam, 4 S.Ram | 31 Arb, 5 Jan, 3 S.Onag | 3 Imam, 25 Pal, 4 S.Ram + **15 Szakali** `(116,162)->(32,118)` | 4 Ele, 25 Pal, 22 Halb | 4 Ele, 29 Arb, 3 S.Onag + **Trade Raid** (`3 SR, 18 Pal, 18 HCA`) + **Wyłom Wsch. (`G2_Snipers`)** |
| **F13** `73:00` (`4380s`) | 37 Halb, 11 Bers, 5 Pet, 4 S.Ram | 32 Husk, 5 F.Cam, 4 S.Ram | 34 Arb, 6 Jan, 3 S.Onag | **3 Imam**, 28 Pal, 4 S.Ram + **16 Szakali** `(52,86)->(76,120)` | **6 Ele**, 28 Pal, 24 Halb | **6 Ele**, 32 Arb, 3 S.Onag *(Signature: Straż Przednia Tytanów)* |
| **F14** `78:30` (`4710s`) | 40 Halb, 12 Bers, 5 Pet, 4 S.Ram | 35 Husk, 5 F.Cam, 4 S.Ram | 37 Arb, 6 Jan, 3 S.Onag | 3 Imam, 31 Pal, 4 S.Ram + **17 Szakali** `(116,162)->(32,168)` | 5 Ele, 31 Pal, 26 Halb | 5 Ele, 35 Arb, 3 S.Onag + **Trade Raid** (`3 SR, 22 Pal, 22 HCA`) |
| **Endless** `84:00+` (`5040s+`, co `330s`) | Skład F14 (skalowany) | Skład F14 (skalowany) | Skład F14 (skalowany) + **Wyłom N+E** | Skład F14 (skalowany) + **17 Szakali** (split `9` N / `8` E, skal.) | Skład F14 (skalowany) | Skład F14 (skalowany) + **Trade Raid F14** (`3 SR, 22 Pal, 22 HCA`, skal.) |

### 3. Reguły specjalne fal (Wyłomy Saperów, Rajdy Handlowe, Tryb Endless)
- **Wzór bazowy Fal 10–14 (`m = wave_num - 9`, dla `m = 1..5`; modyfikacje *Signature Waves* w F10, F11 i F13 powyżej):**
  - `G1_North`: `25+3m` Halb, `7+m` Bers, `3+m//2` Pet, `4` S.Ram | `G1_East`: `20+3m` Husk, `3+m//2` F.Cam, `4` S.Ram
  - `G2_Snipers`: `22+3m` Arb, `4+m//2` Jan, `2+m//3` S.Onag | `G2_Mages`: `2+m//3` Imam, `16+3m` Pal, `4` S.Ram, `12+m` Szakali
  - `G3_North`: `3+m//2` Ele, `16+3m` Pal, `16+2m` Halb | `G3_East`: `3+m//2` Ele, `20+3m` Arb, `2+m//3` S.Onag
- **Wyłom Północny (`G2_Snipers`, `P6`, Fala 9):**
  - `50:15` (`3015s`): alarm (`45s` wyprzedzenia) i flara `(78, 98)` + spawn `2x S.Onag, 8x Halb` na `(78, 90)` -> `attack_move` `(78, 95)`
  - `51:00` (`3060s`): usuwa drzewa `north_breach_trees (75..80, 95..105)` + spawn `2x S.Onag, 14x Halb, 8x Jan` na `(78, 94)` -> `attack_move` `(68, 130)`, flara `(78, 102)`
- **Wyłom Wschodni (`G2_Snipers`, `P6`, Fala 12):**
  - `66:45` (`4005s`): alarm (`45s` wyprzedzenia) i flara `(106, 140)` + spawn `2x S.Onag, 10x Halb` na `(115, 140)` -> `attack_move` `(109, 140)`
  - `67:30` (`4050s`): usuwa drzewa `east_breach_trees (99..109, 137..142)` + spawn `2x S.Onag, 16x Halb, 12x Arb` na `(115, 140)` -> `attack_move` `(68, 146)`, flara `(104, 140)`
- **Wyłom w Trybie Endless (`03_Endless_Forest_Breach_Assault`):** aktywowany co `330s` przez bramkę `G2_Snipers` (`03_Endless_Gate_G2_Snipers`); spawnuje równocześnie `2x S.Onag, 14x Halb, 8x Jan` na `(78, 94)->(68, 130)` oraz `2x S.Onag, 14x Halb, 10x Arb` na `(115, 140)->(68, 146)` (uwaga: wyłomy F9/F12/Endless nie przechodzą przez `scale_comp_for_level`)
- **`Trade_Line_Attack` (`G3_East`, `P8`):** fale `8, 10, 12, 14` i `Endless`; spawn `(162, 180)` -> `attack_move` `(96, 194)`, flara `(162, 184)`; skład w Fali `w`: `3x Siege Ram`, `10+(w-8)*2` Paladin, `10+(w-8)*2` Heavy Cav Archer (skalowany przez `scale_comp_for_level`)
- **Mechanika Trybu Endless:** w `78:30` (`4710s`) zegary Fali 14 każdego obozu aktywują jego indywidualną bramkę `03_Endless_Gate_<camp>` (`looping=True, timer=330s`), a `03_Endless_Announce_Gate` (`4710s`) uruchamia ogłoszenie cykliczne co `330s` + flarę `(104, 114)`; pierwsze uderzenie Endless przypada w `84:00` (`5040s`)

---

## D. Eskalacja Czasowa, Sanktuarium Balansu i Rejestr Jednostek

### 1. Trzystopniowa Eskalacja Czasowa (`04a–04f`, aplikowana przez `ENEMY_UNIT_REGISTRY`)
- **Bieg 1 (`04a`/`04b`, start `20:00` / `1200s`):** natychmiastowy 1. tick w `20:00` i powtórzenie co `300s`: **`+5 HP, +1 Atk`**
- **Bieg 2 (`04c`/`04d`, start `45:00` / `2700s`):** natychmiastowy 1. tick w `45:00` i powtórzenie co `300s`: dodatkowo **`+9 HP, +0 Atk`** (łącznie z Biegiem 1: **`+14 HP, +1 Atk`** co `5` min)
- **Bieg 3 (`04e`/`04f`, start `55:00` / `3300s`):** natychmiastowy 1. tick w `55:00` i powtórzenie co `300s`: dodatkowo **`+6 HP, +1 Atk`** (łącznie z Biegami 1+2: **`+20 HP, +2 Atk`** co `5` min)
- **Kumulacyjny przyrost czasowy (bez Questów i Furii Settlementów):**
  - `20:00`: `+5 HP / +1 Atk` | `30:00`: `+15 HP / +3 Atk` | `40:00`: `+25 HP / +5 Atk`
  - `45:00`: `+39 HP / +6 Atk` | `50:00`: `+53 HP / +7 Atk` | `55:00`: `+73 HP / +9 Atk`
  - `60:00`: `+93 HP / +11 Atk` | `70:00`: `+133 HP / +15 Atk` | `80:00`: `+173 HP / +19 Atk`

### 2. Sanktuarium Balansu (`(4, 138)`, `09_Diff_*`)
- **Strefy komnaty:** pad górny `(2..6, 134..136)` (+1 stopień), pad dolny `(2..6, 140..142)` (-1 stopień), pełna strefa resetu `(2..6, 134..142)`. Po wykryciu Króla `P1` trigger wykonuje `teleport_object` na `(4, 138)`, `stop_object`, przełącza `State_Diff_Lvl_*`, wysyła flarę `(4, 138)` i komunikat czatu do wszystkich graczy `P1–P4` oraz modyfikuje statystyki jednostek w `ENEMY_UNIT_REGISTRY`.
- **Brak blokad czasowych i kolejność topologiczna:** brak timerów zamrażających komnatę (`State_Sanctuary_Unlocked` / `Close_Window` nie istnieją). Przed wielokrotnym przeskokiem w 1 ticku chroni odwrócony porządek rejestracji 8 triggerów:
  - Pad górny (`pad_up_box`, kolejność ID): `09_Diff_Up_P1_to_P2` -> `09_Diff_Up_0_to_P1` -> `09_Diff_Up_M1_to_0` -> `09_Diff_Up_M2_to_M1` (na starcie aktywny tylko `0_to_P1`)
  - Pad dolny (`pad_down_box`, kolejność ID): `09_Diff_Down_M1_to_M2` -> `09_Diff_Down_0_to_M1` -> `09_Diff_Down_P1_to_0` -> `09_Diff_Down_P2_to_P1` (na starcie aktywny tylko `0_to_M1`)
- **Algorytm skalowania liczebności (`scale_comp_for_level`):**
  - Docelowa suma grupy `effective_target = max((total_orig * pct + 50) // 100, sum(min_reqs))` (zaokrąglanie `HALF_UP`)
  - Nadwyżki (`+25%` / `+50%`) przydzielane po `1` szt. wg największej reszty z dzielenia (remis wygrywa wcześniejszy typ w grupie); redukcje (`-20%` / `-40%`) odejmowane wieloprzebiegowo wg najmniejszej reszty wyłącznie z pozycji mających zapas ponad `min_req`
  - Jednostki z `mandatory_min_one=True` nigdy nie spadają poniżej `1` szt. w grupie na poziomach `-1/-2` (nawet gdy grupa jest redukowana o `40%`)
  - Skalowaniem objęte są zarówno składy fal `1–14` i `Endless`, jak i rajdy `Szakali` oraz `Trade_Line_Attack` (wyłomy Saperów są stałe)

| Poziom (`State_Diff_Lvl_*`) | Mnożnik fal (`pct`) | Modyfikator HP wroga (`scales_hp=True`) | Modyfikator Ataku (`attack_class != None`) |
| :--- | :--- | :--- | :--- |
| **`-2` (Bardzo Łatwy)** | `60%` (`-40%`) | `-2 × hp_delta_down` (ok. `-30%` bazowego HP) | `0` |
| **`-1` (Łatwy)** | `80%` (`-20%`) | `-1 × hp_delta_down` (ok. `-15%` bazowego HP) | `0` |
| **`0` (Domyślny)** | `100%` | `0` | `0` |
| **`+1` (Trudny)** | `125%` (`+25%`) | `+15 HP` | `+2 Ataku` |
| **`+2` (Ekstremalny)** | `150%` (`+50%`) | `+30 HP` | `+4 Ataku` |

### 3. Pełny rejestr jednostek wroga (`ENEMY_UNIT_REGISTRY` — 30 jednostek)

| ID | Nazwa w rejestrze | Bazowe HP | `scales_hp` | `hp_delta_down` | `attack_class` | `receives_mage_shield` | `mandatory_min_one` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `75` | Man-at-Arms | `45` | Tak | `7` | `4` (Melee) | Tak | Nie |
| `93` | Spearman | `45` | Tak | `7` | `4` (Melee) | Tak | Nie |
| `358` | Pikeman | `55` | Tak | `8` | `4` (Melee) | Tak | Nie |
| `359` | Halberdier | `60` | Tak | `9` | `4` (Melee) | Tak | Nie |
| `41` | Huskarl | `70` | Tak | `11` | `4` (Melee) | Tak | Nie |
| `694` | Berserker Szturmowy | `185` | Tak | `28` | `4` (Melee) | Tak | **Tak** |
| `448` | Scout Cavalry | `65` | Tak | `10` | `4` (Melee) | Tak | Nie |
| `1370` | Steppe Lancer | `80` | Tak | `12` | `4` (Melee) | Tak | Nie |
| `1372` | Elite Steppe Lancer | `100` | Tak | `15` | `4` (Melee) | Tak | Nie |
| `38` | Knight | `120` | Tak | `18` | `4` (Melee) | Tak | Nie |
| `283` | Cavalier | `140` | Tak | `21` | `4` (Melee) | Tak | Nie |
| `569` | Paladin | `180` | Tak | `27` | `4` (Melee) | Tak | Nie |
| `4` | Archer | `30` | Tak | `5` | `3` (Pierce) | Tak | Nie |
| `24` | Crossbowman | `35` | Tak | `5` | `3` (Pierce) | Tak | Nie |
| `492` | Arbalester | `40` | Tak | `6` | `3` (Pierce) | Tak | Nie |
| `474` | Heavy Cav Archer | `80` | Tak | `12` | `3` (Pierce) | Tak | Nie |
| `557` | Snajper Imperialny | `90` | Tak | `14` | `3` (Pierce) | **Nie** | **Tak** |
| `280` | Mangonel | `50` | Tak | `8` | `4` (Melee) | **Nie** | **Tak** |
| `588` | Moździerz Oblężniczy | `350` | Tak | `53` | `4` (Melee) | **Nie** | **Tak** |
| `1134` | Żelazny Słoń-Tank | `1450` | Tak | `218` | **None** | **Nie** | **Tak** |
| `441` | Szakal Dywersyjny | `95` | Tak | `14` | **None** | **Nie** | Nie |
| `842` | Arcymag Tarczy | `240` | **Nie** | `0` | **None** | **Nie** | **Tak** |
| `440` | Fanatyk Kamikaze (Petard) | `115` | **Nie** | `0` | **None** | **Nie** | **Tak** |
| `1263` | Płonący Wielbłąd | `115` | **Nie** | `0` | **None** | **Nie** | **Tak** |
| `35` | Battering Ram | `175` | **Nie** | `0` | **None** | **Nie** | **Tak** |
| `422` | Capped Ram | `200` | **Nie** | `0` | **None** | Tak | **Tak** |
| `548` | Siege Ram | `270` | **Nie** | `0` | **None** | Tak | **Tak** |
| `330` | Heavy Camel Rider | `140` | Tak | `21` | `4` (Melee) | Tak | Nie |
| `556` | Elite Mameluke | `100` | Tak | `15` | `4` (Melee) | Tak | Nie |
| `698` | Wielki Chan Subotai (Boss) | `4500` | **Nie** | `0` | **None** | **Nie** | **Tak** |

*(Wzór całkowitoliczbowy: `hp_delta_down = max(2, (base_hp * 15 + 50) // 100)`; gwarantuje zerowy dryf HP przy wielokrotnych zmianach poziomu trudności).*

---

## E. Ekspedycje: 4 Questy (Q1–Q4) i 6 Settlementów (G1–G3)

### 1. Mechanika garnizonów, smyczy i zawalania obozów (wspólna dla 10 celów)
- **Detektory (`Garrison_Detect_*_P1..P4`):** uzbrajane w `t=4s` (`01c`) na kwadrat `±20` (`detect_radius=20`) wokół środka obozu `(cx, cy)` dla `Q2–Q4` i `G1–G3`; dla `Q1 - Karawanseraj (154, 190)` przycięte przez `detect_radius=14, detect_y2_max=191` (`140..168, 176..191`), aby wozy jadące szlakiem `y=194` nie budziły garnizonu Q1. Warunek: filtr **`object_type=ObjectType.MILITARY`** oraz jednolity próg **`quantity=1`** dla wszystkich `P1–P4` (brak możliwości obudzenia przez `MAP_REVEALER`).
- **Spawn garnizonu (`Garrison_Spawn_*`):** jednorazowy; szuka wolnych kafelków poza `occupied_tiles` w pierścieniach `r=3..12` wokół `(cx, cy+2)` (przy warunku `max(|x-cx|, |y-cy|) < 13`), stawia oddział i wydaje `attack_move` w promieniu `±13` na `(cx, cy)`. Aktywuje smycz.
- **Smycz (`Garrison_Leash_*`):** pętla co **`2s`**, wydaje `attack_move` na `(cx, cy)` jednostkom właściciela obozu znajdującym się w 4 pasach strefy `ring_inner=14 .. ring_outer=20` wokół `(cx, cy)`.
- **Zniszczenie budynku głównego:** dezaktywuje `t_spawn`, `t_leash` i 4 detektory `t_detect`. Dla `Q2–Q4` i `G1–G3` wywołuje `collapse_camp_buildings` — `kill_object` w promieniu `±14` dla 10 typów budynków (`Castle, Keep, Bombard Tower, Guard Tower, Barracks, Stable, Archery Range, Siege Workshop, Monastery, Fortified Wall`).

### 2. Cztery Questy poboczne (Q1–Q4)

#### `Q1 - Karawanseraj` `(154, 190)` | Właściciel: `P5`
- **Teren i zabudowa:** strefa bez drzew `r=9`, podłoże `DIRT_1` `r=7`; `Market` (`4×4`, cel główny) na `(154, 190)` + `2x Guard Tower` na `(149, 187)` i `(159, 187)`
- **Garnizon (`±14`):** `12x Steppe Lancer`, `10x Crossbowman`, `4x Elite Berserk`
- **Zmiany na mapie po zburzeniu:**
  - Usuwa `Guard Tower` `P5` z obszaru `(145..165, 182..195)` (`remove_object`); teleportuje wszystkie jednostki `P1–P5` z pasa `(105..199, 183..187)` na `(154, 192)`
  - Buduje **Mur Handlowy (`P4`)** z `Fortified Wall` na `y=186, x=105..199` z dwoma 2-kratkowymi otworami wypadowymi (`x=122..123` i `x=170..171`)
  - Stawia **`6x Keep` (`P4`)** osłaniających mur na `y=184` przy `x=115, 122, 145, 160, 170, 190`
  - Stawia pojedynczy sojuszniczy **`Market` (`P2`)** w prawym rogu mapy na `(195, 194)` (flara)
- **Nagroda dla graczy (`P1–P4`):** `+30` Bonus Pop Cap (`230 pop`), `+500 Gold`, `+20%` Work Rate wieśniaków (`×1.20` dla `Villager M/F`), `+25%` prędkości Trade Carts (`×1.25` dla Empty/Full), `4x Trade Cart (Empty)` spawnowane na `(px+0..3, py+5)`
- **Adaptacja Hordy:** **`+8 HP, +1 Atak`**

#### `Q2 - Klif Artylerii` `(28, 32)` | Właściciel: `P6` (Dwuetapowy)
- **Teren i zabudowa:** plateau `flat_radius=9, height=4`, strefa bez drzew `r=11`, `DIRT_2` `r=10`; `University` (`4×4`, cel główny) na `(28, 32)` + `2x Keep` na `(23, 37)` i `(33, 37)` + **`2x Bombard Tower`** na `(24, 34)` i `(32, 34)` (`q2_bombard_towers`)
- **Garnizon (`±20`):** `6x Elite Janissary`, **`1x Siege Onager`**, `14x Halberdier`
- **Etap 1 (`06_Quest2_Shield_Loop` & `06_Quest2_Batteries_Down`):** pętla tarczy startuje z `enabled=False` i jest aktywowana dopiero przez `Garrison_Spawn_Quest2_SniperCliff` (z komunikatem na czacie i flarą na `(28, 30)` wskazującą obie baszty), po czym co `2s` leczy wyłącznie `University` (`object_list_unit_id=BuildingInfo.UNIVERSITY.ID`, `object_type=ObjectType.BUILDING` w `26..30, 28..34`) o `+400 HP`; zniszczenie obu `Bombard Tower` dezaktywuje pętlę tarczy (także w `t_q2` na wypadek siłowego przebicia); etykieta Objectives: `"Q2: Klif Artylerii (28,30) - zniszcz 2 Baszty Bombardowe, by zdjac tarcze Uniwersytetu"`
- **Nagroda dla graczy (`P1–P4`) w Etapie 2 (`06_Quest2_Sniper_Cliff_Buff`):** `collapse_camp_buildings` (`P6, ±14`); darmowe technologie: `Ballistics (93)`, `Chemistry (47)`, `Siege Engineers (377)`, `Thumb Ring (437)`, `PLAYER_RANGED_UNITS` (`+2` Range/Search, `+4` Atak `cl=3`), `PLAYER_MOUNTED_RANGED_UNITS` (`×1.12` prędkości), `PLAYER_CAVALRY_UNITS` (`×1.12` prędkości, `+4` Atak `cl=4`), **`2x Bombard Cannon` (`P3`) na `(27, 36)` i `(29, 36)`** oraz **`MAP_REVEALER` (`P1–P4`) na `G2_Snipers (68, 34)`**
- **Adaptacja Hordy:** **`+8 HP, +1 Atak`**

#### `Q3 - Skarbiec` `(142, 118)` | Właściciel: `P8`
- **Teren i zabudowa:** plateau `flat_radius=10, height=2`, strefa bez drzew `r=11`, `ROAD` `r=10`; `Krepost` (`4×4`, cel główny) na `(142, 118)` + `4x Keep` (`±5, ±5`) + 2 linie `Fortified Wall` (`x=135..149` na `y=110` i `y=126`)
- **Garnizon (`±20`):** `18x Halberdier`, `2x Elite Battle Elephant`, `14x Arbalester`
- **Nagroda dla graczy (`P1–P4`):** `collapse_camp_buildings` (`P8, ±14`); `+20` Bonus Pop Cap (`250 pop`), jednorazowo `+600 Gold, +300 Stone` oraz stały pasywny dochód co `60s` (`06b_Quest3_Passive_Resource_Trickle`): **`+100 Food, +100 Wood, +90 Gold, +20 Stone`** dla każdego gracza `P1–P4` (`310/min` na gracza = `1240/min` dla drużyny)
- **Adaptacja Hordy:** **`+10 HP, +1 Atak`**

#### `Q4 - Krwawy Ołtarz` `(105, 20)` | Właściciel: `P7` (Dwuetapowy)
- **Teren i zabudowa:** plateau `flat_radius=9, height=3`, strefa bez drzew `r=10`, `DIRT_3` `r=9`; `Monastery` (`3×3`, cel główny) na `(105, 20)` + `2x Keep` na `(100, 24)` i `(110, 24)`; polana `(105, 34)` (`r=7`) pod kontratak + zarezerwowany plac `(58, 152)` (`mark_footprint(3, 1)` + `2x TORCH` `(56, 150), (60, 154)`) w Twierdzy
- **Garnizon (`±20`):** `14x Paladin`, `2x Elite Battle Elephant`, `12x Halberdier`
- **Etap 1 (`06_Quest4_Stage1_Altar_Broken`):** po zburzeniu `Monastery` wykonuje `collapse_camp_buildings` (`P7, ±14`), dezaktywuje smycz i detektory `Quest4_BloodAltar`, spawnuje `RELIC` (`GAIA`) na `(105, 20)`, spawnuje kontratak `P7` na `(105, 34) -> (105, 20)` (`6x Heavy Camel Rider + 6x Elite Mameluke + 4x Elite Steppe Lancer`) i aktywuje `Stage2` (`timer=30s`)
- **Nagroda w Etapie 2 (`06_Quest4_Stage2_Ritual_Complete`):** obniża Max HP `IMAM_UNIT_ID` (`P7`) do **`120 HP`** (`Operation.SET`), daje `PLAYER_RANGED + PLAYER_CAVALRY + PLAYER_INFANTRY` **`×1.30` Max HP i `+2/+2` pancerza**, `PLAYER_PROD_BUILDINGS` **`×1.40` Work Rate**, czyści `kill_object` (`ObjectType.BUILDING` dla `P1–P4`) na `(56..60, 150..154)` i stawia **`BuildingInfo.MONASTERY` (`P1`) na `(58, 152)` + `2x Monk` (`P1`) na `(57, 155)` i `(59, 155)`**
- **Adaptacja Hordy:** **`+10 HP, +1 Atak`**

### 3. Sześć Settlementów Hordy (`G1–G3`) i Gradacja Furii (`05_Settlement_Destroyed_*`)

- **Efekty wspólne po zburzeniu każdego Settlementu:**
  - `collapse_camp_buildings` (`±14` wokół `(cx, cy)`), wyłączenie wszystkich triggerów falowych obozu (`03_W*_<camp>_*` i `03_Endless_*_<camp>`) oraz wyłączenie garnizonu i smyczy (`t_spawn`, `t_leash`, `t_detect`)
  - Jednorazowa nagroda `Food`+`Gold` dla każdego `P1–P4`, Furia Hordy (globalny buff przez `ENEMY_UNIT_REGISTRY`), natychmiastowy kontratak spawnowany jako **`PlayerId.EIGHT`** oraz flara na `(cx, cy)`

| Stopień (Grade) | Obozy | Nagroda (`P1–P4`) | Furia Hordy | Kontratak (`P8`) |
| :--- | :--- | :--- | :--- | :--- |
| **Grade 1** | `G1_North`, `G1_East` | `+700 Food, +700 Gold` | **`+8 HP, +1 Atk`** | `8x Cavalier, 10x Pikeman` |
| **Grade 2** | `G2_Snipers`, `G2_Mages` | `+1000 Food, +1000 Gold` | **`+14 HP, +1 Atk`** | `10x Cavalier, 12x Halberdier` |
| **Grade 3** | `G3_North`, `G3_East` | `+1500 Food, +1500 Gold` | **`+20 HP, +2 Atk`** | `1x Iron Elephant, 12x Paladin, 14x Halberdier` |

#### `G1 - Północny` `(76, 72)` | Grade 1 | Właściciel: `P5`
- **Teren i zabudowa:** plateau `flat_radius=9, height=1`, bez drzew `r=11`; cel główny `Guard Tower` `(76, 72)` + `2x Guard Tower` `(71, 76), (81, 76)` + `Barracks` `(70, 68)` + `Siege Workshop` `(82, 68)`
- **Garnizon (`±20`):** `14x Pikeman`, `6x Elite Berserk`, `8x Crossbowman`
- **Po zburzeniu:** `+700F/+700G`, Furia `+8 HP / +1 Atk`, kontratak `8x Cav, 10x Pike` z `(48, 86)->(48, 138)`, wycofuje fale `G1_North` (Berserkerzy, Petardy)

#### `G1 - Wschodni` `(132, 152)` | Grade 1 | Właściciel: `P5`
- **Teren i zabudowa:** plateau `flat_radius=9, height=1`, bez drzew `r=11`; cel główny `Guard Tower` `(132, 152)` + `2x Guard Tower` `(127, 156), (137, 156)` + `Barracks` `(126, 148)` + `Siege Workshop` `(138, 148)`
- **Garnizon (`±20`):** `12x Huskarl`, `10x Pikeman`, `3x Flaming Camel`
- **Po zburzeniu:** `+700F/+700G`, Furia `+8 HP / +1 Atk`, kontratak `8x Cav, 10x Pike` z `(117, 178)->(68, 162)`, wycofuje fale `G1_East` (Huskarle, Płonące Wielbłądy)

#### `G2 - Akademia` `(68, 34)` | Grade 2 | Właściciel: `P6`
- **Teren i zabudowa:** plateau `flat_radius=13, height=2`, bez drzew `r=14`; cel główny `Castle` `(68, 34)` + `Archery Range` `(61, 29)` + `Monastery` `(75, 29)` + `4x Guard Tower` `(59, 25), (73, 25), (59, 43), (77, 43)`
- **Garnizon (`±20`):** `7x Elite Janissary`, `2x Siege Onager`, `16x Halberdier`
- **Po zburzeniu:** `+1000F/+1000G`, Furia `+14 HP / +1 Atk`, kontratak `10x Cav, 12x Halb` z `(48, 86)->(48, 138)`, wycofuje fale `G2_Snipers` (Snajperzy, Moździerze) oraz **wszystkie wyłomy Saperów** (F9, F12, Endless)

#### `G2 - Klasztor` `(148, 72)` | Grade 2 | Właściciel: `P7`
- **Teren i zabudowa:** plateau `flat_radius=13, height=2`, bez drzew `r=14`; cel główny `Castle` `(148, 72)` + `Archery Range` `(141, 67)` + `Monastery` `(155, 67)` + `4x Guard Tower` `(139, 63), (153, 63), (139, 81), (157, 81)`
- **Garnizon (`±20`):** `14x Cavalier`, `8x Szakal (Hussar)`, `1x Arcymag (Imam)`
- **Po zburzeniu:** `+1000F/+1000G`, Furia `+14 HP / +1 Atk`, kontratak `10x Cav, 12x Halb` z `(116, 114)->(54, 146)`, wycofuje fale `G2_Mages` (Arcymagowie, Szakale)

#### `G3 - Cytadela Północna` `(142, 24)` | Grade 3 | Właściciel: `P8`
- **Teren i zabudowa:** plateau `flat_radius=17, height=4`, bez drzew `r=18`; cel główny `Castle` `(142, 24)` + `2x Castle` `(133, 32), (151, 16)` + `Stable` `(135, 17)` + `Siege Workshop` `(149, 31)` + `4x Keep` `(130, 12), (154, 12), (130, 36), (154, 36)`
- **Garnizon (`±20`):** `3x Iron Elephant`, `20x Halberdier`, `12x Paladin`
- **Po zburzeniu:** `+1500F/+1500G`, Furia `+20 HP / +2 Atk`, kontratak `1x Iron Elephant, 12x Pal, 14x Halb` z `(116, 114)->(54, 146)`, wycofuje fale `G3_North` (Słonie-Tanki Płn.)

#### `G3 - Cytadela Wschodnia` `(176, 56)` | Grade 3 | Właściciel: `P8`
- **Teren i zabudowa:** plateau `flat_radius=17, height=4`, bez drzew `r=18`; cel główny `Castle` `(176, 56)` + `2x Castle` `(167, 64), (185, 48)` + `Stable` `(169, 49)` + `Siege Workshop` `(183, 63)` + `4x Keep` `(164, 44), (188, 44), (164, 68), (188, 68)`
- **Garnizon (`±20`):** `3x Iron Elephant`, `20x Arbalester`, `2x Siege Onager`
- **Po zburzeniu:** `+1500F/+1500G`, Furia `+20 HP / +2 Atk`, kontratak `1x Iron Elephant, 12x Pal, 14x Halb` z `(117, 178)->(68, 162)`, wycofuje fale `G3_East` (Słonie Wsch.) oraz **Rajdy Handlowe** (F8, F10, F12, F14, Endless)
