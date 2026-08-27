import copy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError
from research_centre_atlas.schemas import JurisdictionPacket


ROOT = Path(__file__).resolve().parents[1]


def test_local_expert_review_cannot_use_unverified_placeholder_source():
    payload = yaml.safe_load((ROOT / "data/examples/packet-single-level.yaml").read_text())
    bad = copy.deepcopy(payload)
    bad["claims"][0]["review_status"] = "local_expert_reviewed"
    bad["claims"][0]["verified_at"] = "2026-08-27"
    bad["claims"][0]["reviewer_roles"] = ["local_nonprofit_lawyer"]

    with pytest.raises(ValidationError, match="needs an official source"):
        JurisdictionPacket.model_validate(bad)
