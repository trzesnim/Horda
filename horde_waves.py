import inspect

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo

from horde_config import (
    ATTR_ARMOR,
    ATTR_ATTACK,
    ATTR_ATTACK_RELOAD_TIME,
    ATTR_BLAST_ATTACK_LEVEL,
    ATTR_BLAST_WIDTH,
    ATTR_HERO_STATUS,
    ATTR_HIT_POINTS,
    ATTR_LINE_OF_SIGHT,
    ATTR_MAXIMUM_RANGE,
    ATTR_MINIMUM_RANGE,
    ATTR_MOVEMENT_SPEED,
    ATTR_REGENERATION_RATE,
    ATTR_SEARCH_RADIUS,
    ATTR_WORK_RATE,
    BALANCE,
    ELITE_BATTLE_ELEPHANT_ID,
    ELITE_BERSERK_ID,
    ENEMY_UNIT_REGISTRY,
    FEITORIA_ID,
    FLAMING_CAMEL_ID,
    FLARE_UNIT_ID,
    FORTIFIED_PALISADE_ID,
    HUSSAR_ID,
    IMAM_UNIT_ID,
    MAP_REVEALER_ID,
    MAP_SIZE,
    PETARD_ID,
    RES_BONUS_POP_CAP,
    SIEGE_ONAGER_ID,
    TECH_BALLISTICS,
    TECH_BLAST_FURNACE,
    TECH_BLOODLINES,
    TECH_BODKIN_ARROW,
    TECH_BRACER,
    TECH_CARTOGRAPHY,
    TECH_CASTLE_AGE,
    TECH_CHAIN_BARDING,
    TECH_CHAIN_MAIL,
    TECH_CHEMISTRY,
    TECH_FAITH,
    TECH_FEUDAL_AGE,
    TECH_FLETCHING,
    TECH_FORGING,
    TECH_HUSBANDRY,
    TECH_IMPERIAL_AGE,
    TECH_IRON_CASTING,
    TECH_PLATE_BARDING,
    TECH_PLATE_MAIL,
    TECH_SCALE_BARDING,
    TECH_SCALE_MAIL,
    TECH_SIEGE_ENGINEERS,
    TECH_SQUIRES,
    WaveDefinition,
    get_wave_definitions,
)


def safe_call(func, **kwargs):
    sig = inspect.signature(func)
    valid_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
    return func(**valid_kwargs)


def safe_modify_attribute(trigger, source_player, unit_id, attr_id, operation, val, armor_class=None):
    fn = trigger.new_effect.modify_attribute
    base_kwargs = {
        "source_player": source_player,
        "object_list_unit_id": unit_id,
        "object_attributes": attr_id,
        "operation": operation,
    }
    if armor_class is not None:
        try:
            return safe_call(
                fn,
                **base_kwargs,
                armour_attack_class=armor_class,
                armour_attack_quantity=int(val),
            )
        except (ValueError, TypeError):
            return safe_call(
                fn,
                **base_kwargs,
                armour_attack_class=armor_class,
                quantity=val,
            )
    return safe_call(fn, **base_kwargs, quantity=val)


def add_enemy_combat_buff(trigger, ai_players: list[PlayerId], hp_add: int, atk_add: int):
    for ai_p in ai_players:
        for spec in ENEMY_UNIT_REGISTRY.values():
            if spec.scales_hp and hp_add > 0:
                safe_modify_attribute(trigger, ai_p, spec.unit_id, ATTR_HIT_POINTS, Operation.ADD, hp_add)
            if spec.attack_class is not None and atk_add > 0:
                safe_modify_attribute(
                    trigger, ai_p, spec.unit_id, ATTR_ATTACK, Operation.ADD, atk_add, armor_class=spec.attack_class
                )


def set_as_objective(trigger, text: str, order: int, is_header: bool = False):
    if hasattr(trigger, "short_description"):
        trigger.short_description = text
    if hasattr(trigger, "display_on_screen"):
        trigger.display_on_screen = 1
    if hasattr(trigger, "description_order"):
        trigger.description_order = order
    if is_header and hasattr(trigger, "header"):
        trigger.header = 1


def send_highlight_chat(trigger, color_tag: str, message: str, flare_x: int | None = None, flare_y: int | None = None):
    for h_p in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR]:
        safe_call(
            trigger.new_effect.send_chat,
            source_player=h_p,
            message=f"{color_tag}{message}",
        )
        if flare_x is not None and flare_y is not None:
            if hasattr(trigger.new_effect, "flare"):
                safe_call(
                    trigger.new_effect.flare,
                    source_player=h_p,
                    location_x=flare_x,
                    location_y=flare_y,
                )
            safe_call(
                trigger.new_effect.create_object,
                object_list_unit_id=FLARE_UNIT_ID,
                source_player=h_p,
                location_x=flare_x,
                location_y=flare_y,
            )


def add_player_resource(trigger, player: PlayerId, resource_id: int, amount: int):
    safe_call(
        trigger.new_effect.modify_resource,
        source_player=player,
        tribute_list=resource_id,
        operation=Operation.ADD,
        quantity=amount,
    )


def research_techs(trigger, players: list[PlayerId], tech_ids: list[int]):
    for p in players:
        for t_id in tech_ids:
            safe_call(
                trigger.new_effect.research_technology,
                source_player=p,
                technology=t_id,
                force_research_technology=1,
            )


def add_guarded_camp_with_leash(tm, enable_parent_trigger, name: str, ai_player: PlayerId, cx: int, cy: int,
                                units_spec: list[tuple[int, int]]):
    detect_radius = 15
    x1, y1 = max(0, cx - detect_radius), max(0, cy - detect_radius)
    x2, y2 = min(MAP_SIZE - 1, cx + detect_radius), min(MAP_SIZE - 1, cy + detect_radius)

    t_spawn = tm.add_trigger(f"Garrison_Spawn_{name}", enabled=False, looping=False)
    add_spawn_and_attack_effect(t_spawn, ai_player, units_spec, spawn_x=cx, spawn_y=cy + 3, target_x=cx, target_y=cy)

    t_leash = tm.add_trigger(f"Garrison_Leash_{name}", enabled=False, looping=True)
    safe_call(t_leash.new_condition.timer, timer=3)
    ring_inner = 9
    ring_outer = 20
    leash_strips = [
        (cx - ring_outer, cy - ring_outer, cx + ring_outer, cy - ring_inner),
        (cx - ring_outer, cy + ring_inner, cx + ring_outer, cy + ring_outer),
        (cx - ring_outer, cy - ring_inner, cx - ring_inner, cy + ring_inner),
        (cx + ring_inner, cy - ring_inner, cx + ring_outer, cy + ring_inner),
    ]
    for sx1, sy1, sx2, sy2 in leash_strips:
        safe_call(
            t_leash.new_effect.attack_move,
            source_player=ai_player,
            area_x1=max(0, sx1),
            area_y1=max(0, sy1),
            area_x2=min(MAP_SIZE - 1, sx2),
            area_y2=min(MAP_SIZE - 1, sy2),
            location_x=cx,
            location_y=cy,
        )
    safe_call(t_spawn.new_effect.activate_trigger, trigger_id=t_leash.trigger_id)

    detect_triggers = []
    for h_p in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR]:
        req_qty = 2 if h_p == PlayerId.ONE else 1
        t_detect = tm.add_trigger(f"Garrison_Detect_{name}_P{h_p.value}", enabled=False, looping=False)
        safe_call(
            t_detect.new_condition.objects_in_area,
            source_player=h_p,
            area_x1=x1, area_y1=y1, area_x2=x2, area_y2=y2,
            quantity=req_qty,
        )
        safe_call(t_detect.new_effect.activate_trigger, trigger_id=t_spawn.trigger_id)
        safe_call(enable_parent_trigger.new_effect.activate_trigger, trigger_id=t_detect.trigger_id)
        detect_triggers.append(t_detect)

    return (t_spawn, t_leash, detect_triggers)


def add_spawn_and_attack_effect(trigger, ai_player: PlayerId, units_spec: list[tuple[int, int]],
                                spawn_x: int, spawn_y: int, target_x: int, target_y: int,
                                ignore_frontline_move_only: bool = False):
    idx = 0
    for unit_id, count in units_spec:
        for _ in range(count):
            dx = (idx % 6) - 3
            dy = (idx // 6) - 3
            safe_call(
                trigger.new_effect.create_object,
                object_list_unit_id=unit_id,
                source_player=ai_player,
                location_x=spawn_x + dx,
                location_y=spawn_y + dy,
            )
            idx += 1

    order_fn = trigger.new_effect.attack_move
    if ignore_frontline_move_only and hasattr(trigger.new_effect, "move"):
        order_fn = trigger.new_effect.move

    safe_call(
        order_fn,
        source_player=ai_player,
        area_x1=max(0, spawn_x - 8),
        area_y1=max(0, spawn_y - 8),
        area_x2=min(MAP_SIZE - 1, spawn_x + 8),
        area_y2=min(MAP_SIZE - 1, spawn_y + 8),
        location_x=target_x,
        location_y=target_y,
    )


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


def setup_init_aura_and_waves(scenario, ctx: dict) -> None:
    ai_players = ctx["ai_players"]
    allied_citadel = ctx["allied_citadel"]
    balance_king = ctx["balance_king"]
    east_breach_trees = ctx["east_breach_trees"]
    gate_center = ctx["gate_center"]
    gate_east = ctx["gate_east"]
    gate_north = ctx["gate_north"]
    human_players = ctx["human_players"]
    north_breach_trees = ctx["north_breach_trees"]
    q1_bldg = ctx["q1_bldg"]
    q1_pos = ctx["q1_pos"]
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
    tm = ctx["tm"]

    t_init = tm.add_trigger("01_Init_Diplomacy_And_Cartography", enabled=True, looping=False)

    research_techs(t_init, human_players, [TECH_CARTOGRAPHY])
    safe_modify_attribute(t_init, PlayerId.ONE, MAP_REVEALER_ID, ATTR_LINE_OF_SIGHT, Operation.SET, 4)

    safe_modify_attribute(t_init, PlayerId.ONE, UnitInfo.KING.ID, ATTR_HIT_POINTS, Operation.SET, 9999)
    safe_modify_attribute(t_init, PlayerId.ONE, UnitInfo.KING.ID, ATTR_REGENERATION_RATE, Operation.SET, 5000)

    safe_modify_attribute(t_init, PlayerId.TWO, FEITORIA_ID, ATTR_HIT_POINTS, Operation.ADD, 3000)
    add_player_resource(t_init, PlayerId.TWO, RES_BONUS_POP_CAP, 20)

    for h1 in human_players:
        safe_modify_attribute(t_init, h1, FORTIFIED_PALISADE_ID, ATTR_HIT_POINTS, Operation.ADD, 400)
        for h2 in human_players:
            if h1 != h2:
                safe_call(t_init.new_effect.change_diplomacy, source_player=h1, target_player=h2, diplomacy=DiplomacyState.ALLY)
        for ai in ai_players:
            safe_call(t_init.new_effect.change_diplomacy, source_player=h1, target_player=ai, diplomacy=DiplomacyState.ENEMY)
            safe_call(t_init.new_effect.change_diplomacy, source_player=ai, target_player=h1, diplomacy=DiplomacyState.ENEMY)

    for ai1 in ai_players:
        for ai2 in ai_players:
            if ai1 != ai2:
                safe_call(t_init.new_effect.change_diplomacy, source_player=ai1, target_player=ai2, diplomacy=DiplomacyState.ALLY)

    research_techs(t_init, ai_players, [TECH_FEUDAL_AGE, TECH_CASTLE_AGE, TECH_IMPERIAL_AGE])
    research_techs(t_init, [PlayerId.EIGHT], [TECH_FAITH])

    t_ai_smith_feudal = tm.add_trigger("01d_AI_Techs_Feudal_8m30s", enabled=True, looping=False)
    safe_call(t_ai_smith_feudal.new_condition.timer, timer=510)
    research_techs(t_ai_smith_feudal, [PlayerId.FIVE], [TECH_SCALE_MAIL])
    research_techs(t_ai_smith_feudal, [PlayerId.SIX], [TECH_FLETCHING])
    research_techs(t_ai_smith_feudal, [PlayerId.SEVEN], [TECH_FORGING, TECH_BLOODLINES])
    research_techs(t_ai_smith_feudal, [PlayerId.EIGHT], [TECH_FORGING, TECH_SCALE_BARDING])
    safe_modify_attribute(
        t_ai_smith_feudal, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, Operation.SET, BALANCE["tank_unit_atk"], armor_class=4
    )

    t_ai_smith_castle = tm.add_trigger("01e_AI_Techs_Castle_18m", enabled=True, looping=False)
    safe_call(t_ai_smith_castle.new_condition.timer, timer=1080)
    research_techs(t_ai_smith_castle, [PlayerId.FIVE], [TECH_CHAIN_MAIL, TECH_SQUIRES])
    research_techs(t_ai_smith_castle, [PlayerId.SIX], [TECH_BODKIN_ARROW, TECH_BALLISTICS])
    research_techs(t_ai_smith_castle, [PlayerId.SEVEN], [TECH_IRON_CASTING, TECH_HUSBANDRY])
    research_techs(t_ai_smith_castle, [PlayerId.EIGHT], [TECH_IRON_CASTING, TECH_CHAIN_BARDING])
    safe_modify_attribute(
        t_ai_smith_castle, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, Operation.SET, BALANCE["tank_unit_atk"], armor_class=4
    )

    t_ai_smith_imp = tm.add_trigger("01f_AI_Techs_Imperial_34m30s", enabled=True, looping=False)
    safe_call(t_ai_smith_imp.new_condition.timer, timer=2070)
    research_techs(t_ai_smith_imp, [PlayerId.FIVE], [TECH_PLATE_MAIL])
    research_techs(t_ai_smith_imp, [PlayerId.SIX], [TECH_BRACER, TECH_CHEMISTRY, TECH_SIEGE_ENGINEERS])
    research_techs(t_ai_smith_imp, [PlayerId.SEVEN], [TECH_BLAST_FURNACE])
    research_techs(t_ai_smith_imp, [PlayerId.EIGHT], [TECH_BLAST_FURNACE, TECH_PLATE_BARDING, TECH_SIEGE_ENGINEERS])
    safe_modify_attribute(
        t_ai_smith_imp, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, Operation.SET, BALANCE["tank_unit_atk"], armor_class=4
    )

    building_labels = [
        (balance_king, "Inzynier Balansu (Gora = Trudniej, Dol = Latwiej)"),
        (allied_citadel, "Cytadela Sojuszu P2 (Serce Twierdzy - Broncie jej!)"),
        (q1_bldg, "Q1: Karawanseraj (Buduje Mur Handlowy, +30 Pop, +20% Eko)"),
        (q2_bldg, "Q2: Klif Artylerii (+2 Zasiegu, +4 Ataku, Szybkosc)"),
        (q3_bldg, "Q3: Skarbiec (+20 Pop i Duzy Staly Dochod)"),
        (q4_bldg, "Q4: Krwawy Oltarz (+30% HP Armii i +40% Produkcji)"),
        (s_g1_north, "G1 Polnocny (Berserkerzy i Petardy)"),
        (s_g1_east,  "G1 Wschodni (Huskarlowie i Wielblady)"),
        (s_g2_snipers, "G2 Akademia (Snajperzy i Mozdzierze)"),
        (s_g2_mages,   "G2 Klasztor (Arcymagowie i Szakale)"),
        (s_g3_north, "G3 Cytadela Pln. (Zelazne Slonie-Tanki)"),
        (s_g3_east,  "G3 Cytadela Wsch. (Slonie-Tanki i Artyleria)"),
    ]
    for b_unit, label_text in building_labels:
        safe_call(
            t_init.new_effect.change_object_name,
            selected_object_ids=[b_unit.reference_id],
            message=label_text,
        )

    send_highlight_chat(
        t_init, "<YELLOW>",
        "=== KRONIKI RUBIEZY v6.2 === Inzynier Balansu P1 powrocil na (6, 150) w zachodnim lesie! Lewy dolny rog mapy (x=3..23, y=177..198) jest czysty pod Targowiska graczy!",
    )

    t_mutate = tm.add_trigger("01b_Apply_Specialized_Unit_Archetypes", enabled=True, looping=False)
    safe_call(t_mutate.new_condition.timer, timer=3)

    for ai_p in ai_players:
        for monk_id in [IMAM_UNIT_ID, UnitInfo.MISSIONARY.ID, UnitInfo.MONK.ID]:
            safe_modify_attribute(t_mutate, ai_p, monk_id, ATTR_MAXIMUM_RANGE, Operation.SET, 0)
            safe_modify_attribute(t_mutate, ai_p, monk_id, ATTR_WORK_RATE, Operation.SET, 0)

    # 1. TARAN-ŻÓŁW / ŻELAZNY SŁOŃ (Tank P8)
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_HIT_POINTS, Operation.SET, BALANCE["tank_hp"])
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_HERO_STATUS, Operation.SET, 1)
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_MOVEMENT_SPEED, Operation.SET, BALANCE["tank_speed"])
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, Operation.SET, BALANCE["tank_unit_atk"], armor_class=4)
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, Operation.ADD, BALANCE["tank_bldg_bonus"], armor_class=11)
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ATTACK, Operation.ADD, BALANCE["tank_bldg_bonus"], armor_class=21)
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ARMOR, Operation.SET, BALANCE["tank_melee_armor"], armor_class=4)
    safe_modify_attribute(t_mutate, PlayerId.EIGHT, ELITE_BATTLE_ELEPHANT_ID, ATTR_ARMOR, Operation.SET, BALANCE["tank_pierce_armor"], armor_class=3)

    # 2. SZAKAL DYWERSYJNY (Eco-Raider Huzar P7)
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, HUSSAR_ID, ATTR_HIT_POINTS, Operation.SET, BALANCE["raider_hp"])
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, HUSSAR_ID, ATTR_MOVEMENT_SPEED, Operation.SET, BALANCE["raider_speed"])
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, HUSSAR_ID, ATTR_ATTACK, Operation.SET, BALANCE["raider_atk"], armor_class=4)
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, HUSSAR_ID, ATTR_ARMOR, Operation.SET, BALANCE["raider_pierce_armor"], armor_class=3)
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, HUSSAR_ID, ATTR_ARMOR, Operation.SET, 0, armor_class=4)

    # 3. ARCYMAG TARCZY (Imam P7)
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_HIT_POINTS, Operation.SET, BALANCE["mage_hp"])
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_HERO_STATUS, Operation.SET, 1)
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_REGENERATION_RATE, Operation.SET, BALANCE["mage_regen_per_min"])
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_MOVEMENT_SPEED, Operation.SET, BALANCE["mage_speed"])
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_ARMOR, Operation.SET, BALANCE["mage_pierce_armor"], armor_class=3)
    safe_modify_attribute(t_mutate, PlayerId.SEVEN, IMAM_UNIT_ID, ATTR_ARMOR, Operation.SET, BALANCE["mage_melee_armor"], armor_class=4)

    # 4. MOŹDZIERZ OBLĘŻNICZY (Siege Onager P6)
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_HIT_POINTS, Operation.SET, BALANCE["mortar_hp"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_HERO_STATUS, Operation.SET, 1)
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_MAXIMUM_RANGE, Operation.SET, BALANCE["mortar_range"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_MINIMUM_RANGE, Operation.SET, BALANCE["mortar_min_range"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_SEARCH_RADIUS, Operation.SET, 23)
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_LINE_OF_SIGHT, Operation.SET, 23)
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_ATTACK_RELOAD_TIME, Operation.SET, BALANCE["mortar_reload"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_BLAST_WIDTH, Operation.SET, BALANCE["mortar_blast_width"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_BLAST_ATTACK_LEVEL, Operation.SET, 2)
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_MOVEMENT_SPEED, Operation.SET, BALANCE["mortar_speed"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, SIEGE_ONAGER_ID, ATTR_ATTACK, Operation.ADD, BALANCE["mortar_bonus_atk"], armor_class=4)

    # 5. SNAJPER IMPERIALNY (Elitarny Janczar P6)
    safe_modify_attribute(t_mutate, PlayerId.SIX, UnitInfo.ELITE_JANISSARY.ID, ATTR_HIT_POINTS, Operation.SET, BALANCE["sniper_hp"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, UnitInfo.ELITE_JANISSARY.ID, ATTR_HERO_STATUS, Operation.SET, 1)
    safe_modify_attribute(t_mutate, PlayerId.SIX, UnitInfo.ELITE_JANISSARY.ID, ATTR_MAXIMUM_RANGE, Operation.SET, BALANCE["sniper_range"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, UnitInfo.ELITE_JANISSARY.ID, ATTR_SEARCH_RADIUS, Operation.SET, 21)
    safe_modify_attribute(t_mutate, PlayerId.SIX, UnitInfo.ELITE_JANISSARY.ID, ATTR_LINE_OF_SIGHT, Operation.SET, 21)
    safe_modify_attribute(t_mutate, PlayerId.SIX, UnitInfo.ELITE_JANISSARY.ID, ATTR_ATTACK_RELOAD_TIME, Operation.SET, BALANCE["sniper_reload"])
    safe_modify_attribute(t_mutate, PlayerId.SIX, UnitInfo.ELITE_JANISSARY.ID, ATTR_ATTACK, Operation.ADD, BALANCE["sniper_bonus_atk"], armor_class=3)

    # 6. BERSERKERZY I KAMIKAZE (P5)
    for kamikaze_id in [PETARD_ID, FLAMING_CAMEL_ID]:
        safe_modify_attribute(t_mutate, PlayerId.FIVE, kamikaze_id, ATTR_HIT_POINTS, Operation.SET, BALANCE["kamikaze_hp"])
        safe_modify_attribute(t_mutate, PlayerId.FIVE, kamikaze_id, ATTR_MOVEMENT_SPEED, Operation.SET, BALANCE["kamikaze_speed"])
        safe_modify_attribute(t_mutate, PlayerId.FIVE, kamikaze_id, ATTR_BLAST_WIDTH, Operation.SET, BALANCE["kamikaze_blast_width"])
        safe_modify_attribute(t_mutate, PlayerId.FIVE, kamikaze_id, ATTR_ATTACK, Operation.ADD, BALANCE["kamikaze_bonus_atk"], armor_class=4)
        safe_modify_attribute(t_mutate, PlayerId.FIVE, kamikaze_id, ATTR_ARMOR, Operation.SET, 0, armor_class=3)

    safe_modify_attribute(t_mutate, PlayerId.FIVE, ELITE_BERSERK_ID, ATTR_HIT_POINTS, Operation.SET, BALANCE["berserk_hp"])
    safe_modify_attribute(t_mutate, PlayerId.FIVE, ELITE_BERSERK_ID, ATTR_MOVEMENT_SPEED, Operation.SET, BALANCE["berserk_speed"])
    safe_modify_attribute(t_mutate, PlayerId.FIVE, ELITE_BERSERK_ID, ATTR_ATTACK, Operation.ADD, BALANCE["berserk_bonus_atk"], armor_class=4)
    safe_modify_attribute(t_mutate, PlayerId.FIVE, ELITE_BERSERK_ID, ATTR_ARMOR, Operation.SET, 0, armor_class=3)

    t_arm_garrisons = tm.add_trigger("01c_Arm_Garrison_Detectors_At_4s", enabled=True, looping=False)
    safe_call(t_arm_garrisons.new_condition.timer, timer=4)

    camp_leash_handles = {
        "Quest1_Caravan": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Quest1_Caravan", PlayerId.FIVE, *q1_pos,
            units_spec=[(UnitInfo.STEPPE_LANCER.ID, 12), (UnitInfo.CROSSBOWMAN.ID, 10), (ELITE_BERSERK_ID, 4)],
        ),
        "Quest2_SniperCliff": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Quest2_SniperCliff", PlayerId.SIX, *q2_pos,
            units_spec=[(UnitInfo.ELITE_JANISSARY.ID, 6), (SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 14)],
        ),
        "Quest3_SiegeVault": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Quest3_SiegeVault", PlayerId.EIGHT, *q3_pos,
            units_spec=[(UnitInfo.HALBERDIER.ID, 18), (ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.ARBALESTER.ID, 14)],
        ),
        "Quest4_BloodAltar": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Quest4_BloodAltar", PlayerId.EIGHT, *q4_pos,
            units_spec=[(UnitInfo.PALADIN.ID, 14), (ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.HALBERDIER.ID, 12)],
        ),
        "G1_North": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Settle_G1_North", PlayerId.FIVE, *s_coords["G1_North"],
            units_spec=[(UnitInfo.PIKEMAN.ID, 14), (ELITE_BERSERK_ID, 6), (UnitInfo.CROSSBOWMAN.ID, 8)],
        ),
        "G1_East": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Settle_G1_East", PlayerId.FIVE, *s_coords["G1_East"],
            units_spec=[(UnitInfo.HUSKARL.ID, 12), (UnitInfo.PIKEMAN.ID, 10), (FLAMING_CAMEL_ID, 3)],
        ),
        "G2_Snipers": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Settle_G2_Snipers", PlayerId.SIX, *s_coords["G2_Snipers"],
            units_spec=[(UnitInfo.ELITE_JANISSARY.ID, 7), (SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 16)],
        ),
        "G2_Mages": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Settle_G2_Mages", PlayerId.SEVEN, *s_coords["G2_Mages"],
            units_spec=[(UnitInfo.CAVALIER.ID, 14), (HUSSAR_ID, 8), (IMAM_UNIT_ID, 1)],
        ),
        "G3_North": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Settle_G3_North", PlayerId.EIGHT, *s_coords["G3_North"],
            units_spec=[(ELITE_BATTLE_ELEPHANT_ID, 3), (UnitInfo.HALBERDIER.ID, 20), (UnitInfo.PALADIN.ID, 12)],
        ),
        "G3_East": add_guarded_camp_with_leash(
            tm, t_arm_garrisons, "Settle_G3_East", PlayerId.EIGHT, *s_coords["G3_East"],
            units_spec=[(ELITE_BATTLE_ELEPHANT_ID, 3), (UnitInfo.ARBALESTER.ID, 20), (SIEGE_ONAGER_ID, 2)],
        ),
    }

    # ==============================================================================
    # 6. GLOBALNA AURA MAGÓW (AUTOMAT DWUSTANOWY NA REJESTRZE - ETAP 5 - BUG-05)
    # ==============================================================================
    r_local = BALANCE["mage_local_radius"]
    mx1, my1 = max(0, gate_center[0] - r_local), max(0, gate_center[1] - r_local)
    mx2, my2 = min(MAP_SIZE - 1, gate_center[0] + r_local), min(MAP_SIZE - 1, gate_center[1] + r_local)

    global_shielded_units = [spec.unit_id for spec in ENEMY_UNIT_REGISTRY.values() if spec.receives_mage_shield]

    t_shield_on = tm.add_trigger("02a_Mage_Global_Horde_Shield_On", enabled=True, looping=False)
    t_mage_heal_pulse = tm.add_trigger("02b_Mage_AoE_Heal_Pulse_3s", enabled=False, looping=True)
    t_mage_beacon = tm.add_trigger("02c_Mage_Visual_Flare_Beacon_8s", enabled=False, looping=True)
    t_shield_off = tm.add_trigger("02d_Mage_Global_Horde_Shield_Off", enabled=False, looping=False)

    safe_call(
        t_shield_on.new_condition.objects_in_area,
        source_player=PlayerId.SEVEN,
        object_list=IMAM_UNIT_ID,
        area_x1=mx1, area_y1=my1, area_x2=mx2, area_y2=my2,
        quantity=1,
    )
    for ai_p in ai_players:
        for u_id in global_shielded_units:
            safe_modify_attribute(t_shield_on, ai_p, u_id, ATTR_ARMOR, Operation.ADD, BALANCE["mage_shield_armor"], armor_class=3)
            safe_modify_attribute(t_shield_on, ai_p, u_id, ATTR_ARMOR, Operation.ADD, BALANCE["mage_shield_armor"], armor_class=4)
    safe_call(t_shield_on.new_effect.deactivate_trigger, trigger_id=t_shield_on.trigger_id)
    safe_call(t_shield_on.new_effect.activate_trigger, trigger_id=t_mage_heal_pulse.trigger_id)
    safe_call(t_shield_on.new_effect.activate_trigger, trigger_id=t_mage_beacon.trigger_id)
    safe_call(t_shield_on.new_effect.activate_trigger, trigger_id=t_shield_off.trigger_id)
    send_highlight_chat(
        t_shield_on, "<PURPLE>",
        "[GLOBALNA AURA MAGA - 25 KRATEK]: Arcymag (240 HP, regen 5 HP/s, flara!) dal +30/+30 Pancerza i leczenie WSZYSTKIM frakcjom Hordy (P5-P8)! Skupcie na nim ogien!",
        flare_x=114, flare_y=114,
    )

    safe_call(t_mage_heal_pulse.new_condition.timer, timer=3)
    safe_call(
        t_mage_heal_pulse.new_condition.objects_in_area,
        source_player=PlayerId.SEVEN,
        object_list=IMAM_UNIT_ID,
        area_x1=mx1, area_y1=my1, area_x2=mx2, area_y2=my2,
        quantity=1,
    )
    for ai_p in ai_players:
        safe_call(
            t_mage_heal_pulse.new_effect.heal_object,
            source_player=ai_p,
            area_x1=mx1, area_y1=my1, area_x2=mx2, area_y2=my2,
            quantity=BALANCE["mage_aoe_heal_3s"],
        )

    safe_call(t_mage_beacon.new_condition.timer, timer=8)
    safe_call(
        t_mage_beacon.new_condition.objects_in_area,
        source_player=PlayerId.SEVEN,
        object_list=IMAM_UNIT_ID,
        area_x1=mx1, area_y1=my1, area_x2=mx2, area_y2=my2,
        quantity=1,
    )
    send_highlight_chat(
        t_mage_beacon, "<PURPLE>",
        "[FLARA - ARCYMAG TARCZY]: Arcymag (P7 - 240 HP, regen 5 HP/s) w kregu pochodni przed Brama Centralna leczy i utrzymuje +30 Pancerza na Hordzie!",
        flare_x=114, flare_y=114,
    )

    safe_call(
        t_shield_off.new_condition.objects_in_area,
        source_player=PlayerId.SEVEN,
        object_list=IMAM_UNIT_ID,
        area_x1=mx1, area_y1=my1, area_x2=mx2, area_y2=my2,
        quantity=1,
        inverted=1,
    )
    for ai_p in ai_players:
        for u_id in global_shielded_units:
            safe_modify_attribute(t_shield_off, ai_p, u_id, ATTR_ARMOR, Operation.SUBTRACT, BALANCE["mage_shield_armor"], armor_class=3)
            safe_modify_attribute(t_shield_off, ai_p, u_id, ATTR_ARMOR, Operation.SUBTRACT, BALANCE["mage_shield_armor"], armor_class=4)
    safe_call(t_shield_off.new_effect.deactivate_trigger, trigger_id=t_mage_heal_pulse.trigger_id)
    safe_call(t_shield_off.new_effect.deactivate_trigger, trigger_id=t_mage_beacon.trigger_id)
    safe_call(t_shield_off.new_effect.deactivate_trigger, trigger_id=t_shield_off.trigger_id)
    safe_call(t_shield_off.new_effect.activate_trigger, trigger_id=t_shield_on.trigger_id)
    send_highlight_chat(
        t_shield_off, "<GREEN>",
        "[BARIERA PRZELAMANA]: Arcymag zabity! Wszystkie armie Hordy (P5, P6, P7, P8) traca +30 Pancerza i leczenie!",
    )

    t_push_inside = tm.add_trigger("02e_Push_Gate_Units_Deep_Into_Base", enabled=True, looping=True)
    safe_call(t_push_inside.new_condition.timer, timer=15)
    gate_push_zones = [
        (gate_north[0] - 8, gate_north[1] - 4, gate_north[0] + 8, gate_north[1] + 8, 48, 138),
        (gate_center[0] - 8, gate_center[1] - 8, gate_center[0] + 4, gate_center[1] + 8, 54, 146),
        (gate_east[0] - 8, gate_east[1] - 8, gate_east[0] + 4, gate_east[1] + 8, 68, 162),
        (74, 94, 82, 108, 68, 130),
        (98, 135, 112, 144, 68, 146),
    ]
    for ai_p in [PlayerId.FIVE, PlayerId.SIX, PlayerId.EIGHT]:
        for gx1, gy1, gx2, gy2, p_tx, p_ty in gate_push_zones:
            safe_call(
                t_push_inside.new_effect.attack_move,
                source_player=ai_p,
                area_x1=gx1, area_y1=gy1, area_x2=gx2, area_y2=gy2,
                location_x=p_tx, location_y=p_ty,
            )

    # ==============================================================================
    # 7. 3-STOPNIOWA ESKALACJA CZASOWA (ENEMY_UNIT_REGISTRY)
    # ==============================================================================

    t_enable_esc1 = tm.add_trigger("04a_Enable_Escalation_At_20m", enabled=True, looping=False)
    safe_call(t_enable_esc1.new_condition.timer, timer=BALANCE["escalation_start_sec"])
    add_enemy_combat_buff(
        t_enable_esc1, ai_players,
        hp_add=BALANCE["escalation_hp_add"], atk_add=BALANCE["escalation_atk_add"],
    )
    send_highlight_chat(
        t_enable_esc1, "<ORANGE>",
        f"[WZROST SILY HORDY]: Jednostki Hordy otrzymuja +{BALANCE['escalation_hp_add']} HP oraz +{BALANCE['escalation_atk_add']} Ataku!",
    )

    t_escalate1 = tm.add_trigger("04b_Global_Horde_Escalation_Every_5m", enabled=False, looping=True)
    safe_call(t_enable_esc1.new_effect.activate_trigger, trigger_id=t_escalate1.trigger_id)
    safe_call(t_escalate1.new_condition.timer, timer=BALANCE["escalation_interval_sec"])
    add_enemy_combat_buff(
        t_escalate1, ai_players,
        hp_add=BALANCE["escalation_hp_add"], atk_add=BALANCE["escalation_atk_add"],
    )
    send_highlight_chat(
        t_escalate1, "<ORANGE>",
        f"[WZROST SILY HORDY]: Jednostki Hordy otrzymuja +{BALANCE['escalation_hp_add']} HP oraz +{BALANCE['escalation_atk_add']} Ataku!",
    )

    t_enable_esc2 = tm.add_trigger("04c_Enable_LateGame_Escalation_At_45m", enabled=True, looping=False)
    safe_call(t_enable_esc2.new_condition.timer, timer=BALANCE["late_escalation_start_sec"])
    add_enemy_combat_buff(
        t_enable_esc2, ai_players,
        hp_add=BALANCE["late_escalation_hp_add"], atk_add=1,
    )
    send_highlight_chat(
        t_enable_esc2, "<RED>",
        f"[FURIA LATE-GAME]: Horda wchodzi w faze pelnej mobilizacji (+{BALANCE['late_escalation_hp_add']} HP i +1 Ataku)!",
    )

    t_escalate2 = tm.add_trigger("04d_LateGame_Horde_Overdrive_Every_5m", enabled=False, looping=True)
    safe_call(t_enable_esc2.new_effect.activate_trigger, trigger_id=t_escalate2.trigger_id)
    safe_call(t_escalate2.new_condition.timer, timer=BALANCE["escalation_interval_sec"])
    add_enemy_combat_buff(
        t_escalate2, ai_players,
        hp_add=BALANCE["late_escalation_hp_add"], atk_add=1,
    )
    send_highlight_chat(
        t_escalate2, "<RED>",
        f"[FURIA LATE-GAME]: Horda wchodzi w faze pelnej mobilizacji (+{BALANCE['late_escalation_hp_add']} HP i +1 Ataku)!",
    )

    t_enable_esc3 = tm.add_trigger("04e_Enable_Endgame_Escalation_At_55m", enabled=True, looping=False)
    safe_call(t_enable_esc3.new_condition.timer, timer=BALANCE["endgame_escalation_start_sec"])
    add_enemy_combat_buff(
        t_enable_esc3, ai_players,
        hp_add=BALANCE["endgame_escalation_hp_add"], atk_add=2,
    )
    send_highlight_chat(
        t_enable_esc3, "<RED>",
        f"[ESKALACJA ENDGAME]: Elitarne dywizje Hordy zyskuja kolejne +{BALANCE['endgame_escalation_hp_add']} HP i +2 Ataku!",
    )

    t_escalate3 = tm.add_trigger("04f_Endgame_Horde_Escalation_Every_5m", enabled=False, looping=True)
    safe_call(t_enable_esc3.new_effect.activate_trigger, trigger_id=t_escalate3.trigger_id)
    safe_call(t_escalate3.new_condition.timer, timer=BALANCE["escalation_interval_sec"])
    add_enemy_combat_buff(
        t_escalate3, ai_players,
        hp_add=BALANCE["endgame_escalation_hp_add"], atk_add=2,
    )
    send_highlight_chat(
        t_escalate3, "<RED>",
        f"[ESKALACJA ENDGAME]: Elitarne dywizje Hordy zyskuja kolejne +{BALANCE['endgame_escalation_hp_add']} HP i +2 Ataku!",
    )

    # ==============================================================================
    # 8. ZNACZNIKI STANU TRUDNOŚCI, BLOKADA SANKTUARIUM I FAL (ETAP 3A + 3B + 3C)
    # ==============================================================================
    all_settlement_wave_triggers = {
        "G1_North": [], "G1_East": [], "G2_Snipers": [], "G2_Mages": [], "G3_North": [], "G3_East": [],
    }

    eco_raid_targets = [(32, 118), (76, 120), (32, 168), (76, 172)]
    deep_target_north = (48, 138)
    deep_target_center = (54, 146)
    deep_target_east = (68, 162)

    diff_tags = {-2: "M2", -1: "M1", 0: "0", 1: "P1", 2: "P2"}
    state_markers = {}
    for lvl, tag in diff_tags.items():
        trig = tm.add_trigger(f"State_Diff_Lvl_{tag}", enabled=(lvl == 0), looping=False)
        safe_call(trig.new_condition.timer, timer=999999)
        state_markers[lvl] = trig

    t_sanc_unlocked = tm.add_trigger("State_Sanctuary_Unlocked", enabled=True, looping=False)
    safe_call(t_sanc_unlocked.new_condition.timer, timer=999999)

    # ------------------------------------------------------------------------------
    # BRAMKI I WARIANTY TRYBU ENDLESS PO FALI 14 (ETAP 3C - NAPRAWA BUG-03)
    # ------------------------------------------------------------------------------
    settlement_spawn_configs = {
        "G1_North":   (PlayerId.FIVE,  48, 86,  *deep_target_north),
        "G1_East":    (PlayerId.FIVE,  120, 162, *deep_target_east),
        "G2_Snipers": (PlayerId.SIX,   68, 48,  *deep_target_north),
        "G2_Mages":   (PlayerId.SEVEN, 116, 114, *deep_target_center),
        "G3_North":   (PlayerId.EIGHT, 128, 36, *deep_target_center),
        "G3_East":    (PlayerId.EIGHT, 160, 62, *deep_target_east),
    }

    wave_definitions = get_wave_definitions()
    w14_def = wave_definitions[-1]
    endless_settlement_comps = {
        "G1_North":   w14_def.g1_north,
        "G1_East":    w14_def.g1_east,
        "G2_Snipers": w14_def.g2_snipers,
        "G2_Mages":   w14_def.g2_mages,
        "G3_North":   w14_def.g3_north,
        "G3_East":    w14_def.g3_east,
    }

    # Specjalne ataki pętlowe Endless dla wydzielonych obozów
    t_endless_trade = tm.add_trigger("03_Endless_Trade_Line_Attack", enabled=False, looping=False)
    trade_raid_comp = [
        (UnitInfo.SIEGE_RAM.ID, 3),
        (UnitInfo.PALADIN.ID, 10 + (14 - 8) * 2),
        (UnitInfo.HEAVY_CAVALRY_ARCHER.ID, 10 + (14 - 8) * 2),
    ]
    add_spawn_and_attack_effect(
        t_endless_trade, PlayerId.EIGHT, trade_raid_comp,
        spawn_x=162, spawn_y=180, target_x=190, target_y=194,
    )
    send_highlight_chat(
        t_endless_trade, "<ORANGE>",
        "[ATAK NA SZLAK HANDLOWY!]: Wydzielony korpus Hordy z taranami uderza na Mur Handlowy na poludniu (162, 184)!",
        flare_x=162, flare_y=184,
    )
    safe_call(t_endless_trade.new_effect.deactivate_trigger, trigger_id=t_endless_trade.trigger_id)
    all_settlement_wave_triggers["G3_East"].append(t_endless_trade)

    t_endless_sapper = tm.add_trigger("03_Endless_Forest_Breach_Assault", enabled=False, looping=False)
    add_spawn_and_attack_effect(
        t_endless_sapper, PlayerId.SIX,
        [(SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 14), (ELITE_BERSERK_ID, 8)],
        spawn_x=78, spawn_y=94, target_x=68, target_y=130,
    )
    add_spawn_and_attack_effect(
        t_endless_sapper, PlayerId.SIX,
        [(SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 14), (UnitInfo.HUSKARL.ID, 10)],
        spawn_x=110, spawn_y=140, target_x=68, target_y=146,
    )
    safe_call(t_endless_sapper.new_effect.deactivate_trigger, trigger_id=t_endless_sapper.trigger_id)
    all_settlement_wave_triggers["G2_Snipers"].append(t_endless_sapper)

    t_endless_szakale = tm.add_trigger("03_Endless_Szakale_EcoRaid", enabled=False, looping=False)
    add_spawn_and_attack_effect(
        t_endless_szakale, PlayerId.SEVEN, [(HUSSAR_ID, w14_def.raider_count)],
        spawn_x=116, spawn_y=114,
        target_x=eco_raid_targets[0][0], target_y=eco_raid_targets[0][1],
        ignore_frontline_move_only=True,
    )
    safe_call(t_endless_szakale.new_effect.deactivate_trigger, trigger_id=t_endless_szakale.trigger_id)
    all_settlement_wave_triggers["G2_Mages"].append(t_endless_szakale)

    # Ogłoszenie cykliczne Endless
    t_end_ann = tm.add_trigger("03_Endless_Announce_Loop", enabled=False, looping=True)
    safe_call(t_end_ann.new_condition.timer, timer=BALANCE["wave_interval_sec"])
    send_highlight_chat(
        t_end_ann, "<RED>",
        "=== [TRYB ENDLESS - NIESKONCZONA HORDA] === Horda rzuca do walki wszystkie rezerwy! Zniszczcie pozostale Settlementy, aby wygrac!",
        flare_x=gate_center[0], flare_y=gate_center[1],
    )

    t_end_gate_ann = tm.add_trigger("03_Endless_Announce_Gate", enabled=True, looping=False)
    safe_call(t_end_gate_ann.new_condition.timer, timer=4710)
    safe_call(t_end_gate_ann.new_effect.activate_trigger, trigger_id=t_end_ann.trigger_id)

    # Indywidualne Bramki Endless dla każdego Settlementu
    endless_gates = {}
    for s_key, (ai_p, sx, sy, tx, ty) in settlement_spawn_configs.items():
        end_gate = tm.add_trigger(f"03_Endless_Gate_{s_key}", enabled=False, looping=True)
        safe_call(end_gate.new_condition.timer, timer=BALANCE["wave_interval_sec"])
        all_settlement_wave_triggers[s_key].append(end_gate)
        endless_gates[s_key] = end_gate

        end_variants = []
        for lvl, tag in diff_tags.items():
            t_end_var = tm.add_trigger(f"03_Endless_{s_key}_Diff_{tag}", enabled=False, looping=False)
            safe_call(t_end_var.new_condition.trigger_active, trigger_id=state_markers[lvl].trigger_id)
            end_army = scale_comp_for_level(endless_settlement_comps[s_key], lvl)
            add_spawn_and_attack_effect(t_end_var, ai_p, end_army, spawn_x=sx, spawn_y=sy, target_x=tx, target_y=ty)
            all_settlement_wave_triggers[s_key].append(t_end_var)
            end_variants.append(t_end_var)

        # Efekty bramki Endless: zamraża Sanktuarium i budzi warianty
        safe_call(end_gate.new_effect.deactivate_trigger, trigger_id=t_sanc_unlocked.trigger_id)
        for ev in end_variants:
            safe_call(end_gate.new_effect.activate_trigger, trigger_id=ev.trigger_id)
        if s_key == "G3_East":
            safe_call(end_gate.new_effect.activate_trigger, trigger_id=t_endless_trade.trigger_id)
        elif s_key == "G2_Snipers":
            safe_call(end_gate.new_effect.activate_trigger, trigger_id=t_endless_sapper.trigger_id)
        elif s_key == "G2_Mages":
            safe_call(end_gate.new_effect.activate_trigger, trigger_id=t_endless_szakale.trigger_id)

        # Efekty każdego wariantu Endless: wyłącza braci i odblokowuje Sanktuarium
        for ev in end_variants:
            for brother in end_variants:
                safe_call(ev.new_effect.deactivate_trigger, trigger_id=brother.trigger_id)
            safe_call(ev.new_effect.activate_trigger, trigger_id=t_sanc_unlocked.trigger_id)

    # ------------------------------------------------------------------------------
    # HARMONOGRAM FAL 1–14 Z SAMOZAMYKAJĄCYM OKNEM DISPATCHU (ETAP 3B - NAPRAWA BUG-01)
    # ------------------------------------------------------------------------------
    for w_def in wave_definitions:
        w_num = w_def.wave_num
        w_time = w_def.wave_sec
        w_title = w_def.wave_title

        t_ann = tm.add_trigger(f"03_W{w_num:02d}_Announce", enabled=True, looping=False)
        safe_call(t_ann.new_condition.timer, timer=w_time)
        send_highlight_chat(
            t_ann, "<RED>",
            f"=== [{w_title}] === Po odparciu fali wyjdzcie w pole po Questy i Settlementy!",
            flare_x=gate_center[0], flare_y=gate_center[1],
        )

        per_settlement_wave = [
            ("G1_North",   PlayerId.FIVE,  w_def.g1_north, 48, 86,  *deep_target_north),
            ("G1_East",    PlayerId.FIVE,  w_def.g1_east, 120, 162, *deep_target_east),
            ("G2_Snipers", PlayerId.SIX,   w_def.g2_snipers, 68, 48,  *deep_target_north),
            ("G2_Mages",   PlayerId.SEVEN, w_def.g2_mages, 116, 114, *deep_target_center),
            ("G3_North",   PlayerId.EIGHT, w_def.g3_north, 128, 36, *deep_target_center),
            ("G3_East",    PlayerId.EIGHT, w_def.g3_east, 160, 62, *deep_target_east),
        ]

        wave_variants_all_settlements = []

        for s_key, ai_p, comp, sx, sy, tx, ty in per_settlement_wave:
            if not comp:
                continue

            t_clock = tm.add_trigger(f"03_W{w_num:02d}_{s_key}_Clock", enabled=True, looping=False)
            safe_call(t_clock.new_condition.timer, timer=w_time)
            all_settlement_wave_triggers[s_key].append(t_clock)

            settlement_variants = []
            for lvl, tag in diff_tags.items():
                t_var = tm.add_trigger(f"03_W{w_num:02d}_{s_key}_Diff_{tag}", enabled=False, looping=False)
                safe_call(t_var.new_condition.trigger_active, trigger_id=state_markers[lvl].trigger_id)
                scaled_comp = scale_comp_for_level(comp, lvl)
                add_spawn_and_attack_effect(t_var, ai_p, scaled_comp, spawn_x=sx, spawn_y=sy, target_x=tx, target_y=ty)

                all_settlement_wave_triggers[s_key].append(t_var)
                settlement_variants.append(t_var)
                wave_variants_all_settlements.append(t_var)

            # Efekty Zegara Fali Settlementu
            safe_call(t_clock.new_effect.deactivate_trigger, trigger_id=t_sanc_unlocked.trigger_id)
            for v in settlement_variants:
                safe_call(t_clock.new_effect.activate_trigger, trigger_id=v.trigger_id)
            if w_num == 14:
                safe_call(t_clock.new_effect.activate_trigger, trigger_id=endless_gates[s_key].trigger_id)

            # Efekty każdego z 5 wariantów: dezaktywacja braci
            for v in settlement_variants:
                for brother in settlement_variants:
                    safe_call(v.new_effect.deactivate_trigger, trigger_id=brother.trigger_id)

        # Globalny bezpiecznik zamykający okno dispatchu dla fali
        t_close = tm.add_trigger(f"03_W{w_num:02d}_Close_Window", enabled=True, looping=False)
        safe_call(t_close.new_condition.timer, timer=w_time + 1)
        for v in wave_variants_all_settlements:
            safe_call(t_close.new_effect.deactivate_trigger, trigger_id=v.trigger_id)
        safe_call(t_close.new_effect.activate_trigger, trigger_id=t_sanc_unlocked.trigger_id)

        # Ataki specjalne zintegrowane z harmonogramem
        if w_def.raider_count > 0:
            eco_tx, eco_ty = eco_raid_targets[w_num % len(eco_raid_targets)]
            t_raid = tm.add_trigger(f"03_W{w_num:02d}_Szakale_EcoRaid", enabled=True, looping=False)
            safe_call(t_raid.new_condition.timer, timer=w_time)
            add_spawn_and_attack_effect(
                t_raid, PlayerId.SEVEN, [(HUSSAR_ID, w_def.raider_count)],
                spawn_x=116, spawn_y=162 if w_num % 2 == 0 else 114,
                target_x=eco_tx, target_y=eco_ty,
                ignore_frontline_move_only=True,
            )
            all_settlement_wave_triggers["G2_Mages"].append(t_raid)

        if w_num in (8, 10, 12, 14):
            t_trade_raid = tm.add_trigger(f"03_W{w_num:02d}_Trade_Line_Attack", enabled=True, looping=False)
            safe_call(t_trade_raid.new_condition.timer, timer=w_time)
            trade_raid_comp = [
                (UnitInfo.SIEGE_RAM.ID, 3),
                (UnitInfo.PALADIN.ID, 10 + (w_num - 8) * 2),
                (UnitInfo.HEAVY_CAVALRY_ARCHER.ID, 10 + (w_num - 8) * 2),
            ]
            add_spawn_and_attack_effect(
                t_trade_raid, PlayerId.EIGHT, trade_raid_comp,
                spawn_x=162, spawn_y=180, target_x=190, target_y=194,
            )
            send_highlight_chat(
                t_trade_raid, "<ORANGE>",
                "[ATAK NA SZLAK HANDLOWY!]: Wydzielony korpus Hordy z taranami uderza na Mur Handlowy na poludniu (162, 184)!",
                flare_x=162, flare_y=184,
            )
            all_settlement_wave_triggers["G3_East"].append(t_trade_raid)

        if w_num == 9:
            t_warn_forest_n = tm.add_trigger("03_W09_Forest_Breach_North_Warn", enabled=True, looping=False)
            safe_call(t_warn_forest_n.new_condition.timer, timer=w_time - 15)
            add_spawn_and_attack_effect(
                t_warn_forest_n, PlayerId.SIX, [(SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 8)],
                spawn_x=78, spawn_y=90, target_x=78, target_y=95,
            )
            send_highlight_chat(
                t_warn_forest_n, "<ORANGE>",
                "[ALARM SAPERSKI - POLNOCNY LAS]: Wrogie Onagery zaczynaja wyrabywac przesieke w lesie na (78, 100)! Za 15 sekund przebija sie do bazy!",
                flare_x=78, flare_y=98,
            )
            all_settlement_wave_triggers["G2_Snipers"].append(t_warn_forest_n)

            t_breach_n = tm.add_trigger("03_W09_Forest_Breach_North_Execute", enabled=True, looping=False)
            safe_call(t_breach_n.new_condition.timer, timer=w_time)
            for tr_u in north_breach_trees:
                safe_call(t_breach_n.new_effect.remove_object, selected_object_ids=[tr_u.reference_id])
            add_spawn_and_attack_effect(
                t_breach_n, PlayerId.SIX,
                [(SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 14), (ELITE_BERSERK_ID, 8)],
                spawn_x=78, spawn_y=94, target_x=68, target_y=130,
            )
            send_highlight_chat(
                t_breach_n, "<RED>",
                "[PRZESIEKA WYRABANA!]: Onagery Hordy przebily przejscie przez polnocny las na (78, 100) i wlewaja sie na tyly bazy!",
                flare_x=78, flare_y=102,
            )
            all_settlement_wave_triggers["G2_Snipers"].append(t_breach_n)

        if w_num == 12:
            t_warn_forest_e = tm.add_trigger("03_W12_Forest_Breach_East_Warn", enabled=True, looping=False)
            safe_call(t_warn_forest_e.new_condition.timer, timer=w_time - 15)
            add_spawn_and_attack_effect(
                t_warn_forest_e, PlayerId.SIX, [(SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 10)],
                spawn_x=114, spawn_y=140, target_x=109, target_y=140,
            )
            send_highlight_chat(
                t_warn_forest_e, "<ORANGE>",
                "[ALARM SAPERSKI - WSCHODNI LAS]: Wrogie Onagery wyrabuja druga przesieke we wschodnim lesie na (104, 140)! Za 15s przebija sie do bazy!",
                flare_x=106, flare_y=140,
            )
            all_settlement_wave_triggers["G2_Snipers"].append(t_warn_forest_e)

            t_breach_e = tm.add_trigger("03_W12_Forest_Breach_East_Execute", enabled=True, looping=False)
            safe_call(t_breach_e.new_condition.timer, timer=w_time)
            for tr_u in east_breach_trees:
                safe_call(t_breach_e.new_effect.remove_object, selected_object_ids=[tr_u.reference_id])
            add_spawn_and_attack_effect(
                t_breach_e, PlayerId.SIX,
                [(SIEGE_ONAGER_ID, 2), (UnitInfo.HALBERDIER.ID, 16), (UnitInfo.HUSKARL.ID, 12)],
                spawn_x=110, spawn_y=140, target_x=68, target_y=146,
            )
            send_highlight_chat(
                t_breach_e, "<RED>",
                "[DRUGA PRZESIEKA WYRABANA!]: Onagery Hordy przebily wschodni las na (104, 140)!",
                flare_x=104, flare_y=140,
            )
            all_settlement_wave_triggers["G2_Snipers"].append(t_breach_e)

    ctx["all_settlement_wave_triggers"] = all_settlement_wave_triggers
    ctx["camp_leash_handles"] = camp_leash_handles
    ctx["deep_target_center"] = deep_target_center
    ctx["state_markers"] = state_markers
    ctx["t_sanc_unlocked"] = t_sanc_unlocked
