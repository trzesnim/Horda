from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Operation
from AoE2ScenarioParser.datasets.units import UnitInfo

from horde_config import (
    ATTR_ARMOR,
    ATTR_ATTACK,
    ATTR_HIT_POINTS,
    ATTR_MAXIMUM_RANGE,
    ATTR_MOVEMENT_SPEED,
    ATTR_SEARCH_RADIUS,
    ATTR_WORK_RATE,
    BALANCE,
    ELITE_BATTLE_ELEPHANT_ID,
    ENEMY_UNIT_REGISTRY,
    IMAM_UNIT_ID,
    MAP_SIZE,
    PLAYER_CAVALRY_UNITS,
    PLAYER_INFANTRY_UNITS,
    PLAYER_PROD_BUILDINGS,
    PLAYER_RANGED_UNITS,
    RES_BONUS_POP_CAP,
    RES_FOOD,
    RES_GOLD,
    RES_STONE,
    RES_WOOD,
    TECH_BALLISTICS,
    TECH_CHEMISTRY,
    TECH_SIEGE_ENGINEERS,
    TECH_THUMB_RING,
)
from horde_waves import (
    add_enemy_combat_buff,
    add_player_resource,
    add_spawn_and_attack_effect,
    research_techs,
    safe_call,
    safe_modify_attribute,
    send_highlight_chat,
    set_as_objective,
)


def setup_sanctuary_quests_and_victory(scenario, ctx: dict) -> None:
    ai_players = ctx["ai_players"]
    all_settlement_wave_triggers = ctx["all_settlement_wave_triggers"]
    allied_citadel = ctx["allied_citadel"]
    deep_target_center = ctx["deep_target_center"]
    human_players = ctx["human_players"]
    p_coords = ctx["p_coords"]
    q1_bldg = ctx["q1_bldg"]
    q2_bldg = ctx["q2_bldg"]
    q2_pos = ctx["q2_pos"]
    q3_bldg = ctx["q3_bldg"]
    q3_pos = ctx["q3_pos"]
    q4_bldg = ctx["q4_bldg"]
    q4_pos = ctx["q4_pos"]
    s_coords = ctx["s_coords"]
    s_g1_east = ctx["s_g1_east"]
    s_g1_north = ctx["s_g1_north"]
    s_g2_mages = ctx["s_g2_mages"]
    s_g2_snipers = ctx["s_g2_snipers"]
    s_g3_east = ctx["s_g3_east"]
    s_g3_north = ctx["s_g3_north"]
    sanctuary_cx = ctx["sanctuary_cx"]
    sanctuary_cy = ctx["sanctuary_cy"]
    state_markers = ctx["state_markers"]
    t_sanc_unlocked = ctx["t_sanc_unlocked"]
    camp_leash_handles = ctx["camp_leash_handles"]
    tm = ctx["tm"]

    pad_up_box = (sanctuary_cx - 2, sanctuary_cy - 4, sanctuary_cx + 2, sanctuary_cy - 3)
    pad_down_box = (sanctuary_cx - 2, sanctuary_cy + 3, sanctuary_cx + 2, sanctuary_cy + 4)
    full_chamber_box = (sanctuary_cx - 2, sanctuary_cy - 4, sanctuary_cx + 2, sanctuary_cy + 4)

    def deactivate_camp_handles(trig, handle_tuple):
        t_spawn, t_leash, detect_list = handle_tuple
        safe_call(trig.new_effect.deactivate_trigger, trigger_id=t_spawn.trigger_id)
        safe_call(trig.new_effect.deactivate_trigger, trigger_id=t_leash.trigger_id)
        for d_tr in detect_list:
            safe_call(trig.new_effect.deactivate_trigger, trigger_id=d_tr.trigger_id)

    def apply_king_reset_and_safe_stat_shift(trig, mode: str):
        cx1, cy1, cx2, cy2 = full_chamber_box
        safe_call(
            trig.new_effect.teleport_object,
            source_player=PlayerId.ONE,
            object_list_unit_id=UnitInfo.KING.ID,
            area_x1=cx1,
            area_y1=cy1,
            area_x2=cx2,
            area_y2=cy2,
            location_x=sanctuary_cx,
            location_y=sanctuary_cy,
        )
        safe_call(
            trig.new_effect.stop_object,
            source_player=PlayerId.ONE,
            object_list_unit_id=UnitInfo.KING.ID,
            area_x1=cx1,
            area_y1=cy1,
            area_x2=cx2,
            area_y2=cy2,
        )

        if mode in ("pos_up", "pos_down"):
            op = Operation.ADD if mode == "pos_up" else Operation.SUBTRACT
            hp_val = BALANCE["diff_step_up_hp"]
            atk_val = BALANCE["diff_step_up_atk"]
            for ai_p in ai_players:
                for spec in ENEMY_UNIT_REGISTRY.values():
                    if spec.scales_hp:
                        safe_modify_attribute(trig, ai_p, spec.unit_id, ATTR_HIT_POINTS, op, hp_val)
                    if spec.attack_class is not None:
                        safe_modify_attribute(trig, ai_p, spec.unit_id, ATTR_ATTACK, op, atk_val, armor_class=spec.attack_class)
        elif mode in ("neg_down", "neg_up"):
            op = Operation.SUBTRACT if mode == "neg_down" else Operation.ADD
            for ai_p in ai_players:
                for spec in ENEMY_UNIT_REGISTRY.values():
                    if spec.scales_hp:
                        safe_modify_attribute(trig, ai_p, spec.unit_id, ATTR_HIT_POINTS, op, spec.hp_delta_down)

    t_up_0_to_p1 = tm.add_trigger("09_Diff_Up_0_to_P1", enabled=True, looping=False)
    t_down_0_to_m1 = tm.add_trigger("09_Diff_Down_0_to_M1", enabled=True, looping=False)

    t_up_p1_to_p2 = tm.add_trigger("09_Diff_Up_P1_to_P2", enabled=False, looping=False)
    t_down_p1_to_0 = tm.add_trigger("09_Diff_Down_P1_to_0", enabled=False, looping=False)
    t_down_p2_to_p1 = tm.add_trigger("09_Diff_Down_P2_to_P1", enabled=False, looping=False)

    t_up_m1_to_0 = tm.add_trigger("09_Diff_Up_M1_to_0", enabled=False, looping=False)
    t_down_m1_to_m2 = tm.add_trigger("09_Diff_Down_M1_to_M2", enabled=False, looping=False)
    t_up_m2_to_m1 = tm.add_trigger("09_Diff_Up_M2_to_M1", enabled=False, looping=False)

    def wire_difficulty_transition(
        trig,
        is_up: bool,
        stat_mode: str,
        from_lvl: int,
        to_lvl: int,
        to_disable: list,
        to_enable_after_2s: list,
        log_msg: str,
    ):
        bx1, by1, bx2, by2 = pad_up_box if is_up else pad_down_box
        safe_call(
            trig.new_condition.objects_in_area,
            source_player=PlayerId.ONE,
            object_list=UnitInfo.KING.ID,
            area_x1=bx1,
            area_y1=by1,
            area_x2=bx2,
            area_y2=by2,
            quantity=1,
        )
        safe_call(
            trig.new_condition.trigger_active,
            trigger_id=t_sanc_unlocked.trigger_id,
        )
        for d_tr in to_disable:
            safe_call(trig.new_effect.deactivate_trigger, trigger_id=d_tr.trigger_id)

        safe_call(trig.new_effect.deactivate_trigger, trigger_id=state_markers[from_lvl].trigger_id)
        safe_call(trig.new_effect.activate_trigger, trigger_id=state_markers[to_lvl].trigger_id)

        apply_king_reset_and_safe_stat_shift(trig, mode=stat_mode)
        send_highlight_chat(trig, "<RED>" if is_up else "<AQUA>", log_msg, flare_x=sanctuary_cx, flare_y=sanctuary_cy)

        t_relay = tm.add_trigger(f"{trig.name}_Relay2s", enabled=False, looping=False)
        safe_call(t_relay.new_condition.timer, timer=2)
        for e_tr in to_enable_after_2s:
            safe_call(t_relay.new_effect.activate_trigger, trigger_id=e_tr.trigger_id)
        safe_call(t_relay.new_effect.deactivate_trigger, trigger_id=t_relay.trigger_id)
        safe_call(trig.new_effect.activate_trigger, trigger_id=t_relay.trigger_id)

    wire_difficulty_transition(
        t_up_0_to_p1,
        is_up=True,
        stat_mode="pos_up",
        from_lvl=0,
        to_lvl=1,
        to_disable=[t_up_0_to_p1, t_down_0_to_m1],
        to_enable_after_2s=[t_up_p1_to_p2, t_down_p1_to_0],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA do POZIOMU +1 (TRUDNY: +25% wielkosci fal, +15 HP, +2 Ataku)!",
    )
    wire_difficulty_transition(
        t_up_p1_to_p2,
        is_up=True,
        stat_mode="pos_up",
        from_lvl=1,
        to_lvl=2,
        to_disable=[t_up_p1_to_p2, t_down_p1_to_0],
        to_enable_after_2s=[t_down_p2_to_p1],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA do POZIOMU +2 (EKSTREMALNY: +50% wielkosci fal, +30 HP, +4 Ataku)!",
    )
    wire_difficulty_transition(
        t_down_p2_to_p1,
        is_up=False,
        stat_mode="pos_down",
        from_lvl=2,
        to_lvl=1,
        to_disable=[t_down_p2_to_p1],
        to_enable_after_2s=[t_up_p1_to_p2, t_down_p1_to_0],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA z +2 do POZIOMU +1 (TRUDNY: +25% wielkosci fal)!",
    )
    wire_difficulty_transition(
        t_down_p1_to_0,
        is_up=False,
        stat_mode="pos_down",
        from_lvl=1,
        to_lvl=0,
        to_disable=[t_up_p1_to_p2, t_down_p1_to_0],
        to_enable_after_2s=[t_up_0_to_p1, t_down_0_to_m1],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA z +1 do POZIOMU 0 (DOMYSLNY: 100% wielkosci fal)!",
    )
    wire_difficulty_transition(
        t_down_0_to_m1,
        is_up=False,
        stat_mode="neg_down",
        from_lvl=0,
        to_lvl=-1,
        to_disable=[t_up_0_to_p1, t_down_0_to_m1],
        to_enable_after_2s=[t_up_m1_to_0, t_down_m1_to_m2],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA do POZIOMU -1 (LATWY: -20% wielkosci fal, -15% HP wroga)!",
    )
    wire_difficulty_transition(
        t_down_m1_to_m2,
        is_up=False,
        stat_mode="neg_down",
        from_lvl=-1,
        to_lvl=-2,
        to_disable=[t_up_m1_to_0, t_down_m1_to_m2],
        to_enable_after_2s=[t_up_m2_to_m1],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA do POZIOMU -2 (BARDZO LATWY: -40% wielkosci fal, -28% HP wroga)!",
    )
    wire_difficulty_transition(
        t_up_m2_to_m1,
        is_up=True,
        stat_mode="neg_up",
        from_lvl=-2,
        to_lvl=-1,
        to_disable=[t_up_m2_to_m1],
        to_enable_after_2s=[t_up_m1_to_0, t_down_m1_to_m2],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA z -2 do POZIOMU -1 (LATWY: -20% wielkosci fal)!",
    )
    wire_difficulty_transition(
        t_up_m1_to_0,
        is_up=True,
        stat_mode="neg_up",
        from_lvl=-1,
        to_lvl=0,
        to_disable=[t_up_m1_to_0, t_down_m1_to_m2],
        to_enable_after_2s=[t_up_0_to_p1, t_down_0_to_m1],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA z -1 do POZIOMU 0 (DOMYSLNY: 100% wielkosci fal)!",
    )

    t_obj_balance = tm.add_trigger("00_Obj_Balance_Info", enabled=True, looping=False)
    safe_call(t_obj_balance.new_condition.timer, timer=99999)
    set_as_objective(t_obj_balance, "Balans (6,150): Krol P1 Gora=Trudniej / Dol=Latwiej", order=75, is_header=True)

    # ==============================================================================
    # 10. LOGIKA 4 QUESTÓW (POJEDYNCZE TARGOWISKO W PRAWYM ROGU + 10-KRATKOWY SZLAK)
    # ==============================================================================
    t_obj_header_q = tm.add_trigger("00_Obj_Header_Quests", enabled=True, looping=False)
    safe_call(t_obj_header_q.new_condition.timer, timer=99999)
    set_as_objective(t_obj_header_q, "-- QUESTY POBOCZNE (STALE PERKI) --", order=100, is_header=True)

    t_q1 = tm.add_trigger("06_Quest1_Build_Trade_Wall_And_Pop", enabled=True, looping=False)
    set_as_objective(t_q1, "Q1 - Karawanseraj (Mur Handlowy, +30 Pop, +20% Eko)", order=99)
    safe_call(t_q1.new_condition.destroy_object, unit_object=q1_bldg.reference_id)

    # Usunięcie wież strażniczych wroga P5 wokół zniszczonego Karawanseraju
    safe_call(
        t_q1.new_effect.remove_object,
        source_player=PlayerId.FIVE,
        object_list_unit_id=BuildingInfo.GUARD_TOWER.ID,
        area_x1=145,
        area_y1=182,
        area_x2=165,
        area_y2=195,
    )

    for p_clear in human_players + [PlayerId.FIVE]:
        safe_call(
            t_q1.new_effect.teleport_object,
            source_player=p_clear,
            area_x1=105,
            area_y1=183,
            area_x2=199,
            area_y2=187,
            location_x=154,
            location_y=192,
        )

    # Ciągły Kamienny Mur Obronny z Basztami wzdłuż korytarza handlowego (y = 186, baszty y = 184)
    keep_x_positions = {115, 130, 145, 160, 175, 190}
    for wx in range(105, MAP_SIZE):
        if wx in keep_x_positions:
            safe_call(
                t_q1.new_effect.create_object,
                object_list_unit_id=BuildingInfo.KEEP.ID,
                source_player=PlayerId.FOUR,
                location_x=wx,
                location_y=184,
            )
        safe_call(
            t_q1.new_effect.create_object,
            object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
            source_player=PlayerId.FOUR,
            location_x=wx,
            location_y=186,
        )

    # POJEDYNCZE sojusznicze Targowisko w prawym rogu mapy na (195, 194)
    safe_call(
        t_q1.new_effect.create_object,
        object_list_unit_id=BuildingInfo.MARKET.ID,
        source_player=PlayerId.TWO,
        location_x=195,
        location_y=194,
    )

    for h_p in human_players:
        add_player_resource(t_q1, h_p, RES_BONUS_POP_CAP, BALANCE["q1_bonus_pop"])
        add_player_resource(t_q1, h_p, RES_GOLD, 500)
        for vil_id in [UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID]:
            safe_modify_attribute(t_q1, h_p, vil_id, ATTR_WORK_RATE, Operation.MULTIPLY, 1.20)
        safe_modify_attribute(t_q1, h_p, UnitInfo.TRADE_CART_EMPTY.ID, ATTR_MOVEMENT_SPEED, Operation.MULTIPLY, 1.25)
        safe_modify_attribute(t_q1, h_p, UnitInfo.TRADE_CART_FULL.ID, ATTR_MOVEMENT_SPEED, Operation.MULTIPLY, 1.25)
        for i in range(4):
            px, py = p_coords[h_p]
            safe_call(
                t_q1.new_effect.create_object,
                object_list_unit_id=UnitInfo.TRADE_CART_EMPTY.ID,
                source_player=h_p,
                location_x=px + i,
                location_y=py + 5,
            )

    add_enemy_combat_buff(t_q1, ai_players, hp_add=8, atk_add=1)
    deactivate_camp_handles(t_q1, camp_leash_handles["Quest1_Caravan"])

    send_highlight_chat(
        t_q1, "<GREEN>",
        "=== [Q1 UKONCZONY!] === Wybudowano KAMIENNY MUR HANDLOWY i postawiono sojuszniczy Market w prawym rogu (195, 194)! Wszyscy zyskuja +30 POPU, +20% Eko i 4 Wozy!",
        flare_x=195, flare_y=194,
    )

    # QUEST 2: Klif Artylerii
    t_q2 = tm.add_trigger("06_Quest2_Sniper_Cliff_Buff", enabled=True, looping=False)
    set_as_objective(t_q2, "Q2 - Klif Artylerii (+2 Zasiegu, +4 Ataku, Szybkosc)", order=98)
    safe_call(t_q2.new_condition.destroy_object, unit_object=q2_bldg.reference_id)
    research_techs(t_q2, human_players, [TECH_BALLISTICS, TECH_CHEMISTRY, TECH_SIEGE_ENGINEERS, TECH_THUMB_RING])

    for h_p in human_players:
        for r_id in PLAYER_RANGED_UNITS:
            safe_modify_attribute(t_q2, h_p, r_id, ATTR_MAXIMUM_RANGE, Operation.ADD, 2)
            safe_modify_attribute(t_q2, h_p, r_id, ATTR_SEARCH_RADIUS, Operation.ADD, 2)
            safe_modify_attribute(t_q2, h_p, r_id, ATTR_ATTACK, Operation.ADD, 4, armor_class=3)
        for c_id in PLAYER_CAVALRY_UNITS:
            safe_modify_attribute(t_q2, h_p, c_id, ATTR_MOVEMENT_SPEED, Operation.MULTIPLY, 1.12)
            safe_modify_attribute(t_q2, h_p, c_id, ATTR_ATTACK, Operation.ADD, 4, armor_class=4)

    add_enemy_combat_buff(t_q2, ai_players, hp_add=8, atk_add=1)
    deactivate_camp_handles(t_q2, camp_leash_handles["Quest2_SniperCliff"])

    send_highlight_chat(
        t_q2, "<GREEN>",
        "=== [Q2 UKONCZONY!] === Wszyscy otrzymuja Balistyke, Chemie, Siege Engineers, +2 Zasiegu i +4 Ataku dla strzelcow oraz +12% szybkosci i +4 Ataku dla jazdy!",
        flare_x=q2_pos[0], flare_y=q2_pos[1],
    )

    # QUEST 3: Skarbiec Krasnoludów
    t_q3_unlock = tm.add_trigger("06a_Quest3_Siege_Vault_Unlock", enabled=True, looping=False)
    set_as_objective(t_q3_unlock, "Q3 - Skarbiec (+20 Pop i Duzy Staly Dochod)", order=97)
    t_q3_trickle = tm.add_trigger("06b_Quest3_Passive_Resource_Trickle", enabled=False, looping=True)
    safe_call(t_q3_unlock.new_condition.destroy_object, unit_object=q3_bldg.reference_id)
    safe_call(t_q3_unlock.new_effect.activate_trigger, trigger_id=t_q3_trickle.trigger_id)
    for h_p in human_players:
        add_player_resource(t_q3_unlock, h_p, RES_BONUS_POP_CAP, BALANCE["q3_bonus_pop"])
        add_player_resource(t_q3_unlock, h_p, RES_GOLD, 600)
        add_player_resource(t_q3_unlock, h_p, RES_STONE, 300)

    add_enemy_combat_buff(t_q3_unlock, ai_players, hp_add=10, atk_add=1)
    deactivate_camp_handles(t_q3_unlock, camp_leash_handles["Quest3_SiegeVault"])

    send_highlight_chat(
        t_q3_unlock, "<GREEN>",
        "=== [Q3 UKONCZONY!] === Wszyscy zyskuja na stale +20 LIMITU POPULACJI oraz duzy dochod (+250 Zywn/Drewna, +200 Zlota i +40 Kamienia co minute)!",
        flare_x=q3_pos[0], flare_y=q3_pos[1],
    )

    safe_call(t_q3_trickle.new_condition.timer, timer=60)
    tr_res = BALANCE["quest3_trickle"]
    for h_p in human_players:
        add_player_resource(t_q3_trickle, h_p, RES_FOOD, tr_res["food"])
        add_player_resource(t_q3_trickle, h_p, RES_WOOD, tr_res["wood"])
        add_player_resource(t_q3_trickle, h_p, RES_GOLD, tr_res["gold"])
        add_player_resource(t_q3_trickle, h_p, RES_STONE, tr_res["stone"])

    # QUEST 4: Krwawy Ołtarz
    t_q4 = tm.add_trigger("06_Quest4_Blood_Altar_Super_Army", enabled=True, looping=False)
    set_as_objective(t_q4, "Q4 - Krwawy Oltarz (+30% HP Armii i +40% Produkcji)", order=96)
    safe_call(t_q4.new_condition.destroy_object, unit_object=q4_bldg.reference_id)
    safe_modify_attribute(t_q4, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_HIT_POINTS, Operation.SET, 120)

    all_player_combat_units = PLAYER_RANGED_UNITS + PLAYER_CAVALRY_UNITS + PLAYER_INFANTRY_UNITS
    for h_p in human_players:
        for u_id in all_player_combat_units:
            safe_modify_attribute(t_q4, h_p, u_id, ATTR_HIT_POINTS, Operation.MULTIPLY, 1.30)
            safe_modify_attribute(t_q4, h_p, u_id, ATTR_ARMOR, Operation.ADD, 2, armor_class=4)
            safe_modify_attribute(t_q4, h_p, u_id, ATTR_ARMOR, Operation.ADD, 2, armor_class=3)
        for b_id in PLAYER_PROD_BUILDINGS:
            safe_modify_attribute(t_q4, h_p, b_id, ATTR_WORK_RATE, Operation.MULTIPLY, 1.40)

    add_enemy_combat_buff(t_q4, ai_players, hp_add=10, atk_add=1)
    deactivate_camp_handles(t_q4, camp_leash_handles["Quest4_BloodAltar"])

    send_highlight_chat(
        t_q4, "<GREEN>",
        "=== [Q4 UKONCZONY!] === Wasze armie otrzymuja na stale +30% Max HP, +2/+2 Pancerza oraz +40% szybsza produkcje w budynkach wojskowych!",
        flare_x=q4_pos[0], flare_y=q4_pos[1],
    )

    # ==============================================================================
    # 11. ZNISZCZENIE 6 SETTLEMENTÓW (GRADACJA FURII GRADE 1-3)
    # ==============================================================================
    t_obj_header_s = tm.add_trigger("00_Obj_Header_Settlements", enabled=True, looping=False)
    safe_call(t_obj_header_s.new_condition.timer, timer=99999)
    set_as_objective(t_obj_header_s, "-- SETTLEMENTY HORDY --", order=90, is_header=True)

    settlement_defs = [
        ("G1_North", s_g1_north, "G1 - Polnocny (usuwa Berserkerow i Petardy)", 89, 1, 8, 1,
         [(UnitInfo.CAVALIER.ID, 8), (UnitInfo.PIKEMAN.ID, 10)], *s_coords["G1_North"]),
        ("G1_East",  s_g1_east,  "G1 - Wschodni (usuwa Huskarlow i Wielblady)", 88, 1, 8, 1,
         [(UnitInfo.CAVALIER.ID, 8), (UnitInfo.PIKEMAN.ID, 10)], *s_coords["G1_East"]),
        ("G2_Snipers", s_g2_snipers, "G2 - Akademia (usuwa Snajperow i Mozdzierze)", 87, 2, 12, 1,
         [(UnitInfo.CAVALIER.ID, 10), (UnitInfo.HALBERDIER.ID, 12)], *s_coords["G2_Snipers"]),
        ("G2_Mages",   s_g2_mages,   "G2 - Klasztor (usuwa Magow i Szakale)", 86, 2, 12, 1,
         [(UnitInfo.CAVALIER.ID, 10), (UnitInfo.HALBERDIER.ID, 12)], *s_coords["G2_Mages"]),
        ("G3_North", s_g3_north, "G3 - Cytadela Pln. (usuwa Slonie-Tanki Pln.)", 85, 3, 16, 2,
         [(ELITE_BATTLE_ELEPHANT_ID, 1), (UnitInfo.PALADIN.ID, 12), (UnitInfo.HALBERDIER.ID, 14)], *s_coords["G3_North"]),
        ("G3_East",  s_g3_east,  "G3 - Cytadela Wsch. (usuwa Slonie-Tanki Wsch.)", 84, 3, 16, 2,
         [(ELITE_BATTLE_ELEPHANT_ID, 1), (UnitInfo.PALADIN.ID, 12), (UnitInfo.HALBERDIER.ID, 14)], *s_coords["G3_East"]),
    ]

    for s_key, core_unit, obj_label, obj_order, grade, g_hp, g_atk, counter_comp, sx, sy in settlement_defs:
        t_destroy = tm.add_trigger(f"05_Settlement_Destroyed_{s_key}", enabled=True, looping=False)
        set_as_objective(t_destroy, obj_label, order=obj_order)
        safe_call(t_destroy.new_condition.destroy_object, unit_object=core_unit.reference_id)

        for tr_w in all_settlement_wave_triggers[s_key]:
            safe_call(t_destroy.new_effect.deactivate_trigger, trigger_id=tr_w.trigger_id)

        deactivate_camp_handles(t_destroy, camp_leash_handles[s_key])

        for h_p in human_players:
            add_player_resource(t_destroy, h_p, RES_GOLD, 600)
            add_player_resource(t_destroy, h_p, RES_FOOD, 600)

        add_enemy_combat_buff(t_destroy, ai_players, hp_add=g_hp, atk_add=g_atk)

        add_spawn_and_attack_effect(
            t_destroy, PlayerId.EIGHT,
            counter_comp,
            spawn_x=118, spawn_y=114, target_x=deep_target_center[0], target_y=deep_target_center[1],
        )

        send_highlight_chat(
            t_destroy, "<AQUA>",
            f"=== [SETTLEMENT ZNISZCZONY: {s_key} (Stopien {grade})] === Jego oddzialy znikaja z fal (+600 Zlota/Zywnosci), a pozostale obozy zyskuja +{g_hp} HP i +{g_atk} Ataku!",
            flare_x=sx, flare_y=sy,
        )

    # 12. Warunki Zwycięstwa i Porażki
    t_win = tm.add_trigger("07_Victory_All_6_Settlements_Destroyed", enabled=True, looping=False)
    for s_def in settlement_defs:
        core_unit = s_def[1]
        safe_call(t_win.new_condition.destroy_object, unit_object=core_unit.reference_id)
    for h_p in human_players:
        safe_call(t_win.new_effect.declare_victory, source_player=h_p, enabled=1)

    t_lose = tm.add_trigger("08_Defeat_Citadel_Lost", enabled=True, looping=False)
    safe_call(t_lose.new_condition.destroy_object, unit_object=allied_citadel.reference_id)
    for ai_p in ai_players:
        safe_call(t_lose.new_effect.declare_victory, source_player=ai_p, enabled=1)
