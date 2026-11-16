# BALANCE_DOSSIER.md — Kroniki Rubieży: Horda i Ekspedycje (`v7.0.3`)

Zestawienie surowych danych liczbowych, współrzędnych i mechanik wyeksportowanych bezpośrednio z modułów `horde_config.py`, `horde_map.py`, `horde_waves.py` oraz `horde_quests.py`.

---

## 1. Parametry startowe i mapa (`200×200`)

### 1.1. Konfiguracja graczy, zasoby startowe i populacja (`0:00–0:01`)

| Gracz | Typ / Cywilizacja | `lock_civ` | Zasoby startowe (`F/W/G/S`) | TC `(cx, cy)` (`4×4`) | Domki (`2×2`) | Jednostki startowe | Budynki / Obiekty startowe | Bonus Pop Cap (`0:01`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1 (Niebieski)** | Człowiek / Dowolna | `False` | `500 / 600 / 400 / 300` | `(76, 124)` | `2` (`+10 pop`) | `6x Villager`, `1x Scout`, `1x King` `(4,138)` | `1x TC`, `2x House`, `1x Gate` `(104,114)`, `11x Fort. Palisade`, `2x Guard Tower`, `12x Map Revealer` | `+0` |
| **P2 (Czerwony)** | Człowiek / Dowolna | `False` | `500 / 600 / 400 / 300` | `(32, 164)` | `6` (`+30 pop`) | `6x Villager`, `1x Scout`, `1x King` `(4,164)` | `1x TC`, `6x House`, `1x Feitoria` `(54,146)` (`5×5`, `+3000 HP`), `2x Map Revealer` | `+20` (`RES=32`) |
| **P3 (Zielony)** | Człowiek / Dowolna | `False` | `500 / 600 / 400 / 300` | `(32, 122)` | `2` (`+10 pop`) | `6x Villager`, `1x Scout` | `1x TC`, `2x House`, `1x Gate` `(48,100)`, `11x Fort. Palisade`, `2x Guard Tower`, `2x Map Revealer` | `+0` |
| **P4 (Żółty)** | Człowiek / Dowolna | `False` | `500 / 600 / 400 / 300` | `(76, 168)` | `2` (`+10 pop`) | `6x Villager`, `1x Scout` | `1x TC`, `2x House`, `2x Gate` `(104,162)/(104,193)`, `21x Fort. Palisade`, `4x Guard Tower`, `2x Map Revealer` | `+0` |
| **P5 (Turkusowy)** | AI / `VIKINGS` | `True` | `0 / 0 / 0 / 0` | — | `0` | `0` | `8x Guard Tower`, `2x Barracks`, `2x Siege Workshop`, `1x Market` (`Q1`) | `+0` |
| **P6 (Fioletowy)** | AI / `TURKS` | `True` | `0 / 0 / 0 / 0` | — | `0` | `0` | `1x Castle`, `1x Archery Range`, `1x Monastery`, `4x Guard Tower`, `1x University` (`Q2`), `2x Keep`, `2x Bombard Tower` | `+0` |
| **P7 (Szary)** | AI / `SARACENS` | `True` | `0 / 0 / 0 / 0` | — | `0` | `0` | `1x Castle`, `1x Archery Range`, `2x Monastery` (`G2_M`, `Q4`), `4x Guard Tower`, `2x Keep` | `+0` |
| **P8 (Pomarańczowy)** | AI / `PERSIANS` | `True` | `0 / 0 / 0 / 0` | — | `0` | `0` | `6x Castle`, `2x Stable`, `2x Siege Workshop`, `12x Keep`, `1x Krepost` (`Q3`), `30x Fortified Wall` (`Q3`) | `+0` |

- **Dyplomacja (`01_Init`):** `P1–P4` `ALLY`, `P5–P8` `ALLY`, `P1–P4` vs `P5–P8` `ENEMY`; `TECH_CARTOGRAPHY (19)` dla `P1–P4`; `MAP_REVEALER_ID (837)` ma `ATTR_LINE_OF_SIGHT = 4`; `FORTIFIED_PALISADE_ID (119)` oraz wszystkie bramy palisadowe (`789, 792, 793, 797, 801`) dla `P1–P4` otrzymują **`+600 HP`**; `UnitInfo.KING.ID` dla `P1` i `P2` ma `HP = 9999` i `Regeneration = 5000/min` (`83.33 HP/s`).
- **Łączna liczba obiektów startowych (`5350`):** `P0 (Gaia) = 5142`, `P1 = 37`, `P2 = 18`, `P3 = 26`, `P4 = 39`, `P5 = 13`, `P6 = 12`, `P7 = 10`, `P8 = 53`.

### 1.2. Złoża surowców i obiekty `GAIA` (`P0 = 5142`)

| Obiekt (`ID`) | Łącznie na mapie | Rozkład wewnątrz Twierdzy (na bazę `P1–P4`, offsety od TC `(cx, cy)`) | Rozkład poza Twierdzą (`GAIA`) |
| :--- | :--- | :--- | :--- |
| **Gold Mine (`66`)** | `81` | `14` na gracza (`56` łącznie): klaster `8` na `(+7, -6)` oraz klaster `6` na `(+7, +5)` | `24` przy Reliktach (`4×6` na `(rx+3, ry+3)`) + `1` na `PoI 2 (124, 178)` |
| **Stone Mine (`102`)** | `24` | `6` na gracza (`24` łącznie): klaster `6` na `(-8, +5)` | `0` |
| **Forage Bush (`59`)** | `24` | `6` na gracza (`24` łącznie): klaster `6` na `(-8, -4)` | `0` |
| **Sheep (`594`)** | `24` | `6` na gracza: `(-3..0, +2)` i `(-3..-2, +3)` | `0` |
| **Wild Boar (`48`)** | `8` | `2` na gracza: `(-9, -1)` i `(+1, +9)` | `0` |
| **Deer (`65`)** | `16` | `4` na gracza: `(-7..-8, -7..-8)` | `0` |
| **Relic (`285`)** | `4` | `0` (dodatkowy `1` spawnuje `Q4` po zburzeniu) | `4`: `(54, 62)`, `(116, 88)`, `(168, 128)`, `(92, 44)` |
| **Drzewa (`349` Oak / `350` Pine)** | `4834` (`1598` + `3236`) | `6` dębów przy TC + 2 zagajniki (`r=4.8` na `(-14,0)` i `(0,+14)`), lasy obwodowe `y=95..105` i `x=99..109`, puszcza zaplecza `x=0..13` i `x=26..98, y=180..188`, zagajniki `(54,122)` i `(54,172)` | `11` organicznych lasów (`r=5.0..7.5`), wyłom północny `(75..80, 95..105)` (`66` drzew), wyłom wschodni `(99..109, 137..142)` (`66` drzew) |
| **Klify / Flagi / Pochodnie / Outpost** | `97` / `4` / `24` / `2` | Komnaty `(4, 138)` i `(4, 164)`: obwody `ROCK_CLIFF_ID`, `2× FLAG_A`, `2× FLAG_B`, `8× TORCH` | Grzbiety `(16,48)->(44,48)` i `(124,134)->(158,134)`; krąg `8× TORCH` (`r=10` wokół `116,114`); `PoI 1/2/3`: `2× OUTPOST`, `6× TORCH` |

### 1.3. Geometria Twierdzy Sojuszu, bram i przeszkód terenowych

- **Obszar Twierdzy Sojuszu:** `x = 0..104`, `y = 100..199` (`105×100` kratek; bariera północna `y = 100` z wzgórzami `height = 3` co `8` kratek poza `x = 72..84`, pas lasu `x = 0..108, y = 95..105`; bariera wschodnia `x = 104` z wzgórzami `height = 3` co `8` kratek dla `y = 100..180` poza `y = 134..146`, pas lasu `x = 99..109, y = 95..199`).
- **Bramy (`4` przełęcze, każda z płaską strefą `13×13` bez drzew):**
  - `Brama Północna (48, 100)` [`P3`, oś X]: Brama `789` (`x=46..49`, szer. `4`), mur `119` (`x=41..55`, `11` pól), `2× Guard Tower` `(44, 104)` i `(52, 104)`.
  - `Brama Centralna (104, 114)` [`P1`, oś Y]: Brama `793` (`y=112..115`, szer. `4`), mur `119` (`y=107..121`, `11` pól), `2× Guard Tower` `(100, 110)` i `(100, 118)`.
  - `Brama Wschodnia (104, 162)` [`P4`, oś Y]: Brama `793` (`y=160..163`, szer. `4`), mur `119` (`y=155..169`, `11` pól), `2× Guard Tower` `(100, 158)` i `(100, 166)`.
  - `Brama Handlowa (104, 193)` [`P4`, oś Y]: Brama `793` (`y=191..194`, szer. `4`), mur `119` (`y=186..199`, `10` pól), `2× Guard Tower` `(100, 189)` i `(100, 197)`.
- **Plac Targowy i Korytarz Handlowy:** czysty plac `x = 2..24, y = 176..198` (`23×23`, `elev=0`), korytarz bez drzew `x = 2..199, y = 189..199` z drogą na `y = 194` (`x = 3..198`), pas pod Mur Q1 `x = 104..199, y = 183..188`.
- **Rzeka (`TERRAIN_WATER = 1`, `r = 2`):** `rx = round(62 + 0.9t)`, `ry = round(8 + 0.8t + 3*sin(0.08t))` dla `t = 0..139` przy warunku `rx > 112 or ry < 90`; **3 brody (`TERRAIN_SHALLOWS = 4`, `r = 5`):** `(84, 30)`, `(122, 62)`, `(154, 92)`.

### 1.4. Macierz odległości euklidesowych w kratkach

| Punkt `(x, y)` | `P1_TC` `(76,124)` | `P2_TC` `(32,164)` | `P3_TC` `(32,122)` | `P4_TC` `(76,168)` | `Feitoria` `(54,146)` | `G_North` `(48,100)` | `G_Center` `(104,114)` | `G_East` `(104,162)` | `G_Trade` `(104,193)` |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **P1_TC `(76,124)`** | `0.0` | `59.5` | `44.0` | `44.0` | `31.1` | `36.9` | `29.7` | `47.2` | `74.5` |
| **P2_TC `(32,164)`** | `59.5` | `0.0` | `42.0` | `44.2` | `28.4` | `66.0` | `87.7` | `72.0` | `77.6` |
| **P3_TC `(32,122)`** | `44.0` | `42.0` | `0.0` | `63.7` | `32.6` | `27.2` | `72.4` | `82.4` | `101.1` |
| **P4_TC `(76,168)`** | `44.0` | `44.2` | `63.7` | `0.0` | `31.1` | `73.5` | `60.8` | `28.6` | `37.5` |
| **Feitoria `(54,146)`** | `31.1` | `28.4` | `32.6` | `31.1` | `0.0` | `46.4` | `59.4` | `52.5` | `68.6` |
| **G1_North `(76,72)`** | `52.0` | `102.0` | `66.6` | `96.0` | `77.2` | `39.6` | `50.5` | `94.3` | `124.2` |
| **G1_East `(132,152)`** | `62.6` | `100.7` | `104.4` | `58.2` | `78.2` | `98.8` | `47.2` | `29.7` | `49.6` |
| **G2_Snipers `(68,34)`** | `90.4` | `134.9` | `95.1` | `134.2` | `112.9` | `69.0` | `87.7` | `133.0` | `163.0` |
| **G2_Mages `(148,72)`** | `88.8` | `148.1` | `126.3` | `120.0` | `119.6` | `103.8` | `60.8` | `100.2` | `128.8` |
| **G3_North `(142,24)`** | `119.8` | `178.0` | `147.3` | `158.4` | `150.4` | `120.9` | `97.7` | `143.1` | `173.2` |
| **G3_East `(176,56)`** | `120.9` | `180.0` | `158.4` | `150.1` | `151.6` | `135.4` | `92.5` | `128.1` | `154.8` |
| **Q1 `(154,190)`** | `102.2` | `124.7` | `139.7` | `81.0` | `109.3` | `139.1` | `91.0` | `57.3` | `50.1` |
| **Q2 `(28,32)`** | `103.8` | `132.1` | `90.1` | `144.2` | `116.9` | `70.9` | `111.8` | `150.6` | `178.0` |
| **Q3 `(142,118)`** | `66.3` | `119.2` | `110.1` | `82.8` | `92.3` | `95.7` | `38.2` | `58.1` | `84.1` |
| **Q4 `(105,20)`** | `108.0` | `161.4` | `125.4` | `150.8` | `135.9` | `98.2` | `94.0` | `142.0` | `173.0` |
| **PoI 1 `(30,76)`** | `66.5` | `88.0` | `46.0` | `102.9` | `74.0` | `30.0` | `83.2` | `113.5` | `138.4` |
| **PoI 2 `(124,178)`** | `72.2` | `93.1` | `107.7` | `49.0` | `77.0` | `108.9` | `67.1` | `25.6` | `25.0` |
| **PoI 3 `(50,90)`** | `42.8` | `76.2` | `36.7` | `82.2` | `56.1` | `10.2` | `59.1` | `90.0` | `116.3` |
| **Bród 1 `(84,30)`** | `94.3` | `143.7` | `105.7` | `138.2` | `119.8` | `78.7` | `86.3` | `133.5` | `164.2` |
| **Bród 2 `(122,62)`** | `77.2` | `136.0` | `108.2` | `115.6` | `108.1` | `83.2` | `55.0` | `101.6` | `132.2` |
| **Bród 3 `(154,92)`** | `84.3` | `141.7` | `125.6` | `108.9` | `113.6` | `106.3` | `54.6` | `86.0` | `112.7` |
| **Sp_G1N `(48,86)`** | `47.2` | `79.6` | `39.4` | `86.6` | `60.3` | `14.0` | `62.6` | `94.4` | `120.8` |
| **Sp_G1E `(117,178)`** | `67.8` | `86.1` | `101.8` | `42.2` | `70.7` | `104.1` | `65.3` | `20.6` | `19.8` |
| **Sp_G2S `(68,60)`** | `64.5` | `110.1` | `71.7` | `108.3` | `87.1` | `44.7` | `64.9` | `108.2` | `137.8` |
| **Sp_G2M `(116,114)`** | `41.2` | `97.8` | `84.4` | `67.2` | `69.8` | `69.4` | `12.0` | `49.5` | `79.9` |
| **Sp_G3N `(106,72)`** | `60.0` | `118.1` | `89.3` | `100.6` | `90.4` | `64.4` | `42.0` | `90.0` | `121.0` |
| **Sp_G3E `(156,152)`** | `84.8` | `124.6` | `127.6` | `81.6` | `102.2` | `119.9` | `64.4` | `53.0` | `66.2` |
| **Sp_Trade `(162,180)`** | `102.6` | `131.0` | `142.4` | `86.8` | `113.2` | `139.3` | `87.9` | `60.7` | `59.4` |
| **Sp_JackalN `(52,86)`** | `44.9` | `80.5` | `41.2` | `85.4` | `60.0` | `14.6` | `59.1` | `92.1` | `119.0` |
| **Sp_JackalE `(116,162)`** | `55.2` | `84.0` | `93.0` | `40.4` | `64.0` | `92.0` | `49.5` | `12.0` | `33.2` |
| **Sp_BreachN `(78,94)`** | `30.1` | `83.8` | `53.9` | `74.0` | `57.3` | `30.6` | `32.8` | `72.8` | `102.4` |
| **Sp_BreachE `(115,140)`** | `42.2` | `86.4` | `84.9` | `48.0` | `61.3` | `78.0` | `28.2` | `24.6` | `54.1` |

---

## 2. Pełny rejestr jednostek (`ENEMY_UNIT_REGISTRY` + modyfikacje `01b` i `01d–01f`)

- **Wspólna blokada konwersji AI (`01b`):** dla `P5–P8` jednostki `IMAM_UNIT_ID (842)`, `MISSIONARY` oraz `MONK` mają `ATTR_MAXIMUM_RANGE = 0` i `ATTR_WORK_RATE = 0`.
- **Skalowanie ujemne (`hp_delta_down`):** `max(2, (base_hp * 15 + 50) // 100)` jeśli `scales_hp=True`, inaczej `0`.

| ID | Nazwa / Rola | Właściciel | `base_hp` (`01b`) | `scales_hp` | `hp_delta_down` | Atak (`01b` / Cap) & `attack_class` | Pancerz `M/P` (`01b` / Cap) | Prędkość (`01b` / Cap) | Zasięg `Min/Max` (`LOS/Srch`) | Reload / Blast | Hero | `receives_mage_shield` | `mandatory_min_one` |
| :--- | :--- | :--- | ---: | :--- | ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `75` | Man-at-Arms | `P5` | `45` | `True` | `7` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Squires | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `93` | Spearman | `P5` | `45` | `True` | `7` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Squires | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `358` | Pikeman | `P5, P8` | `55` | `True` | `8` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Squires | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `359` | Halberdier | `P5, P6, P7, P8` | `60` | `True` | `9` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Squires | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `41` | Huskarl | `P5` | `70` | `True` | `11` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Squires | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `694` | Berserker Szturmowy | `P5` | `185` | `True` | `28` | baz. + `+12` + Kuźnia (`cl=4`) | baz. M / `0` P (Cap) | `1.40` (Cap) | `0 / 0` (melee) | bazowy | `0` | `True` | `True` |
| `448` | Scout Cavalry | `P5, P7` | `65` | `True` | `10` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `1370` | Steppe Lancer | `P5` | `80` | `True` | `12` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | baz. (`1`) | bazowy | `0` | `True` | `False` |
| `1372` | Elite Steppe Lancer | `P7` (`Q4`) | `100` | `True` | `15` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | baz. (`1`) | bazowy | `0` | `True` | `False` |
| `38` | Knight | `P5, P7, P8` | `120` | `True` | `18` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `283` | Cavalier | `P7, P8` | `140` | `True` | `21` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `569` | Paladin | `P7, P8` | `180` | `True` | `27` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `4` | Archer | `P5, P7` | `30` | `True` | `5` | baz. + Kuźnia/Chem (`cl=3`) | baz. + Kuźnia | bazowy | baz. + Kuźnia | bazowy | `0` | `True` | `False` |
| `24` | Crossbowman | `P5, P6, P8` | `35` | `True` | `5` | baz. + Kuźnia/Chem (`cl=3`) | baz. + Kuźnia | bazowy | baz. + Kuźnia | bazowy | `0` | `True` | `False` |
| `492` | Arbalester | `P6, P8` | `40` | `True` | `6` | baz. + Kuźnia/Chem (`cl=3`) | baz. + Kuźnia | bazowy | baz. + Kuźnia | bazowy | `0` | `True` | `False` |
| `474` | Heavy Cav Archer | `P8` | `80` | `True` | `12` | baz. + Kuźnia/Chem (`cl=3`) | baz. + Kuźnia | baz. + Husbandry | baz. + Kuźnia | bazowy | `0` | `True` | `False` |
| `557` | Snajper Imperialny | `P6` | `90` | `True` | `14` | baz. + `+85` (`cl=3`) | baz. + Kuźnia | baz. + Squires | `0 / 19` (Cap; `21/21`) | `6.5s` | `1` | `False` | `True` |
| `280` | Mangonel | `P5` | `50` | `True` | `8` | baz. (`cl=4`) | bazowy | bazowy | baz. + SE | bazowy | `0` | `False` | `True` |
| `588` | Moździerz Oblężniczy | `P6, P8` | `350` | `True` | `53` | baz. + `+75` (`cl=4`) | bazowy | `0.58` (Cap) | `6 / 21` (Cap; `23/23`) | `10.0s` / `W=2.6, Lvl=2` | `1` | `False` | `True` |
| `1134` | Żelazny Słoń-Tank | `P8` | `1450` | `True` | `218` | `3` (`cl=4`, Cap) + `+140` (`cl=11,21`) (`None`) | `10 / 12` (Cap) | `0.72` (Cap) | `0 / 0` (melee) | bazowy | `1` | `False` | `True` |
| `441` | Szakal Dywersyjny | `P7` | `95` | `True` | `14` | `7` (`cl=4`, Cap) (`None`) | `0 / 6` (Cap) | `1.62` (Cap) | `0 / 0` (melee) | bazowy | `0` | `False` | `False` |
| `842` | Arcymag Tarczy | `P7` | `240` (`Q4:120`) | `False` | `0` | `0` (`range=0, work_rate=0`) (`None`) | `3 / 4` (`01b`) | `0.78` (Cap) | `0 / 0` | `regen 300/min` (`5/s`) | `1` | `False` | `True` |
| `440` | Fanatyk Kamikaze (Petard) | `P5` | `115` | `False` | `0` | baz. + `+95` (`None`) | baz. M / `0` P (Cap) | `1.50` (Cap) | `0 / 0` | `W=2.4` | `0` | `False` | `True` |
| `1263` | Płonący Wielbłąd | `P5` | `115` | `False` | `0` | baz. + `+95` (`None`) | baz. M / `0` P (Cap) | `1.50` (Cap) | `0 / 0` | `W=2.4` | `0` | `False` | `True` |
| `35` | Battering Ram | `P5, P7` | `175` | `False` | `0` | bazowy (`None`) | bazowy | bazowy | `0 / 0` | bazowy | `0` | `False` | `True` |
| `422` | Capped Ram | `P5, P7` | `200` | `False` | `0` | bazowy (`None`) | bazowy | bazowy | `0 / 0` | bazowy | `0` | `True` | `True` |
| `548` | Siege Ram | `P5, P7, P8` | `270` | `False` | `0` | bazowy (`None`) | bazowy | bazowy | `0 / 0` | bazowy | `0` | `True` | `True` |
| `330` | Heavy Camel Rider | `P7` (`Q4`) | `140` | `True` | `21` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | `0 / 0` (melee) | bazowy | `0` | `True` | `False` |
| `556` | Elite Mameluke | `P7` (`Q4`) | `100` | `True` | `15` | baz. + Kuźnia (`cl=4`) | baz. + Kuźnia | baz. + Husbandry | bazowy | bazowy | `0` | `True` | `False` |
| `698` | Wielki Chan Subotai | `P8` | `4500` | `False` | `0` | `45` (`cl=3`) (`None`) | `8 / 10` (`01b`) | `0.85` (`01b`) | bazowy | bazowy | `1` | `False` | `True` |

- **Uwaga do `01d` (`510s`):** po zbadaniu `TECH_BLOODLINES (435)` dla `P5–P8`, `HUSSAR_ID (441)` i `ELITE_BATTLE_ELEPHANT_ID (1134)` otrzymują `ATTR_HIT_POINTS SUBTRACT 20` (neutralizacja `+20 HP` z Bloodlines).
- **Listy jednostek graczy w `horde_config.py`:** `PLAYER_RANGED_UNITS` = `43` ID, `PLAYER_MOUNTED_RANGED_UNITS` = `19` ID, `PLAYER_CAVALRY_UNITS` = `41` ID, `PLAYER_INFANTRY_UNITS` = `44` ID, `PLAYER_PROD_BUILDINGS` = `7` ID (`Barracks, Stable, Archery Range, Castle, Siege Workshop, Krepost, Donjon`).

---

## 3. Harmonogram Fal 1–14, Rajdy Handlowe, Wyłomy, Szakale i Tryb Endless

### 3.1. Technologie AI (`01_Init`, `01d–01f`), Eskalacja Czasowa (`04a–04f`) i Poziomy Trudności

- **Technologie AI:**
  - `0:00` (`01_Init`): `Feudal Age (101)`, `Castle Age (102)`, `Imperial Age (103)` dla `P5–P8`; `TECH_FAITH (45)` dla `P8`.
  - `8:30` (`510s`, `01d`): `Forging (67)`, `Scale Mail (74)`, `Scale Barding (81)`, `Fletching (199)`, `Bloodlines (435)` + korekta `-20 HP` dla `441, 1134` + `enforce_specialized_unit_caps`.
  - `18:00` (`1080s`, `01e`): `Iron Casting (68)`, `Chain Mail (76)`, `Squires (215)`, `Chain Barding (82)`, `Bodkin Arrow (200)`, `Ballistics (93)`, `Husbandry (39)`, `TECH_FAITH (45)` dla `P5–P8` + `enforce_specialized_unit_caps`.
  - `34:30` (`2070s`, `01f`): `Blast Furnace (75)`, `Plate Mail (77)`, `Plate Barding (80)`, `Bracer (201)`, `Chemistry (47)`, `Siege Engineers (377)` + `enforce_specialized_unit_caps`.
- **Eskalacja Czasowa (pierwszy tick natychmiastowy w czasie startowym, następnie co `300s`, dotyczy jednostek z `scales_hp=True` / `attack_class != None`):**
  - **Bieg 1 (`04a`/`04b`, start `1200s` = `20:00`):** `+5 HP`, `+1 Atk` co `300s`.
  - **Bieg 2 (`04c`/`04d`, start `2700s` = `45:00`):** dodatkowo `+9 HP`, `+0 Atk` co `300s` (suma z Biegiem 1: `+14 HP`, `+1 Atk` co `300s`).
  - **Bieg 3 (`04e`/`04f`, start `3300s` = `55:00`):** dodatkowo `+6 HP`, `+1 Atk` co `300s` (suma z Biegami 1–2: `+20 HP`, `+2 Atk` co `300s`).
- **Mnożniki Sanktuarium Balansu (`scale_comp_for_level`):**
  - Poziom `-2`: `60%` liczebności (`HALF_UP`), `-2 × hp_delta_down` HP, `+0` Atk.
  - Poziom `-1`: `80%` liczebności (`HALF_UP`), `-1 × hp_delta_down` HP, `+0` Atk.
  - Poziom `0`: `100%` liczebności, `+0` HP, `+0` Atk.
  - Poziom `+1`: `125%` liczebności (`HALF_UP`), `+15` HP, `+2` Atk.
  - Poziom `+2`: `150%` liczebności (`HALF_UP`), `+30` HP, `+4` Atk.
  - *Reguła podziału:* pozycje z `mandatory_min_one=True` zachowują min. `1` szt. w grupie; nadwyżki/redukcje przydzielane metodą największych/najmniejszych reszt.

### 3.2. Składy fal 1–14 i Trybu Endless (wartości bazowe = Poziom `0`)

| Fala | Czas (`s`) | Przerwa (`s`) | Eskalacja (`+HP/+Atk`) | Tech AI | `G1_North` (`P5`) `(48,86)->(48,138)` | `G1_East` (`P5`) `(117,178)->(68,162)` | `G2_Snipers` (`P6`) `(68,60)->(48,138)` | `G2_Mages` (`P7`) `(116,114)->(54,146)` | `G3_North` (`P8`) `(106,72)->(54,146)` | `G3_East` (`P8`) `(156,152)->(68,162)` | Szakale (`P7`) + cel `MOVE` | Zdarzenia specjalne (Trade Raid `P8` / Wyłomy `P6`) |
| :--- | ---: | ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **F1** | `8:30` (`510`) | `510` | `+0 / +0` | `01d` | `6` MAA, `5` Arch | `6` MAA, `5` Scout | — | — | — | — | `0` | — |
| **F2** | `13:00` (`780`) | `270` | `+0 / +0` | `01d` | `8` MAA, `6` Arch, `1` B.Ram | `8` Spear, `6` Scout, `1` Mang | — | `5` Scout, `6` Arch | — | — | `0` | — |
| **F3** | `18:00` (`1080`) | `300` | `+0 / +0` | `01e` | `11` Pike, `3` Bers, `1` Pet, `1` B.Ram | `8` Husk, `5` Kni, `1` F.Cam | `10` Xbow, `2` Jan | `6` Kni, `1` B.Ram | — | — | `5` `(52,86)->(76,172)` | — |
| **F4** | `23:30` (`1410`) | `330` | `+5 / +1` | `01e` | `14` Pike, `4` Bers, `2` B.Ram | `10` Husk, `6` Kni, `2` F.Cam | `12` Xbow, `3` Jan | `1` Imam, `10` Kni, `2` B.Ram | — | — | `6` `(116,162)->(32,118)` | — |
| **F5** | `29:00` (`1740`) | `330` | `+10 / +2` | `01e` | `16` Pike, `4` Bers, `2` Pet, `2` C.Ram | `12` Husk, `2` F.Cam, `2` C.Ram | `14` Xbow, `3` Jan, `1` S.Onag | `1` Imam, `12` Kni | `8` Kni, `10` Pike | — | `7` `(52,86)->(76,120)` | — |
| **F6** | `34:30` (`2070`) | `330` | `+15 / +3` | `01f` | `18` Pike, `5` Bers, `2` C.Ram | `14` Husk, `3` F.Cam, `2` C.Ram | `16` Xbow, `3` Jan, `1` S.Onag | `1` Imam, `12` Cav, `2` C.Ram | `1` Ele, `10` Kni, `12` Pike | `14` Xbow, `8` Kni | `8` `(116,162)->(32,168)` | — |
| **F7** | `40:00` (`2400`) | `330` | `+25 / +5` | `01f` | `20` Halb, `5` Bers, `3` Pet, `3` C.Ram | `16` Husk, `3` F.Cam, `2` C.Ram | `18` Arb, `4` Jan, `1` S.Onag | `1` Imam, `18` Cav | `2` Ele, `16` Cav, `12` Halb, `2` S.Ram | `1` Ele, `16` Arb | `9` `(52,86)->(76,172)` | — |
| **F8** | `45:30` (`2730`) | `330` | `+39 / +6` | `01f` | `22` Halb, `6` Bers, `3` S.Ram | `18` Husk, `3` F.Cam, `3` S.Ram | `20` Arb, `4` Jan, `2` S.Onag | `2` Imam, `16` Cav, `3` S.Ram | `2` Ele, `14` Cav, `14` Halb | `2` Ele, `18` Arb, `1` S.Onag | `10` `(116,162)->(32,118)` | **Trade Raid:** `3` S.Ram, `10` Pal, `10` HCA |
| **F9** | `51:00` (`3060`) | `330` | `+53 / +7` | `01f` | `25` Halb, `7` Bers, `3` Pet, `3` S.Ram | `20` Husk, `4` F.Cam, `3` S.Ram | `22` Arb, `4` Jan, `2` S.Onag | `2` Imam, `16` Pal, `3` S.Ram | `3` Ele, `15` Pal, `16` Halb | `2` Ele, `20` Arb, `2` S.Onag | `12` `(52,86)->(76,120)` | **Wyłom N (`6×11`):** `50:15` `2` S.Onag, `8` Halb; `51:00` `2` S.Onag, `14` Halb, `8` Jan |
| **F10** | `56:30` (`3390`) | `330` | `+73 / +9` | `01f` | `28` Halb, `8` Bers, `3` Pet, `4` S.Ram | `23` Husk, `3` F.Cam, `4` S.Ram | `25` Arb, `4` Jan, `2` S.Onag | `2` Imam, `19` Pal, `4` S.Ram | `3` Ele, `19` Pal, `18` Halb | `3` Ele, `23` Arb, `2` S.Onag | `22` `(116,162)->(32,168)` | **Trade Raid:** `3` S.Ram, `14` Pal, `14` HCA |
| **F11** | `62:00` (`3720`) | `330` | `+93 / +11` | `01f` | `31` Halb, `9` Bers, `4` Pet, `4` S.Ram | `26` Husk, `4` F.Cam, `4` S.Ram | `28` Arb, `8` Jan, `4` S.Onag | `2` Imam, `22` Pal, `4` S.Ram | `4` Ele, `22` Pal, `20` Halb | `4` Ele, `26` Arb, `4` S.Onag | `14` `(52,86)->(76,172)` | — |
| **F12** | `67:30` (`4050`) | `330` | `+113 / +13` | `01f` | `34` Halb, `10` Bers, `4` Pet, `4` S.Ram | `29` Husk, `4` F.Cam, `4` S.Ram | `31` Arb, `5` Jan, `3` S.Onag | `3` Imam, `25` Pal, `4` S.Ram | `4` Ele, `25` Pal, `22` Halb | `4` Ele, `29` Arb, `3` S.Onag | `15` `(116,162)->(32,118)` | **Trade Raid:** `3` S.Ram, `18` Pal, `18` HCA; **Wyłom E (`11×6`):** `66:45` `2` S.Onag, `10` Halb; `67:30` `2` S.Onag, `16` Halb, `12` Arb |
| **F13** | `73:00` (`4380`) | `330` | `+133 / +15` | `01f` | `37` Halb, `11` Bers, `5` Pet, `4` S.Ram | `32` Husk, `5` F.Cam, `4` S.Ram | `34` Arb, `6` Jan, `3` S.Onag | `3` Imam, `28` Pal, `4` S.Ram | `6` Ele, `28` Pal, `24` Halb | `6` Ele, `32` Arb, `3` S.Onag | `16` `(52,86)->(76,120)` | — |
| **F14** | `78:30` (`4710`) | `330` | `+153 / +17` | `01f` | `40` Halb, `12` Bers, `5` Pet, `4` S.Ram | `35` Husk, `5` F.Cam, `4` S.Ram | `37` Arb, `6` Jan, `3` S.Onag | `3` Imam, `31` Pal, `4` S.Ram | `5` Ele, `31` Pal, `26` Halb | `5` Ele, `35` Arb, `3` S.Onag | `17` `(116,162)->(32,168)` | **Trade Raid:** `3` S.Ram, `22` Pal, `22` HCA |
| **Endless** | `84:00+` (`5040+`) | `330` | `+173 / +19` (`84:00`) | `01f` | `40` Halb, `12` Bers, `5` Pet, `4` S.Ram | `35` Husk, `5` F.Cam, `4` S.Ram | `37` Arb, `6` Jan, `3` S.Onag | `3` Imam, `31` Pal, `4` S.Ram | `5` Ele, `31` Pal, `26` Halb | `5` Ele, `35` Arb, `3` S.Onag | `9` `(52,86)->(32,118)` + `8` `(116,162)->(76,172)` | **Trade Raid F14:** `3` S.Ram, `22` Pal, `22` HCA; **Wyłom N+E:** `2` S.Onag, `14` Halb, `8` Jan + `2` S.Onag, `14` Halb, `10` Arb |

### 3.3. Liczebność sektorowa i sumy HP dla poziomów `-2`, `-1`, `0`, `+1`, `+2`

- **Sektory:** `Północ` = `G1_N + G2_S` (+ `34` Wyłom N w F9, `24` w Endless); `Centrum` = `G2_M + G3_N`; `Wschód` = `G1_E + G3_E + Trade Raid` (+ `42` Wyłom E w F12, `26` w Endless); `Szakale` = rajdy `P7`.

| Fala | Poziom `-2` (`N / C / E / R = Suma` \| `Łączne HP`) | Poziom `-1` (`N / C / E / R = Suma`) | Poziom `0` (`N / C / E / R = Suma` \| `Łączne HP`) | Poziom `+1` (`N / C / E / R = Suma`) | Poziom `+2` (`N / C / E / R = Suma` \| `Łączne HP`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **F1** | `7 / 0 / 7 / 0 = 14` \| `443` | `9 / 0 / 9 / 0 = 18` | `11 / 0 / 11 / 0 = 22` \| `1015` | `14 / 0 / 14 / 0 = 28` | `17 / 0 / 17 / 0 = 34` \| `2590` |
| **F2** | `9 / 7 / 9 / 0 = 25` \| `929` | `12 / 9 / 12 / 0 = 33` | `15 / 11 / 15 / 0 = 41` \| `2020` | `19 / 14 / 19 / 0 = 52` | `23 / 17 / 23 / 0 = 63` \| `5005` |
| **F3** | `17 / 4 / 8 / 3 = 32` \| `2181` | `23 / 6 / 11 / 4 = 44` | `28 / 7 / 14 / 5 = 54` \| `4625` | `35 / 9 / 18 / 6 = 68` | `42 / 11 / 21 / 8 = 82` \| `9360` |
| **F4** | `21 / 8 / 11 / 4 = 44` \| `3209` | `28 / 10 / 14 / 5 = 57` | `35 / 13 / 18 / 6 = 72` \| `6885` | `44 / 16 / 23 / 8 = 91` | `53 / 20 / 27 / 9 = 109` \| `13435` |
| **F5** | `25 / 19 / 10 / 4 = 58` \| `4510` | `33 / 24 / 13 / 6 = 76` | `42 / 31 / 16 / 7 = 96` \| `9555` | `53 / 39 / 20 / 9 = 121` | `63 / 47 / 24 / 11 = 145` \| `18305` |
| **F6** | `27 / 23 / 24 / 5 = 79` \| `7390` | `36 / 30 / 33 / 6 = 105` | `45 / 38 / 41 / 8 = 132` \| `14890` | `56 / 48 / 52 / 10 = 166` | `68 / 58 / 62 / 12 = 200` \| `28735` |
| **F7** | `33 / 30 / 23 / 5 = 91` \| `10536` | `43 / 41 / 31 / 7 = 122` | `54 / 51 / 38 / 9 = 152` \| `21920` | `68 / 64 / 47 / 11 = 190` | `82 / 77 / 58 / 14 = 231` \| `40375` |
| **F8** | `35 / 31 / 41 / 6 = 113` \| `15005` | `46 / 41 / 54 / 8 = 149` | `57 / 51 / 68 / 10 = 186` \| `31666` | `72 / 64 / 85 / 13 = 234` | `86 / 77 / 103 / 15 = 281` \| `55641` |
| **F9** | `74 / 33 / 30 / 7 = 144` \| `21144` | `86 / 44 / 41 / 10 = 181` | `100 / 55 / 51 / 12 = 218` \| `40320` | `117 / 69 / 64 / 15 = 265` | `133 / 83 / 77 / 18 = 311` \| `67267` |
| **F10** | `45 / 39 / 54 / 13 = 151` \| `26320` | `59 / 52 / 71 / 18 = 200` | `74 / 65 / 89 / 22 = 250` \| `52591` | `93 / 81 / 112 / 28 = 314` | `112 / 98 / 134 / 33 = 377` \| `90876` |
| **F11** | `53 / 45 / 40 / 8 = 146` \| `28988` | `70 / 59 / 54 / 11 = 194` | `88 / 74 / 68 / 14 = 244` \| `58361` | `110 / 93 / 86 / 18 = 307` | `132 / 111 / 102 / 21 = 366` \| `97469` |
| **F12** | `54 / 50 / 109 / 9 = 222` \| `46629` | `73 / 67 / 132 / 12 = 284` | `91 / 83 / 154 / 15 = 343` \| `83846` | `114 / 104 / 182 / 19 = 419` | `137 / 125 / 211 / 23 = 496` \| `135598` |
| **F13** | `60 / 56 / 50 / 10 = 176` \| `43182` | `80 / 74 / 66 / 13 = 233` | `100 / 93 / 82 / 16 = 291` \| `82703` | `125 / 117 / 102 / 20 = 364` | `151 / 140 / 124 / 24 = 439` \| `136943` |
| **F14** | `65 / 60 / 80 / 10 = 215` \| `53779` | `86 / 80 / 107 / 14 = 287` | `107 / 100 / 134 / 17 = 358` \| `103555` | `134 / 126 / 168 / 21 = 449` | `161 / 150 / 202 / 26 = 539` \| `171663` |
| **Endless (`84:00`)** | `89 / 60 / 106 / 10 = 265` \| `69317` | `110 / 80 / 133 / 14 = 337` | `131 / 100 / 160 / 17 = 408` \| `123005` | `158 / 126 / 194 / 21 = 499` | `185 / 150 / 228 / 26 = 589` \| `195933` |

### 3.4. Mechanika spawnu i popychania bram (`02e`)

- **Siatka spawnu (`add_spawn_and_attack_effect`):** 11 kolumn (`dx = (idx % 11) - 5`, `dy = (idx // 11) - 5`, maks. `121` pól), obszar rozkazu `spawn_x ± 8, spawn_y ± 8`.
- **Czyszczenie polan spawnu:** dla `spawn_x > 105 or spawn_y < 96` wykonuje `kill_object(BUILDING)` dla `P1–P4` w `spawn_x ± 6, spawn_y ± 6` (z `ky2 <= 182` dla `spawn_x > 105 and spawn_y >= 172`).
- **Popychanie bram (`02e_Push_Gate_Units_Deep_Into_Base`, pętla `15s`):**
  - `(40..56, 96..108)` -> `(48, 138)` [`P5, P6, P8`]; `(96..108, 106..122)` -> `(54, 146)` [`P5, P6, P7, P8`];
  - `(96..108, 154..170)` -> `(68, 162)` [`P5, P6, P8`]; `(74..82, 94..108)` -> `(68, 130)` [`P5, P6, P8`]; `(98..112, 135..144)` -> `(68, 146)` [`P5, P6, P8`].

---

## 4. Pełna tabela systemów na mapie

### 4.1. Sześć Settlementów (`G1–G3`) — detektor `±20` (`ObjectType.MILITARY`, `quantity=1` dla `P1–P4`), smycz `2s` (`ring 14..20`)

| Obóz | Pozycja `(cx, cy)` / Właściciel | Zabudowa (cel główny + poboczne) | Garnizon (`Garrison_Spawn_*`) | Kontratak (`P8`) + trasa | Nagroda (`P1–P4`) | *Furia Hordy* | Wyłączane fale i mechaniki |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`G1_North`** | `(76, 72)` / `P5` | `Guard Tower` (cel) + `2× Guard Tower`, `Barracks`, `Siege Workshop` | `14` Pike, `6` Berserk, `8` Xbow | `8` Cav, `10` Pike `(48,86)->(48,138)` | `+700 F`, `+700 G` | `+8 HP`, `+1 Atk` | Fale `G1_North` (Berserkerzy, Petardy) |
| **`G1_East`** | `(132, 152)` / `P5` | `Guard Tower` (cel) + `2× Guard Tower`, `Barracks`, `Siege Workshop` | `12` Husk, `10` Pike, `3` Fl.Camel | `8` Cav, `10` Pike `(117,178)->(68,162)` | `+700 F`, `+700 G` | `+8 HP`, `+1 Atk` | Fale `G1_East` (Huskarle, Pł. Wielbłądy) |
| **`G2_Snipers`** | `(68, 34)` / `P6` | `Castle` (cel) + `Archery Range`, `Monastery`, `4× Guard Tower` | `7` Jan, `2` S.Onag, `16` Halb | `10` Cav, `12` Halb `(48,86)->(48,138)` | `+1000 F`, `+1000 G` | `+14 HP`, `+1 Atk` | Fale `G2_Snipers` (Snajperzy, Moździerze) + Wyłomy Saperów (F9, F12, Endless) |
| **`G2_Mages`** | `(148, 72)` / `P7` | `Castle` (cel) + `Archery Range`, `Monastery`, `4× Guard Tower` | `14` Cav, `8` Hussar, `1` Imam | `10` Cav, `12` Halb `(116,114)->(54,146)` | `+1000 F`, `+1000 G` | `+14 HP`, `+1 Atk` | Fale `G2_Mages` (Arcymagowie) + Rajdy Szakali |
| **`G3_North`** | `(142, 24)` / `P8` | `Castle` (cel) + `2× Castle`, `Stable`, `Siege Workshop`, `4× Keep` | `3` Ele, `20` Halb, `12` Pal | `1` Ele, `12` Pal, `14` Halb `(116,114)->(54,146)` | `+1500 F`, `+1500 G` | `+20 HP`, `+2 Atk` | Fale `G3_North` (Żelazne Słonie Płn.) |
| **`G3_East`** | `(176, 56)` / `P8` | `Castle` (cel) + `2× Castle`, `Stable`, `Siege Workshop`, `4× Keep` | `3` Ele, `20` Arb, `2` S.Onag | `1` Ele, `12` Pal, `14` Halb `(117,178)->(68,162)` | `+1500 F`, `+1500 G` | `+20 HP`, `+2 Atk` | Fale `G3_East` (Żelazne Słonie Wsch.) + `Trade_Line_Attack` |

- Po zburzeniu celu głównego `collapse_camp_buildings` wykonuje `kill_object` w `cx ± 14, cy ± 14` dla `10` typów budynków (`G1–G3`, `Q2–Q4`).

### 4.2. Cztery Questy (`Q1–Q4`)

| Quest | Pozycja `(cx, cy)` / Właściciel / Detektor | Zabudowa & Garnizon | Mechanika etapów / tarcz | Nagrody (`P1–P4`) | *Adaptacja Hordy* |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Q1` Karawanseraj** | `(154, 190)` / `P5` / `±14, y2<=191` (`140..168, 176..191`) | `Market` (cel) + `2× Guard Tower` `(149/159, 187)`; Garnizon: `12` Steppe Lancer, `10` Xbow, `4` Berserk | Jednoetapowy; po zburzeniu usuwa wieże `P5` w `(145..165, 182..195)` i teleportuje jednostki `P1–P5` z `(105..199, 183..187)` na `(154, 192)` | `+30` Pop Cap, `+500 G`, `Villager Work Rate ×1.20`, `Trade Cart Speed ×1.25`, `4× Trade Cart` na `(px+0..3, py+5)`, `Market` `P2` `(195, 194)`, `Fortified Wall` `P4` na `y=186` (`x=105..199`, luki `x=122..123, 170..171`), `6× Keep` `P4` na `y=184` (`x=115, 122, 145, 160, 170, 190`) | `+8 HP`, `+1 Atk` |
| **`Q2` Klif Artylerii** | `(28, 32)` / `P6` / `±20` | `University` (cel) + `2× Keep` `(23/33, 37)` + `2× Bombard Tower` `(24,34),(32,34)`; Garnizon: `6` Jan, `1` S.Onag, `14` Halb | Dwuetapowy: `Garrison_Spawn` aktywuje `06_Quest2_Shield_Loop` (`heal_object` `+400 HP / 2s` z filtrem `UNIVERSITY` + `ObjectType.BUILDING` w `26..30, 28..34`); zniszczenie obu `Bombard Tower` wyłącza tarczę | Techy: `Ballistics, Chemistry, Siege Engineers, Thumb Ring`; `PLAYER_RANGED`: `+2` Range/Search, `+4` Atk (`cl=3`); `PLAYER_MOUNTED_RANGED`: `Speed ×1.12`; `PLAYER_CAVALRY`: `Speed ×1.12, +4` Atk (`cl=4`); `2× Bombard Cannon` `P3` `(27/29, 36)`; `MAP_REVEALER` `P1–P4` na `G2_Snipers (68,34)` | `+8 HP`, `+1 Atk` |
| **`Q3` Skarbiec** | `(142, 118)` / `P8` / `±20` | `Krepost` (cel) + `4× Keep` `(±5, ±5)` + `30× Fortified Wall` (`y=110, 126`); Garnizon: `18` Halb, `2` Ele, `14` Arb | Jednoetapowy | `+20` Pop Cap, `+600 G`, `+300 S`; pętla `60s` (`06b`): **`+100 F, +100 W, +90 G, +20 S` na minutę** dla każdego `P1–P4` (`310/min` na gracza; łącznie dla drużyny: `+400 F, +400 W, +360 G, +80 S / min`) | `+10 HP`, `+1 Atk` |
| **`Q4` Krwawy Ołtarz** | `(105, 20)` / `P7` / `±20` | `Monastery` (cel) + `2× Keep` `(100/110, 24)`; Garnizon: `14` Pal, `2` Ele, `12` Halb | Dwuetapowy: Stage 1 spawnuje `Relic` `(105,20)` i kontratak `P7` z `(105,34)->(105,20)`: `6` H.Camel, `6` E.Mameluke, `4` E.Steppe Lancer; Stage 2 po `timer=30s` | `IMAM (842)` `P7` HP `-> 120`; `PLAYER_RANGED+CAV+INF`: `HP ×1.30`, `+2/+2` Armor (`cl=4,3`); `PLAYER_PROD_BUILDINGS`: `Work Rate ×1.40`; czyści `(56..60, 150..154)` i buduje `Monastery` `P1` `(58, 152)` + `2× Monk` `P1` `(57/59, 155)` | `+10 HP`, `+1 Atk` |

### 4.3. Punkty Eksploracyjne (`Map PoI 1–3`), Kwatermistrz `P2`, Sanktuarium `P1`, Aura i Boss

- **Map PoI (`P1–P4`, jednorazowe dla pierwszego odkrywcy, detektory `r=3`):**
  - `PoI 1 (30, 76)`: detekcja `27..33, 73..79`; odblokowanie w **`10:00` (`600s`)**; nagroda: `2× Capped Ram` `(29/31, 76)` + `2× Petard` `(29/31, 77)` dla odkrywcy, `+200 W`, `+200 G` dla `P1–P4`.
  - `PoI 2 (124, 178)`: detekcja `121..127, 175..181`; aktywny od **`0:00`**; nagroda: `+350 F`, `+350 G` dla `P1–P4`, `MAP_REVEALER` `P1–P4` na `Q1 (154, 190)`.
  - `PoI 3 (50, 90)`: detekcja `47..53, 87..93`; aktywny od **`0:00`**; nagroda: `2× Light Cavalry` `(49/51, 90)` dla odkrywcy, `+150 S`, `+150 G` dla `P1–P4`, `MAP_REVEALER` `P1–P4` na bród `(122, 62)`.
- **Posterunek Kwatermistrza `P2` `(4, 164)` (komnata `x=2..6, y=160..168`, tylko `UnitInfo.KING.ID` `P2`, wspólny cooldown `240s`, flara `(54, 149)`):**
  - `Tier 1 (10:00–20:00)` (`timer=600s`): Flaga Płn. `(4, 161)` = `4× Conquistador` + `1× Mangonel`; Flaga Płd. `(4, 167)` = `+125 F, +125 W, +100 G` dla `P1–P4` (`0` naprawy; przy cyklu `240s`: `31.25 F / 31.25 W / 25.0 G` na min na gracza).
  - `Tier 2 (20:00–30:00)` (`timer=1200s`): Flaga Płn. = `4× Conquistador` + `2× Bombard Cannon`; Flaga Płd. = `+200 F, +200 W, +200 G` dla `P1–P4` + naprawa budynków w `(0..110, 95..199)` (`P1–P4`) i `(111..199, 183..187)` (`P4`) o `+250 HP` (`50.0 F / 50.0 W / 50.0 G` na min na gracza).
  - `Tier 3 (30:00+)` (`timer=1800s`): Flaga Płn. = `6× Elite Conquistador` + `2× Bombard Cannon` + `2× Siege Ram`; Flaga Płd. = `+300 F, +300 W, +300 G` dla `P1–P4` + naprawa w `(0..110, 95..199)` i `(111..199, 183..187)` o `+500 HP` (`75.0 F / 75.0 W / 75.0 G` na min na gracza; drużynowo `300 F / 300 W / 300 G` na min).
- **Sanktuarium Balansu `P1` `(4, 138)`:** komnata `x=2..6, y=134..142`; pad górny `(2..6, 134..136)` (`FLAG_A` `(4,135)`), pad dolny `(2..6, 140..142)` (`FLAG_B` `(4,141)`); odwrócona kolejność topologiczna ID triggerów `09_Diff_*` (`ID(P1->P2) < ID(0->P1) < ID(M1->0) < ID(M2->M1)` i analogicznie pad dolny); natychmiastowy teleport na `(4, 138)` + `stop_object`, brak timerów blokujących.
- **Globalna Aura Arcymaga (`02a–02d`):** warunek obecności `≥1` `IMAM (842)` `P7` w `(92..128, 96..132)` (`±18` wokół `(110, 114)`): nakłada globalnie `P5–P8` **`+8/+8` pancerza** (`cl=3, 4`) dla `20/30` jednostek z `receives_mage_shield=True`, leczy wszystkie obiekty `P5–P8` w tej strefie o `+15 HP / 3s` (`5.0 HP/s`), puszcza flarę `(114, 114)` co `20s`. Brak Imama w strefie zdejmuje **`-8/-8`** i reaktywuje czujnik.
- **Finałowy Boss Fight (`07a -> 07b -> 07c -> 07d`) i Porażka (`08`):**
  - `07a_All_Settlements_Destroyed_Boss_Warning`: po zburzeniu `6` Settlementów dezaktywuje eskalację `04a–04f`, triggery Endless oraz wszystkie `337` triggerów Zegara Fal (`00_Wave_Timer_UI_*` / `Tick_*`), aktywuje `00_Wave_Timer_Boss_Banner`, czyści budynki `P1–P4` w `(110..124, 108..128)`, stawia `MAP_REVEALER` na `(104, 114)` i `(116, 114)`, odtwarza dźwięk i uruchamia `timer=60s`.
  - `07b_Spawn_Final_Boss_Wave` (`timer=60s`): uderza na **3 bramy**: Centralna `(116, 114) -> (54, 146)` `P8`: `1× Wielki Chan Subotai (698)` (`4500 HP`, `8/10` armor, `45` atk `cl=3`, speed `0.85`), `6× Żelazny Słoń (1134)`, `16× Paladin (569)`, `4× Siege Ram (548)` oraz `(118, 122) -> (54, 146)` `2× Arcymag (842)` `P7`; Północna `(68, 60) -> (48, 136)` `P8`: `10× Paladin`, `10× Heavy Cav Archer`, `2× Siege Ram`; Wschodnia `(116, 162) -> (68, 152)` `P8`: `10× Paladin`, `10× Heavy Cav Archer`, `2× Siege Ram`.
  - `07b_Boss_Elephant_Guard_Heal` (`looping=True, timer=3s`): leczy `Subotaia (698)` o **`+180 HP / 3s` (`+60.0 HP/s`)**, dopóki w strefie bitwy **`(40, 90, 135, 175)`** żyje `≥1` `ELITE_BATTLE_ELEPHANT_ID (1134)` `P8` (wyłączane przez `07b_Boss_Elephants_Slain_Disable_Heal` z `timer=10s` po opuszczeniu strefy / śmierci Słoni `P8` w `(40..135, 90..175)`).
  - `07c_Confirm_Boss_Spawned` -> `07d_Victory_Final_Boss_Defeated` (`timer=5s` + brak żywego `698` `P8` na `0..199`): wyłącza pętlę gwardii i `00_Wave_Timer_Boss_Banner`, ogłasza `declare_victory` dla `P1–P4`.
  - `08_Defeat_Citadel_Lost`: zniszczenie `Feitoria` `P2` `(54, 146)` -> `declare_victory` dla `P5–P8`.
