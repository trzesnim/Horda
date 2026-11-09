from dataclasses import dataclass
from pathlib import Path

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

TREE_OAK_ID = 349


TREE_PINE_ID = 350


ROCK_CLIFF_ID = 623


RELIC_ID = 285


MAP_REVEALER_ID = 837


FLARE_UNIT_ID = 112


TORCH_ID = 499


FEITORIA_ID = 1021


KREPOST_ID = 1251


FORTIFIED_PALISADE_ID = 119


PALISADE_GATE_SW_NE_ID = 789


PALISADE_GATE_NW_SE_ID = 793


IMAM_UNIT_ID = 842


SIEGE_ONAGER_ID = 588


PETARD_ID = 440


FLAMING_CAMEL_ID = 1263


ELITE_BERSERK_ID = 694


ELITE_BATTLE_ELEPHANT_ID = 1134


HUSSAR_ID = 441


TERRAIN_WATER = 1


TERRAIN_SHALLOWS = 4


RES_FOOD = 0


RES_WOOD = 1


RES_STONE = 2


RES_GOLD = 3


RES_BONUS_POP_CAP = 32


ATTR_HIT_POINTS = 0


ATTR_LINE_OF_SIGHT = 1


ATTR_MOVEMENT_SPEED = 5


ATTR_ARMOR = 8


ATTR_ATTACK = 9


ATTR_ATTACK_RELOAD_TIME = 10


ATTR_MAXIMUM_RANGE = 12


ATTR_WORK_RATE = 13


ATTR_MINIMUM_RANGE = 20


ATTR_BLAST_WIDTH = 22


ATTR_SEARCH_RADIUS = 23


ATTR_HERO_STATUS = 40


ATTR_BLAST_ATTACK_LEVEL = 44  # 2 = obrażenia obszarowe ranią jednostki i budynki, ale NIE ścinają drzew


ATTR_REGENERATION_RATE = 109


TECH_CARTOGRAPHY = 19


TECH_FAITH = 45


TECH_FEUDAL_AGE = 101


TECH_CASTLE_AGE = 102


TECH_IMPERIAL_AGE = 103


TECH_FORGING = 67


TECH_IRON_CASTING = 68


TECH_BLAST_FURNACE = 75


TECH_SCALE_MAIL = 74


TECH_CHAIN_MAIL = 76


TECH_PLATE_MAIL = 77


TECH_SQUIRES = 215


TECH_SCALE_BARDING = 81


TECH_CHAIN_BARDING = 82


TECH_PLATE_BARDING = 80


TECH_BLOODLINES = 435


TECH_HUSBANDRY = 39


TECH_FLETCHING = 199


TECH_BODKIN_ARROW = 200


TECH_BRACER = 201


TECH_BALLISTICS = 93


TECH_CHEMISTRY = 47


TECH_THUMB_RING = 437


TECH_SIEGE_ENGINEERS = 377


PLAYER_RANGED_UNITS = [
    UnitInfo.ARCHER.ID,
    UnitInfo.CROSSBOWMAN.ID,
    UnitInfo.ARBALESTER.ID,
    UnitInfo.SKIRMISHER.ID,
    UnitInfo.ELITE_SKIRMISHER.ID,
    UnitInfo.IMPERIAL_SKIRMISHER.ID,
    UnitInfo.CAVALRY_ARCHER.ID,
    UnitInfo.HEAVY_CAVALRY_ARCHER.ID,
    UnitInfo.HAND_CANNONEER.ID,
    UnitInfo.SLINGER.ID,
    UnitInfo.GENITOUR.ID,
    UnitInfo.ELITE_GENITOUR.ID,
    UnitInfo.ELEPHANT_ARCHER.ID,
    UnitInfo.ELITE_ELEPHANT_ARCHER.ID,
    UnitInfo.LONGBOWMAN.ID,
    UnitInfo.ELITE_LONGBOWMAN.ID,
    UnitInfo.CHU_KO_NU.ID,
    UnitInfo.ELITE_CHU_KO_NU.ID,
    UnitInfo.MANGUDAI.ID,
    UnitInfo.ELITE_MANGUDAI.ID,
    UnitInfo.WAR_WAGON.ID,
    UnitInfo.ELITE_WAR_WAGON.ID,
    UnitInfo.PLUMED_ARCHER.ID,
    UnitInfo.ELITE_PLUMED_ARCHER.ID,
    UnitInfo.CONQUISTADOR.ID,
    UnitInfo.ELITE_CONQUISTADOR.ID,
    UnitInfo.GENOESE_CROSSBOWMAN.ID,
    UnitInfo.ELITE_GENOESE_CROSSBOWMAN.ID,
    UnitInfo.CAMEL_ARCHER.ID,
    UnitInfo.ELITE_CAMEL_ARCHER.ID,
    UnitInfo.RATTAN_ARCHER.ID,
    UnitInfo.ELITE_RATTAN_ARCHER.ID,
    UnitInfo.KIPCHAK.ID,
    UnitInfo.ELITE_KIPCHAK.ID,
    UnitInfo.COMPOSITE_BOWMAN.ID,
    UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
    UnitInfo.JANISSARY.ID,
    UnitInfo.ELITE_JANISSARY.ID,
    UnitInfo.ARAMBAI.ID,
    UnitInfo.ELITE_ARAMBAI.ID,
    UnitInfo.CHAKRAM_THROWER.ID,
    UnitInfo.ELITE_CHAKRAM_THROWER.ID,
    UnitInfo.RATHA_RANGED.ID,
]

PLAYER_MOUNTED_RANGED_UNITS = [
    UnitInfo.CAVALRY_ARCHER.ID,
    UnitInfo.HEAVY_CAVALRY_ARCHER.ID,
    UnitInfo.MANGUDAI.ID,
    UnitInfo.ELITE_MANGUDAI.ID,
    UnitInfo.CAMEL_ARCHER.ID,
    UnitInfo.ELITE_CAMEL_ARCHER.ID,
    UnitInfo.CONQUISTADOR.ID,
    UnitInfo.ELITE_CONQUISTADOR.ID,
    UnitInfo.KIPCHAK.ID,
    UnitInfo.ELITE_KIPCHAK.ID,
    UnitInfo.ELEPHANT_ARCHER.ID,
    UnitInfo.ELITE_ELEPHANT_ARCHER.ID,
    UnitInfo.ARAMBAI.ID,
    UnitInfo.ELITE_ARAMBAI.ID,
    UnitInfo.RATHA_RANGED.ID,
]

PLAYER_CAVALRY_UNITS = [
    UnitInfo.SCOUT_CAVALRY.ID,
    UnitInfo.LIGHT_CAVALRY.ID,
    HUSSAR_ID,
    UnitInfo.WINGED_HUSSAR.ID,
    UnitInfo.KNIGHT.ID,
    UnitInfo.CAVALIER.ID,
    UnitInfo.PALADIN.ID,
    UnitInfo.SAVAR.ID,
    UnitInfo.STEPPE_LANCER.ID,
    UnitInfo.ELITE_STEPPE_LANCER.ID,
    UnitInfo.CAMEL_SCOUT.ID,
    UnitInfo.CAMEL_RIDER.ID,
    UnitInfo.HEAVY_CAMEL_RIDER.ID,
    UnitInfo.IMPERIAL_CAMEL_RIDER.ID,
    UnitInfo.BATTLE_ELEPHANT.ID,
    ELITE_BATTLE_ELEPHANT_ID,
    UnitInfo.WAR_ELEPHANT.ID,
    UnitInfo.ELITE_WAR_ELEPHANT.ID,
    UnitInfo.SHRIVAMSHA_RIDER.ID,
    UnitInfo.ELITE_SHRIVAMSHA_RIDER.ID,
    UnitInfo.RATHA_MELEE.ID,
    UnitInfo.CATAPHRACT.ID,
    UnitInfo.ELITE_CATAPHRACT.ID,
    UnitInfo.TARKAN.ID,
    UnitInfo.ELITE_TARKAN.ID,
    UnitInfo.BOYAR.ID,
    UnitInfo.ELITE_BOYAR.ID,
    UnitInfo.MAGYAR_HUSZAR.ID,
    UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
    UnitInfo.KONNIK.ID,
    UnitInfo.ELITE_KONNIK.ID,
    UnitInfo.LEITIS.ID,
    UnitInfo.ELITE_LEITIS.ID,
    UnitInfo.KESHIK.ID,
    UnitInfo.ELITE_KESHIK.ID,
    UnitInfo.COUSTILLIER.ID,
    UnitInfo.ELITE_COUSTILLIER.ID,
    UnitInfo.MONASPA.ID,
    UnitInfo.ELITE_MONASPA.ID,
    UnitInfo.CENTURION.ID,
    UnitInfo.ELITE_CENTURION.ID,
]

PLAYER_INFANTRY_UNITS = [
    UnitInfo.MILITIA.ID,
    UnitInfo.MAN_AT_ARMS.ID,
    UnitInfo.LONG_SWORDSMAN.ID,
    UnitInfo.TWO_HANDED_SWORDSMAN.ID,
    UnitInfo.CHAMPION.ID,
    UnitInfo.LEGIONARY.ID,
    UnitInfo.SPEARMAN.ID,
    UnitInfo.PIKEMAN.ID,
    UnitInfo.HALBERDIER.ID,
    UnitInfo.EAGLE_SCOUT.ID,
    UnitInfo.EAGLE_WARRIOR.ID,
    UnitInfo.ELITE_EAGLE_WARRIOR.ID,
    UnitInfo.WOAD_RAIDER.ID,
    UnitInfo.ELITE_WOAD_RAIDER.ID,
    UnitInfo.THROWING_AXEMAN.ID,
    UnitInfo.ELITE_THROWING_AXEMAN.ID,
    UnitInfo.HUSKARL.ID,
    UnitInfo.ELITE_HUSKARL.ID,
    UnitInfo.TEUTONIC_KNIGHT.ID,
    UnitInfo.ELITE_TEUTONIC_KNIGHT.ID,
    UnitInfo.SAMURAI.ID,
    UnitInfo.ELITE_SAMURAI.ID,
    UnitInfo.BERSERK.ID,
    ELITE_BERSERK_ID,
    UnitInfo.JAGUAR_WARRIOR.ID,
    UnitInfo.ELITE_JAGUAR_WARRIOR.ID,
    UnitInfo.KAMAYUK.ID,
    UnitInfo.ELITE_KAMAYUK.ID,
    UnitInfo.CONDOTTIERO.ID,
    UnitInfo.SHOTEL_WARRIOR.ID,
    UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
    UnitInfo.GBETO.ID,
    UnitInfo.ELITE_GBETO.ID,
    UnitInfo.KARAMBIT_WARRIOR.ID,
    UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
    UnitInfo.OBUCH.ID,
    UnitInfo.ELITE_OBUCH.ID,
    UnitInfo.URUMI_SWORDSMAN.ID,
    UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
    UnitInfo.GHULAM.ID,
    UnitInfo.ELITE_GHULAM.ID,
    UnitInfo.SERJEANT.ID,
    UnitInfo.ELITE_SERJEANT.ID,
    UnitInfo.FLEMISH_MILITIA.ID,
]

PLAYER_PROD_BUILDINGS = [
    BuildingInfo.BARRACKS.ID,
    BuildingInfo.STABLE.ID,
    BuildingInfo.ARCHERY_RANGE.ID,
    BuildingInfo.CASTLE.ID,
    BuildingInfo.SIEGE_WORKSHOP.ID,
    KREPOST_ID,
    BuildingInfo.DONJON.ID,
]


def populate_ingame_scenario_descriptions(scenario):
    mm_msg = getattr(scenario, "message_manager", None)
    if mm_msg is None:
        return

    instructions_text = (
        "KRONIKI RUBIEZY: HORDA I EKSPEDYCJE (v6.6 - 4P Co-op)\n\n"
        "USTAWIENIA LOBBY I STARTU:\n"
        "- Gracze P5-P8 sa automatycznie skonfigurowani jako AI z zablokowanymi cywilizacjami (P5 Wikingowie, P6 Turcy, P7 Saraceni, P8 Persowie). Ustaw trudnosc AI na EKSTREMALNY (Extreme)!\n"
        "- Gracze P1, P3 i P4 startuja z 2 wybudowanymi domkami na polnoc od TC, a Gracz P2 z 6 domkami (kompensacja 20 popu zajmowanego przez Feitorie).\n"
        "- W panelu Celow (Objectives) dziala ZEGAR FALI odliczajacy czas do kolejnego uderzenia co 30 sekund oraz dynamiczny znacznik aktualnego Poziomu Trudnosci.\n\n"
        "SANKTUARIUM BALANSU (Wspolrzedne 6, 150 w zachodnim lesie):\n"
        "- Gracz 1 posiada odizolowanego Inzyniera Balansu (Krola) na (6, 150).\n"
        "- Wejscie Krolem na GORNA flage (6, 146) ZWIEKSZA trudnosc (+25% fal, +15 HP, +2 Ataku wroga na poziom).\n"
        "- Wejscie Krolem na DOLNA flage (6, 154) ZMNIEJSZA trudnosc (-20% fal, -15% HP wroga na poziom; kluczowe jednostki specjalne i tarany zachowuja min. 1 szt. w grupie).\n"
        "- Dokladne poziomy trudnosci:\n"
        "  * Poziom -2 (Bardzo Latwy): -40% fal, -30% HP wroga.\n"
        "  * Poziom -1 (Latwy): -20% fal, -15% HP wroga.\n"
        "  * Poziom  0 (Domyslny): 100% wielkosci fal i statystyk bazowych.\n"
        "  * Poziom +1 (Trudny): +25% fal, +15 HP, +2 Ataku wroga.\n"
        "  * Poziom +2 (Ekstremalny): +50% fal, +30 HP, +4 Ataku wroga.\n"
        "- Po kazdej zmianie Krol jest automatycznie zatrzymywany i wraca na srodek (zmiana trudnosci jest dostepna w kazdym momencie gry, bez blokad).\n\n"
        "SZLAK HANDLOWY I PLAC GRACZY (Lewy dolny rog mapy x=2..24, y=176..198):\n"
        "- W lewym dolnym rogu bazy znajduje sie duzy, czysty Plac pod Targowiska graczy.\n"
        "- Zburzenie Q1 (Karawanseraj) stawia pojedyncze Targowisko sojusznicze w prawym rogu (195, 194) oraz buduje Kamienny Mur Obronny na y=186 (z 2-kratkowymi otworami wypadowymi na x=122..123 i x=170..171 oslonietych Basztami na y=184)!\n\n"
        "ZASADY ROZGRYWKI (Horyzont 60-90 minut):\n"
        "- Fala 1 w 8:30 (bez taranow), Fala 2 w 13:00 (z taranem/mangonelem i uderzeniem na wszystkie 3 bramy, bez mutantow), Fala 3 w 18:00, kolejne co 5,5 min.\n"
        "- Trzypoziomowa eskalacja czasowa (natychmiastowy 1. tick i powtorzenie co 5 min):\n"
        "  * Od 20:00: +5 HP, +1 Atak co 5 min.\n"
        "  * Od 45:00: dodatkowo +9 HP, +1 Atak co 5 min (lacznie +14 HP, +2 Ataku co 5 min).\n"
        "  * Od 55:00: dodatkowo +6 HP, +1 Atak co 5 min (lacznie +20 HP, +3 Ataku co 5 min).\n"
        "- Od 45. minuty (Fale 8-14) co druga fala wysyla szturm na SZLAK HANDLOWY w kierunku Bramy Handlowej.\n"
        "- W Falach 9 (51:00) i 12 (67:30) Saperzy P6 wyrabuja przesieki w lesie (6x11 na polnocy, 11x6 na wschodzie)!\n"
    )

    hints_text = (
        "BESTIARIUSZ HORDY (WYSPECJALIZOWANE JEDNOSTKI Z POSWIATA BOHATERA):\n"
        "1. Taran-Zolw / Zelazny Slon (P8 - Tank): 1450 HP, szybkosc 0.72, +10/+12 pancerza, odporny na konwersje. Zadaje zawsze 3 dmg jednostkom (odpornosc na buffy ataku), ale +220 dmg budynkom!\n"
        "2. Szakale Dywersyjne (Huzarzy P7 - Eco-Raiders): Szybkosc 1.62, +6 pancerza na strzaly, zawsze 2 ataku (skaluja wylacznie HP). Wjezdzaja pod TC atakowac chlopow!\n"
        "3. Arcymag Tarczy (Imam P7 - Globalny Support): Gdy stoi w strefie przedpola (promien 18 kratek wokol 110, 114) przed Brama Centralna, daje GLOBALNIE +30/+30 Pancerza wszystkim armiom Hordy (P5-P8 na calej mapie) oraz LOKALNIE leczy (+15 HP/3s) jednostki Hordy w tej strefie! Ma 240 HP i regeneracje 5 HP/s. Zabicie go zdejmuje aure z calej Hordy!\n"
        "4. Mozdzierz Oblezniczy (Onager P6): 350 HP, szybkosc 0.58, 21 zasiegu, wybuch co 10s, MARTWA STREFA 6 kratek. Pociski maja Blast Attack Level = 2 (nie scinaja drzew wokol bram).\n"
        "5. Snajperzy (Janczarzy P6): 90 HP, 19 zasiegu, ~107 dmg w 1 cel.\n"
        "6. Berserkerzy i Kamikaze (P5): Szybkie jednostki szturmowe o zerowym pancerzu na strzaly.\n"
    )

    scouts_text = (
        "RAPORT ZWIADOWCZY - 4 QUESTY I 6 SETTLEMENTOW:\n"
        "- UWAGA: Kazdy wykonany Quest (Q1-Q4) daje potezne nagrody graczom, ale wywoluje tez Adaptacje Hordy:\n"
        "  * Q1 Karawanseraj (154, 190): Mur Handlowy (y=186, baszty y=184, otwory wypadowe x=122..123 i 170..171), Market P2 (195, 194), +30 Popu, +20% szybsi Wiesniacy i 4 szybkie wozy handlowe. [Adaptacja Hordy: +8 HP, +1 Atak]\n"
        "  * Q2 Klif Artylerii (28, 32): Balistyka, Chemia, Siege Engineers, Thumb Ring; +2 Zasiegu i +4 Ataku strzelcow (w tym UU); +12% szybkosci i +4 Ataku jazdy oraz +12% szybkosci strzelcow konnych (w tym UU). [Adaptacja Hordy: +8 HP, +1 Atak]\n"
        "  * Q3 Skarbiec (142, 118): +20 Popu i staly dochod co minute (+250F, +250W, +200G, +40S dla KAZDEGO gracza P1-P4). [Adaptacja Hordy: +10 HP, +1 Atak]\n"
        "  * Q4 Krwawy Oltarz (105, 20): +30% HP armii, +2/+2 pancerza (piechota, jazda, strzelcy i UU), +40% szybsza produkcja wojska (w tym Krepost, Donjon i Siege Workshop); obnizenie HP Arcymaga do 120 HP. [Adaptacja Hordy: +10 HP, +1 Atak]\n"
        "- Stopniowanie Nagrod i Furii Settlementow (zburzenie obozu zawala jego budynki poboczne, wycofuje wojska z fal i wywoluje kontratak z odpowiedniego kierunku):\n"
        "  * Grade 1 (G1 Polnocny, G1 Wschodni): Nagroda +700F/+700G, Furia +5 HP i +0 Ataku wroga, odwet 8 Cavalier + 10 Pikeman.\n"
        "  * Grade 2 (G2 Akademia [usuwa tez Saperow], G2 Klasztor): Nagroda +1000F/+1000G, Furia +10 HP i +1 Atak wroga, odwet 10 Cavalier + 12 Halberdier.\n"
        "  * Grade 3 (G3 Cytadela Pln., G3 Cytadela Wsch. [usuwa tez Rajdy Handlowe]): Nagroda +1500F/+1500G, Furia +15 HP i +2 Atak wroga, odwet 1 Zelazny Slon + 12 Paladin + 14 Halberdier.\n"
    )

    if hasattr(mm_msg, "instructions"):
        mm_msg.instructions = instructions_text
    if hasattr(mm_msg, "hints"):
        mm_msg.hints = hints_text
    if hasattr(mm_msg, "scouts"):
        mm_msg.scouts = scouts_text
    if hasattr(mm_msg, "history"):
        mm_msg.history = f"{instructions_text}\n{hints_text}"


def find_scenario_folder() -> Path:
    aoe_base = Path.home() / "Games" / "Age of Empires 2 DE"
    if aoe_base.exists():
        for folder in aoe_base.glob("*/resources/_common/scenario"):
            if (folder / "template.aoe2scenario").exists():
                return folder
        for folder in aoe_base.glob("*/resources/_common/scenario"):
            if folder.parent.parent.parent.name != "0":
                return folder
    return Path(__file__).parent


SCENARIO_FOLDER = find_scenario_folder()


INPUT_TEMPLATE = SCENARIO_FOLDER / "template.aoe2scenario"


OUTPUT_SCENARIO = SCENARIO_FOLDER / "Kroniki_Rubiezy_Horda_Coop.aoe2scenario"


MAP_SIZE = 200


BALANCE = {
    "wave1_sec": 510,                     # 8:30
    "wave2_sec": 780,                     # 13:00
    "wave3_sec": 1080,                    # 18:00
    "wave_interval_sec": 330,             # Co 5,5 minuty (330s)

    "escalation_start_sec": 1200,         # Od 20:00 (Bieg 1): +5 HP i +1 Ataku co 5 minut
    "escalation_interval_sec": 300,
    "escalation_hp_add": 5,
    "escalation_atk_add": 1,
    "late_escalation_start_sec": 2700,    # Od 45:00 (Bieg 2): +9 HP i +1 Ataku co 5 minut
    "late_escalation_hp_add": 9,
    "endgame_escalation_start_sec": 3300, # Od 55:00 (Bieg 3): +6 HP i +1 Ataku co 5 minut
    "endgame_escalation_hp_add": 6,

    "diff_step_up_hp": 15,
    "diff_step_up_atk": 2,

    "tank_hp": 1450,
    "tank_unit_atk": 3,
    "tank_bldg_bonus": 220,
    "tank_melee_armor": 10,
    "tank_pierce_armor": 12,
    "tank_speed": 0.72,

    "raider_hp": 95,
    "raider_speed": 1.62,
    "raider_atk": 2,
    "raider_pierce_armor": 6,

    "mage_hp": 240,
    "mage_melee_armor": 3,
    "mage_pierce_armor": 4,
    "mage_regen_per_min": 300,
    "mage_local_radius": 18,
    "mage_shield_armor": 30,
    "mage_aoe_heal_3s": 15,
    "mage_speed": 0.78,

    "mortar_hp": 350,
    "mortar_range": 21,
    "mortar_min_range": 6,
    "mortar_reload": 10.0,
    "mortar_blast_width": 2.6,
    "mortar_bonus_atk": 75,
    "mortar_speed": 0.58,

    "sniper_hp": 90,
    "sniper_range": 19,
    "sniper_bonus_atk": 85,
    "sniper_reload": 6.5,

    "berserk_hp": 185,
    "berserk_speed": 1.40,
    "berserk_bonus_atk": 12,
    "kamikaze_hp": 115,
    "kamikaze_speed": 1.50,
    "kamikaze_blast_width": 2.4,
    "kamikaze_bonus_atk": 95,

    "q1_bonus_pop": 30,
    "q3_bonus_pop": 20,
    "quest3_trickle": {"food": 250, "wood": 250, "gold": 200, "stone": 40},
    "human_start_res": {"food": 500, "wood": 600, "gold": 400, "stone": 300},
    "human_start_houses": 2,
    "p2_start_houses": 6,
}


@dataclass(frozen=True)
class WaveDefinition:
    wave_num: int
    wave_sec: int
    wave_title: str
    g1_north: list[tuple[int, int]]
    g1_east: list[tuple[int, int]]
    g2_snipers: list[tuple[int, int]]
    g2_mages: list[tuple[int, int]]
    g3_north: list[tuple[int, int]]
    g3_east: list[tuple[int, int]]
    raider_count: int

    def __iter__(self):
        return iter((
            self.wave_num,
            self.wave_sec,
            self.wave_title,
            self.g1_north,
            self.g1_east,
            self.g2_snipers,
            self.g2_mages,
            self.g3_north,
            self.g3_east,
            self.raider_count,
        ))


@dataclass(frozen=True)
class EnemyUnitSpec:
    unit_id: int
    name: str
    base_hp: int
    attack_class: int | None
    scales_hp: bool
    receives_mage_shield: bool
    mandatory_min_one: bool

    @property
    def hp_delta_down(self) -> int:
        if not self.scales_hp:
            return 0
        return max(2, (self.base_hp * 15 + 50) // 100)


ENEMY_UNIT_REGISTRY: dict[int, EnemyUnitSpec] = {
    UnitInfo.MAN_AT_ARMS.ID: EnemyUnitSpec(
        unit_id=UnitInfo.MAN_AT_ARMS.ID, name="Man-at-Arms", base_hp=45, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.SPEARMAN.ID: EnemyUnitSpec(
        unit_id=UnitInfo.SPEARMAN.ID, name="Spearman", base_hp=45, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.PIKEMAN.ID: EnemyUnitSpec(
        unit_id=UnitInfo.PIKEMAN.ID, name="Pikeman", base_hp=55, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.HALBERDIER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.HALBERDIER.ID, name="Halberdier", base_hp=60, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.HUSKARL.ID: EnemyUnitSpec(
        unit_id=UnitInfo.HUSKARL.ID, name="Huskarl", base_hp=70, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    ELITE_BERSERK_ID: EnemyUnitSpec(
        unit_id=ELITE_BERSERK_ID, name="Berserker Szturmowy", base_hp=185, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=True
    ),
    UnitInfo.SCOUT_CAVALRY.ID: EnemyUnitSpec(
        unit_id=UnitInfo.SCOUT_CAVALRY.ID, name="Scout Cavalry", base_hp=65, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.STEPPE_LANCER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.STEPPE_LANCER.ID, name="Steppe Lancer", base_hp=80, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.KNIGHT.ID: EnemyUnitSpec(
        unit_id=UnitInfo.KNIGHT.ID, name="Knight", base_hp=120, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.CAVALIER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.CAVALIER.ID, name="Cavalier", base_hp=140, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.PALADIN.ID: EnemyUnitSpec(
        unit_id=UnitInfo.PALADIN.ID, name="Paladin", base_hp=180, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.ARCHER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.ARCHER.ID, name="Archer", base_hp=30, attack_class=3, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.CROSSBOWMAN.ID: EnemyUnitSpec(
        unit_id=UnitInfo.CROSSBOWMAN.ID, name="Crossbowman", base_hp=35, attack_class=3, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.ARBALESTER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.ARBALESTER.ID, name="Arbalester", base_hp=40, attack_class=3, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.HEAVY_CAVALRY_ARCHER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.HEAVY_CAVALRY_ARCHER.ID, name="Heavy Cav Archer", base_hp=80, attack_class=3, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.ELITE_JANISSARY.ID: EnemyUnitSpec(
        unit_id=UnitInfo.ELITE_JANISSARY.ID, name="Snajper Imperialny", base_hp=90, attack_class=3, scales_hp=True, receives_mage_shield=False, mandatory_min_one=True
    ),
    UnitInfo.MANGONEL.ID: EnemyUnitSpec(
        unit_id=UnitInfo.MANGONEL.ID, name="Mangonel", base_hp=50, attack_class=4, scales_hp=True, receives_mage_shield=False, mandatory_min_one=True
    ),
    SIEGE_ONAGER_ID: EnemyUnitSpec(
        unit_id=SIEGE_ONAGER_ID, name="Mozdzierz Oblezniczy", base_hp=350, attack_class=4, scales_hp=True, receives_mage_shield=False, mandatory_min_one=True
    ),
    ELITE_BATTLE_ELEPHANT_ID: EnemyUnitSpec(
        unit_id=ELITE_BATTLE_ELEPHANT_ID, name="Zelazny Slon-Tank", base_hp=1450, attack_class=None, scales_hp=True, receives_mage_shield=False, mandatory_min_one=True
    ),
    HUSSAR_ID: EnemyUnitSpec(
        unit_id=HUSSAR_ID, name="Szakal Dywersyjny", base_hp=95, attack_class=None, scales_hp=True, receives_mage_shield=False, mandatory_min_one=False
    ),
    IMAM_UNIT_ID: EnemyUnitSpec(
        unit_id=IMAM_UNIT_ID, name="Arcymag Tarczy", base_hp=240, attack_class=None, scales_hp=False, receives_mage_shield=False, mandatory_min_one=True
    ),
    PETARD_ID: EnemyUnitSpec(
        unit_id=PETARD_ID, name="Fanatyk Kamikaze", base_hp=115, attack_class=None, scales_hp=False, receives_mage_shield=False, mandatory_min_one=True
    ),
    FLAMING_CAMEL_ID: EnemyUnitSpec(
        unit_id=FLAMING_CAMEL_ID, name="Plonacy Wielblad", base_hp=115, attack_class=None, scales_hp=False, receives_mage_shield=False, mandatory_min_one=True
    ),
    UnitInfo.BATTERING_RAM.ID: EnemyUnitSpec(
        unit_id=UnitInfo.BATTERING_RAM.ID, name="Battering Ram", base_hp=175, attack_class=None, scales_hp=False, receives_mage_shield=False, mandatory_min_one=True
    ),
    UnitInfo.CAPPED_RAM.ID: EnemyUnitSpec(
        unit_id=UnitInfo.CAPPED_RAM.ID, name="Capped Ram", base_hp=200, attack_class=None, scales_hp=False, receives_mage_shield=True, mandatory_min_one=True
    ),
    UnitInfo.SIEGE_RAM.ID: EnemyUnitSpec(
        unit_id=UnitInfo.SIEGE_RAM.ID, name="Siege Ram", base_hp=270, attack_class=None, scales_hp=False, receives_mage_shield=True, mandatory_min_one=True
    ),
}


def get_wave_definitions() -> list[WaveDefinition]:
    wave_definitions = [
        (
            1, 510, "Fala 1/14 (8:30 - Szturm Feudalny bez taranow)",
            [(UnitInfo.MAN_AT_ARMS.ID, 6), (UnitInfo.ARCHER.ID, 5)],
            [(UnitInfo.MAN_AT_ARMS.ID, 6), (UnitInfo.SCOUT_CAVALRY.ID, 5)],
            [], [], [], [], 0,
        ),
        (
            2, 780, "Fala 2/14 (13:00 - Feudalna z Taranem i Mangonelem, bez jednostek specjalnych)",
            [(UnitInfo.MAN_AT_ARMS.ID, 8), (UnitInfo.ARCHER.ID, 6), (UnitInfo.BATTERING_RAM.ID, 1)],
            [(UnitInfo.SPEARMAN.ID, 8), (UnitInfo.SCOUT_CAVALRY.ID, 6), (UnitInfo.MANGONEL.ID, 1)],
            [],
            [(UnitInfo.SCOUT_CAVALRY.ID, 5), (UnitInfo.ARCHER.ID, 6)],
            [], [], 0,
        ),
        (
            3, 1080, "Fala 3/14 (18:00 - Castle Age + pierwsi Berserkerzy, Snajperzy i Szakale!)",
            [(UnitInfo.PIKEMAN.ID, 11), (ELITE_BERSERK_ID, 3), (PETARD_ID, 1), (UnitInfo.BATTERING_RAM.ID, 1)],
            [(UnitInfo.HUSKARL.ID, 8), (UnitInfo.KNIGHT.ID, 5), (FLAMING_CAMEL_ID, 1)],
            [(UnitInfo.CROSSBOWMAN.ID, 10), (UnitInfo.ELITE_JANISSARY.ID, 2)],
            [(UnitInfo.KNIGHT.ID, 6), (UnitInfo.BATTERING_RAM.ID, 1)],
            [], [], 5,
        ),
        (
            4, 1410, "Fala 4/14 (23:30 - Castle Age + Arcymag Tarczy dajacy +30 Pancerza calej Hordzie!)",
            [(UnitInfo.PIKEMAN.ID, 14), (ELITE_BERSERK_ID, 4), (UnitInfo.BATTERING_RAM.ID, 2)],
            [(UnitInfo.HUSKARL.ID, 10), (UnitInfo.KNIGHT.ID, 6), (FLAMING_CAMEL_ID, 2)],
            [(UnitInfo.CROSSBOWMAN.ID, 12), (UnitInfo.ELITE_JANISSARY.ID, 3)],
            [(IMAM_UNIT_ID, 1), (UnitInfo.KNIGHT.ID, 10), (UnitInfo.BATTERING_RAM.ID, 2)],
            [], [], 6,
        ),
        (
            5, 1740, "Fala 5/14 (29:00 - Pozny Castle Age + Mozdzierz Oblezniczy!)",
            [(UnitInfo.PIKEMAN.ID, 16), (ELITE_BERSERK_ID, 4), (PETARD_ID, 2), (UnitInfo.CAPPED_RAM.ID, 2)],
            [(UnitInfo.HUSKARL.ID, 12), (FLAMING_CAMEL_ID, 2), (UnitInfo.CAPPED_RAM.ID, 2)],
            [(UnitInfo.CROSSBOWMAN.ID, 14), (UnitInfo.ELITE_JANISSARY.ID, 3), (SIEGE_ONAGER_ID, 1)],
            [(IMAM_UNIT_ID, 1), (UnitInfo.KNIGHT.ID, 12)],
            [(UnitInfo.KNIGHT.ID, 8), (UnitInfo.PIKEMAN.ID, 10)],
            [], 7,
        ),
        (
            6, 2070, "Fala 6/14 (34:30 - Debiut Zelaznego Slonia-Tanka 1450 HP!)",
            [(UnitInfo.PIKEMAN.ID, 18), (ELITE_BERSERK_ID, 5), (UnitInfo.CAPPED_RAM.ID, 2)],
            [(UnitInfo.HUSKARL.ID, 14), (FLAMING_CAMEL_ID, 3), (UnitInfo.CAPPED_RAM.ID, 2)],
            [(UnitInfo.CROSSBOWMAN.ID, 16), (UnitInfo.ELITE_JANISSARY.ID, 3), (SIEGE_ONAGER_ID, 1)],
            [(IMAM_UNIT_ID, 1), (UnitInfo.CAVALIER.ID, 12), (UnitInfo.CAPPED_RAM.ID, 2)],
            [(ELITE_BATTLE_ELEPHANT_ID, 1), (UnitInfo.KNIGHT.ID, 10), (UnitInfo.PIKEMAN.ID, 12)],
            [(UnitInfo.CROSSBOWMAN.ID, 14), (UnitInfo.KNIGHT.ID, 8)],
            8,
        ),
        (
            7, 2400, "Fala 7/14 (40:00 - Wczesny Imperial Age)",
            [(UnitInfo.HALBERDIER.ID, 20), (ELITE_BERSERK_ID, 5), (PETARD_ID, 3), (UnitInfo.CAPPED_RAM.ID, 3)],
            [(UnitInfo.HUSKARL.ID, 16), (FLAMING_CAMEL_ID, 3), (UnitInfo.CAPPED_RAM.ID, 2)],
            [(UnitInfo.ARBALESTER.ID, 18), (UnitInfo.ELITE_JANISSARY.ID, 4), (SIEGE_ONAGER_ID, 1)],
            [(IMAM_UNIT_ID, 1), (UnitInfo.CAVALIER.ID, 14)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.CAVALIER.ID, 12), (UnitInfo.HALBERDIER.ID, 12)],
            [(ELITE_BATTLE_ELEPHANT_ID, 1), (UnitInfo.ARBALESTER.ID, 16)],
            9,
        ),
        (
            8, 2730, "Fala 8/14 (45:30 - Imperial Age + UDERZENIE NA SZLAK HANDLOWY!)",
            [(UnitInfo.HALBERDIER.ID, 22), (ELITE_BERSERK_ID, 6), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.HUSKARL.ID, 18), (FLAMING_CAMEL_ID, 3), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.ARBALESTER.ID, 20), (UnitInfo.ELITE_JANISSARY.ID, 4), (SIEGE_ONAGER_ID, 2)],
            [(IMAM_UNIT_ID, 2), (UnitInfo.CAVALIER.ID, 16), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.CAVALIER.ID, 14), (UnitInfo.HALBERDIER.ID, 14)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.ARBALESTER.ID, 18), (SIEGE_ONAGER_ID, 1)],
            10,
        ),
        (
            9, 3060, "Fala 9/14 (51:00 - Imperial Age + PRZEBICIE PRZEZ POLNOCNY LAS!)",
            [(UnitInfo.HALBERDIER.ID, 25), (ELITE_BERSERK_ID, 7), (PETARD_ID, 3), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.HUSKARL.ID, 20), (FLAMING_CAMEL_ID, 4), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.ARBALESTER.ID, 22), (UnitInfo.ELITE_JANISSARY.ID, 4), (SIEGE_ONAGER_ID, 2)],
            [(IMAM_UNIT_ID, 2), (UnitInfo.PALADIN.ID, 16), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(ELITE_BATTLE_ELEPHANT_ID, 3), (UnitInfo.PALADIN.ID, 15), (UnitInfo.HALBERDIER.ID, 16)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.ARBALESTER.ID, 20), (SIEGE_ONAGER_ID, 2)],
            12,
        ),
    ]

    for w_late in range(10, 15):
        m = w_late - 9
        wave_sec = 3060 + m * 330
        minute_mark = wave_sec // 60
        extra_tag = ""
        if w_late in (10, 12, 14):
            extra_tag += " + ATAK NA TRADE LINE"
        if w_late == 12:
            extra_tag += " + PRZEBICIE PRZEZ LAS"
        wave_definitions.append((
            w_late, wave_sec,
            f"Fala {w_late}/14 ({minute_mark}m - Late Imperial{extra_tag}!)",
            [(UnitInfo.HALBERDIER.ID, 25 + m * 3), (ELITE_BERSERK_ID, 7 + m), (PETARD_ID, 3 + (m // 2)), (UnitInfo.SIEGE_RAM.ID, 4)],
            [(UnitInfo.HUSKARL.ID, 20 + m * 3), (FLAMING_CAMEL_ID, 3 + (m // 2)), (UnitInfo.SIEGE_RAM.ID, 4)],
            [(UnitInfo.ARBALESTER.ID, 22 + m * 3), (UnitInfo.ELITE_JANISSARY.ID, 4 + (m // 2)), (SIEGE_ONAGER_ID, 2 + (m // 3))],
            [(IMAM_UNIT_ID, 2 + (m // 3)), (UnitInfo.PALADIN.ID, 16 + m * 3), (UnitInfo.SIEGE_RAM.ID, 4)],
            [(ELITE_BATTLE_ELEPHANT_ID, 3 + (m // 2)), (UnitInfo.PALADIN.ID, 16 + m * 3), (UnitInfo.HALBERDIER.ID, 16 + m * 2)],
            [(ELITE_BATTLE_ELEPHANT_ID, 3 + (m // 2)), (UnitInfo.ARBALESTER.ID, 20 + m * 3), (SIEGE_ONAGER_ID, 2 + (m // 3))],
            12 + m,
        ))
    return [WaveDefinition(*w) for w in wave_definitions]
