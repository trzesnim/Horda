from dataclasses import dataclass
from pathlib import Path

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.units import UnitInfo

if not hasattr(UnitInfo, "SUBOTAI"):
    UnitInfo.SUBOTAI = HeroInfo.SUBOTAI
if not hasattr(UnitInfo, "RELIC"):
    UnitInfo.RELIC = OtherInfo.RELIC
if not hasattr(UnitInfo, "HEAVY_CAV_ARCHER"):
    UnitInfo.HEAVY_CAV_ARCHER = UnitInfo.HEAVY_CAVALRY_ARCHER

TREE_OAK_ID = 349


TREE_PINE_ID = 350


ROCK_CLIFF_ID = 623


RELIC_ID = 285


FLAG_A_ID = OtherInfo.FLAG_A.ID


FLAG_B_ID = OtherInfo.FLAG_B.ID


GOLD_MINE_ID = OtherInfo.GOLD_MINE.ID


FINAL_BOSS_HERO_ID = UnitInfo.SUBOTAI.ID


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


ONAGER_PROJECTILE_ID = ProjectileInfo.ONAGER.ID


ONAGER_FIRE_PROJECTILE_ID = ProjectileInfo.ONAGER_FIRE.ID


ONAGER_SECONDARY_PROJECTILE_ID = ProjectileInfo.MANGONEL_SECONDARY.ID


ONAGER_SECONDARY_FIRE_PROJECTILE_ID = ProjectileInfo.MANGONEL_SECONDARY_FIRE.ID


ONAGER_PROJECTILE_IDS = [
    ONAGER_PROJECTILE_ID,
    ONAGER_FIRE_PROJECTILE_ID,
    ONAGER_SECONDARY_PROJECTILE_ID,
    ONAGER_SECONDARY_FIRE_PROJECTILE_ID,
]


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
    UnitInfo.WAR_WAGON.ID,
    UnitInfo.ELITE_WAR_WAGON.ID,
    UnitInfo.GENITOUR.ID,
    UnitInfo.ELITE_GENITOUR.ID,
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

    tldr_block = (
        "TL;DR (NAJWAZNIEJSZE ZASADY W 30 SEKUND):\n"
        "- CEL GRY: Bron Cytadeli (Feitorii P2) w sercu bazy (54, 146) - jej utrata to natychmiastowa porazka wszystkich! Wyjdz za mury, zniszcz 6 Twierdz Hordy (G1-G3), a po 60s na powrot armii zgladz Wielkiego Chana Subotaia (4500 HP) przed Brama Centralna.\n"
        "- USTAWIENIA I FALE: Gracze P1-P4 (ludzie, P2 najlepiej Hiszpanie) vs P5-P8 (AI Extreme). 14 fal od 8:30 do 92:00 (od F7 rozrzedzone co 6-8 min; potem Endless co 10 min od 102:00) - zegar do kolejnej fali i poziom trudnosci sa zawsze na gorze Objectives (a skrot zasad w zakladce Objectives!).\n"
        "- ROLE GRACZY (P1-P4):\n"
        "  * P1 (Niebieski): Brama Centralna + Krol w odizolowanym Sanktuarium (4, 138) (wejscie na flage zmienia trudnosc -2..+2).\n"
        "  * P2 (Czerwony): Handel, obrona chlopow przed Szakalami + Krol-Kwatermistrz w odizolowanej komnacie (4, 164) (od 10:00 co 4 min rosnace wsparcie: 10-20m Male, 20-30m Srednie, 30m+ Duze).\n"
        "  * P3 (Zielony): Brama Polnocna (uwaga: w 52:00 alarm 2 min, w 53:30 alarm 30s, a w 54:00 saperzy wyrabia wylom w polnocnym lesie!).\n"
        "  * P4 (Zolty): Brama Wschodnia (w 74:00 alarm 2 min, w 75:30 alarm 30s, w 76:00 wylom we wschodnim lesie) + korytarz handlowy na poludniu.\n"
        "- WYPRAWY (SETTLEMENTY I QUESTY): Zburzenie kazdego Settlementu (G1-G3) daje surowce i na stale wylacza jego fale oraz jednostki specjalne (wywolujac jeden kontratak i Furie). Questy (Q1-Q4) daja potezne perki calej druzynie (Q1: mur i handel; Q2: rozbij 2 Baszty Bombardowe by zdjac tarcze Uniwersytetu -> bonus strzelcow/jazdy; Q3: staly dochod co 1 min; Q4: przetrwaj 30s odwetu -> +30% HP/pancerz i Wielki Klasztor).\n"
        "- 3 ZLOTE ZASADY W WALCE: (1) W pierwszej kolejnosci zabijaj Arcymaga (Imama) przed Brama Centralna (daje kolumnie P7 tarcze +8/+8 pancerza i leczy pobliskich wrogow +25 HP/3s!), (2) Chron wiesniakow pod TC przed szybkimi Szakalami (7 ataku!), (3) Nie buduj na polanach spawnu Hordy przed bramami (fala niszczy budynki w miejscu swojego pojawienia sie).\n\n"
    )

    instructions_text = (
        "KRONIKI RUBIEZY: HORDA I EKSPEDYCJE (v7.0.4 - 4P Co-op)\n\n"
        f"{tldr_block}"
        "USTAWIENIA LOBBY I STARTU:\n"
        "- Gracze P5-P8 sa automatycznie skonfigurowani jako AI z zablokowanymi cywilizacjami (P5 Wikingowie, P6 Turcy, P7 Saraceni, P8 Persowie). Ustaw trudnosc AI na EKSTREMALNY (Extreme)!\n"
        "- Gracze P1, P3 i P4 startuja z 2 wybudowanymi domkami na polnoc od TC, a Gracz P2 z 6 domkami (kompensacja 20 popu zajmowanego przez Feitorie).\n"
        "- W panelu Celow (Objectives) dziala ZEGAR FALI odliczajacy czas do kolejnego uderzenia co 30 sekund oraz dynamiczny znacznik aktualnego Poziomu Trudnosci.\n\n"
        "SANKTUARIUM BALANSU (Wspolrzedne 4, 138 na zachodniej krawedzi mapy - pelna izolacja klifami i pasem lasu):\n"
        "- Gracz 1 posiada odizolowanego Inzyniera Balansu (Krola) na (4, 138) w zamknietej komnacie 5x9 (x=2..6, y=134..142).\n"
        "- Wejscie Krolem na GORNA flage (4, 135) ZWIEKSZA trudnosc (+25% fal, +15 HP, +2 Ataku wroga na poziom).\n"
        "- Wejscie Krolem na DOLNA flage (4, 141) ZMNIEJSZA trudnosc (-20% fal, -15% HP wroga na poziom; kluczowe jednostki specjalne i tarany zachowuja min. 1 szt. w grupie).\n"
        "- Dokladne poziomy trudnosci:\n"
        "  * Poziom -2 (Bardzo Latwy): -40% fal, -30% HP wroga.\n"
        "  * Poziom -1 (Latwy): -20% fal, -15% HP wroga.\n"
        "  * Poziom  0 (Domyslny): 100% wielkosci fal i statystyk bazowych.\n"
        "  * Poziom +1 (Trudny): +25% fal, +15 HP, +2 Ataku wroga.\n"
        "  * Poziom +2 (Ekstremalny): +50% fal, +30 HP, +4 Ataku wroga.\n"
        "- Po kazdej zmianie Krol jest automatycznie zatrzymywany i wraca na srodek (4, 138) (zmiana trudnosci jest dostepna w kazdym momencie gry, bez blokad).\n\n"
        "POSTERUNEK KWATERMISTRZA P2 (Wspolrzedne 4, 164 na zachodniej krawedzi mapy - pelna izolacja, odblokowywany w 10:00):\n"
        "- Gracz 2 (Czerwony) posiada Kwatermistrza (Krola P2 na 4, 164) w zamknietej komnacie 5x9 (x=2..6, y=160..168) z dwiema roznymi flagami rozkazow (odblokowanie w 10:00 po Fali 1, wspolny cooldown 240s / 4 min; dziala wylacznie po wejsciu Krolem P2 na flage):\n"
        "  * Poziom 1 (10:00-20:00 - Maly Bonus): Flaga Polnocna (4, 161) = 4x Konkwistador + 1x Mangonel wokol (54, 149); Flaga Poludniowa (4, 167) = +125 Zywnosci/+125 Drewna/+100 Zlota dla kazdego P1-P4 (bez naprawy murow).\n"
        "  * Poziom 2 (20:00-30:00 - Sredni Bonus): Flaga Polnocna (4, 161) = 4x Konkwistador + 2x Kolubryna; Flaga Poludniowa (4, 167) = +200 F/W/G dla kazdego P1-P4 oraz naprawa Twierdzy i Muru Handlowego Q1 (+250 HP).\n"
        "  * Poziom 3 (od 30:00+ - Duzy Bonus): Flaga Polnocna (4, 161) = 6x Elitarny Konkwistador + 2x Kolubryna + 2x Taran Oblezniczy; Flaga Poludniowa (4, 167) = +300 F/W/G dla kazdego P1-P4 oraz naprawa Twierdzy i Muru Handlowego Q1 (+500 HP).\n\n"
        "SZLAK HANDLOWY I PLAC GRACZY (Lewy dolny rog mapy x=2..24, y=176..198):\n"
        "- W lewym dolnym rogu bazy znajduje sie duzy, czysty Plac pod Targowiska graczy.\n"
        "- Zburzenie Q1 (Karawanseraj) stawia pojedyncze Targowisko sojusznicze w prawym rogu (195, 194) oraz buduje Kamienny Mur Obronny na y=186 (z 2-kratkowymi otworami wypadowymi na x=122..123 i x=170..171 oslonietych Basztami na y=184)!\n\n"
        "ZASADY ROZGRYWKI I WARUNEK ZWYCIESTWA (Horyzont 60-95 minut):\n"
        "- Fale 1-6: 8:30, 13:00, 18:00, 23:30, 29:00, 34:30; Fale 7-14 (rozrzedzone): 40:30, 47:00, 54:00, 61:00, 68:30, 76:00, 84:00, 92:00; Tryb Endless od 102:00 co 10 minut (600s).\n"
        "- Rozlaczna trzypoziomowa eskalacja czasowa (przesunieta o +17s, twardy sufit w 65:30):\n"
        "  * Bieg 1 (20:17 -> 35:17): +5 HP, +1 Atak co 5 min (3 ticki: 25:17, 30:17, 35:17).\n"
        "  * Bieg 2 (35:17 -> 55:17, wylacza Bieg 1): +8 HP, +1 Atak co 5 min (4 ticki: 40:17, 45:17, 50:17, 55:17).\n"
        "  * Bieg 3 (55:17 -> 65:17, wylacza Bieg 2): +10 HP, +1 Atak co 5 min (2 ticki: 60:17, 65:17).\n"
        "  * Twardy Limit (65:30): zatrzymuje cala eskalacje czasowa na pulapie +67 HP i +9 Ataku!\n"
        "- Od 47. minuty (Fale 8, 10, 12, 14 i Endless) co druga fala wysyla szturm na SZLAK HANDLOWY w kierunku Bramy Handlowej.\n"
        "- W Falach 9 (54:00, alarmy 52:00 i 53:30) i 12 (76:00, alarmy 74:00 i 75:30) Saperzy P6 wyrabuja przesieki w lesie (6x11 na polnocy, 11x6 na wschodzie)!\n"
        "- FINALOWY BOSS FIGHT: Po zniszczeniu wszystkich 6 Settlementow Hordy macie 60 sekund na powrot armii pod Brama Centralna (104, 114), zanim Wielki Chan Subotai (4500 HP) uderzy z (116, 114) wsparty skrzydlami na Brame Polnocna (68, 60 -> 48, 136) i Wschodnia (116, 162 -> 68, 152). Dopoki w strefie bitwy (40..135, 90..175) zyje przynajmniej 1 Zelazny Slon gwardii P8, Chan regeneruje +180 HP co 3s! Zgladz Chana, aby wygrac!\n"
    )

    hints_text = (
        f"{tldr_block}"
        "BESTIARIUSZ HORDY (WYSPECJALIZOWANE JEDNOSTKI Z POSWIATA BOHATERA):\n"
        "1. Taran-Zolw / Zelazny Slon (P8 - Tank): 1450 HP, szybkosc 0.72, +10/+12 pancerza, odporny na konwersje. Zadaje zawsze 3 dmg jednostkom (odpornosc na buffy ataku), ale +140 dmg budynkom!\n"
        "2. Szakale Dywersyjne (Huzarzy P7 - Eco-Raiders): Szybkosc 1.62, +6 pancerza na strzaly, zawsze 7 ataku (skaluja wylacznie HP). Wjezdzaja pod TC atakowac chlopow!\n"
        "3. Arcymag Tarczy (Imam P7 - Lokalny Support Bramy Centralnej): Gdy stoi w strefie przedpola (promien 18 kratek wokol 110, 114) przed Brama Centralna, daje kolumnie P7 +8/+8 Pancerza oraz LOKALNIE leczy (+25 HP/3s) wszystkie jednostki Hordy w tej strefie! Ma 240 HP i regeneracje 5 HP/s. Zabicie go zdejmuje tarcze i leczenie!\n"
        "4. Mozdzierz Oblezniczy (Onager P6 - Glass Cannon): 70 HP (nie skaluje HP!), pancerz 0/3, szybkosc 0.58, 21 zasiegu, spowolniony lot pocisku (3.2), wybuch co 10s, MARTWA STREFA 6 kratek. Pociski maja Blast Attack Level = 2 (nie scinaja drzew wokol bram).\n"
        "5. Snajperzy (Janczarzy P6): 90 HP, 19 zasiegu, ~107 dmg w 1 cel.\n"
        "6. Berserkerzy i Kamikaze (P5): Szybkie jednostki szturmowe o zerowym pancerzu na strzaly.\n"
        "7. Wielki Chan Subotai (P8 - Finalowy Boss): 4500 HP, 45 ataku, 8/10 pancerza, szybkosc 0.85. Po upadku 6 Settlementow daje 60s na przegrupowanie, po czym pojawia sie z eskorta P8 (6x Zelazny Slon, 16x Paladyn, 4x Siege Ram) na (116, 114), 2x Arcymag P7 na (118, 122) oraz skrzydlami na Brame Polnocna (68, 60 -> 48, 136) i Wschodnia (116, 162 -> 68, 152) (po 10x Paladyn, 10x Heavy Cav Archer, 2x Siege Ram). Dopoki w strefie bitwy (40..135, 90..175) zyje choc 1 Zelazny Slon P8, Chan odzyskuje +180 HP co 3s - wybij najpierw gwardie sloni lub skup caly ogien na Chanie!\n"
    )

    scouts_text = (
        "RAPORT ZWIADOWCZY - 4 QUESTY, 3 PUNKTY EKSPLORACYJNE (PoI) I 6 SETTLEMENTOW:\n"
        "- UWAGA: Kazdy wykonany Quest (Q1-Q4) daje potezne nagrody graczom, ale wywoluje tez Adaptacje Hordy:\n"
        "  * Q1 Karawanseraj (154, 190): Mur Handlowy (y=186, baszty y=184, otwory wypadowe x=122..123 i 170..171), Market P2 (195, 194), +30 Popu, +20% szybsi Wiesniacy i 4 szybkie wozy handlowe. [Adaptacja Hordy: +8 HP, +1 Atak]\n"
        "  * Q2 Klif Artylerii (28, 32 - Dwuetapowy): Po obudzeniu garnizonu Q2 wlacza sie oslona leczaca Uniwersytetu (+400 HP/2s); zniszcz 2 wysuniete Baszty Artyleryjskie (24, 34 i 32, 34), aby zdjac oslone! Nagroda: Balistyka, Chemia, Siege Engineers, Thumb Ring, +2 Zasiegu i +4 Ataku strzelcow (w tym UU), +12% szybkosci i +4 Ataku jazdy, +12% szybkosci strzelcow konnych (w tym UU), 2x Kolubryna dla P3 na (27, 36) i (29, 36) oraz wizja na G2 Akademia! [Adaptacja Hordy: +8 HP, +1 Atak]\n"
        "  * Q3 Skarbiec (142, 118): +20 Popu i staly dochod co minute (+100F, +100W, +90G, +20S dla KAZDEGO gracza P1-P4). [Adaptacja Hordy: +10 HP, +1 Atak]\n"
        "  * Q4 Krwawy Oltarz (105, 20 - Dwuetapowy): Zburzenie Klasztoru spawnuje Relikt i odwet P7 (6x Heavy Camel, 6x Elite Mameluke, 4x Elite Steppe Lancer z 105, 34); przetrwaj 30s Krwawego Odwetu Zakonu! Nagroda: +30% HP armii, +2/+2 pancerza, +40% szybsza produkcja wojska, Arcymagowie oslabieni do 120 HP oraz Wielki Klasztor na (58, 152) i 2 Mnichow P1 na (57, 155) i (59, 155)! [Adaptacja Hordy: +10 HP, +1 Atak]\n"
        "- Trzy Zdarzenia Eksploracyjne na Mapie (PoI - jednorazowe dla pierwszego odkrywcy):\n"
        "  * PoI 1 Opuszczony Oboz Inzynierow (30, 76 - odblokowywany w 10:00): 2x Tarany (Capped Ram) + 2x Petarda dla odkrywcy oraz +200W/+200G dla P1-P4.\n"
        "  * PoI 2 Zaginiona Karawana (124, 178): +350F/+350G dla P1-P4 i odkrycie obozu Q1 (154, 190).\n"
        "  * PoI 3 Kamien Wedrowca i Zwiadowcy (50, 90): 2x Lekka Kawaleria (Light Cavalry) dla odkrywcy, +150S/+150G dla P1-P4 oraz odkrycie brodu rzecznego (122, 62).\n"
        "- Stopniowanie Nagrod i Furii Settlementow (zburzenie obozu zawala jego budynki poboczne, wycofuje wojska z fal i wywoluje kontratak z odpowiedniego kierunku):\n"
        "  * Grade 1 (G1 Polnocny, G1 Wschodni): Nagroda +700F/+700G, Furia +8 HP i +1 Atak wroga, odwet 8 Cavalier + 10 Pikeman.\n"
        "  * Grade 2 (G2 Akademia [usuwa tez Saperow], G2 Klasztor): Nagroda +1000F/+1000G, Furia +14 HP i +1 Atak wroga, odwet 10 Cavalier + 12 Halberdier.\n"
        "  * Grade 3 (G3 Cytadela Pln., G3 Cytadela Wsch. [usuwa tez Rajdy Handlowe]): Nagroda +1500F/+1500G, Furia +20 HP i +2 Atak wroga, odwet 1 Zelazny Slon + 12 Paladin + 14 Halberdier.\n"
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
    "wave_interval_sec": 330,             # Co 5,5 minuty (330s) dla Fal 3-6
    "endless_start_sec": 6120,            # 102:00 (10 minut po Fali 14 w 92:00)
    "endless_repeat_interval": 600,       # Co 10 minut (600s) w Trybie Endless

    "escalation_start_sec": 1217,         # Od 20:17 (Bieg 1): +5 HP i +1 Ataku co 5 minut (3 ticki: 25:17, 30:17, 35:17)
    "escalation_interval_sec": 300,
    "escalation_hp_add": 5,
    "escalation_atk_add": 1,
    "gear1_atk": 1,
    "late_escalation_start_sec": 2117,    # Od 35:17 (Bieg 2, wylacza Bieg 1): +8 HP i +1 Ataku co 5 minut (4 ticki: 40:17..55:17)
    "late_escalation_hp_add": 8,
    "late_escalation_atk_add": 1,
    "gear2_atk": 1,
    "endgame_escalation_start_sec": 3317, # Od 55:17 (Bieg 3, wylacza Bieg 2): +10 HP i +1 Ataku co 5 minut (2 ticki: 60:17, 65:17)
    "endgame_escalation_hp_add": 10,
    "endgame_escalation_atk_add": 1,
    "gear3_atk": 1,
    "escalation_cap_sec": 3930,           # 65:30 Twardy Wylacznik Koncowy (sufit: +67 HP, +9 Ataku)

    "diff_step_up_hp": 15,
    "diff_step_up_atk": 2,

    "tank_hp": 1450,
    "tank_unit_atk": 3,
    "tank_bldg_bonus": 140,
    "tank_melee_armor": 10,
    "tank_pierce_armor": 12,
    "tank_speed": 0.72,

    "raider_hp": 95,
    "raider_speed": 1.62,
    "raider_atk": 7,
    "raider_pierce_armor": 6,

    "mage_hp": 240,
    "mage_melee_armor": 3,
    "mage_pierce_armor": 4,
    "mage_regen_per_min": 300,
    "mage_local_radius": 18,
    "mage_shield_armor": 8,
    "mage_aoe_heal_3s": 25,
    "mage_speed": 0.78,

    "mortar_hp": 70,
    "mortar_pierce_armor": 3,
    "mortar_melee_armor": 0,
    "mortar_range": 21,
    "mortar_min_range": 6,
    "mortar_reload": 10.0,
    "mortar_blast_width": 2.6,
    "mortar_bonus_atk": 75,
    "mortar_speed": 0.58,
    "mortar_projectile_speed": 3.2,

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
    "quest3_trickle": {"food": 100, "wood": 100, "gold": 90, "stone": 20},
    "fury_g1_hp": 8,
    "fury_g1_atk": 1,
    "fury_g2_hp": 14,
    "fury_g2_atk": 1,
    "fury_g3_hp": 20,
    "fury_g3_atk": 2,
    "human_start_res": {"food": 500, "wood": 600, "gold": 400, "stone": 300},
    "human_start_houses": 2,
    "p2_start_houses": 6,

    "final_boss_hp": 4500,
    "final_boss_regen_3s": 180,
    "final_boss_wait_sec": 60,
    "final_boss_atk": 45,
    "final_boss_melee_armor": 8,
    "final_boss_pierce_armor": 10,
    "final_boss_speed": 0.85,
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
    base_atk: int = 0
    is_ranged: bool = False
    scales_atk: bool = False
    hp_delta_up: int = 15
    custom_hp_delta_down: int | None = None

    @property
    def hp_delta_down(self) -> int:
        if self.custom_hp_delta_down is not None:
            return self.custom_hp_delta_down
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
    UnitInfo.ELITE_STEPPE_LANCER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.ELITE_STEPPE_LANCER.ID, name="Elite Steppe Lancer", base_hp=100, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
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
        unit_id=SIEGE_ONAGER_ID,
        name="Mozdzierz Oblezniczy",
        base_hp=70,
        attack_class=None,
        scales_hp=False,
        receives_mage_shield=False,
        mandatory_min_one=True,
        scales_atk=False,
        hp_delta_up=10,
        custom_hp_delta_down=15,
    ),
    ELITE_BATTLE_ELEPHANT_ID: EnemyUnitSpec(
        unit_id=ELITE_BATTLE_ELEPHANT_ID, name="Zelazny Slon-Tank", base_hp=1450, attack_class=None, scales_hp=True, receives_mage_shield=False, mandatory_min_one=True
    ),
    HUSSAR_ID: EnemyUnitSpec(
        unit_id=HUSSAR_ID, name="Szakal Dywersyjny", base_hp=95, attack_class=None, scales_hp=True, receives_mage_shield=False, mandatory_min_one=False, base_atk=7
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
    UnitInfo.HEAVY_CAMEL_RIDER.ID: EnemyUnitSpec(
        unit_id=UnitInfo.HEAVY_CAMEL_RIDER.ID, name="Heavy Camel Rider", base_hp=140, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    UnitInfo.ELITE_MAMELUKE.ID: EnemyUnitSpec(
        unit_id=UnitInfo.ELITE_MAMELUKE.ID, name="Elite Mameluke", base_hp=100, attack_class=4, scales_hp=True, receives_mage_shield=True, mandatory_min_one=False
    ),
    FINAL_BOSS_HERO_ID: EnemyUnitSpec(
        unit_id=FINAL_BOSS_HERO_ID,
        name="Wielki Chan Subotai",
        base_hp=4500,
        attack_class=None,
        scales_hp=False,
        receives_mage_shield=False,
        mandatory_min_one=True,
        base_atk=45,
        is_ranged=True,
        scales_atk=False,
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
            4, 1410, "Fala 4/14 (23:30 - Castle Age + Arcymag Tarczy dajacy +8/+8 Pancerza kolumnie P7 i leczenie 25 HP/3s!)",
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
            7, 2430, "Fala 7/14 (40:30 - Wczesny Imperial: PANCERNA SZARZA!)",
            [(UnitInfo.HALBERDIER.ID, 20), (ELITE_BERSERK_ID, 5), (PETARD_ID, 3), (UnitInfo.CAPPED_RAM.ID, 3)],
            [(UnitInfo.HUSKARL.ID, 16), (FLAMING_CAMEL_ID, 3), (UnitInfo.CAPPED_RAM.ID, 2)],
            [(UnitInfo.ARBALESTER.ID, 18), (UnitInfo.ELITE_JANISSARY.ID, 4), (SIEGE_ONAGER_ID, 1)],
            [(IMAM_UNIT_ID, 1), (UnitInfo.CAVALIER.ID, 18)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.CAVALIER.ID, 16), (UnitInfo.HALBERDIER.ID, 12), (UnitInfo.SIEGE_RAM.ID, 2)],
            [(ELITE_BATTLE_ELEPHANT_ID, 1), (UnitInfo.ARBALESTER.ID, 16)],
            9,
        ),
        (
            8, 2820, "Fala 8/14 (47:00 - Imperial Age + UDERZENIE NA SZLAK HANDLOWY!)",
            [(UnitInfo.HALBERDIER.ID, 22), (ELITE_BERSERK_ID, 6), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.HUSKARL.ID, 18), (FLAMING_CAMEL_ID, 3), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.ARBALESTER.ID, 20), (UnitInfo.ELITE_JANISSARY.ID, 4), (SIEGE_ONAGER_ID, 2)],
            [(IMAM_UNIT_ID, 2), (UnitInfo.CAVALIER.ID, 16), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.CAVALIER.ID, 14), (UnitInfo.HALBERDIER.ID, 14)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.ARBALESTER.ID, 18), (SIEGE_ONAGER_ID, 1)],
            10,
        ),
        (
            9, 3240, "Fala 9/14 (54:00 - Imperial Age + PRZEBICIE PRZEZ POLNOCNY LAS!)",
            [(UnitInfo.HALBERDIER.ID, 25), (ELITE_BERSERK_ID, 7), (PETARD_ID, 3), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.HUSKARL.ID, 20), (FLAMING_CAMEL_ID, 4), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(UnitInfo.ARBALESTER.ID, 22), (UnitInfo.ELITE_JANISSARY.ID, 4), (SIEGE_ONAGER_ID, 2)],
            [(IMAM_UNIT_ID, 2), (UnitInfo.PALADIN.ID, 16), (UnitInfo.SIEGE_RAM.ID, 3)],
            [(ELITE_BATTLE_ELEPHANT_ID, 3), (UnitInfo.PALADIN.ID, 15), (UnitInfo.HALBERDIER.ID, 16)],
            [(ELITE_BATTLE_ELEPHANT_ID, 2), (UnitInfo.ARBALESTER.ID, 20), (SIEGE_ONAGER_ID, 2)],
            12,
        ),
    ]

    late_wave_times = {
        10: 3660,
        11: 4110,
        12: 4560,
        13: 5040,
        14: 5520,
    }

    for w_late in range(10, 15):
        m = w_late - 9
        wave_sec = late_wave_times[w_late]
        time_label = f"{wave_sec // 60}:{wave_sec % 60:02d}"
        extra_tag = ""
        if w_late in (10, 12, 14):
            extra_tag += " + ATAK NA TRADE LINE"
        if w_late == 12:
            extra_tag += " + PRZEBICIE PRZEZ LAS"
        wave_title = f"Fala {w_late}/14 ({time_label} - Late Imperial{extra_tag}!)"

        g1_north = [(UnitInfo.HALBERDIER.ID, 25 + m * 3), (ELITE_BERSERK_ID, 7 + m), (PETARD_ID, 3 + (m // 2)), (UnitInfo.SIEGE_RAM.ID, 4)]
        g1_east = [(UnitInfo.HUSKARL.ID, 20 + m * 3), (FLAMING_CAMEL_ID, 3 + (m // 2)), (UnitInfo.SIEGE_RAM.ID, 4)]
        g2_snipers = [(UnitInfo.ARBALESTER.ID, 22 + m * 3), (UnitInfo.ELITE_JANISSARY.ID, 4 + (m // 2)), (SIEGE_ONAGER_ID, 2 + (m // 3))]
        g2_mages = [(IMAM_UNIT_ID, 2 + (m // 3)), (UnitInfo.PALADIN.ID, 16 + m * 3), (UnitInfo.SIEGE_RAM.ID, 4)]
        g3_north = [(ELITE_BATTLE_ELEPHANT_ID, 3 + (m // 2)), (UnitInfo.PALADIN.ID, 16 + m * 3), (UnitInfo.HALBERDIER.ID, 16 + m * 2)]
        g3_east = [(ELITE_BATTLE_ELEPHANT_ID, 3 + (m // 2)), (UnitInfo.ARBALESTER.ID, 20 + m * 3), (SIEGE_ONAGER_ID, 2 + (m // 3))]
        raider_count = 12 + m

        if w_late == 10:
            wave_title = "Fala 10/14 (61:00 - NOC SZAKALI + ATAK NA TRADE LINE!)"
            raider_count = 22
        elif w_late == 11:
            wave_title = "Fala 11/14 (68:30 - NAWALNICA ARTYLERII I SNAJPEROW!)"
            g2_snipers = [(UnitInfo.ARBALESTER.ID, 28), (UnitInfo.ELITE_JANISSARY.ID, 8), (SIEGE_ONAGER_ID, 4)]
            g3_east = [(ELITE_BATTLE_ELEPHANT_ID, 4), (UnitInfo.ARBALESTER.ID, 26), (SIEGE_ONAGER_ID, 4)]
        elif w_late == 13:
            wave_title = "Fala 13/14 (84:00 - STRAZ PRZEDNIA TYTANOW!)"
            g2_mages = [(IMAM_UNIT_ID, 3), (UnitInfo.PALADIN.ID, 28), (UnitInfo.SIEGE_RAM.ID, 4)]
            g3_north = [(ELITE_BATTLE_ELEPHANT_ID, 6), (UnitInfo.PALADIN.ID, 28), (UnitInfo.HALBERDIER.ID, 24)]
            g3_east = [(ELITE_BATTLE_ELEPHANT_ID, 6), (UnitInfo.ARBALESTER.ID, 32), (SIEGE_ONAGER_ID, 3)]

        wave_definitions.append((
            w_late, wave_sec, wave_title,
            g1_north, g1_east, g2_snipers, g2_mages, g3_north, g3_east, raider_count,
        ))
    return [WaveDefinition(*w) for w in wave_definitions]
