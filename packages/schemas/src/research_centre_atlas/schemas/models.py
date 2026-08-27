from __future__ import annotations

from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ApplicabilityStatus(StrEnum):
    SUITABLE = "suitable"
    POTENTIALLY_SUITABLE = "potentially_suitable"
    UNSUITABLE = "unsuitable"
    UNKNOWN = "unknown"
    LOCAL_REVIEW_REQUIRED = "local_review_required"
    SPECIALIST_REVIEW_REQUIRED = "specialist_review_required"


class SourceTier(StrEnum):
    OFFICIAL_PRIMARY = "official_primary"
    OFFICIAL_INTERPRETIVE = "official_interpretive"
    PROFESSIONAL_SECONDARY = "professional_secondary"
    COMMUNITY_REFERENCE = "community_reference"
    UNVERIFIED_LEAD = "unverified_lead"


class ReviewStatus(StrEnum):
    DRAFT = "draft"
    SOURCE_CHECKED = "source_checked"
    LOCAL_EXPERT_REVIEWED = "local_expert_reviewed"
    STALE = "stale"
    WITHDRAWN = "withdrawn"


class PublicationStatus(StrEnum):
    ILLUSTRATIVE = "illustrative"
    DRAFT = "draft"
    REVIEWED = "reviewed"
    STALE = "stale"
    WITHDRAWN = "withdrawn"


class CoverageStatus(StrEnum):
    NOT_STARTED = "not_started"
    PLANNED = "planned"
    PARTIAL = "partial"
    COMPLETE = "complete"
    NOT_APPLICABLE = "not_applicable"


class Source(StrictModel):
    source_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]+$")
    title: str
    publisher: str
    url: HttpUrl
    source_tier: SourceTier
    scope: list[str] = Field(min_length=1)
    accessed_at: date
    locator: str | None = None
    excerpt: str | None = None
    checksum: str | None = None
    snapshot_ref: str | None = None
    verified_at: date | None = None


class Claim(StrictModel):
    claim_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]+$")
    text: str
    claim_type: str
    source_ids: list[str] = Field(min_length=1)
    verified_at: date | None = None
    review_status: ReviewStatus = ReviewStatus.DRAFT
    reviewer_roles: list[str] = Field(default_factory=list)


class Stage(StrictModel):
    id: str
    title: str


class Route(StrictModel):
    route_id: str
    title: str
    entity_family: str
    intended_uses: list[str] = Field(default_factory=list)
    suitability: dict[str, ApplicabilityStatus] = Field(default_factory=dict)
    stages: list[Stage] = Field(min_length=1)
    review_status: ReviewStatus = ReviewStatus.DRAFT
    reviewed_at: date | None = None
    next_review_due: date | None = None
    reviewer_roles: list[str] = Field(default_factory=list)
    disclaimer: str


class Requirement(StrictModel):
    requirement_id: str
    title: str
    stage_id: str
    depends_on: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(min_length=1)
    review_status: ReviewStatus = ReviewStatus.DRAFT


class Obligation(StrictModel):
    obligation_id: str
    title: str
    cadence: str
    source_ids: list[str] = Field(min_length=1)
    review_status: ReviewStatus = ReviewStatus.DRAFT


class JurisdictionPacket(StrictModel):
    schema_version: Literal["0.1.0"]
    jurisdiction_id: str
    display_name: str
    parent_jurisdiction_id: str | None = None
    publication_status: PublicationStatus
    operational: bool = False
    coverage: dict[str, CoverageStatus]
    routes: list[Route] = Field(default_factory=list)
    requirements: list[Requirement] = Field(default_factory=list)
    obligations: list[Obligation] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    local_review_questions: list[str] = Field(default_factory=list)
    legal_notice: str

    @model_validator(mode="after")
    def enforce_integrity(self) -> "JurisdictionPacket":
        if self.publication_status == PublicationStatus.ILLUSTRATIVE and self.operational:
            raise ValueError("illustrative packets cannot be operational")
        if self.publication_status == PublicationStatus.REVIEWED and not self.operational:
            raise ValueError("reviewed packets must be explicitly operational")

        source_map = {source.source_id: source for source in self.sources}
        requirement_ids = {requirement.requirement_id for requirement in self.requirements}
        stage_ids = {stage.id for route in self.routes for stage in route.stages}

        for claim in self.claims:
            missing = set(claim.source_ids) - source_map.keys()
            if missing:
                raise ValueError(f"claim {claim.claim_id} references missing sources: {sorted(missing)}")
            if claim.review_status == ReviewStatus.LOCAL_EXPERT_REVIEWED:
                if claim.verified_at is None or not claim.reviewer_roles:
                    raise ValueError(
                        f"claim {claim.claim_id} needs verified_at and reviewer_roles for local expert review"
                    )
                official = [
                    source_map[source_id]
                    for source_id in claim.source_ids
                    if source_map[source_id].source_tier
                    in {SourceTier.OFFICIAL_PRIMARY, SourceTier.OFFICIAL_INTERPRETIVE}
                ]
                if not official:
                    raise ValueError(f"claim {claim.claim_id} needs an official source")
                if not any(source.locator or source.excerpt for source in official):
                    raise ValueError(f"claim {claim.claim_id} needs a precise official locator or excerpt")

        for requirement in self.requirements:
            missing_sources = set(requirement.source_ids) - source_map.keys()
            if missing_sources:
                raise ValueError(
                    f"requirement {requirement.requirement_id} references missing sources: {sorted(missing_sources)}"
                )
            missing_dependencies = set(requirement.depends_on) - requirement_ids
            if missing_dependencies:
                raise ValueError(
                    f"requirement {requirement.requirement_id} has missing dependencies: {sorted(missing_dependencies)}"
                )
            if requirement.stage_id not in stage_ids:
                raise ValueError(
                    f"requirement {requirement.requirement_id} references unknown stage {requirement.stage_id}"
                )

        for obligation in self.obligations:
            missing_sources = set(obligation.source_ids) - source_map.keys()
            if missing_sources:
                raise ValueError(
                    f"obligation {obligation.obligation_id} references missing sources: {sorted(missing_sources)}"
                )

        return self


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]
