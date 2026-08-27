from pathlib import Path

import yaml
from research_centre_atlas.schemas import JurisdictionPacket


ROOT = Path(__file__).resolve().parents[1]


def test_all_examples_are_non_operational_and_valid():
    paths = sorted((ROOT / "data" / "examples").glob("*.yaml"))
    assert len(paths) == 3
    for path in paths:
        packet = JurisdictionPacket.model_validate(yaml.safe_load(path.read_text()))
        assert packet.publication_status.value == "illustrative"
        assert packet.operational is False
