from datetime import date
from pathlib import Path

import yaml
from research_centre_atlas.schemas import JurisdictionPacket

from scripts.check_freshness import freshness_failures


ROOT = Path(__file__).resolve().parents[1]


def _payload() -> dict:
    return yaml.safe_load((ROOT / "data/examples/packet-single-level.yaml").read_text())


def test_non_operational_examples_do_not_fail_freshness():
    packet = JurisdictionPacket.model_validate(_payload())
    assert freshness_failures(packet, today=date(2030, 1, 1)) == []


def test_operational_packet_fails_when_current_evidence_expires():
    payload = _payload()
    payload["publication_status"] = "draft"
    payload["operational"] = True
    source = payload["sources"][0]
    source["source_tier"] = "official_primary"
    source["accessed_at"] = "2026-01-01"
    source["verified_at"] = "2026-01-01"
    source["freshness_days"] = 30
    source["locator"] = "illustrative locator"
    claim = payload["claims"][0]
    claim["review_status"] = "source_checked"
    claim["verified_at"] = "2026-01-01"

    packet = JurisdictionPacket.model_validate(payload)
    failures = freshness_failures(packet, today=date(2026, 3, 1))

    assert failures == ["source src-example-1 verification expired on 2026-01-31"]


def test_reviewed_packet_fails_after_packet_review_due_date():
    payload = _payload()
    payload["publication_status"] = "reviewed"
    payload["operational"] = True
    payload["reviewed_at"] = "2026-01-01"
    payload["next_review_due"] = "2026-02-01"
    payload["reviewer_roles"] = ["local_nonprofit_lawyer"]

    packet = JurisdictionPacket.model_validate(payload)
    failures = freshness_failures(packet, today=date(2026, 3, 1))

    assert failures == ["packet ZZ-EXAMPLE-1 review expired on 2026-02-01"]
