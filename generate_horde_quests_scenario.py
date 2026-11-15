from pathlib import Path

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from horde_config import (
    INPUT_TEMPLATE,
    OUTPUT_SCENARIO,
    populate_ingame_scenario_descriptions,
)
from horde_map import build_map_and_entities
from horde_quests import setup_sanctuary_quests_and_victory
from horde_waves import setup_init_aura_and_waves


def build_horde_scenario(output_path: Path | str | None = None) -> Path:
    if not INPUT_TEMPLATE.exists():
        raise FileNotFoundError(f"Nie znaleziono szablonu: {INPUT_TEMPLATE}")

    target_path = Path(output_path) if output_path is not None else OUTPUT_SCENARIO

    scenario = AoE2DEScenario.from_file(str(INPUT_TEMPLATE))
    populate_ingame_scenario_descriptions(scenario)

    ctx = build_map_and_entities(scenario)
    setup_init_aura_and_waves(scenario, ctx)
    setup_sanctuary_quests_and_victory(scenario, ctx)

    scenario.write_to_file(str(target_path))
    print(f"Gotowe! Modularny scenariusz Hordy zapisano w: {target_path}")
    return target_path


if __name__ == "__main__":
    build_horde_scenario()
