from enum import StrEnum
from pathlib import Path

import yaml
from research_centre_atlas.schemas.models import (
    ApplicabilityStatus,
    ClaimType,
    CoverageArea,
    CoverageStatus,
    PublicationStatus,
    ReviewStatus,
    SourceTier,
)


ROOT = Path(__file__).resolve().parents[1]


def _values(enum_type: type[StrEnum]) -> list[str]:
    return [item.value for item in enum_type]


def test_checked_in_vocabularies_match_executable_schema():
    payload = yaml.safe_load((ROOT / "data/controlled-vocabularies/core.yaml").read_text())

    assert payload["schema_version"] == "0.2.0"
    assert payload["applicability_status"] == _values(ApplicabilityStatus)
    assert payload["source_tier"] == _values(SourceTier)
    assert payload["review_status"] == _values(ReviewStatus)
    assert payload["publication_status"] == _values(PublicationStatus)
    assert payload["coverage_status"] == _values(CoverageStatus)
    assert payload["coverage_area"] == _values(CoverageArea)
    assert payload["claim_type"] == _values(ClaimType)
