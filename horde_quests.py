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
    PLAYER_MOUNTED_RANGED_UNITS,
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

    # QUEST 2: Klif Artylerii
    t_q2 = tm.add_trigger("06_Quest2_Sniper_Cliff_Buff", enabled=True, looping=False)
    set_as_objective(t_q2, "Q2 - Klif Artylerii (+2 Zasiegu, +4 Ataku, Szybkosc)", order=98)
    safe_call(t_q2.new_condition.destroy_object, unit_object=q2_bldg.reference_id)
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

    add_enemy_combat_buff(t_q2, ai_players, hp_add=8, atk_add=1)
    deactivate_camp_handles(t_q2, camp_leash_handles["Quest2_SniperCliff"])

    send_highlight_chat(
        t_q2, "<GREEN>",
        "=== [Q2 UKONCZONY!] === Wszyscy otrzymuja Balistyke, Chemie, Siege Engineers, +2 Zasiegu i +4 Ataku strzelcow oraz +12% szybkosci i +4 Ataku jazdy! [Adaptacja Hordy: +8 HP, +1 Atak]",
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

    # QUEST 4: Krwawy Ołtarz
    t_q4 = tm.add_trigger("06_Quest4_Blood_Altar_Super_Army", enabled=True, looping=False)
    set_as_objective(t_q4, "Q4 - Krwawy Oltarz (+30% HP Armii i +40% Produkcji)", order=96)
    safe_call(t_q4.new_condition.destroy_object, unit_object=q4_bldg.reference_id)
    collapse_camp_buildings(t_q4, PlayerId.SEVEN, *q4_pos)
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
        "=== [Q4 UKONCZONY!] === Armie graczy otrzymuja +30% Max HP, +2/+2 Pancerza i +40% szybsza produkcje, a HP Arcymaga spada do 120! [Adaptacja Hordy: +10 HP, +1 Atak]",
        flare_x=q4_pos[0], flare_y=q4_pos[1],
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

    # 12. Warunki Zwycięstwa i Porażki
    t_win = tm.add_trigger("07_Victory_All_6_Settlements_Destroyed", enabled=True, looping=False)
    for s_def in settlement_defs:
        core_unit = s_def[2]
        safe_call(t_win.new_condition.destroy_object, unit_object=core_unit.reference_id)
    for h_p in human_players:
        safe_call(t_win.new_effect.declare_victory, source_player=h_p, enabled=1)

    t_lose = tm.add_trigger("08_Defeat_Citadel_Lost", enabled=True, looping=False)
    safe_call(t_lose.new_condition.destroy_object, unit_object=allied_citadel.reference_id)
    for ai_p in ai_players:
        safe_call(t_lose.new_effect.declare_victory, source_player=ai_p, enabled=1)

    # 13. Licznik Czasu do Następnej Fali (Crash-Safe w panelu Objectives)
    setup_wave_countdown_timer(tm)
