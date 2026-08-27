import copy
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError
from research_centre_atlas.schemas import JurisdictionPacket


ROOT = Path(__file__).resolve().parents[1]


def _promoted_claim_payload() -> dict:
    payload = yaml.safe_load((ROOT / "data/examples/packet-single-level.yaml").read_text())
    promoted = copy.deepcopy(payload)
    promoted["claims"][0]["review_status"] = "local_expert_reviewed"
    promoted["claims"][0]["verified_at"] = "2026-08-27"
    promoted["claims"][0]["reviewer_roles"] = ["local_nonprofit_lawyer"]
    return promoted


def _verified_official_source(payload: dict) -> dict:
    source = payload["sources"][0]
    source["source_tier"] = "official_primary"
    source["verified_at"] = "2026-08-27"
    source["freshness_days"] = 180
    source["locator"] = "illustrative section 1"
    return source


def test_local_expert_review_rejects_unverified_placeholder_source():
    bad = _promoted_claim_payload()

    with pytest.raises(ValidationError, match="verified, freshness-scoped source"):
        JurisdictionPacket.model_validate(bad)


def test_local_expert_review_requires_official_source():
    bad = _promoted_claim_payload()
    source = bad["sources"][0]
    source["source_tier"] = "professional_secondary"
    source["verified_at"] = "2026-08-27"
    source["freshness_days"] = 180
    source["locator"] = "section 1"

    with pytest.raises(ValidationError, match="needs an official source"):
        JurisdictionPacket.model_validate(bad)


def test_local_expert_review_requires_precise_official_support():
    bad = _promoted_claim_payload()
    source = bad["sources"][0]
    source["source_tier"] = "official_primary"
    source["verified_at"] = "2026-08-27"
    source["freshness_days"] = 180

    with pytest.raises(ValidationError, match="precise official locator or excerpt"):
        JurisdictionPacket.model_validate(bad)


def test_local_expert_review_accepts_verified_official_locator():
    good = _promoted_claim_payload()
    _verified_official_source(good)

    JurisdictionPacket.model_validate(good)


def test_review_cannot_predate_source_verification():
    bad = _promoted_claim_payload()
    source = _verified_official_source(bad)
    source["verified_at"] = "2026-08-28"

    with pytest.raises(ValidationError, match="verified, freshness-scoped source"):
        JurisdictionPacket.model_validate(bad)


def test_review_must_fall_inside_source_freshness_window():
    bad = _promoted_claim_payload()
    source = _verified_official_source(bad)
    source["accessed_at"] = "2026-01-01"
    source["verified_at"] = "2026-01-01"
    source["freshness_days"] = 30

    with pytest.raises(ValidationError, match="verified, freshness-scoped source"):
        JurisdictionPacket.model_validate(bad)


def test_review_must_fall_inside_source_effective_period():
    bad = _promoted_claim_payload()
    source = _verified_official_source(bad)
    source["effective_from"] = "2026-09-01"

    with pytest.raises(ValidationError, match="verified, freshness-scoped source"):
        JurisdictionPacket.model_validate(bad)


def test_local_expert_reviewed_route_requires_next_review_due():
    bad = yaml.safe_load((ROOT / "data/examples/packet-single-level.yaml").read_text())
    _verified_official_source(bad)
    route = bad["routes"][0]
    route["review_status"] = "local_expert_reviewed"
    route["verified_at"] = "2026-08-27"
    route["reviewer_roles"] = ["local_nonprofit_lawyer"]

    with pytest.raises(ValidationError, match="needs next_review_due for local expert review"):
        JurisdictionPacket.model_validate(bad)
