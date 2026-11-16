from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectState, ObjectType, Operation
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
    FINAL_BOSS_HERO_ID,
    FLARE_UNIT_ID,
    IMAM_UNIT_ID,
    MAP_REVEALER_ID,
    MAP_SIZE,
    PLAYER_CAVALRY_UNITS,
    PLAYER_INFANTRY_UNITS,
    PLAYER_MOUNTED_RANGED_UNITS,
    PLAYER_PROD_BUILDINGS,
    PLAYER_RANGED_UNITS,
    RELIC_ID,
    RES_BONUS_POP_CAP,
    RES_FOOD,
    RES_GOLD,
    RES_STONE,
    RES_WOOD,
    TECH_BALLISTICS,
    TECH_CHEMISTRY,
    TECH_SIEGE_ENGINEERS,
    TECH_THUMB_RING,
    get_wave_definitions,
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


def format_mm_ss(sec: int) -> str:
    return f"{sec // 60}:{sec % 60:02d}"


def setup_wave_countdown_timer(tm) -> None:
    """
    Stabilny, odporny na crashe licznik czasu do następnej fali w panelu Celów (Objectives).
    Używa statycznych banerów UI z `timer=999999` (nigdy nie ulegają przekreśleniu ani wykonaniu)
    przełączanych co 30s przez triggery zegarowe za pomocą `activate_trigger` / `deactivate_trigger`.
    Zero użycia niebezpiecznego efektu `display_timer`.
    """
    wave_defs = get_wave_definitions()
    milestones = [(w.wave_num, w.wave_sec) for w in wave_defs]

    ui_steps: list[tuple[int, str, str | None]] = [
        (0, "Zegar Fali: Fala 1/14 za 8:30 (uderzenie 8:30)", None),
    ]

    for t in range(30, 5040 + 1, 30):
        next_w = None
        for w_num, w_sec in milestones:
            if w_sec > t:
                next_w = (w_num, w_sec)
                break
        if next_w is not None:
            w_num, w_sec = next_w
            rem = w_sec - t
            label = f"Zegar Fali: Fala {w_num}/14 za {format_mm_ss(rem)} (uderzenie {format_mm_ss(w_sec)})"
            chat_warn = None
            if rem == 60:
                chat_warn = f"[ZEGAR FALI]: Pozostala 1 minuta do uderzenia Fali {w_num}/14 ({format_mm_ss(w_sec)})!"
            elif w_num == 1 and rem == 30:
                chat_warn = "[ZEGAR FALI]: Pozostalo 30 sekund do Pierwszej Fali Hordy (8:30)!"
            ui_steps.append((t, label, chat_warn))
        elif t < 5040:
            rem = 5040 - t
            label = f"Zegar Fali: Tryb Endless za {format_mm_ss(rem)} (od 84:00 co 5:30)"
            chat_warn = None
            if rem == 60:
                chat_warn = "[ZEGAR FALI]: Pozostala 1 minuta do pierwszego szturmu TRYBU ENDLESS (84:00)!"
            ui_steps.append((t, label, chat_warn))
        else:
            label = "Zegar Fali: TRYB ENDLESS AKTYWNY (szturm co 5:30)"
            ui_steps.append((t, label, None))

    ui_banners = []
    for idx, (t, label, _) in enumerate(ui_steps):
        t_ui = tm.add_trigger(f"00_Wave_Timer_UI_{idx:03d}_{t:04d}s", enabled=(idx == 0), looping=False)
        safe_call(t_ui.new_condition.timer, timer=999999)
        set_as_objective(t_ui, label, order=110, is_header=True)
        ui_banners.append(t_ui)

    for idx in range(1, len(ui_steps)):
        t, _, chat_warn = ui_steps[idx]
        t_tick = tm.add_trigger(f"00_Wave_Timer_Tick_{idx:03d}_{t:04d}s", enabled=True, looping=False)
        safe_call(t_tick.new_condition.timer, timer=t)
        safe_call(t_tick.new_effect.deactivate_trigger, trigger_id=ui_banners[idx - 1].trigger_id)
        safe_call(t_tick.new_effect.activate_trigger, trigger_id=ui_banners[idx].trigger_id)
        if chat_warn is not None:
            send_highlight_chat(t_tick, "<YELLOW>", chat_warn)


def setup_sanctuary_quests_and_victory(scenario, ctx: dict) -> None:
    ai_players = ctx["ai_players"]
    all_settlement_wave_triggers = ctx["all_settlement_wave_triggers"]
    allied_citadel = ctx["allied_citadel"]
    deep_target_center = ctx["deep_target_center"]
    deep_target_east = ctx["deep_target_east"]
    deep_target_north = ctx["deep_target_north"]
    endless_triggers = ctx["endless_triggers"]
    escalation_triggers = ctx["escalation_triggers"]
    human_players = ctx["human_players"]
    p2_qm_pads = ctx["p2_qm_pads"]
    p_coords = ctx["p_coords"]
    q1_bldg = ctx["q1_bldg"]
    q1_pos = ctx["q1_pos"]
    q2_bldg = ctx["q2_bldg"]
    q2_bombard_towers = ctx["q2_bombard_towers"]
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

    camp_building_ids = [
        BuildingInfo.CASTLE.ID,
        BuildingInfo.KEEP.ID,
        BuildingInfo.BOMBARD_TOWER.ID,
        BuildingInfo.GUARD_TOWER.ID,
        BuildingInfo.BARRACKS.ID,
        BuildingInfo.STABLE.ID,
        BuildingInfo.ARCHERY_RANGE.ID,
        BuildingInfo.SIEGE_WORKSHOP.ID,
        BuildingInfo.MONASTERY.ID,
        BuildingInfo.FORTIFIED_WALL.ID,
    ]

    def collapse_camp_buildings(trig, owner: PlayerId, cx: int, cy: int, radius: int = 14):
        ax1 = max(0, cx - radius)
        ay1 = max(0, cy - radius)
        ax2 = min(MAP_SIZE - 1, cx + radius)
        ay2 = min(MAP_SIZE - 1, cy + radius)
        for b_id in camp_building_ids:
            safe_call(
                trig.new_effect.kill_object,
                source_player=owner,
                object_list_unit_id=b_id,
                area_x1=ax1,
                area_y1=ay1,
                area_x2=ax2,
                area_y2=ay2,
            )

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

    # Pad GÓRNY (pad_up_box): P1->P2 (id+0) < 0->P1 (id+1) < M1->0 (id+2) < M2->M1 (id+3)
    t_up_p1_to_p2 = tm.add_trigger("09_Diff_Up_P1_to_P2", enabled=False, looping=False)
    t_up_0_to_p1 = tm.add_trigger("09_Diff_Up_0_to_P1", enabled=True, looping=False)
    t_up_m1_to_0 = tm.add_trigger("09_Diff_Up_M1_to_0", enabled=False, looping=False)
    t_up_m2_to_m1 = tm.add_trigger("09_Diff_Up_M2_to_M1", enabled=False, looping=False)

    # Pad DOLNY (pad_down_box): M1->M2 (id+4) < 0->M1 (id+5) < P1->0 (id+6) < P2->P1 (id+7)
    t_down_m1_to_m2 = tm.add_trigger("09_Diff_Down_M1_to_M2", enabled=False, looping=False)
    t_down_0_to_m1 = tm.add_trigger("09_Diff_Down_0_to_M1", enabled=True, looping=False)
    t_down_p1_to_0 = tm.add_trigger("09_Diff_Down_P1_to_0", enabled=False, looping=False)
    t_down_p2_to_p1 = tm.add_trigger("09_Diff_Down_P2_to_P1", enabled=False, looping=False)

    def wire_difficulty_transition(
        trig,
        is_up: bool,
        stat_mode: str,
        from_lvl: int,
        to_lvl: int,
        to_disable: list,
        to_enable: list,
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
        for d_tr in to_disable:
            safe_call(trig.new_effect.deactivate_trigger, trigger_id=d_tr.trigger_id)

        safe_call(trig.new_effect.deactivate_trigger, trigger_id=state_markers[from_lvl].trigger_id)
        safe_call(trig.new_effect.activate_trigger, trigger_id=state_markers[to_lvl].trigger_id)

        apply_king_reset_and_safe_stat_shift(trig, mode=stat_mode)
        send_highlight_chat(trig, "<RED>" if is_up else "<AQUA>", log_msg, flare_x=sanctuary_cx, flare_y=sanctuary_cy)

        for e_tr in to_enable:
            safe_call(trig.new_effect.activate_trigger, trigger_id=e_tr.trigger_id)

    wire_difficulty_transition(
        t_up_0_to_p1,
        is_up=True,
        stat_mode="pos_up",
        from_lvl=0,
        to_lvl=1,
        to_disable=[t_up_0_to_p1, t_down_0_to_m1],
        to_enable=[t_up_p1_to_p2, t_down_p1_to_0],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA do POZIOMU +1 (TRUDNY: +25% wielkosci fal, +15 HP, +2 Ataku)!",
    )
    wire_difficulty_transition(
        t_up_p1_to_p2,
        is_up=True,
        stat_mode="pos_up",
        from_lvl=1,
        to_lvl=2,
        to_disable=[t_up_p1_to_p2, t_down_p1_to_0],
        to_enable=[t_down_p2_to_p1],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA do POZIOMU +2 (EKSTREMALNY: +50% wielkosci fal, +30 HP, +4 Ataku)!",
    )
    wire_difficulty_transition(
        t_down_p2_to_p1,
        is_up=False,
        stat_mode="pos_down",
        from_lvl=2,
        to_lvl=1,
        to_disable=[t_down_p2_to_p1],
        to_enable=[t_up_p1_to_p2, t_down_p1_to_0],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA z +2 do POZIOMU +1 (TRUDNY: +25% wielkosci fal)!",
    )
    wire_difficulty_transition(
        t_down_p1_to_0,
        is_up=False,
        stat_mode="pos_down",
        from_lvl=1,
        to_lvl=0,
        to_disable=[t_up_p1_to_p2, t_down_p1_to_0],
        to_enable=[t_up_0_to_p1, t_down_0_to_m1],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA z +1 do POZIOMU 0 (DOMYSLNY: 100% wielkosci fal)!",
    )
    wire_difficulty_transition(
        t_down_0_to_m1,
        is_up=False,
        stat_mode="neg_down",
        from_lvl=0,
        to_lvl=-1,
        to_disable=[t_up_0_to_p1, t_down_0_to_m1],
        to_enable=[t_up_m1_to_0, t_down_m1_to_m2],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA do POZIOMU -1 (LATWY: -20% wielkosci fal, -15% HP wroga)!",
    )
    wire_difficulty_transition(
        t_down_m1_to_m2,
        is_up=False,
        stat_mode="neg_down",
        from_lvl=-1,
        to_lvl=-2,
        to_disable=[t_up_m1_to_0, t_down_m1_to_m2],
        to_enable=[t_up_m2_to_m1],
        log_msg="[LOG BALANSU]: Trudnosc ZMNIEJSZONA do POZIOMU -2 (BARDZO LATWY: -40% wielkosci fal, -30% HP wroga)!",
    )
    wire_difficulty_transition(
        t_up_m2_to_m1,
        is_up=True,
        stat_mode="neg_up",
        from_lvl=-2,
        to_lvl=-1,
        to_disable=[t_up_m2_to_m1],
        to_enable=[t_up_m1_to_0, t_down_m1_to_m2],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA z -2 do POZIOMU -1 (LATWY: -20% wielkosci fal)!",
    )
    wire_difficulty_transition(
        t_up_m1_to_0,
        is_up=True,
        stat_mode="neg_up",
        from_lvl=-1,
        to_lvl=0,
        to_disable=[t_up_m1_to_0, t_down_m1_to_m2],
        to_enable=[t_up_0_to_p1, t_down_0_to_m1],
        log_msg="[LOG BALANSU]: Trudnosc ZWIEKSZONA z -1 do POZIOMU 0 (DOMYSLNY: 100% wielkosci fal)!",
    )

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

    # Kamienny Mur Obronny z Basztami i 2-kratkowymi otworami wypadowymi (x=122..123 oraz x=170..171)
    keep_x_positions = {115, 122, 145, 160, 170, 190}
    sally_gap_x = {122, 123, 170, 171}
    for wx in range(105, MAP_SIZE):
        if wx in keep_x_positions:
            safe_call(
                t_q1.new_effect.create_object,
                object_list_unit_id=BuildingInfo.KEEP.ID,
                source_player=PlayerId.FOUR,
                location_x=wx,
                location_y=184,
            )
        if wx not in sally_gap_x:
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
        "=== [Q1 UKONCZONY!] === Wybudowano MUR HANDLOWY i postawiono Market P2 na (195, 194)! Wszyscy zyskuja +30 POPU, +20% Eko i 4 Wozy! [Adaptacja Hordy: +8 HP, +1 Atak]",
        flare_x=195, flare_y=194,
    )

    # QUEST 2: Klif Artylerii (Dwuetapowy: Baszty Artyleryjskie -> Uniwersytet)
    t_q2_shield = tm.add_trigger("06_Quest2_Shield_Loop", enabled=False, looping=True)
    safe_call(t_q2_shield.new_condition.timer, timer=2)
    safe_call(
        t_q2_shield.new_effect.heal_object,
        source_player=PlayerId.SIX,
        object_list_unit_id=BuildingInfo.UNIVERSITY.ID,
        area_x1=26,
        area_y1=28,
        area_x2=30,
        area_y2=34,
        quantity=400,
    )
    t_q2_garr_spawn = camp_leash_handles["Quest2_SniperCliff"][0]
    safe_call(t_q2_garr_spawn.new_effect.activate_trigger, trigger_id=t_q2_shield.trigger_id)

    t_q2_batteries = tm.add_trigger("06_Quest2_Batteries_Down", enabled=True, looping=False)
    for bt in q2_bombard_towers:
        safe_call(t_q2_batteries.new_condition.destroy_object, unit_object=bt.reference_id)
    safe_call(t_q2_batteries.new_effect.deactivate_trigger, trigger_id=t_q2_shield.trigger_id)
    send_highlight_chat(
        t_q2_batteries,
        "<YELLOW>",
        "[QUEST 2 - ETAP 1/2] Baszty Artyleryjskie zniszczone! Osłona Uniwersytetu opadła!",
        flare_x=q2_pos[0],
        flare_y=q2_pos[1],
    )

    t_q2 = tm.add_trigger("06_Quest2_Sniper_Cliff_Buff", enabled=True, looping=False)
    set_as_objective(t_q2, "Q2: Klif Artylerii (28,30) - zniszcz 2 Baszty Bombardowe, by zdjac tarcze Uniwersytetu", order=98)
    safe_call(t_q2.new_condition.destroy_object, unit_object=q2_bldg.reference_id)
    safe_call(t_q2.new_effect.deactivate_trigger, trigger_id=t_q2_shield.trigger_id)
    safe_call(t_q2.new_effect.deactivate_trigger, trigger_id=t_q2_batteries.trigger_id)
    collapse_camp_buildings(t_q2, PlayerId.SIX, *q2_pos)
    research_techs(t_q2, human_players, [TECH_BALLISTICS, TECH_CHEMISTRY, TECH_SIEGE_ENGINEERS, TECH_THUMB_RING])

    for h_p in human_players:
        for r_id in PLAYER_RANGED_UNITS:
            safe_modify_attribute(t_q2, h_p, r_id, ATTR_MAXIMUM_RANGE, Operation.ADD, 2)
            safe_modify_attribute(t_q2, h_p, r_id, ATTR_SEARCH_RADIUS, Operation.ADD, 2)
            safe_modify_attribute(t_q2, h_p, r_id, ATTR_ATTACK, Operation.ADD, 4, armor_class=3)
        for mr_id in PLAYER_MOUNTED_RANGED_UNITS:
            safe_modify_attribute(t_q2, h_p, mr_id, ATTR_MOVEMENT_SPEED, Operation.MULTIPLY, 1.12)
        for c_id in PLAYER_CAVALRY_UNITS:
            safe_modify_attribute(t_q2, h_p, c_id, ATTR_MOVEMENT_SPEED, Operation.MULTIPLY, 1.12)
            safe_modify_attribute(t_q2, h_p, c_id, ATTR_ATTACK, Operation.ADD, 4, armor_class=4)
        safe_call(
            t_q2.new_effect.create_object,
            source_player=h_p,
            object_list_unit_id=MAP_REVEALER_ID,
            location_x=s_coords["G2_Snipers"][0],
            location_y=s_coords["G2_Snipers"][1],
        )

    for bc_x in (27, 29):
        safe_call(
            t_q2.new_effect.create_object,
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.BOMBARD_CANNON.ID,
            location_x=bc_x,
            location_y=36,
        )

    add_enemy_combat_buff(t_q2, ai_players, hp_add=8, atk_add=1)
    deactivate_camp_handles(t_q2, camp_leash_handles["Quest2_SniperCliff"])

    send_highlight_chat(
        t_q2, "<GREEN>",
        "=== [Q2 UKONCZONY!] === Wszyscy otrzymuja Balistyke, Chemie, Siege Engineers, +2 Zasiegu i +4 Ataku strzelcow, +12% szybkosci i +4 Ataku jazdy, 2x Kolubryne dla Zielonego na (27, 36) i (29, 36) oraz wywiad nad Obozem Snajperow! [Adaptacja Hordy: +8 HP, +1 Atak]",
        flare_x=q2_pos[0], flare_y=q2_pos[1],
    )

    # QUEST 3: Skarbiec Krasnoludów
    t_q3_unlock = tm.add_trigger("06a_Quest3_Siege_Vault_Unlock", enabled=True, looping=False)
    set_as_objective(t_q3_unlock, "Q3 - Skarbiec (+20 Pop i Duzy Staly Dochod)", order=97)
    t_q3_trickle = tm.add_trigger("06b_Quest3_Passive_Resource_Trickle", enabled=False, looping=True)
    safe_call(t_q3_unlock.new_condition.destroy_object, unit_object=q3_bldg.reference_id)
    collapse_camp_buildings(t_q3_unlock, PlayerId.EIGHT, *q3_pos)
    safe_call(t_q3_unlock.new_effect.activate_trigger, trigger_id=t_q3_trickle.trigger_id)
    for h_p in human_players:
        add_player_resource(t_q3_unlock, h_p, RES_BONUS_POP_CAP, BALANCE["q3_bonus_pop"])
        add_player_resource(t_q3_unlock, h_p, RES_GOLD, 600)
        add_player_resource(t_q3_unlock, h_p, RES_STONE, 300)

    add_enemy_combat_buff(t_q3_unlock, ai_players, hp_add=10, atk_add=1)
    deactivate_camp_handles(t_q3_unlock, camp_leash_handles["Quest3_SiegeVault"])

    send_highlight_chat(
        t_q3_unlock, "<GREEN>",
        "=== [Q3 UKONCZONY!] === Kazdy gracz zyskuje +20 POPU oraz staly dochod (+250F, +250W, +200G i +40S co minute)! [Adaptacja Hordy: +10 HP, +1 Atak]",
        flare_x=q3_pos[0], flare_y=q3_pos[1],
    )

    safe_call(t_q3_trickle.new_condition.timer, timer=60)
    tr_res = BALANCE["quest3_trickle"]
    for h_p in human_players:
        add_player_resource(t_q3_trickle, h_p, RES_FOOD, tr_res["food"])
        add_player_resource(t_q3_trickle, h_p, RES_WOOD, tr_res["wood"])
        add_player_resource(t_q3_trickle, h_p, RES_GOLD, tr_res["gold"])
        add_player_resource(t_q3_trickle, h_p, RES_STONE, tr_res["stone"])

    # QUEST 4: Krwawy Ołtarz (Dwuetapowy: Zburzenie Ołtarza -> 30s Krwawy Odwet Zakonu -> Klasztor w Twierdzy)
    t_q4_s1 = tm.add_trigger("06_Quest4_Stage1_Altar_Broken", enabled=True, looping=False)
    t_q4_s2 = tm.add_trigger("06_Quest4_Stage2_Ritual_Complete", enabled=False, looping=False)

    set_as_objective(t_q4_s1, "Q4 (1/2) - Zburz Krwawy Oltarz i przetrwaj Odwet Zakonu", order=96)
    safe_call(t_q4_s1.new_condition.destroy_object, unit_object=q4_bldg.reference_id)
    collapse_camp_buildings(t_q4_s1, PlayerId.SEVEN, *q4_pos)
    deactivate_camp_handles(t_q4_s1, camp_leash_handles["Quest4_BloodAltar"])
    safe_call(
        t_q4_s1.new_effect.create_object,
        source_player=PlayerId.GAIA,
        object_list_unit_id=RELIC_ID,
        location_x=105,
        location_y=20,
    )
    send_highlight_chat(
        t_q4_s1,
        "<ORANGE>",
        "[QUEST 4 - ETAP 1/2] Krwawy Ołtarz zburzony! Utrzymajcie wzgórze przez 30 sekund przed Krwawym Odwetem Zakonu!",
        flare_x=105,
        flare_y=20,
    )
    add_spawn_and_attack_effect(
        t_q4_s1,
        PlayerId.SEVEN,
        [
            (UnitInfo.HEAVY_CAMEL_RIDER.ID, 6),
            (UnitInfo.ELITE_MAMELUKE.ID, 6),
            (UnitInfo.ELITE_STEPPE_LANCER.ID, 4),
        ],
        spawn_x=105,
        spawn_y=34,
        target_x=105,
        target_y=20,
    )
    safe_call(t_q4_s1.new_effect.activate_trigger, trigger_id=t_q4_s2.trigger_id)

    set_as_objective(t_q4_s2, "Q4 (2/2) - Utrzymaj wzgorze (105, 20) przez 30s!", order=96)
    safe_call(t_q4_s2.new_condition.timer, timer=30)
    safe_modify_attribute(t_q4_s2, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_HIT_POINTS, Operation.SET, 120)

    all_player_combat_units = PLAYER_RANGED_UNITS + PLAYER_CAVALRY_UNITS + PLAYER_INFANTRY_UNITS
    for h_p in human_players:
        for u_id in all_player_combat_units:
            safe_modify_attribute(t_q4_s2, h_p, u_id, ATTR_HIT_POINTS, Operation.MULTIPLY, 1.30)
            safe_modify_attribute(t_q4_s2, h_p, u_id, ATTR_ARMOR, Operation.ADD, 2, armor_class=4)
            safe_modify_attribute(t_q4_s2, h_p, u_id, ATTR_ARMOR, Operation.ADD, 2, armor_class=3)
        for b_id in PLAYER_PROD_BUILDINGS:
            safe_modify_attribute(t_q4_s2, h_p, b_id, ATTR_WORK_RATE, Operation.MULTIPLY, 1.40)

    add_enemy_combat_buff(t_q4_s2, ai_players, hp_add=10, atk_add=1)
    for h_p in human_players:
        safe_call(
            t_q4_s2.new_effect.kill_object,
            source_player=h_p,
            object_type=ObjectType.BUILDING,
            area_x1=56,
            area_y1=150,
            area_x2=60,
            area_y2=154,
        )
    safe_call(
        t_q4_s2.new_effect.create_object,
        source_player=PlayerId.ONE,
        object_list_unit_id=BuildingInfo.MONASTERY.ID,
        location_x=58,
        location_y=152,
    )
    for monk_x in (57, 59):
        safe_call(
            t_q4_s2.new_effect.create_object,
            source_player=PlayerId.ONE,
            object_list_unit_id=UnitInfo.MONK.ID,
            location_x=monk_x,
            location_y=155,
        )

    send_highlight_chat(
        t_q4_s2, "<GREEN>",
        "=== [Q4 UKONCZONY!] === Armie graczy otrzymuja +30% Max HP, +2/+2 Pancerza i +40% szybsza produkcje, HP Arcymaga spada do 120, a na placu Twierdzy (58, 152) powstaje Klasztor P1 z 2 Mnichami na (57, 155) i (59, 155)! [Adaptacja Hordy: +10 HP, +1 Atak]",
        flare_x=58, flare_y=152,
    )

    # ==============================================================================
    # 10b. AKTYWNA ROLA GRACZA 2: POSTERUNEK KWATERMISTRZA TWIERDZY (20, 162)
    # ==============================================================================
    qm_cx, qm_cy = p2_qm_pads["center"]
    mil_x, mil_y = p2_qm_pads["mil_pad"]
    eco_x, eco_y = p2_qm_pads["eco_pad"]

    t_qm_ready = tm.add_trigger("State_P2_QM_Ready", enabled=True, looping=False)
    safe_call(t_qm_ready.new_condition.timer, timer=999999)

    t_qm_cooldown = tm.add_trigger("06d_P2_QM_Cooldown_240s", enabled=False, looping=True)
    t_qm_mil = tm.add_trigger("06d_P2_QM_Military_Drop", enabled=False, looping=True)
    t_qm_eco = tm.add_trigger("06d_P2_QM_Eco_Drop", enabled=False, looping=True)

    safe_call(t_qm_cooldown.new_condition.timer, timer=240)
    safe_call(t_qm_cooldown.new_effect.activate_trigger, trigger_id=t_qm_ready.trigger_id)
    safe_call(t_qm_cooldown.new_effect.activate_trigger, trigger_id=t_qm_mil.trigger_id)
    safe_call(t_qm_cooldown.new_effect.activate_trigger, trigger_id=t_qm_eco.trigger_id)
    send_highlight_chat(
        t_qm_cooldown,
        "<AQUA>",
        "[KWATERMISTRZ P2] Rozkazy Kwatermistrza (20, 162) są ponownie gotowe do użycia!",
        flare_x=20,
        flare_y=162,
    )
    safe_call(t_qm_cooldown.new_effect.deactivate_trigger, trigger_id=t_qm_cooldown.trigger_id)

    safe_call(
        t_qm_mil.new_condition.objects_in_area,
        source_player=PlayerId.TWO,
        object_list=UnitInfo.KING.ID,
        area_x1=mil_x - 2,
        area_y1=mil_y - 2,
        area_x2=mil_x + 2,
        area_y2=mil_y + 2,
        quantity=1,
    )
    safe_call(
        t_qm_mil.new_effect.teleport_object,
        source_player=PlayerId.TWO,
        object_list_unit_id=UnitInfo.KING.ID,
        area_x1=mil_x - 2,
        area_y1=mil_y - 2,
        area_x2=mil_x + 2,
        area_y2=mil_y + 2,
        location_x=qm_cx,
        location_y=qm_cy,
    )
    for conq_x, conq_y in [(52, 149), (53, 149), (55, 149), (56, 149)]:
        safe_call(
            t_qm_mil.new_effect.create_object,
            source_player=PlayerId.TWO,
            object_list_unit_id=UnitInfo.ELITE_CONQUISTADOR.ID,
            location_x=conq_x,
            location_y=conq_y,
        )
    for bc_x, bc_y in [(53, 150), (55, 150)]:
        safe_call(
            t_qm_mil.new_effect.create_object,
            source_player=PlayerId.TWO,
            object_list_unit_id=UnitInfo.BOMBARD_CANNON.ID,
            location_x=bc_x,
            location_y=bc_y,
        )
    send_highlight_chat(
        t_qm_mil,
        "<RED>",
        "[KWATERMISTRZ P2] Czerwony wezwał Gwardię Najemną (4x Elitarny Konkwistador + 2x Kolubryna) na dziedziniec wokół (54, 149)! Odnowienie: 4 min.",
        flare_x=54,
        flare_y=149,
    )
    safe_call(t_qm_mil.new_effect.deactivate_trigger, trigger_id=t_qm_ready.trigger_id)
    safe_call(t_qm_mil.new_effect.deactivate_trigger, trigger_id=t_qm_mil.trigger_id)
    safe_call(t_qm_mil.new_effect.deactivate_trigger, trigger_id=t_qm_eco.trigger_id)
    safe_call(t_qm_mil.new_effect.activate_trigger, trigger_id=t_qm_cooldown.trigger_id)

    safe_call(
        t_qm_eco.new_condition.objects_in_area,
        source_player=PlayerId.TWO,
        object_list=UnitInfo.KING.ID,
        area_x1=eco_x - 2,
        area_y1=eco_y - 2,
        area_x2=eco_x + 2,
        area_y2=eco_y + 2,
        quantity=1,
    )
    safe_call(
        t_qm_eco.new_effect.teleport_object,
        source_player=PlayerId.TWO,
        object_list_unit_id=UnitInfo.KING.ID,
        area_x1=eco_x - 2,
        area_y1=eco_y - 2,
        area_x2=eco_x + 2,
        area_y2=eco_y + 2,
        location_x=qm_cx,
        location_y=qm_cy,
    )
    for h_p in human_players:
        add_player_resource(t_qm_eco, h_p, RES_FOOD, 300)
        add_player_resource(t_qm_eco, h_p, RES_WOOD, 300)
        add_player_resource(t_qm_eco, h_p, RES_GOLD, 300)
        safe_call(
            t_qm_eco.new_effect.heal_object,
            source_player=h_p,
            object_type=ObjectType.BUILDING,
            area_x1=0,
            area_y1=95,
            area_x2=110,
            area_y2=199,
            quantity=500,
        )
    safe_call(
        t_qm_eco.new_effect.heal_object,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.BUILDING,
        area_x1=105,
        area_y1=183,
        area_x2=199,
        area_y2=187,
        quantity=500,
    )
    send_highlight_chat(
        t_qm_eco,
        "<YELLOW>",
        "[KWATERMISTRZ P2] Czerwony wysłał Konwój Zaopatrzeniowy (+300 Żywności/Drewna/Złota dla każdego i naprawa murów Twierdzy oraz Q1)! Odnowienie: 4 min.",
        flare_x=54,
        flare_y=149,
    )
    safe_call(t_qm_eco.new_effect.deactivate_trigger, trigger_id=t_qm_ready.trigger_id)
    safe_call(t_qm_eco.new_effect.deactivate_trigger, trigger_id=t_qm_mil.trigger_id)
    safe_call(t_qm_eco.new_effect.deactivate_trigger, trigger_id=t_qm_eco.trigger_id)
    safe_call(t_qm_eco.new_effect.activate_trigger, trigger_id=t_qm_cooldown.trigger_id)

    # ==============================================================================
    # 10c. ZDARZENIA EKSPLORACYJNE NA MAPIE (MAP PoI) I BRAMKA 10:00
    # ==============================================================================
    poi1_triggers = [
        tm.add_trigger(f"06e_PoI1_Engineers_P{p_idx}", enabled=False, looping=False)
        for p_idx in range(1, 5)
    ]
    for h_p, t_poi in zip(human_players, poi1_triggers):
        safe_call(
            t_poi.new_condition.objects_in_area,
            source_player=h_p,
            area_x1=26,
            area_y1=72,
            area_x2=34,
            area_y2=80,
            quantity=1,
        )
        for other_t in poi1_triggers:
            safe_call(t_poi.new_effect.deactivate_trigger, trigger_id=other_t.trigger_id)
        for ram_x, ram_y in [(29, 76), (31, 76)]:
            safe_call(
                t_poi.new_effect.create_object,
                source_player=h_p,
                object_list_unit_id=UnitInfo.CAPPED_RAM.ID,
                location_x=ram_x,
                location_y=ram_y,
            )
        for pet_x, pet_y in [(29, 77), (31, 77)]:
            safe_call(
                t_poi.new_effect.create_object,
                source_player=h_p,
                object_list_unit_id=UnitInfo.PETARD.ID,
                location_x=pet_x,
                location_y=pet_y,
            )
        for ally_p in human_players:
            add_player_resource(t_poi, ally_p, RES_WOOD, 200)
            add_player_resource(t_poi, ally_p, RES_GOLD, 200)
        send_highlight_chat(
            t_poi,
            "<GREEN>",
            f"[EKSPLORACJA - OBÓZ INŻYNIERÓW (30, 76)] Gracz P{h_p.value} przejął sprzęt oblężniczy (2x Taran + 2x Petarda) oraz +200 Drewna i +200 Złota dla całego Sojuszu!",
            flare_x=30,
            flare_y=76,
        )

    t_unlock_qm_poi1 = tm.add_trigger("06d_Unlock_Quartermaster_And_PoI1_10m", enabled=True, looping=False)
    safe_call(t_unlock_qm_poi1.new_condition.timer, timer=600)
    safe_call(t_unlock_qm_poi1.new_effect.activate_trigger, trigger_id=t_qm_mil.trigger_id)
    safe_call(t_unlock_qm_poi1.new_effect.activate_trigger, trigger_id=t_qm_eco.trigger_id)
    for t_poi1 in poi1_triggers:
        safe_call(t_unlock_qm_poi1.new_effect.activate_trigger, trigger_id=t_poi1.trigger_id)
    send_highlight_chat(
        t_unlock_qm_poi1,
        "<AQUA>",
        "[KWATERMISTRZ P2] Posterunek Kwatermistrza (20, 162) oraz Obóz Inżynierów (30, 76) są już dostępne!",
        flare_x=20,
        flare_y=162,
    )

    poi2_triggers = [
        tm.add_trigger(f"06e_PoI2_Caravan_P{p_idx}", enabled=True, looping=False)
        for p_idx in range(1, 5)
    ]
    for h_p, t_poi in zip(human_players, poi2_triggers):
        safe_call(
            t_poi.new_condition.objects_in_area,
            source_player=h_p,
            area_x1=124,
            area_y1=170,
            area_x2=132,
            area_y2=178,
            quantity=1,
        )
        for other_t in poi2_triggers:
            safe_call(t_poi.new_effect.deactivate_trigger, trigger_id=other_t.trigger_id)
        for ally_p in human_players:
            add_player_resource(t_poi, ally_p, RES_FOOD, 350)
            add_player_resource(t_poi, ally_p, RES_GOLD, 350)
            safe_call(
                t_poi.new_effect.create_object,
                source_player=ally_p,
                object_list_unit_id=MAP_REVEALER_ID,
                location_x=q1_pos[0],
                location_y=q1_pos[1],
            )
        send_highlight_chat(
            t_poi,
            "<YELLOW>",
            f"[EKSPLORACJA - ZAGINIONA KARAWANA (128, 174)] Gracz P{h_p.value} odnalazł wozy z łupem (+350 Żywności i +350 Złota dla każdego) oraz mapy ujawniające Obóz Karawany Q1 (154, 190)!",
            flare_x=128,
            flare_y=174,
        )

    # ==============================================================================
    # 11. ZNISZCZENIE 6 SETTLEMENTÓW (GRADACJA FURII GRADE 1-3 + KIERUNKOWE ODWETY)
    # ==============================================================================
    t_obj_header_s = tm.add_trigger("00_Obj_Header_Settlements", enabled=True, looping=False)
    safe_call(t_obj_header_s.new_condition.timer, timer=99999)
    set_as_objective(t_obj_header_s, "-- SETTLEMENTY HORDY --", order=90, is_header=True)

    settlement_defs = [
        ("G1_North", PlayerId.FIVE, s_g1_north, "G1 - Polnocny (usuwa Berserkerow i Petardy)", 89, 1, 700, 5, 0,
         [(UnitInfo.CAVALIER.ID, 8), (UnitInfo.PIKEMAN.ID, 10)], *s_coords["G1_North"],
         48, 86, *deep_target_north),
        ("G1_East",  PlayerId.FIVE, s_g1_east,  "G1 - Wschodni (usuwa Huskarlow i Wielblady)", 88, 1, 700, 5, 0,
         [(UnitInfo.CAVALIER.ID, 8), (UnitInfo.PIKEMAN.ID, 10)], *s_coords["G1_East"],
         117, 178, *deep_target_east),
        ("G2_Snipers", PlayerId.SIX, s_g2_snipers, "G2 - Akademia (usuwa Snajperow, Mozdzierze i Saperow)", 87, 2, 1000, 10, 1,
         [(UnitInfo.CAVALIER.ID, 10), (UnitInfo.HALBERDIER.ID, 12)], *s_coords["G2_Snipers"],
         48, 86, *deep_target_north),
        ("G2_Mages",   PlayerId.SEVEN, s_g2_mages,   "G2 - Klasztor (usuwa Magow i Szakale)", 86, 2, 1000, 10, 1,
         [(UnitInfo.CAVALIER.ID, 10), (UnitInfo.HALBERDIER.ID, 12)], *s_coords["G2_Mages"],
         116, 114, *deep_target_center),
        ("G3_North", PlayerId.EIGHT, s_g3_north, "G3 - Cytadela Pln. (usuwa Slonie-Tanki Pln.)", 85, 3, 1500, 15, 2,
         [(ELITE_BATTLE_ELEPHANT_ID, 1), (UnitInfo.PALADIN.ID, 12), (UnitInfo.HALBERDIER.ID, 14)], *s_coords["G3_North"],
         116, 114, *deep_target_center),
        ("G3_East",  PlayerId.EIGHT, s_g3_east,  "G3 - Cytadela Wsch. (usuwa Slonie Wsch. i Rajdy Handlowe)", 84, 3, 1500, 15, 2,
         [(ELITE_BATTLE_ELEPHANT_ID, 1), (UnitInfo.PALADIN.ID, 12), (UnitInfo.HALBERDIER.ID, 14)], *s_coords["G3_East"],
         117, 178, *deep_target_east),
    ]

    for s_key, s_owner, core_unit, obj_label, obj_order, grade, reward_res, g_hp, g_atk, counter_comp, sx, sy, ret_sx, ret_sy, ret_tx, ret_ty in settlement_defs:
        t_destroy = tm.add_trigger(f"05_Settlement_Destroyed_{s_key}", enabled=True, looping=False)
        set_as_objective(t_destroy, obj_label, order=obj_order)
        safe_call(t_destroy.new_condition.destroy_object, unit_object=core_unit.reference_id)
        collapse_camp_buildings(t_destroy, s_owner, sx, sy)

        for tr_w in all_settlement_wave_triggers[s_key]:
            safe_call(t_destroy.new_effect.deactivate_trigger, trigger_id=tr_w.trigger_id)

        deactivate_camp_handles(t_destroy, camp_leash_handles[s_key])

        for h_p in human_players:
            add_player_resource(t_destroy, h_p, RES_GOLD, reward_res)
            add_player_resource(t_destroy, h_p, RES_FOOD, reward_res)

        add_enemy_combat_buff(t_destroy, ai_players, hp_add=g_hp, atk_add=g_atk)

        add_spawn_and_attack_effect(
            t_destroy, PlayerId.EIGHT,
            counter_comp,
            spawn_x=ret_sx, spawn_y=ret_sy, target_x=ret_tx, target_y=ret_ty,
        )

        send_highlight_chat(
            t_destroy, "<AQUA>",
            f"=== [SETTLEMENT ZNISZCZONY: {s_key} (Stopien {grade})] === Jego oddzialy znikaja z fal (+{reward_res} Zlota/Zywnosci), a pozostale obozy zyskuja +{g_hp} HP i +{g_atk} Ataku!",
            flare_x=sx, flare_y=sy,
        )

    # 12. Warunki Zwycięstwa (Czterofazowy Finałowy Boss) i Porażki
    t_boss_warn = tm.add_trigger("07a_All_Settlements_Destroyed_Boss_Warning", enabled=True, looping=False)
    t_boss_spawn = tm.add_trigger("07b_Spawn_Final_Boss_Wave", enabled=False, looping=False)
    t_boss_confirm = tm.add_trigger("07c_Confirm_Boss_Spawned", enabled=False, looping=False)
    t_win = tm.add_trigger("07d_Victory_Final_Boss_Defeated", enabled=False, looping=False)

    for s_def in settlement_defs:
        core_unit = s_def[2]
        safe_call(t_boss_warn.new_condition.destroy_object, unit_object=core_unit.reference_id)

    for esc_t in escalation_triggers:
        safe_call(t_boss_warn.new_effect.deactivate_trigger, trigger_id=esc_t.trigger_id)
    for end_t in endless_triggers:
        safe_call(t_boss_warn.new_effect.deactivate_trigger, trigger_id=end_t.trigger_id)

    for h_p in human_players:
        safe_call(
            t_boss_warn.new_effect.kill_object,
            source_player=h_p,
            object_type=ObjectType.BUILDING,
            area_x1=110,
            area_y1=108,
            area_x2=124,
            area_y2=128,
        )

    for rx, ry in [(104, 114), (116, 114)]:
        for h_p in human_players:
            safe_call(
                t_boss_warn.new_effect.create_object,
                source_player=h_p,
                object_list_unit_id=MAP_REVEALER_ID,
                location_x=rx,
                location_y=ry,
            )

    for h_p in human_players:
        safe_call(
            t_boss_warn.new_effect.play_sound,
            source_player=h_p,
            location_x=116,
            location_y=114,
            global_sound=1,
            sound_name="Play_Tribute_Received",
        )

    send_highlight_chat(
        t_boss_warn,
        "<RED>",
        "[FINAŁOWY ALARM] Wszystkie 6 Twierdz Hordy runęło! Macie 45 sekund na wycofanie armii pod Bramę Centralną (104, 114) — nadciąga Wielki Chan Subotai (3500 HP)!",
        flare_x=116,
        flare_y=114,
    )
    safe_call(t_boss_warn.new_effect.activate_trigger, trigger_id=t_boss_spawn.trigger_id)

    safe_call(t_boss_spawn.new_condition.timer, timer=45)
    add_spawn_and_attack_effect(
        t_boss_spawn,
        PlayerId.EIGHT,
        [
            (FINAL_BOSS_HERO_ID, 1),
            (ELITE_BATTLE_ELEPHANT_ID, 4),
            (UnitInfo.PALADIN.ID, 14),
            (UnitInfo.SIEGE_RAM.ID, 3),
        ],
        spawn_x=116,
        spawn_y=114,
        target_x=54,
        target_y=146,
    )
    add_spawn_and_attack_effect(
        t_boss_spawn,
        PlayerId.SEVEN,
        [(IMAM_UNIT_ID, 2)],
        spawn_x=118,
        spawn_y=122,
        target_x=54,
        target_y=146,
    )
    send_highlight_chat(
        t_boss_spawn,
        "<RED>",
        "[OSTATNI SZTURM] Wielki Chan Subotai (3500 HP) z gwardią na (116, 114) i Arcymagami na (118, 122) rusza na Bramę Centralną! Zgładźcie Chana, aby zwyciężyć!",
        flare_x=116,
        flare_y=114,
    )
    safe_call(t_boss_spawn.new_effect.activate_trigger, trigger_id=t_boss_confirm.trigger_id)

    safe_call(
        t_boss_confirm.new_condition.objects_in_area,
        area_x1=0,
        area_y1=0,
        area_x2=MAP_SIZE - 1,
        area_y2=MAP_SIZE - 1,
        source_player=PlayerId.EIGHT,
        object_list=FINAL_BOSS_HERO_ID,
        object_state=ObjectState.ALIVE,
        quantity=1,
    )
    safe_call(t_boss_confirm.new_effect.activate_trigger, trigger_id=t_win.trigger_id)

    set_as_objective(t_win, "FINAL: Zgladz Wielkiego Chana Subotaia (3500 HP) przed Brama Centralna!", order=99)
    safe_call(t_win.new_condition.timer, timer=5)
    safe_call(
        t_win.new_condition.objects_in_area,
        area_x1=0,
        area_y1=0,
        area_x2=MAP_SIZE - 1,
        area_y2=MAP_SIZE - 1,
        source_player=PlayerId.EIGHT,
        object_list=FINAL_BOSS_HERO_ID,
        object_state=ObjectState.ALIVE,
        quantity=1,
        inverted=True,
    )
    send_highlight_chat(
        t_win,
        "<GREEN>",
        "=== [ZWYCIĘSTWO!] === Wielki Chan Subotai padł przed Bramą Centralną! Ostatni Szturm Hordy został złamany!",
        flare_x=104,
        flare_y=114,
    )
    for h_p in human_players:
        safe_call(
            t_win.new_effect.create_object,
            source_player=h_p,
            object_list_unit_id=FLARE_UNIT_ID,
            location_x=54,
            location_y=146,
        )
        safe_call(t_win.new_effect.declare_victory, source_player=h_p, enabled=1)

    t_lose = tm.add_trigger("08_Defeat_Citadel_Lost", enabled=True, looping=False)
    safe_call(t_lose.new_condition.destroy_object, unit_object=allied_citadel.reference_id)
    for ai_p in ai_players:
        safe_call(t_lose.new_effect.declare_victory, source_player=ai_p, enabled=1)

    # 13. Licznik Czasu do Następnej Fali (Crash-Safe w panelu Objectives)
    setup_wave_countdown_timer(tm)
