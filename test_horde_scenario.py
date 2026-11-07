"""
test_horde_scenario.py - Kompleksowy zestaw testow jednostkowych, integracyjnych
oraz walidacji binarnej pliku .aoe2scenario dla scenariusza Kroniki Rubiezy: Horda (v6.4).
"""

import unittest

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from horde_config import (
    ATTR_ARMOR,
    ATTR_ATTACK,
    ATTR_BLAST_ATTACK_LEVEL,
    ATTR_HIT_POINTS,
    ATTR_MAXIMUM_RANGE,
    ATTR_MOVEMENT_SPEED,
    BALANCE,
    ELITE_BATTLE_ELEPHANT_ID,
    ELITE_BERSERK_ID,
    ENEMY_UNIT_REGISTRY,
    FLAMING_CAMEL_ID,
    HUSSAR_ID,
    IMAM_UNIT_ID,
    OUTPUT_SCENARIO,
    PETARD_ID,
    SIEGE_ONAGER_ID,
    TECH_BALLISTICS,
    TECH_BLAST_FURNACE,
    TECH_BLOODLINES,
    TECH_BODKIN_ARROW,
    TECH_BRACER,
    TECH_CHAIN_BARDING,
    TECH_CHAIN_MAIL,
    TECH_CHEMISTRY,
    TECH_FLETCHING,
    TECH_FORGING,
    TECH_HUSBANDRY,
    TECH_IRON_CASTING,
    TECH_PLATE_BARDING,
    TECH_PLATE_MAIL,
    TECH_SCALE_BARDING,
    TECH_SCALE_MAIL,
    TECH_SIEGE_ENGINEERS,
    TECH_SQUIRES,
    TREE_OAK_ID,
    TREE_PINE_ID,
    get_wave_definitions,
)
from horde_waves import scale_comp_for_level

_CACHED_SCENARIO: AoE2DEScenario | None = None


def get_compiled_scenario() -> AoE2DEScenario:
    global _CACHED_SCENARIO
    if _CACHED_SCENARIO is None:
        _CACHED_SCENARIO = AoE2DEScenario.from_file(str(OUTPUT_SCENARIO))
    return _CACHED_SCENARIO


class TestWaveScalingAlgorithm(unittest.TestCase):
    """Testy deterministycznego algorytmu skalowania kompozycji jednostek (Etap 2 / BUG-04)."""

    def test_empty_and_zero_compositions(self):
        self.assertEqual(scale_comp_for_level([], -2), [])
        self.assertEqual(scale_comp_for_level([], 0), [])
        self.assertEqual(scale_comp_for_level([], 2), [])
        self.assertEqual(scale_comp_for_level([(UnitInfo.ELITE_JANISSARY.ID, 0), (IMAM_UNIT_ID, 0)], -2), [])
        self.assertEqual(scale_comp_for_level([(UnitInfo.ELITE_JANISSARY.ID, 0)], 1), [])

    def test_single_unit_scaling(self):
        u_id = UnitInfo.ELITE_JANISSARY.ID
        # Poziom 0: dokladna tozsamosc
        self.assertEqual(scale_comp_for_level([(u_id, 2)], 0), [(u_id, 2)])
        # Poziom +1 (+25%): round_half_up(2 * 1.25) = round_half_up(2.5) = 3
        self.assertEqual(scale_comp_for_level([(u_id, 2)], 1), [(u_id, 3)])
        # Poziom +2 (+50%): 2 * 1.5 = 3
        self.assertEqual(scale_comp_for_level([(u_id, 2)], 2), [(u_id, 3)])
        # Poziom -1 (-20%): 2 * 0.8 = 1.6 -> 2
        self.assertEqual(scale_comp_for_level([(u_id, 2)], -1), [(u_id, 2)])
        # Poziom -2 (-40%): 2 * 0.6 = 1.2 -> 1
        self.assertEqual(scale_comp_for_level([(u_id, 2)], -2), [(u_id, 1)])

    def test_multi_pass_reduction_with_mandatory_units(self):
        # 10 pozycji ze specjalistami (mandatory_min_one=True, np. Snajper Imperialny = 557) po 1 szt.
        # oraz 1 pozycja zwykla (np. PIKEMAN = 358) 10 szt. na poziomie -2 (60%).
        # Sumarycznie: 20 jednostek * 0.60 = 12 jednostek docelowo.
        # Wszyscy specjalisci musza zachowac minimum 1 szt. (10 * 1 = 10),
        # wiec zwykla jednostka musi zostac zredukowana do 2 szt.
        comp = [(557, 1)] * 10 + [(358, 10)]
        scaled = scale_comp_for_level(comp, -2)
        total_scaled = sum(cnt for _, cnt in scaled)
        self.assertEqual(total_scaled, 12)
        # Specjalisci zachowuja min. 1 sztuke
        for i in range(10):
            self.assertEqual(scaled[i], (557, 1))
        # Pikinierzy zredukowani do 2
        self.assertEqual(scaled[10], (358, 2))

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            scale_comp_for_level([(UnitInfo.ELITE_JANISSARY.ID, -1)], 0)
        with self.assertRaises(ValueError):
            scale_comp_for_level([(UnitInfo.ELITE_JANISSARY.ID, 2)], 99)

    def test_full_wave_sweep_monotonicity_and_integrity(self):
        """Sprawdza wszystkie 14 fal, wszystkie obozy i poziomy -2..+2 pod katem monotonicznosci."""
        wave_defs = get_wave_definitions()
        s_keys = ["g1_north", "g1_east", "g2_snipers", "g2_mages", "g3_north", "g3_east"]

        for w_def in wave_defs:
            for s_key in s_keys:
                comp = getattr(w_def, s_key)
                if not comp:
                    continue
                orig_total = sum(cnt for _, cnt in comp)

                totals = {}
                for lvl in [-2, -1, 0, 1, 2]:
                    scaled = scale_comp_for_level(comp, lvl)
                    t_sum = sum(cnt for _, cnt in scaled)
                    totals[lvl] = t_sum
                    self.assertGreater(t_sum, 0, f"Fala {w_def.wave_num} {s_key} lvl {lvl} ma 0 jednostek!")

                # Poziom 0 musi miec dokladnie orig_total
                self.assertEqual(totals[0], orig_total)
                # Monotonicznosc: sum(-2) <= sum(-1) <= sum(0) <= sum(1) <= sum(2)
                self.assertLessEqual(totals[-2], totals[-1])
                self.assertLessEqual(totals[-1], totals[0])
                self.assertLessEqual(totals[0], totals[1])
                self.assertLessEqual(totals[1], totals[2])


class TestEnemyUnitRegistryAndSanctuary(unittest.TestCase):
    """Testy spojnosci rejestru jednostek oraz odwracalnosci zmian trudnosci w Sanktuarium."""

    def test_registry_completeness_across_all_spawns(self):
        """Wszystkie ID uzywane w triggerach spawnu Hordy P5-P8 musza byc w ENEMY_UNIT_REGISTRY."""
        scenario = get_compiled_scenario()
        ai_players = {PlayerId.FIVE.value, PlayerId.SIX.value, PlayerId.SEVEN.value, PlayerId.EIGHT.value}
        spawned_unit_ids = set()

        for tr in scenario.trigger_manager.triggers:
            for eff in tr.effects:
                if eff.effect_type == EffectId.CREATE_OBJECT and eff.source_player in ai_players:
                    spawned_unit_ids.add(eff.object_list_unit_id)

        self.assertGreater(len(spawned_unit_ids), 0, "Brak spawnujacych sie jednostek AI!")
        for u_id in spawned_unit_ids:
            self.assertIn(u_id, ENEMY_UNIT_REGISTRY, f"Brak jednostki ID {u_id} w ENEMY_UNIT_REGISTRY!")

    def test_iron_elephant_and_jackal_attack_immunity(self):
        """Zelazny Slon i Szakal nie moga miec attack_class, aby nie dostawac bonusow ataku."""
        elephant_spec = ENEMY_UNIT_REGISTRY[ELITE_BATTLE_ELEPHANT_ID]
        self.assertIsNone(elephant_spec.attack_class)
        self.assertTrue(elephant_spec.scales_hp)

        jackal_spec = ENEMY_UNIT_REGISTRY[HUSSAR_ID]
        self.assertIsNone(jackal_spec.attack_class)
        self.assertTrue(jackal_spec.scales_hp)

    def test_sanctuary_cycle_mathematical_zero_drift(self):
        """Symulacja pelnego cyklu 0 -> +1 -> +2 -> +1 -> 0 -> -1 -> -2 -> -1 -> 0 daje dokladnie zero driftu."""
        sim_hp = {u_id: 0 for u_id in ENEMY_UNIT_REGISTRY}
        sim_atk = {u_id: 0 for u_id in ENEMY_UNIT_REGISTRY}

        cycle_transitions = ["pos_up", "pos_up", "pos_down", "pos_down", "neg_down", "neg_down", "neg_up", "neg_up"]

        for mode in cycle_transitions:
            if mode == "pos_up":
                for u_id, spec in ENEMY_UNIT_REGISTRY.items():
                    if spec.scales_hp:
                        sim_hp[u_id] += BALANCE["diff_step_up_hp"]
                    if spec.attack_class is not None:
                        sim_atk[u_id] += BALANCE["diff_step_up_atk"]
            elif mode == "pos_down":
                for u_id, spec in ENEMY_UNIT_REGISTRY.items():
                    if spec.scales_hp:
                        sim_hp[u_id] -= BALANCE["diff_step_up_hp"]
                    if spec.attack_class is not None:
                        sim_atk[u_id] -= BALANCE["diff_step_up_atk"]
            elif mode == "neg_down":
                for u_id, spec in ENEMY_UNIT_REGISTRY.items():
                    if spec.scales_hp:
                        sim_hp[u_id] -= spec.hp_delta_down
            elif mode == "neg_up":
                for u_id, spec in ENEMY_UNIT_REGISTRY.items():
                    if spec.scales_hp:
                        sim_hp[u_id] += spec.hp_delta_down

        for u_id, spec in ENEMY_UNIT_REGISTRY.items():
            self.assertEqual(sim_hp[u_id], 0, f"Dryf HP dla {spec.name} ({u_id}): {sim_hp[u_id]}")
            self.assertEqual(sim_atk[u_id], 0, f"Dryf Ataku dla {spec.name} ({u_id}): {sim_atk[u_id]}")


class TestScenarioBinaryStructure(unittest.TestCase):
    """Asercje na wygenerowanym binarnym pliku .aoe2scenario."""

    @classmethod
    def setUpClass(cls):
        cls.scenario = get_compiled_scenario()
        cls.tm = cls.scenario.trigger_manager
        cls.triggers = cls.tm.triggers
        cls.t_map = {t.name: t for t in cls.triggers}

    def test_state_markers_and_sanctuary_lock(self):
        """Tylko State_Diff_Lvl_0 jest aktywny na starcie. Mechanizmy blokad i relay zostaly usuniete."""
        for lvl_tag in ["M2", "M1", "0", "P1", "P2"]:
            name = f"State_Diff_Lvl_{lvl_tag}"
            self.assertIn(name, self.t_map)
            tr = self.t_map[name]
            expected_enabled = 1 if lvl_tag == "0" else 0
            self.assertEqual(tr.enabled, expected_enabled, f"{name} ma zly stan enabled!")
            self.assertEqual(tr.looping, 0)

        # Upewnij sie, ze stare triggery blokujace i przekaznikowe nie istnieja
        for t_name in self.t_map:
            self.assertNotIn("Sanctuary_Unlocked", t_name, f"Znaleziono stary trigger {t_name}!")
            self.assertNotIn("Close_Window", t_name, f"Znaleziono stary trigger {t_name}!")
            self.assertNotIn("Relay2s", t_name, f"Znaleziono stary trigger {t_name}!")

    def test_difficulty_transitions_isolation_bug01(self):
        """Asercja anty-regresyjna BUG-01: triggery 09_Diff_* nie dotykaja zadnych fal i maja wlasciwy porzadek topologiczny."""
        diff_names = [
            "09_Diff_Up_0_to_P1", "09_Diff_Up_P1_to_P2", "09_Diff_Down_P2_to_P1", "09_Diff_Down_P1_to_0",
            "09_Diff_Down_0_to_M1", "09_Diff_Down_M1_to_M2", "09_Diff_Up_M2_to_M1", "09_Diff_Up_M1_to_0",
        ]

        for d_name in diff_names:
            self.assertIn(d_name, self.t_map)
            tr = self.t_map[d_name]

            # Dokladnie 1 warunek: OBJECTS_IN_AREA dla Krola P1
            self.assertEqual(len(tr.conditions), 1, f"{d_name} powinien miec dokladnie 1 warunek!")
            cond = tr.conditions[0]
            self.assertEqual(cond.condition_type, ConditionId.OBJECTS_IN_AREA)
            self.assertEqual(cond.source_player, PlayerId.ONE.value)
            self.assertEqual(cond.object_list, UnitInfo.KING.ID)

            # Teleport i Stop Krola
            has_teleport = any(e.effect_type == EffectId.TELEPORT_OBJECT for e in tr.effects)
            has_stop = any(e.effect_type == EffectId.STOP_OBJECT for e in tr.effects)
            self.assertTrue(has_teleport, f"{d_name} brak teleport_object!")
            self.assertTrue(has_stop, f"{d_name} brak stop_object!")

            # Zero wplywu na fale 03_W* i 03_Endless*
            for eff in tr.effects:
                if eff.effect_type in (EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER):
                    target_tr = self.tm.triggers[eff.trigger_id]
                    self.assertFalse(
                        target_tr.name.startswith("03_W") or target_tr.name.startswith("03_Endless"),
                        f"{d_name} modyfikuje trigger fali {target_tr.name}! (Regresja BUG-01)",
                    )

        # Porzadek topologiczny trigger_id (565..572)
        # Pad GORNY: P1->P2 (565) < 0->P1 (566) < M1->0 (567) < M2->M1 (568)
        id_up_p1_p2 = self.t_map["09_Diff_Up_P1_to_P2"].trigger_id
        id_up_0_p1 = self.t_map["09_Diff_Up_0_to_P1"].trigger_id
        id_up_m1_0 = self.t_map["09_Diff_Up_M1_to_0"].trigger_id
        id_up_m2_m1 = self.t_map["09_Diff_Up_M2_to_M1"].trigger_id
        self.assertEqual((id_up_p1_p2, id_up_0_p1, id_up_m1_0, id_up_m2_m1), (565, 566, 567, 568))

        # Pad DOLNY: M1->M2 (569) < 0->M1 (570) < P1->0 (571) < P2->P1 (572)
        id_down_m1_m2 = self.t_map["09_Diff_Down_M1_to_M2"].trigger_id
        id_down_0_m1 = self.t_map["09_Diff_Down_0_to_M1"].trigger_id
        id_down_p1_0 = self.t_map["09_Diff_Down_P1_to_0"].trigger_id
        id_down_p2_p1 = self.t_map["09_Diff_Down_P2_to_P1"].trigger_id
        self.assertEqual((id_down_m1_m2, id_down_0_m1, id_down_p1_0, id_down_p2_p1), (569, 570, 571, 572))

    def test_siege_onager_blast_attack_level_bug02(self):
        """01b musi ustawiac ATTR_BLAST_ATTACK_LEVEL = 44 na 2 dla SIEGE_ONAGER_ID dla wszystkich 4 graczy AI."""
        tr_01b = self.t_map["01b_Apply_Specialized_Unit_Archetypes"]
        blast_effects = [
            eff for eff in tr_01b.effects
            if (
                eff.effect_type == EffectId.MODIFY_ATTRIBUTE
                and eff.object_list_unit_id == SIEGE_ONAGER_ID
                and eff.object_attributes == ATTR_BLAST_ATTACK_LEVEL
            )
        ]
        self.assertEqual(len(blast_effects), 4, f"Oczekiwano 4 efektow blast_attack_level, znaleziono {len(blast_effects)}!")
        ai_players = {PlayerId.FIVE.value, PlayerId.SIX.value, PlayerId.SEVEN.value, PlayerId.EIGHT.value}
        found_players = {eff.source_player for eff in blast_effects}
        self.assertEqual(found_players, ai_players)
        for eff in blast_effects:
            self.assertEqual(eff.quantity, 2)

    def test_iron_elephant_attack_resets_in_forge(self):
        """01d, 01e, 01f musza resetowac atak Zelaznego Slonia (do 3) i Szakala (do 2) dla wszystkich 4 graczy AI."""
        ai_players = {PlayerId.FIVE.value, PlayerId.SIX.value, PlayerId.SEVEN.value, PlayerId.EIGHT.value}
        for t_name in ["01d_AI_Techs_Feudal_8m30s", "01e_AI_Techs_Castle_18m", "01f_AI_Techs_Imperial_34m30s"]:
            tr = self.t_map[t_name]

            # Reset ataku Zelaznego Slonia
            elephant_resets = [
                eff for eff in tr.effects
                if (
                    eff.effect_type == EffectId.MODIFY_ATTRIBUTE
                    and eff.object_list_unit_id == ELITE_BATTLE_ELEPHANT_ID
                    and eff.object_attributes == ATTR_ATTACK
                )
            ]
            self.assertEqual(len(elephant_resets), 4, f"{t_name} brak 4 resetow ataku Slonia (jest {len(elephant_resets)})!")
            self.assertEqual({e.source_player for e in elephant_resets}, ai_players)
            for eff in elephant_resets:
                val = eff.armour_attack_quantity if eff.armour_attack_quantity is not None else (eff.quantity % 65536)
                self.assertEqual(val, BALANCE["tank_unit_atk"])

            # Reset ataku Szakala
            jackal_resets = [
                eff for eff in tr.effects
                if (
                    eff.effect_type == EffectId.MODIFY_ATTRIBUTE
                    and eff.object_list_unit_id == HUSSAR_ID
                    and eff.object_attributes == ATTR_ATTACK
                )
            ]
            self.assertEqual(len(jackal_resets), 4, f"{t_name} brak 4 resetow ataku Szakala (jest {len(jackal_resets)})!")
            self.assertEqual({e.source_player for e in jackal_resets}, ai_players)
            for eff in jackal_resets:
                val = eff.armour_attack_quantity if eff.armour_attack_quantity is not None else (eff.quantity % 65536)
                self.assertEqual(val, BALANCE["raider_atk"])

    def test_escalation_prompt_buffs_bug08(self):
        """04a, 04c, 04e musza natychmiast aplikowac 1. tick eskalacji."""
        for esc_name in ["04a_Enable_Escalation_At_20m", "04c_Enable_LateGame_Escalation_At_45m", "04e_Enable_Endgame_Escalation_At_55m"]:
            tr = self.t_map[esc_name]
            mod_effects = [e for e in tr.effects if e.effect_type == EffectId.MODIFY_ATTRIBUTE]
            self.assertGreater(len(mod_effects), 0, f"{esc_name} brak efektow modify_attribute!")
            chat_effects = [e for e in tr.effects if e.effect_type in (EffectId.DISPLAY_INSTRUCTIONS, EffectId.SEND_CHAT)]
            self.assertGreater(len(chat_effects), 0, f"{esc_name} brak czatu!")

    def test_archmage_aura_automaton_bug05(self):
        """Aura Arcymaga 02a/02d musi tworzyc dwustanowy automat z inverted=1."""
        t_on = self.t_map["02a_Mage_Global_Horde_Shield_On"]
        t_off = self.t_map["02d_Mage_Global_Horde_Shield_Off"]

        self.assertEqual(t_on.enabled, 1)
        self.assertEqual(t_on.looping, 0)
        self.assertEqual(t_off.enabled, 0)
        self.assertEqual(t_off.looping, 0)

        # 02d ma warunek inverted=1
        cond_oia = [c for c in t_off.conditions if c.condition_type == ConditionId.OBJECTS_IN_AREA]
        self.assertEqual(len(cond_oia), 1)
        self.assertEqual(cond_oia[0].inverted, 1)

        # 02d reaktywuje 02a
        act_effs = [e.trigger_id for e in t_off.effects if e.effect_type == EffectId.ACTIVATE_TRIGGER]
        self.assertIn(t_on.trigger_id, act_effs)

        # Zadna fala nie aktywuje 02a
        for tr in self.triggers:
            if tr.name.startswith("03_W"):
                for e in tr.effects:
                    if e.effect_type == EffectId.ACTIVATE_TRIGGER:
                        self.assertNotEqual(e.trigger_id, t_on.trigger_id, f"{tr.name} aktywuje 02a!")

    def test_trade_wall_geometry_and_cleaning_bug09(self):
        """Q1: Usuniecie wiez P5, mur na y=186, baszty na y=184."""
        t_q1 = self.t_map["06_Quest1_Build_Trade_Wall_And_Pop"]

        # remove_object wiez P5
        rem_effs = [
            e for e in t_q1.effects
            if e.effect_type == EffectId.REMOVE_OBJECT and e.source_player == PlayerId.FIVE.value
        ]
        self.assertGreater(len(rem_effs), 0, "Q1 nie usuwa wiez P5!")

        # mury i baszty
        wall_y_values = set()
        keep_y_values = set()
        for eff in t_q1.effects:
            if eff.effect_type == EffectId.CREATE_OBJECT:
                if eff.object_list_unit_id == BuildingInfo.FORTIFIED_WALL.ID:
                    wall_y_values.add(eff.location_y)
                elif eff.object_list_unit_id == BuildingInfo.KEEP.ID:
                    keep_y_values.add(eff.location_y)

        self.assertEqual(wall_y_values, {186}, f"Mury Q1 na zlym Y: {wall_y_values}")
        self.assertEqual(keep_y_values, {184}, f"Baszty Q1 na zlym Y: {keep_y_values}")

    def test_camp_deactivations_bug06(self):
        """Zniszczenie kazdego z 10 obozow musi dezaktywowac spawn, leash i 4 detektory."""
        camps = [
            ("06_Quest1_Build_Trade_Wall_And_Pop", "Quest1_Caravan"),
            ("06_Quest2_Sniper_Cliff_Buff", "Quest2_SniperCliff"),
            ("06a_Quest3_Siege_Vault_Unlock", "Quest3_SiegeVault"),
            ("06_Quest4_Blood_Altar_Super_Army", "Quest4_BloodAltar"),
            ("05_Settlement_Destroyed_G1_North", "Settle_G1_North"),
            ("05_Settlement_Destroyed_G1_East", "Settle_G1_East"),
            ("05_Settlement_Destroyed_G2_Snipers", "Settle_G2_Snipers"),
            ("05_Settlement_Destroyed_G2_Mages", "Settle_G2_Mages"),
            ("05_Settlement_Destroyed_G3_North", "Settle_G3_North"),
            ("05_Settlement_Destroyed_G3_East", "Settle_G3_East"),
        ]

        for dest_name, camp_tag in camps:
            tr_dest = self.t_map[dest_name]
            deact_ids = {e.trigger_id for e in tr_dest.effects if e.effect_type == EffectId.DEACTIVATE_TRIGGER}

            t_spawn = self.t_map[f"Garrison_Spawn_{camp_tag}"]
            t_leash = self.t_map[f"Garrison_Leash_{camp_tag}"]
            self.assertIn(t_spawn.trigger_id, deact_ids)
            self.assertIn(t_leash.trigger_id, deact_ids)

            for p in range(1, 5):
                t_det = self.t_map[f"Garrison_Detect_{camp_tag}_P{p}"]
                self.assertIn(t_det.trigger_id, deact_ids)

    def test_settlement_fury_gradation_and_retaliations(self):
        """Gradacja Furii Settlementow Grade 1-3 w 05_Settlement_Destroyed_*."""
        grades = {
            "05_Settlement_Destroyed_G1_North": (8, 1),
            "05_Settlement_Destroyed_G1_East": (8, 1),
            "05_Settlement_Destroyed_G2_Snipers": (12, 1),
            "05_Settlement_Destroyed_G2_Mages": (12, 1),
            "05_Settlement_Destroyed_G3_North": (16, 2),
            "05_Settlement_Destroyed_G3_East": (16, 2),
        }

        for trig_name, (exp_hp, exp_atk) in grades.items():
            tr = self.t_map[trig_name]
            hp_mods = [e.quantity for e in tr.effects if e.effect_type == EffectId.MODIFY_ATTRIBUTE and e.object_attributes == ATTR_HIT_POINTS]
            self.assertGreater(len(hp_mods), 0, f"{trig_name} brak modyfikacji HP!")
            self.assertTrue(all(val == exp_hp for val in hp_mods), f"{trig_name} zly buff HP: {hp_mods}")

            atk_mods = [
                (e.armour_attack_quantity if e.armour_attack_quantity is not None else (e.quantity % 65536))
                for e in tr.effects if e.effect_type == EffectId.MODIFY_ATTRIBUTE and e.object_attributes == ATTR_ATTACK
            ]
            self.assertGreater(len(atk_mods), 0, f"{trig_name} brak modyfikacji Atk!")
            self.assertTrue(all(val == exp_atk for val in atk_mods), f"{trig_name} zly buff Atk: {atk_mods}")

    def test_player_perks_q2_and_q4(self):
        """Perki graczy w Q2 i Q4 obejmuja rozszerzone listy jednostek."""
        t_q2 = self.t_map["06_Quest2_Sniper_Cliff_Buff"]
        q2_units = {e.object_list_unit_id for e in t_q2.effects if e.effect_type == EffectId.MODIFY_ATTRIBUTE}
        # Elite Steppe Lancer (1372) i Heavy Camel (330)
        self.assertIn(1372, q2_units)
        self.assertIn(330, q2_units)

        t_q4 = self.t_map["06_Quest4_Blood_Altar_Super_Army"]
        q4_units = {e.object_list_unit_id for e in t_q4.effects if e.effect_type == EffectId.MODIFY_ATTRIBUTE}
        # Militia (74), Eagle Scout (751), Siege Workshop (49)
        self.assertIn(74, q4_units)
        self.assertIn(751, q4_units)
        self.assertIn(49, q4_units)

        # Imam HP = 120
        imam_mod = [
            e for e in t_q4.effects
            if e.effect_type == EffectId.MODIFY_ATTRIBUTE and e.object_list_unit_id == IMAM_UNIT_ID and e.object_attributes == ATTR_HIT_POINTS
        ]
        self.assertEqual(len(imam_mod), 1)
        self.assertEqual(imam_mod[0].quantity, 120)
        self.assertEqual(imam_mod[0].operation, Operation.SET.value)

    def test_wave_clocks_variants_and_endless_gates_bug03(self):
        """Sprawdza strukture Zegarow fal 1-14 oraz indywidualnych bramek i wariantow Endless."""
        wave_defs = get_wave_definitions()
        s_keys = ["G1_North", "G1_East", "G2_Snipers", "G2_Mages", "G3_North", "G3_East"]

        for w_def in wave_defs:
            w_num = w_def.wave_num
            for s_key in s_keys:
                clock_name = f"03_W{w_num:02d}_{s_key}_Clock"
                if clock_name in self.t_map:
                    tr_c = self.t_map[clock_name]
                    self.assertEqual(tr_c.enabled, 1)
                    self.assertEqual(tr_c.looping, 0)
                    for lvl_tag in ["M2", "M1", "0", "P1", "P2"]:
                        v_name = f"03_W{w_num:02d}_{s_key}_Diff_{lvl_tag}"
                        self.assertIn(v_name, self.t_map)
                        tr_v = self.t_map[v_name]
                        self.assertEqual(tr_v.enabled, 0)
                        self.assertEqual(tr_v.looping, 0)

        # Endless Gates i Warianty Endless
        for s_key in s_keys:
            gate_name = f"03_Endless_Gate_{s_key}"
            self.assertIn(gate_name, self.t_map)
            tr_g = self.t_map[gate_name]
            self.assertEqual(tr_g.enabled, 0)
            self.assertEqual(tr_g.looping, 1)

            for lvl_tag in ["M2", "M1", "0", "P1", "P2"]:
                var_name = f"03_Endless_{s_key}_Diff_{lvl_tag}"
                self.assertIn(var_name, self.t_map)
                tr_ev = self.t_map[var_name]
                self.assertEqual(tr_ev.enabled, 0)
                self.assertEqual(tr_ev.looping, 0)

    def test_leash_and_p7_spawn_separation_geometry(self):
        """Weryfikacja, ze punkty spawnu Szakala P7 sa oddalone od smyczy Magow (116, 114) o > 20 kratek."""
        mage_camp_x, mage_camp_y = 116, 114
        leash_outer_radius = 20

        checked_spawns = 0
        for tr in self.triggers:
            if tr.name.startswith("03_W") or tr.name.startswith("03_Endless"):
                for eff in tr.effects:
                    if (
                        eff.effect_type == EffectId.CREATE_OBJECT
                        and eff.source_player == PlayerId.SEVEN.value
                        and eff.object_list_unit_id == HUSSAR_ID
                    ):
                        sx, sy = eff.location_x, eff.location_y
                        chebyshev_dist = max(abs(sx - mage_camp_x), abs(sy - mage_camp_y))
                        self.assertGreater(
                            chebyshev_dist,
                            leash_outer_radius,
                            f"{tr.name} spawnuje Szakala P7 na ({sx}, {sy}), co lezy w obrebie smyczy Magow (d={chebyshev_dist} <= {leash_outer_radius})!",
                        )
                        checked_spawns += 1

        self.assertGreater(checked_spawns, 0, "Brak sprawdzonych spawnów Szakala P7!")

    def test_spawn_grid_11col_and_all_camp_leash_separation(self):
        """Weryfikuje 11-kolumnowa siatke [-5..+5, -5..+5], brak kolizji z Garrison_Leash_* oraz drzewami."""
        camps_by_player = {
            PlayerId.FIVE.value: [
                ("Settle_G1_North", 76, 72),
                ("Settle_G1_East", 132, 152),
                ("Quest1_Caravan", 154, 190),
            ],
            PlayerId.SIX.value: [
                ("Settle_G2_Snipers", 68, 34),
                ("Quest2_SniperCliff", 28, 32),
            ],
            PlayerId.SEVEN.value: [
                ("Settle_G2_Mages", 148, 72),
            ],
            PlayerId.EIGHT.value: [
                ("Settle_G3_North", 142, 24),
                ("Settle_G3_East", 176, 56),
                ("Quest3_SiegeVault", 142, 118),
                ("Quest4_BloodAltar", 105, 20),
            ],
        }
        ring_inner = 14
        ring_outer = 20

        # Zbierz wspolrzedne drzew na mapie (poza drzewami wycinanymi przez Saperow w Fali 9 i 12)
        breach_n_tr = self.t_map["03_W09_Forest_Breach_North_Execute"]
        breach_e_tr = self.t_map["03_W12_Forest_Breach_East_Execute"]
        n_removed_ids = {
            eff.selected_object_ids[0]
            for eff in breach_n_tr.effects
            if eff.effect_type == EffectId.REMOVE_OBJECT and eff.selected_object_ids
        }
        e_removed_ids = {
            eff.selected_object_ids[0]
            for eff in breach_e_tr.effects
            if eff.effect_type == EffectId.REMOVE_OBJECT and eff.selected_object_ids
        }
        self.assertEqual(len(n_removed_ids), 66, f"Przesieka polnocna 6x11 powinna wycinac 66 drzew, wycina {len(n_removed_ids)}!")
        self.assertEqual(len(e_removed_ids), 66, f"Przesieka wschodnia 11x6 powinna wycinac 66 drzew, wycina {len(e_removed_ids)}!")

        permanent_tree_tiles = set()
        for u in self.scenario.unit_manager.units[PlayerId.GAIA.value]:
            if u.unit_const in (TREE_OAK_ID, TREE_PINE_ID) and u.reference_id not in (n_removed_ids | e_removed_ids):
                permanent_tree_tiles.add((int(u.x), int(u.y)))

        max_group_size = 0
        total_spawn_groups = 0

        for tr in self.triggers:
            current_creates = []
            for eff in tr.effects:
                if eff.effect_type == EffectId.CREATE_OBJECT and eff.source_player in camps_by_player:
                    current_creates.append(eff)
                elif eff.effect_type in (EffectId.ATTACK_MOVE, EffectId.TASK_OBJECT) and current_creates:
                    total_spawn_groups += 1
                    group_len = len(current_creates)
                    max_group_size = max(max_group_size, group_len)
                    self.assertLessEqual(group_len, 121, f"{tr.name} spawnuje {group_len} > 121 jednostek!")

                    # Srodek spawnu wyznaczony z pierwszej jednostki (idx=0 -> dx=-5, dy=-5) i zgodny z obszarem rozkazu +-8
                    spawn_x = current_creates[0].location_x + 5
                    spawn_y = current_creates[0].location_y + 5
                    self.assertEqual(eff.area_x1, max(0, spawn_x - 8))
                    self.assertEqual(eff.area_y1, max(0, spawn_y - 8))
                    self.assertEqual(eff.area_x2, min(199, spawn_x + 8))
                    self.assertEqual(eff.area_y2, min(199, spawn_y + 8))

                    for idx, cr_eff in enumerate(current_creates):
                        dx = cr_eff.location_x - spawn_x
                        dy = cr_eff.location_y - spawn_y
                        self.assertEqual(dx, (idx % 11) - 5, f"{tr.name} zla kolumna dx dla idx={idx}")
                        self.assertEqual(dy, (idx // 11) - 5, f"{tr.name} zly wiersz dy dla idx={idx}")
                        self.assertGreaterEqual(dx, -5)
                        self.assertLessEqual(dx, 5)
                        self.assertGreaterEqual(dy, -5)
                        self.assertLessEqual(dy, 5)

                        ux, uy = cr_eff.location_x, cr_eff.location_y
                        self.assertNotIn(
                            (ux, uy),
                            permanent_tree_tiles,
                            f"{tr.name} spawnuje jednostke na drzewie ({ux}, {uy})!",
                        )

                        for camp_name, cx, cy in camps_by_player[cr_eff.source_player]:
                            dist = max(abs(ux - cx), abs(uy - cy))
                            if tr.name == f"Garrison_Spawn_{camp_name}":
                                self.assertLess(
                                    dist,
                                    ring_inner,
                                    f"{tr.name} spawnuje garnizon w obrebie smyczy ({ux}, {uy}), d={dist}!",
                                )
                            else:
                                self.assertGreater(
                                    dist,
                                    ring_outer,
                                    f"{tr.name} spawnuje jednostke na ({ux}, {uy}) w zasiegu smyczy {camp_name} ({cx}, {cy}), d={dist} <= {ring_outer}!",
                                )
                    current_creates = []

        self.assertGreater(total_spawn_groups, 0)
        self.assertEqual(max_group_size, 93, f"Najwieksza grupa spawnu (W14 G3_North P2) powinna liczyc 93 jednostki, a liczy {max_group_size}!")

    def test_ai_techs_completeness_and_specialized_unit_caps(self):
        """Weryfikuje pelen zestaw technologii w 01d, 01e, 01f oraz pulapy enforce_specialized_unit_caps."""
        ai_players = {PlayerId.FIVE.value, PlayerId.SIX.value, PlayerId.SEVEN.value, PlayerId.EIGHT.value}
        expected_techs = {
            "01d_AI_Techs_Feudal_8m30s": {
                TECH_FORGING, TECH_SCALE_MAIL, TECH_SCALE_BARDING, TECH_FLETCHING, TECH_BLOODLINES,
            },
            "01e_AI_Techs_Castle_18m": {
                TECH_IRON_CASTING, TECH_CHAIN_MAIL, TECH_SQUIRES, TECH_CHAIN_BARDING,
                TECH_BODKIN_ARROW, TECH_BALLISTICS, TECH_HUSBANDRY,
            },
            "01f_AI_Techs_Imperial_34m30s": {
                TECH_BLAST_FURNACE, TECH_PLATE_MAIL, TECH_PLATE_BARDING,
                TECH_BRACER, TECH_CHEMISTRY, TECH_SIEGE_ENGINEERS,
            },
        }

        for t_name, tech_set in expected_techs.items():
            tr = self.t_map[t_name]
            for ai_p in ai_players:
                researched = {
                    e.technology
                    for e in tr.effects
                    if e.effect_type == EffectId.RESEARCH_TECHNOLOGY and e.source_player == ai_p
                }
                self.assertEqual(researched, tech_set, f"{t_name} niekompletne technologie dla gracza P{ai_p}: {researched}")

            # Sprawdz, ze wszystkie efekty MODIFY_ATTRIBUTE wystepuja PO efektach RESEARCH_TECHNOLOGY
            last_tech_idx = max(i for i, e in enumerate(tr.effects) if e.effect_type == EffectId.RESEARCH_TECHNOLOGY)
            first_mod_idx = min(i for i, e in enumerate(tr.effects) if e.effect_type == EffectId.MODIFY_ATTRIBUTE)
            self.assertGreater(first_mod_idx, last_tech_idx, f"{t_name}: modyfikacje atrybutow musza byc po technologiach!")

            # Sprawdz pulapy statystyk (enforce_specialized_unit_caps) dla wszystkich 4 graczy AI
            for ai_p in ai_players:
                p_mods = [
                    e for e in tr.effects
                    if e.effect_type == EffectId.MODIFY_ATTRIBUTE and e.source_player == ai_p and e.operation == Operation.SET.value
                ]

                def get_set_val(
                    unit_id: int,
                    attr_id: int,
                    armor_class: int | None = None,
                    mods=p_mods,
                    trig_label=t_name,
                    player_id=ai_p,
                ):
                    matches = [
                        e for e in mods
                        if e.object_list_unit_id == unit_id
                        and e.object_attributes == attr_id
                        and (armor_class is None or e.armour_attack_class == armor_class)
                    ]
                    self.assertEqual(
                        len(matches),
                        1,
                        f"{trig_label} P{player_id} brak SET dla unit={unit_id}, attr={attr_id}, class={armor_class}",
                    )
                    eff = matches[0]
                    if armor_class is not None:
                        return eff.armour_attack_quantity if eff.armour_attack_quantity is not None else (eff.quantity % 65536)
                    return eff.quantity

                # Zelazny Slon: atak 3, pancerz 10/12, predkosc 0.52
                self.assertEqual(get_set_val(ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, 4), BALANCE["tank_unit_atk"])
                self.assertEqual(get_set_val(ELITE_BATTLE_ELEPHANT_ID, ATTR_ARMOR, 4), BALANCE["tank_melee_armor"])
                self.assertEqual(get_set_val(ELITE_BATTLE_ELEPHANT_ID, ATTR_ARMOR, 3), BALANCE["tank_pierce_armor"])
                self.assertAlmostEqual(get_set_val(ELITE_BATTLE_ELEPHANT_ID, ATTR_MOVEMENT_SPEED), BALANCE["tank_speed"], places=2)

                # Szakal: atak 2, predkosc 1.62, pancerz 0/6
                self.assertEqual(get_set_val(HUSSAR_ID, ATTR_ATTACK, 4), BALANCE["raider_atk"])
                self.assertAlmostEqual(get_set_val(HUSSAR_ID, ATTR_MOVEMENT_SPEED), BALANCE["raider_speed"], places=2)
                self.assertEqual(get_set_val(HUSSAR_ID, ATTR_ARMOR, 3), BALANCE["raider_pierce_armor"])
                self.assertEqual(get_set_val(HUSSAR_ID, ATTR_ARMOR, 4), 0)

                # Berserker: pancerz strzelecki 0, predkosc 1.40
                self.assertEqual(get_set_val(ELITE_BERSERK_ID, ATTR_ARMOR, 3), 0)
                self.assertAlmostEqual(get_set_val(ELITE_BERSERK_ID, ATTR_MOVEMENT_SPEED), BALANCE["berserk_speed"], places=2)

                # Kamikaze (Petard + Flaming Camel): pancerz strzelecki 0, predkosc 1.50
                for kam_id in (PETARD_ID, FLAMING_CAMEL_ID):
                    self.assertEqual(get_set_val(kam_id, ATTR_ARMOR, 3), 0)
                    self.assertAlmostEqual(get_set_val(kam_id, ATTR_MOVEMENT_SPEED), BALANCE["kamikaze_speed"], places=2)

                # Mozdzierz Oblezniczy: zasieg 21
                self.assertEqual(get_set_val(SIEGE_ONAGER_ID, ATTR_MAXIMUM_RANGE), BALANCE["mortar_range"])

        # Korekta -20 HP dla HUSSAR_ID w 01d po zbadaniu Bloodlines
        tr_01d = self.t_map["01d_AI_Techs_Feudal_8m30s"]
        hussar_hp_subs = [
            e for e in tr_01d.effects
            if (
                e.effect_type == EffectId.MODIFY_ATTRIBUTE
                and e.object_list_unit_id == HUSSAR_ID
                and e.object_attributes == ATTR_HIT_POINTS
                and e.operation == Operation.SUBTRACT.value
            )
        ]
        self.assertEqual(len(hussar_hp_subs), 4)
        self.assertEqual({e.source_player for e in hussar_hp_subs}, ai_players)
        for e in hussar_hp_subs:
            self.assertEqual(e.quantity, 20)

    def test_endless_jackal_dual_flank_raids(self):
        """Weryfikuje podzial Szakali w 03_Endless_G2_Mages_Diff_* na dwie flanki: (52, 86)->(54, 119) i (116, 162)->(54, 170)."""
        w14_raiders = get_wave_definitions()[-1].raider_count
        diff_tags = {-2: "M2", -1: "M1", 0: "0", 1: "P1", 2: "P2"}

        for lvl, tag in diff_tags.items():
            tr = self.t_map[f"03_Endless_G2_Mages_Diff_{tag}"]
            expected_total = sum(cnt for _, cnt in scale_comp_for_level([(HUSSAR_ID, w14_raiders)], lvl))
            expected_north = (expected_total + 1) // 2
            expected_east = expected_total // 2

            hussar_spawns = [
                e for e in tr.effects
                if e.effect_type == EffectId.CREATE_OBJECT and e.object_list_unit_id == HUSSAR_ID
            ]
            self.assertEqual(len(hussar_spawns), expected_total)

            north_spawns = [e for e in hussar_spawns if 44 <= e.location_x <= 60 and 78 <= e.location_y <= 94]
            east_spawns = [e for e in hussar_spawns if 108 <= e.location_x <= 124 and 154 <= e.location_y <= 170]
            self.assertEqual(len(north_spawns), expected_north)
            self.assertEqual(len(east_spawns), expected_east)

            move_effs = [
                e for e in tr.effects
                if e.effect_type == EffectId.TASK_OBJECT
                and e.source_player == PlayerId.SEVEN.value
                and e.action_type == ActionType.MOVE.value
            ]
            self.assertEqual(len(move_effs), 2)
            self.assertEqual((move_effs[0].location_x, move_effs[0].location_y), (54, 119))
            self.assertEqual((move_effs[1].location_x, move_effs[1].location_y), (54, 170))


if __name__ == "__main__":
    unittest.main()
