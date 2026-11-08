# ROADMAP.md — Plan Naprawczy i Rozwojowy (`Kroniki Rubieży: Horda` v6.2 -> v6.5)

## 0. Protokół Wykonawczy dla Agenta IDE (Antigravity / VS Code)
1. **Atomowość etapów:** Realizuj podetapy ściśle po kolei (`Etap 0` -> `1A` -> `1B` -> `2` -> `3A` -> `3B` -> `3C` -> `4` -> `5` -> `6A` -> `6B` -> `6C` -> `7` -> `8`). **Zabrania się łączenia kilku podetapów (szczególnie 3A, 3B i 3C) w jedną edycję.**
2. **Weryfikacja po każdym podetapie:** Po zakończeniu każdego podetapu uruchom w terminalu:
   - `python generate_horde_quests_scenario.py` (musi zakończyć się sukcesem),
   - `ruff check .` (musi zwrócić `All checks passed!`).
3. **Zakaz cichych wyjątków:** Nigdy nie używaj `try: ... except Exception: pass`. Jeśli wywołanie `AoE2ScenarioParser` zgłosi błąd, zatrzymaj się i napraw przyczynę.

---

## Etap 0: Kontrola stanu repozytorium i kompatybilności formatu triggerów (Preflight Check) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** Brak (tylko odczyt i test kompatybilności w terminalu)

### Cel i kroki wykonawcze:
1. Odczytaj wszystkie pliki z lokalnego repozytorium (`generate_horde_quests_scenario.py`, `horde_config.py`, `horde_map.py`, `horde_waves.py`, `horde_quests.py`, `horda.md`) oraz zapisz branch i commit (`git rev-parse HEAD`).
2. Wykonaj test serializacji warunku `trigger_active` oraz wersji triggerów w `template.aoe2scenario` (warunek `TRIGGER_ACTIVE` wymaga `AoE2ScenarioParser >= 1.54` i `trigger_version >= 4.1`):
   ```powershell
   python -c "import tempfile; from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario; from horde_config import INPUT_TEMPLATE; s = AoE2DEScenario.from_file(str(INPUT_TEMPLATE)); tm = s.trigger_manager; t1 = tm.add_trigger('T1'); t2 = tm.add_trigger('T2'); t2.new_condition.trigger_active(trigger_id=t1.trigger_id); tmp = tempfile.mktemp(suffix='.aoe2scenario'); s.write_to_file(tmp); s2 = AoE2DEScenario.from_file(tmp); print('Trigger version:', getattr(s2.trigger_manager, 'trigger_version', 'unknown'), 'Conds:', len(s2.trigger_manager.triggers[-1].conditions), 'Target:', s2.trigger_manager.triggers[-1].conditions[0].trigger_id == t1.trigger_id)"
   ```
3. Jeśli powyższy jednowierszowiec wypisze `Conds: 1 Target: True`, w Etapie 3A użyj wariantu `trigger_active`. Jeśli rzuci wyjątek lub zgubi warunek przy ponownym wczytaniu, zgłoś to i w Etapie 3A użyj opisanego wariantu zapasowego.

### Kryterium akceptacji:
- Potwierdzony hash commitu bazowego oraz jednoznaczny wynik testu round-trip serializacji `trigger_active` na pliku `template.aoe2scenario`.

---

## Etap 1A: Naprawa ścinania drzew przez Moździerze Oblężnicze (`BUG-02`) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_config.py`, `horde_waves.py`

### Cel i miejsce w kodzie:
1. W `horde_config.py` dodaj stałą:
   ```python
   ATTR_BLAST_ATTACK_LEVEL = 44  # 2 = obrażenia obszarowe ranią jednostki i budynki, ale NIE ścinają drzew
   ```
   *(Nie zmieniaj `BALANCE["mortar_blast_width"] = 2.6` — zachowujemy dotychczasowy promień rażenia Moździerza).*
2. W `horde_waves.py` zaimportuj `ATTR_BLAST_ATTACK_LEVEL` z `horde_config` i w triggerze `01b_Apply_Specialized_Unit_Archetypes` (`t_mutate`) dodaj dla `SIEGE_ONAGER_ID` (`PlayerId.SIX`):
   ```python
   safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_BLAST_ATTACK_LEVEL, Operation.SET, 2)
   ```

### Kryterium akceptacji:
- Skrypt kompiluje się bez błędów, a w wygenerowanym pliku trigger `01b_Apply_Specialized_Unit_Archetypes` posiada efekt `modify_attribute` dla `object_list_unit_id = 588` (`PlayerId.SIX`) z `object_attributes = 44`, `operation = Operation.SET`, `quantity = 2`.

---

## Etap 1B: Centralny Rejestr Jednostek (`ENEMY_UNIT_REGISTRY`), `WaveDefinition` i pełna unifikacja modyfikacji statystyk (`BUG-10`, Balans) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_config.py`, `horde_waves.py`, `horde_quests.py`

### Cel i miejsce w kodzie:
1. W `horde_config.py`:
   - Zdefiniuj `@dataclass(frozen=True) class WaveDefinition` (`wave_num`, `wave_sec`, `wave_title`, `g1_north`, `g1_east`, `g2_snipers`, `g2_mages`, `g3_north`, `g3_east`, `raider_count`) i zmień `get_wave_definitions() -> list[WaveDefinition]`, aby zwracała listę obiektów `WaveDefinition`.
   - Zdefiniuj `@dataclass(frozen=True) class EnemyUnitSpec`:
```python
@dataclass(frozen=True)
class EnemyUnitSpec:
    unit_id: int
    name: str
    base_hp: int                 # Bazowe HP w tym scenariuszu (po 01b i technologiach, przed eskalacją/Sanktuarium)
    attack_class: int | None     # 4 = Base Melee, 3 = Base Pierce, None = ZAKAZ skalowania ataku
    scales_hp: bool              # Czy otrzymuje bonusy HP (eskalacja, Sanktuarium, Questy, Furia)
    receives_mage_shield: bool   # Czy otrzymuje +30/+30 pancerza z Globalnej Aury Arcymaga
    mandatory_min_one: bool      # Czy w scale_comp_for_level ma gwarancję min. 1 szt. na poziomach -2/-1

    @property
    def hp_delta_down(self) -> int:
        """Odwracalna całkowita zmiana HP na stopień trudności w dół (~15% bazowego HP scenariusza)."""
        if not self.scales_hp:
            return 0
        return max(2, (self.base_hp * 15 + 50) // 100)
```
   - Zdefiniuj kompletny słownik `ENEMY_UNIT_REGISTRY: dict[int, EnemyUnitSpec]` z dokładnie poniższymi 26 wpisami (pokrywającymi 100% jednostek z fal, garnizonów, rajdów i odwetów):

| Stała / `unit_id` | `name` | `base_hp` | `hp_delta_down` | `attack_class` | `scales_hp` | `receives_mage_shield` | `mandatory_min_one` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `UnitInfo.MAN_AT_ARMS.ID` (`75`) | `"Man-at-Arms"` | `45` | `7` | `4` | `True` | `True` | `False` |
| `UnitInfo.SPEARMAN.ID` (`93`) | `"Spearman"` | `45` | `7` | `4` | `True` | `True` | `False` |
| `UnitInfo.PIKEMAN.ID` (`358`) | `"Pikeman"` | `55` | `8` | `4` | `True` | `True` | `False` |
| `UnitInfo.HALBERDIER.ID` (`359`) | `"Halberdier"` | `60` | `9` | `4` | `True` | `True` | `False` |
| `UnitInfo.HUSKARL.ID` (`41`) | `"Huskarl"` | `70` | `11` | `4` | `True` | `True` | `False` |
| `ELITE_BERSERK_ID` (`694`) | `"Berserker Szturmowy"` | `185` | `28` | `4` | `True` | `True` | `True` |
| `UnitInfo.SCOUT_CAVALRY.ID` (`448`) | `"Scout Cavalry"` | `65` | `10` | `4` | `True` | `True` | `False` |
| `UnitInfo.STEPPE_LANCER.ID` (`1370`) | `"Steppe Lancer"` | `80` | `12` | `4` | `True` | `True` | `False` |
| `UnitInfo.KNIGHT.ID` (`38`) | `"Knight"` | `120` | `18` | `4` | `True` | `True` | `False` |
| `UnitInfo.CAVALIER.ID` (`283`) | `"Cavalier"` | `140` | `21` | `4` | `True` | `True` | `False` |
| `UnitInfo.PALADIN.ID` (`569`) | `"Paladin"` | `180` | `27` | `4` | `True` | `True` | `False` |
| `UnitInfo.ARCHER.ID` (`4`) | `"Archer"` | `30` | `5` | `3` | `True` | `True` | `False` |
| `UnitInfo.CROSSBOWMAN.ID` (`24`) | `"Crossbowman"` | `35` | `5` | `3` | `True` | `True` | `False` |
| `UnitInfo.ARBALESTER.ID` (`492`) | `"Arbalester"` | `40` | `6` | `3` | `True` | `True` | `False` |
| `UnitInfo.HEAVY_CAVALRY_ARCHER.ID` (`474`) | `"Heavy Cav Archer"` | `80` | `12` | `3` | `True` | `True` | `False` |
| `UnitInfo.ELITE_JANISSARY.ID` (`375`) | `"Snajper Imperialny"` | `90` | `14` | `3` | `True` | `False` | `True` |
| `UnitInfo.MANGONEL.ID` (`280`) | `"Mangonel"` | `50` | `8` | `4` | `True` | `False` | `True` |
| `SIEGE_ONAGER_ID` (`588`) | `"Mozdzierz Oblezniczy"` | `350` | `53` | `4` | `True` | `False` | `True` |
| `ELITE_BATTLE_ELEPHANT_ID` (`1134`) | `"Zelazny Slon-Tank"` | `1450` | `218` | `None` | `True` | `False` | `True` |
| `HUSSAR_ID` (`441`) | `"Szakal Dywersyjny"` | `95` | `14` | `None` | `True` | `False` | `False` |
| `IMAM_UNIT_ID` (`842`) | `"Arcymag Tarczy"` | `240` | `0` | `None` | `False` | `False` | `True` |
| `PETARD_ID` (`440`) | `"Fanatyk Kamikaze"` | `115` | `0` | `None` | `False` | `False` | `True` |
| `FLAMING_CAMEL_ID` (`1263`) | `"Plonacy Wielblad"` | `115` | `0` | `None` | `False` | `False` | `True` |
| `UnitInfo.BATTERING_RAM.ID` (`125`) | `"Battering Ram"` | `175` | `0` | `None` | `False` | `False` | `True` |
| `UnitInfo.CAPPED_RAM.ID` (`422`) | `"Capped Ram"` | `200` | `0` | `None` | `False` | `True` | `True` |
| `UnitInfo.SIEGE_RAM.ID` (`548`) | `"Siege Ram"` | `270` | `0` | `None` | `False` | `True` | `True` |

   - Dodaj w `horde_config.py` również centralne listy dla jednostek i budynków graczy (`Q2` i `Q4`):
     - `PLAYER_RANGED_UNITS`: `ARCHER`, `CROSSBOWMAN`, `ARBALESTER`, `SKIRMISHER`, `ELITE_SKIRMISHER`, `CAVALRY_ARCHER`, `HEAVY_CAVALRY_ARCHER`, `HAND_CANNONEER`.
     - `PLAYER_CAVALRY_UNITS`: `SCOUT_CAVALRY`, `LIGHT_CAVALRY`, `HUSSAR_ID`, `KNIGHT`, `CAVALIER`, `PALADIN`, `STEPPE_LANCER`, `ELITE_STEPPE_LANCER` (`1372`), `CAMEL_RIDER`, `HEAVY_CAMEL_RIDER` (`330`).
     - `PLAYER_INFANTRY_UNITS`: `MILITIA` (`74`), `MAN_AT_ARMS`, `LONG_SWORDSMAN`, `TWO_HANDED_SWORDSMAN`, `CHAMPION`, `SPEARMAN`, `PIKEMAN`, `HALBERDIER`, `EAGLE_SCOUT` (`751`), `EAGLE_WARRIOR` (`753`), `ELITE_EAGLE_WARRIOR` (`752`).
     - `PLAYER_PROD_BUILDINGS`: `BARRACKS`, `STABLE`, `ARCHERY_RANGE`, `CASTLE`, `SIEGE_WORKSHOP`.
2. W `horde_waves.py` i `horde_quests.py`:
   - Usuń lokalne listy `enemy_melee_units` i `enemy_ranged_units` z obu plików oraz ze słownika `ctx`.
   - Usuń zduplikowaną tablicę `wave_definitions` z `horde_waves.py` (dostosuj pętlę w `horde_waves.py` do odczytu pól obiektów `WaveDefinition` zwracanych przez `get_wave_definitions()`).
   - Przebuduj `add_enemy_combat_buff(trigger, ai_players, hp_add, atk_add)` w `horde_waves.py`, aby korzystała wyłącznie z `ENEMY_UNIT_REGISTRY`:
```python
def add_enemy_combat_buff(trigger, ai_players: list[PlayerId], hp_add: int, atk_add: int):
    for ai_p in ai_players:
        for spec in ENEMY_UNIT_REGISTRY.values():
            if spec.scales_hp and hp_add > 0:
                safe_modify_attribute(trigger, ai_p, spec.unit_id, ATTR_HIT_POINTS, Operation.ADD, hp_add)
            if spec.attack_class is not None and atk_add > 0:
                safe_modify_attribute(
                    trigger, ai_p, spec.unit_id, ATTR_ATTACK, Operation.ADD, atk_add, armor_class=spec.attack_class
                )
```
   - W `horde_waves.py` w triggerach Kuźni AI (`01d_AI_Techs_Feudal_8m30s`, `01e_AI_Techs_Castle_18m`, `01f_AI_Techs_Imperial_34m30s`) po zbadaniu technologii przez `PlayerId.EIGHT` (`TECH_FORGING` / `TECH_IRON_CASTING` / `TECH_BLAST_FURNACE`) dodaj natychmiastowy reset ataku Żelaznego Słonia w jednostki:
```python
safe_modify_attribute(
    trig, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, Operation.SET, BALANCE["tank_unit_atk"], armor_class=4
)
```

### Kryterium akceptacji:
- W całym projekcie nie istnieją już oddzielne listy `enemy_melee_units` / `enemy_ranged_units` — wszystkie bonusy w `horde_waves.py` i `horde_quests.py` przechodzą przez `ENEMY_UNIT_REGISTRY`.
- `ELITE_BATTLE_ELEPHANT_ID` ma `attack_class = None` i reset po technologiach Kuźni P8, dzięki czemu nigdy nie przekracza `3` ataku w jednostki.

---

## Etap 2: Zamknięty matematycznie algorytm skalowania składów `scale_comp_for_level()` (`BUG-04`) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_waves.py`

### Cel i miejsce w kodzie:
W `horde_waves.py` zastąp funkcję `scale_comp(comp, factor)` deterministyczną funkcją `scale_comp_for_level(comp: list[tuple[int, int]], level: int) -> list[tuple[int, int]]`:
```python
def scale_comp_for_level(comp: list[tuple[int, int]], level: int) -> list[tuple[int, int]]:
    if any(cnt < 0 for _, cnt in comp):
        raise ValueError(f"Ujemna liczebnosc w kompozycji: {comp}")
    active_comp = [(u_id, cnt) for u_id, cnt in comp if cnt > 0]
    if not active_comp:
        return []
    if level == 0:
        return list(active_comp)

    pct_map = {-2: 60, -1: 80, 1: 125, 2: 150}
    if level not in pct_map:
        raise ValueError(f"Nieobslugiwany poziom trudnosci: {level}")
    pct = pct_map[level]

    total_orig = sum(cnt for _, cnt in active_comp)
    raw_target = max(1, (total_orig * pct + 50) // 100)  # Zaokrąglanie HALF_UP

    min_reqs = []
    allocations = []
    remainders = []
    for idx, (u_id, cnt) in enumerate(active_comp):
        spec = ENEMY_UNIT_REGISTRY.get(u_id)
        min_req = 1 if (spec is not None and spec.mandatory_min_one) else 0
        min_reqs.append(min_req)
        base_alloc = max(min_req, (cnt * pct) // 100)
        allocations.append(base_alloc)
        rem = (cnt * pct) - base_alloc * 100
        remainders.append((rem, idx))

    effective_target = max(raw_target, sum(min_reqs))
    diff = effective_target - sum(allocations)

    if diff > 0:
        # Sortowanie malejąco po reszcie; przy remisie pierwszeństwo ma mniejszy indeks (wcześniejsza jednostka)
        order = sorted(range(len(active_comp)), key=lambda i: (remainders[i][0], -i), reverse=True)
        for step in range(diff):
            allocations[order[step % len(order)]] += 1
    elif diff < 0:
        # Wieloprzebiegowa redukcja tylko z pozycji posiadających zapas ponad min_reqs[i]
        order = sorted(range(len(active_comp)), key=lambda i: (remainders[i][0], i))
        to_reduce = -diff
        while to_reduce > 0:
            progressed = False
            for i in order:
                if to_reduce <= 0:
                    break
                if allocations[i] > min_reqs[i]:
                    allocations[i] -= 1
                    to_reduce -= 1
                    progressed = True
            if not progressed:
                break

    assert sum(allocations) == effective_target
    assert all(a >= m for a, m in zip(allocations, min_reqs))
    return [(u_id, cnt) for (u_id, _), cnt in zip(active_comp, allocations) if cnt > 0]
```

### Kryterium akceptacji:
- `scale_comp_for_level([(375, 0), (842, 0)], -2)` zwraca `[]`.
- `scale_comp_for_level([(375, 2)], 0)` zwraca `[(375, 2)]`, a dla `level = +1` zwraca `[(375, 3)]`.
- Test wielokrotnej redukcji `diff < 0` (np. 10 pozycji z `mandatory_min_one=True` po `1` szt. oraz 1 pozycja zwykła `10` szt. na `level = -2`) kończy się bez błędu asercji z `sum(allocations) == effective_target == 12`.

---

## Etap 3A: Znaczniki Stanu Trudności (`State_Diff_Lvl_*`) i Bezblokadowe Sanktuarium [DONE / WDROŻONE — zaktualizowane w R4]
**Oznaczenie trudności:** `[ARCHITECT-REVIEW]`  
**Modyfikowane pliki:** `horde_waves.py`, `horde_quests.py`

### Cel i miejsce w kodzie:
1. W `horde_waves.py` utwórz 5 triggerów-znaczników stanu trudności `State_Diff_Lvl_{M2, M1, 0, P1, P2}` (`enabled = (lvl == 0)`, `looping = False`, `timer = 999999`) i zapisz `state_markers` w słowniku `ctx`.
2. W `horde_quests.py` (`wire_difficulty_transition`):
   - Każdy z 8 triggerów przejścia `09_Diff_*` ma dokładnie 1 warunek `OBJECTS_IN_AREA` dla Króla P1 (usunięto sztuczne blokady `State_Sanctuary_Unlocked` oraz `09_Diff_*_Relay2s`).
   - Odwrócony porządek topologiczny utworzenia triggerów (`P1->P2 < 0->P1 < M1->0 < M2->M1` dla padu górnego oraz `M1->M2 < 0->M1 < P1->0 < P2->P1` dla padu dolnego) uniemożliwia kaskadowy przeskok o więcej niż 1 poziom w jednym ticku silnika.
   - Sanktuarium przełącza wyłącznie `state_markers[from_lvl]` -> `state_markers[to_lvl]` i nie dotyka żadnych triggerów fal `03_W*` ani `03_Endless*`.

### Kryterium akceptacji:
- Żaden trigger `09_Diff_*` w `horde_quests.py` nie aktywuje ani nie dezaktywuje triggerów fal.
- W całym scenariuszu nie istnieją triggery `State_Sanctuary_Unlocked`, `Close_Window` ani `Relay2s`.

---

## Etap 3B: Jednorazowy harmonogram Fal 1–14 ze skalowanymi wariantami trudności (`BUG-01`, `BUG-03`) [DONE / WDROŻONE — zaktualizowane w R4]
**Oznaczenie trudności:** `[ARCHITECT-REVIEW]`  
**Modyfikowane pliki:** `horde_waves.py`

### Cel i miejsce w kodzie:
W `horde_waves.py` dla każdej fali `w_def` (`w_num = 1..14`, `w_time = w_def.wave_sec`):
1. Utwórz ogłoszenie `03_W{w_num:02d}_Announce` (`enabled = True`, `looping = False`, `timer = w_time`).
2. Dla każdego aktywnego w tej fali Settlementu `s_key`:
   - Utwórz **Zegar Fali Settlementu**: `t_clock = tm.add_trigger(f"03_W{w_num:02d}_{s_key}_Clock", enabled=True, looping=False)` z warunkiem `timer = w_time`.
   - Utwórz 5 jednorazowych wariantów dispatchu dla `lvl ∈ {-2, -1, 0, 1, 2}`:
     `t_var = tm.add_trigger(f"03_W{w_num:02d}_{s_key}_Diff_{lvl_tag}", enabled=False, looping=False)` z warunkiem `trigger_active(trigger_id=state_markers[lvl].trigger_id)`.
   - `t_clock` aktywuje wszystkie 5 wariantów `t_var` dla `s_key` (a w Fali 14 uzbraja też `endless_gates[s_key]`).
   - Aktywny wariant `t_var` spawnuje przeskalowane wojsko (oraz przeskalowane `Szakale` w `G2_Mages` i `Trade Raid` w `G3_East`), a następnie dezaktywuje wszystkie 5 wariantów braci.

### Kryterium akceptacji:
- Zmiana poziomu trudności przed falą powoduje uruchomienie dokładnie jednego wariantu `03_W*_*_Diff_*` odpowiadającego bieżącemu `State_Diff_Lvl_*`.

---

## Etap 3C: Indywidualne Bramki Endless (`03_Endless_Gate_{s_key}`) i jednorazowe warianty dispatchu Endless [DONE / WDROŻONE — zaktualizowane w R4/R7/R8]
**Oznaczenie trudności:** `[ARCHITECT-REVIEW]`  
**Modyfikowane pliki:** `horde_waves.py`, `horde_quests.py`

### Cel i miejsce w kodzie:
1. Dla każdego z 6 Settlementów `s_key` utwórz pętlową bramkę `03_Endless_Gate_{s_key}` (`enabled = False`, `looping = True`, `timer = 330`), uzbrajaną przez zegar Fali 14 (`4710s`), dzięki czemu pierwszy tick Endless uderza w `5040s` (`84:00`).
2. Dla każdego Settlementu `s_key` utwórz 5 jednorazowych (`looping = False`) wariantów `03_Endless_{s_key}_Diff_{lvl_tag}` z warunkiem `trigger_active(state_markers[lvl].trigger_id)`.
3. W `G2_Mages` Szakale Endless są dzielone na dwie flanki: `(52, 86) -> (32, 118)` (eko P3) oraz `(116, 162) -> (76, 172)` (eko P4) z rozkazem `ActionType.MOVE`.
4. Zniszczenie Settlementu w `05_Settlement_Destroyed_{s_key}` trwale dezaktywuje wszystkie jego zegary fal 1–14, bramkę `03_Endless_Gate_{s_key}` oraz wszystkie warianty.

### Kryterium akceptacji:
- Wszystkie warianty `03_Endless_*_Diff_*` mają `enabled = False` oraz `looping = False`, a bramki `03_Endless_Gate_*` mają `enabled = False`, `looping = True`, `timer = 330`.

---

## Etap 4: Odwracalne delty HP w Sanktuarium Balansu (wszystkie gałęzie z rejestru) i korekta 1. ticku eskalacji (`BUG-07`, `BUG-08`) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_waves.py`, `horde_quests.py`

### Cel i miejsce w kodzie:
1. W `horde_quests.py` przebuduj `apply_king_reset_and_safe_stat_shift(trig, mode: str)`, aby **zarówno dla poziomów dodatnich (`pos_up`, `pos_down`), jak i ujemnych (`neg_down`, `neg_up`) korzystała wyłącznie z `ENEMY_UNIT_REGISTRY`**:
   - `pos_up` (`0 -> +1`, `+1 -> +2`): wywołuje `add_enemy_combat_buff(trig, ai_players, hp_add=BALANCE["diff_step_up_hp"], atk_add=BALANCE["diff_step_up_atk"])`.
   - `pos_down` (`+2 -> +1`, `+1 -> 0`): iteruje po `ENEMY_UNIT_REGISTRY.values()`:
     - jeśli `spec.scales_hp`: odejmuje `BALANCE["diff_step_up_hp"]` (`15`) od `ATTR_HIT_POINTS`,
     - jeśli `spec.attack_class is not None`: odejmuje `BALANCE["diff_step_up_atk"]` (`2`) od `ATTR_ATTACK` dla `armor_class = spec.attack_class`.
   - `neg_down` (`0 -> -1`, `-1 -> -2`): iteruje po `ENEMY_UNIT_REGISTRY.values()` i dla jednostek z `spec.scales_hp` odejmuje `spec.hp_delta_down` od `ATTR_HIT_POINTS` (bez modyfikacji ataku!).
   - `neg_up` (`-2 -> -1`, `-1 -> 0`): iteruje po `ENEMY_UNIT_REGISTRY.values()` i dla jednostek z `spec.scales_hp` dodaje `spec.hp_delta_down` do `ATTR_HIT_POINTS`.
2. W `horde_waves.py` w triggerach `04a_Enable_Escalation_At_20m` (`1200s`), `04c_Enable_LateGame_Escalation_At_45m` (`2700s`) i `04e_Enable_Endgame_Escalation_At_55m` (`3300s`) dodaj wywołanie `add_enemy_combat_buff(...)` oraz `send_highlight_chat(...)`, aby pierwszy tick każdego biegu wchodził punktualnie w `20:00`, `45:00` i `55:00`.

### Kryterium akceptacji:
- Pełny cykl `0 -> +1 -> +2 -> +1 -> 0 -> -1 -> -2 -> -1 -> 0` daje dla każdej z 26 jednostek w `ENEMY_UNIT_REGISTRY` sumaryczną zmianę `ΔHP == 0` oraz `ΔAtk == 0`.
- Pierwsze wzmocnienie eskalacji czasowej pojawia się dokładnie w `20:00` (`1200s`).

---

## Etap 5: Automat skończony dla Globalnej Aury Arcymaga Tarczy (`BUG-05`) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_waves.py`

### Cel i miejsce w kodzie:
W `horde_waves.py` skonfiguruj triggery Aury Arcymaga (`02a`..`02d`) jako dwustanowy automat skończony:
1. Lista jednostek objętych tarczą jest generowana z rejestru:
   `global_shielded_units = [spec.unit_id for spec in ENEMY_UNIT_REGISTRY.values() if spec.receives_mage_shield]`.
2. Usuń z triggerów fal jakiekolwiek wywołania `activate_trigger(t_shield_on.trigger_id)`.
3. Trigger `t_shield_on` (`02a_Mage_Global_Horde_Shield_On`) ustaw na starcie jako **`enabled = True`, `looping = False`**:
   - Warunek: `objects_in_area(source_player=PlayerId.SEVEN, object_list=IMAM_UNIT_ID, area_x1=mx1, area_y1=my1, area_x2=mx2, area_y2=my2, quantity=1)` (bez argumentu `object_list_unit_id`!).
   - Efekty: dodaje `+30` pancerza (`armor_class = 3` i `4`) jednostkom z `global_shielded_units`, dezaktywuje `t_shield_on`, aktywuje `t_mage_heal_pulse`, `t_mage_beacon` oraz `t_shield_off`.
4. Trigger `t_shield_off` (`02d_Mage_Global_Horde_Shield_Off`) ustaw na starcie jako **`enabled = False`, `looping = False`**:
   - Warunek: `objects_in_area(source_player=PlayerId.SEVEN, object_list=IMAM_UNIT_ID, area_x1=mx1, area_y1=my1, area_x2=mx2, area_y2=my2, quantity=1, inverted=1)`.
   - Efekty: odejmuje `30` pancerza (`armor_class = 3` i `4`) jednostkom z `global_shielded_units`, dezaktywuje `t_mage_heal_pulse`, `t_mage_beacon` oraz `t_shield_off`, a następnie **aktywuje `t_shield_on`**.

### Kryterium akceptacji:
- `t_shield_on` i `t_shield_off` nigdy nie są aktywne jednocześnie, a żaden trigger fali nie wywołuje `activate_trigger` na `t_shield_on`.
- Zabicie Imama przed Bramą Centralną zdejmuje tarczę niezależnie od obecności Imama w obozie `G2_Mages`.

---

## Etap 6A: Dezaktywacja garnizonów, detektorów i smyczy po zniszczeniu celu (`BUG-06`) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_waves.py`, `horde_quests.py`, `horde_map.py`

### Cel i miejsce w kodzie:
1. W `horde_waves.py` zmień `add_guarded_camp_with_leash()`, aby zwracała krotkę `(t_spawn, t_leash, detect_triggers)`, i zapisz uchwyty wszystkich 10 obozów (4 Questy + 6 Settlementów) w słowniku `ctx["camp_leash_handles"][camp_key]`.
2. W `horde_quests.py` utwórz funkcję `deactivate_camp_handles(trig, handle_tuple)`, wyłączającą `t_spawn`, `t_leash` i wszystkie 4 `detect_triggers`, i wywołaj ją w `t_q1`, `t_q2`, `t_q3_unlock`, `t_q4` oraz w każdym z 6 `t_destroy` (`05_Settlement_Destroyed_*`).
3. Oczyść słownik `ctx` w `horde_map.py` i `horde_waves.py` z tymczasowych zmiennych pętlowych.

### Kryterium akceptacji:
- Zniszczenie każdego z 10 celów dezaktywuje jego `Garrison_Spawn_*`, `Garrison_Leash_*` oraz 4 triggery `Garrison_Detect_*`.

---

## Etap 6B: Korekta geometrii i czyszczenia wież Karawanseraju po ukończeniu Q1 (`BUG-09`) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_quests.py`

### Cel i miejsce w kodzie:
W `horde_quests.py` w triggerze `06_Quest1_Build_Trade_Wall_And_Pop` (`t_q1`):
1. Przed pętlą budującą mur dodaj efekt `remove_object` usuwający obie wieże strażnicze `PlayerId.FIVE` wokół Karawanseraju:
   ```python
   safe_call(
       t_q1.new_effect.remove_object,
       source_player=PlayerId.FIVE,
       object_list_unit_id=BuildingInfo.GUARD_TOWER.ID,
       area_x1=145, area_y1=182, area_x2=165, area_y2=195,
   )
   ```
2. Przesuń linię budowanego muru `FORTIFIED_WALL` z `y = 188` na `y = 186`, a Baszty (`BuildingInfo.KEEP.ID`) z `y = 190` na `y = 184`.

### Kryterium akceptacji:
- Korytarz handlowy `y = 189..199` jest wolny od Baszt i poza zasięgiem wież P5 z Karawanseraju.

---

## Etap 6C: Uzupełnienie list nagród Q2/Q4 oraz stopniowanie Furii Settlementów (`Grade 1–3`) z użyciem `ENEMY_UNIT_REGISTRY` [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_quests.py`

### Cel i miejsce w kodzie:
1. W `horde_quests.py` zaimportuj z `horde_config.py` listy `PLAYER_RANGED_UNITS`, `PLAYER_CAVALRY_UNITS`, `PLAYER_INFANTRY_UNITS`, `PLAYER_PROD_BUILDINGS` i użyj ich w `t_q2` oraz `t_q4`.
2. W `t_q4` zmień docelowe HP Imama (`IMAM_UNIT_ID`) z `140` na `120` (`Operation.SET, 120`).
3. W `t_q1`, `t_q2`, `t_q3_unlock`, `t_q4` oraz w pętli `settlement_defs` wszystkie wzmocnienia Hordy wywołuj wyłącznie przez `add_enemy_combat_buff(trig, ai_players, hp_add=..., atk_add=...)` (opartą na `ENEMY_UNIT_REGISTRY`).
4. W `settlement_defs` uzależnij Furię Hordy i kontratak od klasy obozu (`grade`):
   - `Grade 1` (`G1_North`, `G1_East`): `hp_add = 8, atk_add = 1`, odwet: `8 Cavalier + 10 Pikeman`.
   - `Grade 2` (`G2_Snipers`, `G2_Mages`): `hp_add = 12, atk_add = 1`, odwet: `10 Cavalier + 12 Halberdier`.
   - `Grade 3` (`G3_North`, `G3_East`): `hp_add = 16, atk_add = 2`, odwet: `1 Żelazny Słoń + 12 Paladin + 14 Halberdier`.

### Kryterium akceptacji:
- Żaden bonus w `horde_quests.py` nie modyfikuje ataku Żelaznego Słonia (`1134`) ani Szakala (`441`).
- Nagroda `Q4` obejmuje `Siege Workshop`, a `Q2` obejmuje `Elite Steppe Lancer` i `Heavy Camel Rider`.

---

## Etap 7: Kompleksowy walidator strukturalny scenariusza (`test_horde_scenario.py`) [DONE / WDROŻONE — rozbudowane w R6–R8 do 26 testów]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `test_horde_scenario.py`

### Cel i miejsce w kodzie:
Skrypt `test_horde_scenario.py` wykonuje automatyczną budowę scenariusza (jeśli plik wynikowy nie istnieje) oraz weryfikuje:
1. **Testy danych i algorytmów (`unittest`):**
   - Sprawdzenie, że każdy `unit_id` występujący w `CREATE_OBJECT` dla P5–P8 znajduje się w `ENEMY_UNIT_REGISTRY`.
   - Test `scale_comp_for_level` dla pustych kompozycji, kompozycji zerowych, wielokrotnej redukcji `diff < 0` oraz wszystkich `14 fal × 6 Settlementów × 5 poziomów`.
   - Test pełnej odwracalności delt HP i ataku w Sanktuarium Balansu zarówno matematycznie, jak i na skompilowanych efektach `MODIFY_ATTRIBUTE` z 8 triggerów `09_Diff_*`.
2. **Walidację wygenerowanego pliku binarnego po ponownym wczytaniu (`AoE2DEScenario.from_file(str(OUTPUT_SCENARIO))`):**
   - Dokładnie jeden początkowo aktywny `State_Diff_Lvl_0` (`enabled == 1`) i cztery nieaktywne (`enabled == 0`) oraz brak przestarzałych triggerów `Sanctuary_Unlocked` / `Close_Window` / `Relay2s`.
   - Wszystkie oczekiwane zegary fal `03_W{01..14}_{s_key}_Clock` mają `enabled == 1`, `looping == 0` oraz `timer == w_def.wave_sec` (bez pomijania brakujących zegarów).
   - Każdy wariant `Diff_{-2..+2}` (zarówno w Falach 1–14, jak i w Endless) ma na starcie `enabled == 0`, `looping == 0`, dokładnie jeden warunek `trigger_active` wskazujący na właściwy `State_Diff_Lvl_*`.
   - Wszystkie 6 bramek `03_Endless_Gate_{s_key}` mają `enabled == 0`, `looping == 1`, `timer == 330`.
   - **Asercja anty-regresyjna `BUG-01`:** Żaden z 8 triggerów `09_Diff_*` nie dotyka żadnego triggera `03_W*` ani `03_Endless*`.
   - Każdy z 6 triggerów `05_Settlement_Destroyed_{s_key}` dezaktywuje komplet przypisanych do niego zegarów fal, bramek Endless, wariantów oraz smyczy garnizonowej i spawnuje odwet na właściwej bramie kierunkowej.
   - `t_shield_on` i `t_shield_off` tworzą dwustanowy automat skończony.
   - Konfiguracja graczy AI P5–P8 (`human == False`, `lock_civ == True`, cywilizacje `VIKINGS/TURKS/SARACENS/PERSIANS`), domki startowe (`2` dla P1/P3/P4 i `6` dla P2) oraz bezpieczny Zegar Fali w Objectives (`0` efektów `DISPLAY_TIMER`, 169 banerów UI z `timer == 999999` i 168 przełączników co 30s).

### Kryterium akceptacji:
- `python test_horde_scenario.py` kończy się statusem `OK` (26/26 testów), a `ruff check .` zwraca `All checks passed!`.

---

## Etap 8: Aktualizacja dokumentacji `horda.md` oraz opisów w grze (`populate_ingame_scenario_descriptions`) [DONE / WDROŻONE]
**Oznaczenie trudności:** `[FLASH-SAFE]`  
**Modyfikowane pliki:** `horde_config.py`, `horda.md`

### Cel i miejsce w kodzie:
Zaktualizuj `horda.md` oraz teksty w `populate_ingame_scenario_descriptions()` (`horde_config.py`), uwzględniając:
1. **Rzeczywistą semantykę poziomów trudności w Sanktuarium Balansu (`6, 150`):**
   - **Poziom `-2` (Bardzo Łatwy):** celuje w `60%` liczebności bazowej (zachowując minimum 1 szt. dla wskazanych jednostek specjalnych i bossów, więc w małych grupach udział procentowy może być wyższy) oraz odejmuje dwukrotność delty HP (ok. `-30%` bazowego HP scenariusza dla jednostek ze skalowaniem HP).
   - **Poziom `-1` (Łatwy):** celuje w `80%` liczebności bazowej (z zachowaniem minimum 1 szt. dla specjalistów/bossów) oraz odejmuje pojedynczą deltę HP (ok. `-15%` bazowego HP scenariusza, min. `2` HP).
   - **Poziom `0` (Domyślny):** `100%` bazowej liczebności i bazowe statystyki.
   - **Poziom `+1` (Trudny):** `125%` liczebności bazowej oraz `+15 HP` i `+2 Ataku`.
   - **Poziom `+2` (Ekstremalny):** `150%` liczebności bazowej oraz `+30 HP` i `+4 Ataku`.
2. **Jawne wyjątki z bonusów HP i ataku (`ENEMY_UNIT_REGISTRY`):**
   - Wyjaśnij, że bonusy ataku dotyczą jednostek bojowych piechoty, jazdy, strzelców i artylerii, natomiast **Żelazny Słoń-Tank** (zawsze `3` dmg w jednostki, `+220` w budynki) oraz **Szakal Dywersyjny** (zawsze `2` dmg) otrzymują ze skalowania wyłącznie punkty życia (`HP`), a Tarany, Kamikaze i Arcymagowie mają stałe statystyki bazowe.
3. **Tabelę skumulowanej eskalacji czasowej (`20:00`, `45:00`, `55:00`) oraz rozbicie bonusów za Questy (`+36 HP, +4 Ataku`) i stopniowanej Furii za Settlementy (`Grade 1: +8 HP/+1 Atk`, `Grade 2: +12 HP/+1 Atk`, `Grade 3: +16 HP/+2 Atk`, łącznie `+72 HP, +8 Ataku`).**
4. **Informację, że pociski Moździerza Oblężniczego (`P6`) nie ścinają drzew wokół bram (`Blast Attack Level = 2`), a wycinanie lasu następuje wyłącznie w zapowiedzianych akcjach saperskich w Fali 9 (`6×11` kratek na północy) i Fali 12 (`11×6` kratek na wschodzie).**

### Kryterium akceptacji:
- Pełna zgodność wszystkich reguł i liczb między `horda.md`, `populate_ingame_scenario_descriptions()` oraz kodem źródłowym.

---

## Plan Naprawczy Po Audycie i Playteście v6.3 -> v6.5 (Etapy R1–R8)

- **Etap R1 `[FLASH-SAFE]` `[DONE / WDROŻONE]`:** Czyszczenie konfiguracji, usunięcie duplikatów `PLAYER_*` i `populate_ingame_scenario_descriptions`, usunięcie błędnego `object_list_unit_id` z `objects_in_area`, uszczelnienie `safe_call` i usunięcie `try...except` z `safe_modify_attribute`.
- **Etap R2 `[FLASH-SAFE]` `[DONE / WDROŻONE]`:** Unifikacja mutacji 6 archetypów w `01b` dla wszystkich `ai_players` (`P5–P8`), `TECH_BLOODLINES` dla wszystkich `ai_players` w `01d` (z korektą `-20 HP` dla Szakala) oraz `enforce_specialized_unit_caps` w `01d`, `01e`, `01f`.
- **Etap R3 `[FLASH-SAFE]` `[DONE / WDROŻONE]`:** Separacja spawnów i rozkazów `Szakale_EcoRaid` (`P7`) od `G2_Mages` (`BUG-11`), korekta smyczy `ring_inner=14, ring_outer=20` i odsunięcie spawnów fal 6 Settlementów poza promień smyczy (`BUG-17`), uzupełnienie `P7` w `02e`, pełny wóz handlowy i czyszczenie pasa muru w `Q1` oraz korekta tagu Fali 14.
- **Etap R4 `[ARGON/SONNET-REQUIRED]` `[DONE / WDROŻONE]`:** Przebudowa Sanktuarium Balansu — całkowite usunięcie blokad czasowych (`State_Sanctuary_Unlocked`, `03_W*_Close_Window`, `09_Diff_*_Relay2s`), odwrócony porządek topologiczny triggerów `09_Diff_*` oraz pełne skalowanie `Szakale_EcoRaid` i `Trade_Line_Attack` w wariantach fal (`BUG-12`).
- **Etap R5 `[FLASH-SAFE]` `[DONE / WDROŻONE]`:** Synchronizacja dokumentacji `horda.md`, `populate_ingame_scenario_descriptions` i komunikatów czatu z wartościami eskalacji z `BALANCE` (`+5/+9/+10 HP`) oraz rzeczywistymi współrzędnymi 6 Settlementów (`BUG-13`, `BUG-14`).
- **Etap R6 `[ARGON/SONNET-REQUIRED]` `[DONE / WDROŻONE]`:** Rozbudowa i uszczelnienie `test_horde_scenario.py` do 20/20 testów (weryfikacja `assertGreater` na kolekcjach `BUG-16`, realne ID `557`, pełny skan `CREATE_OBJECT` przeciwko `ENEMY_UNIT_REGISTRY`, testy geometrii separacji smyczy i spawnów P7, testy odblokowanego Sanktuarium i porządku topologicznego triggerów).
- **Etap R7 `[ARGON-HIGH AUDIT]` `[DONE / WDROŻONE]`:** Naprawa przepełnienia siatki spawnu do 11 kolumn (`dx = (idx % 11) - 5, dy = (idx // 11) - 5`), zwiększenie bufora polan spawnu do `radius=7` (z pełną ochroną 66 drzew północnej i 66 drzew wschodniej przesieki), korekta współrzędnych spawnu `G1_East` `(117, 178)`, odwetu Settlementów `(116, 114)` i wschodnich Saperów `(115, 140)` zapewniająca odległość Czebyszewa $> 20$ od wszystkich 10 smyczy obozowych (`BUG-20`), pełna unifikacja technologii `01d–01f` dla `P5–P8` z zamrożeniem prędkości Żelaznego Słonia po `Husbandry` (`BUG-21`), podział rajdów Szakali w Trybie Endless na dwie flanki `(52, 86) -> (54, 119)` i `(116, 162) -> (54, 170)` (`BUG-22`), naprawa martwej gałęzi `hasattr(trigger.new_effect, "move")` na `task_object(..., action_type=ActionType.MOVE)` (`BUG-24`), optymalizacja `test_horde_scenario.py` do jednokrotnego odczytu binarnego (~15s, 23/23 testów OK) oraz usunięcie martwych plików `split_into_modules.py` i `generate_horde_quests_scenario_monolith.bak` (`BUG-23`).
- **Etap R8 `[PLAYTEST + EXTERNAL AUDIT v6.5]` `[DONE / WDROŻONE]`:**
  1. **Wymuszenie AI i cywilizacji P5–P8 w pliku scenariusza (`horde_map.py`):** `human = False`, `lock_civ = True`, `allied_victory = True` oraz przypisanie `Civilization.VIKINGS` (P5), `TURKS` (P6), `SARACENS` (P7), `PERSIANS` (P8) wraz z `pm.set_diplomacy_teams(human_players, ai_players)`.
  2. **Poziom trudności AI `Extreme` w `horda.md` i instrukcjach w grze:** Zaktualizowano zalecenia lobby na `Ekstremalny (Extreme)`, aby jednostki AI działały bez błędów taktycznych.
  3. **Domki startowe dla P1–P4 (`horde_map.py`):** P1, P3 i P4 rozpoczynają grę z `2` wybudowanymi domkami ~5 kratek na północ od krawędzi TC (`(cx, cy - 7)`, `(cx + 3, cy - 7)`), a P2 rozpoczyna z `6` domkami (kompensacja 20 popu zajmowanego przez Feitorię w `0:00`).
  4. **Odporny na crashe Zegar Fali (`setup_wave_countdown_timer` w `horde_quests.py`):** Zbudowany bez użycia `display_timer` na 169 statycznych banerach UI w Objectives (`00_Wave_Timer_UI_*`, `order=110`, `timer=999999`) przełączanych co 30s przez 168 triggerów `00_Wave_Timer_Tick_*` wraz z ostrzeżeniami czatu na 1 min przed każdą falą.
  5. **Rozwiązanie kolizji rozkazów Szakali P7 z `02e_Push_Gate_Units_Deep_Into_Base` (`BUG-25`, `horde_waves.py`):** Wykluczenie `PlayerId.SEVEN` ze stref `02e` przy Bramie Północnej, Wschodniej i wyłomach leśnych (pozostawienie P7 wyłącznie w Bramie Centralnej) oraz skierowanie Szakali Endless bezpośrednio w strefy ekonomiczne `(32, 118)` (P3 TC) i `(76, 172)` (P4 TC).
  6. **Normalizacja HP Żelaznego Słonia po `Bloodlines` (`BUG-26`, `horde_waves.py`):** Odjęcie `20 HP` (`Operation.SUBTRACT, 20`) dla `ELITE_BATTLE_ELEPHANT_ID` w `01d_AI_Techs_Feudal_8m30s` dla wszystkich `ai_players` oraz egzekwowanie zasięgu Snajpera (`19`) i prędkości Arcymaga (`0.78`) w `enforce_specialized_unit_caps`.
  7. **Rozszerzenie list `PLAYER_*` o jednostki unikalne i regionalne (`horde_config.py`), kierunkowe spawny odwetów Settlementów (`05_Settlement_Destroyed_*` w `horde_quests.py`) oraz wzmocnienie walidatora `test_horde_scenario.py` do 26/26 testów.**
