import copy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError
from research_centre_atlas.schemas import JurisdictionPacket


ROOT = Path(__file__).resolve().parents[1]


def _payload(name: str) -> dict:
    return yaml.safe_load((ROOT / f"data/examples/{name}").read_text())


def test_duplicate_source_ids_are_rejected():
    bad = _payload("packet-single-level.yaml")
    bad["sources"].append(copy.deepcopy(bad["sources"][0]))

    with pytest.raises(ValidationError, match="duplicate source IDs"):
        JurisdictionPacket.model_validate(bad)


def test_requirement_dependency_cycles_are_rejected():
    bad = _payload("packet-multilevel.yaml")
    bad["requirements"][0]["depends_on"] = ["EX2-R2"]

    with pytest.raises(ValidationError, match="requirement dependency cycle"):
        JurisdictionPacket.model_validate(bad)


def test_requirement_stage_is_scoped_to_its_route():
    bad = _payload("packet-single-level.yaml")
    second_route = copy.deepcopy(bad["routes"][0])
    second_route["route_id"] = "second-route"
    second_route["stages"] = [{"id": "other", "title": "Other stage"}]
    bad["routes"].append(second_route)
    bad["requirements"][0]["route_id"] = "second-route"

    with pytest.raises(ValidationError, match="unknown stage form in route second-route"):
        JurisdictionPacket.model_validate(bad)


def test_cross_route_requirement_dependencies_are_rejected():
    bad = _payload("packet-multilevel.yaml")
    second_route = copy.deepcopy(bad["routes"][0])
    second_route["route_id"] = "second-route"
    bad["routes"].append(second_route)
    second_requirement = copy.deepcopy(bad["requirements"][1])
    second_requirement["requirement_id"] = "EX2-R3"
    second_requirement["route_id"] = "second-route"
    second_requirement["depends_on"] = ["EX2-R1"]
    bad["requirements"].append(second_requirement)

    with pytest.raises(ValidationError, match="cross-route dependencies"):
        JurisdictionPacket.model_validate(bad)
