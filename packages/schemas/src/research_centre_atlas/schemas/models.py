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


class CoverageArea(StrEnum):
    ENTITY_FORMATION = "entity_formation"
    TAX_EXEMPTION = "tax_exemption"
    CHARITABLE_SOLICITATION = "charitable_solicitation"
    GOVERNANCE = "governance"
    RECURRING_COMPLIANCE = "recurring_compliance"
    EMPLOYMENT = "employment"
    IMMIGRATION = "immigration"
    BANKING = "banking"
    CROSS_BORDER_GRANTS = "cross_border_grants"
    FOREIGN_DONATIONS = "foreign_donations"
    GRANTMAKING = "grantmaking"
    DATA_PROTECTION = "data_protection"
    RESEARCH_REGULATION = "research_regulation"
    SANCTIONS_EXPORT_CONTROLS = "sanctions_export_controls"
    POLITICAL_ACTIVITY = "political_activity"


class ClaimType(StrEnum):
    PROCEDURAL = "procedural"
    APPLICABILITY = "applicability"
    FORMATION = "formation"
    GOVERNANCE = "governance"
    TAX = "tax"
    FUNDRAISING = "fundraising"
    COST = "cost"
    TIMING = "timing"
    OBLIGATION = "obligation"
    RISK_ESCALATION = "risk_escalation"
    MODELING_EXAMPLE = "modeling_example"


class Source(StrictModel):
    source_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]+$")
    title: str
    publisher: str
    url: HttpUrl
    source_tier: SourceTier
    scope: list[str] = Field(min_length=1)
    accessed_at: date
    effective_from: date | None = None
    effective_to: date | None = None
    locator: str | None = None
    excerpt: str | None = None
    checksum: str | None = Field(default=None, pattern=r"^(?:sha256:)?[0-9a-fA-F]{64}$")
    snapshot_ref: str | None = None
    verified_at: date | None = None
    freshness_days: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def validate_dates(self) -> "Source":
        if self.effective_from and self.effective_to and self.effective_to < self.effective_from:
            raise ValueError(f"source {self.source_id} effective_to precedes effective_from")
        if self.verified_at and self.verified_at < self.accessed_at:
            raise ValueError(f"source {self.source_id} verified_at precedes accessed_at")
        if self.freshness_days is not None and self.verified_at is None:
            raise ValueError(f"source {self.source_id} freshness_days requires verified_at")
        return self


class Claim(StrictModel):
    claim_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]+$")
    text: str
    claim_type: ClaimType
    source_ids: list[str] = Field(min_length=1)
    route_ids: list[str] = Field(default_factory=list)
    verified_at: date | None = None
    review_status: ReviewStatus = ReviewStatus.DRAFT
    reviewer_roles: list[str] = Field(default_factory=list)


class Stage(StrictModel):
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    title: str


class Route(StrictModel):
    route_id: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    title: str
    entity_family: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    intended_uses: list[str] = Field(default_factory=list)
    suitability: dict[str, ApplicabilityStatus] = Field(default_factory=dict)
    stages: list[Stage] = Field(min_length=1)
    source_ids: list[str] = Field(min_length=1)
    review_status: ReviewStatus = ReviewStatus.DRAFT
    verified_at: date | None = None
    next_review_due: date | None = None
    reviewer_roles: list[str] = Field(default_factory=list)
    disclaimer: str


class Requirement(StrictModel):
    requirement_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]+$")
    title: str
    route_id: str
    stage_id: str
    depends_on: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(min_length=1)
    verified_at: date | None = None
    review_status: ReviewStatus = ReviewStatus.DRAFT
    reviewer_roles: list[str] = Field(default_factory=list)


class Obligation(StrictModel):
    obligation_id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]+$")
    title: str
    cadence: str
    route_ids: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(min_length=1)
    verified_at: date | None = None
    review_status: ReviewStatus = ReviewStatus.DRAFT
    reviewer_roles: list[str] = Field(default_factory=list)


class JurisdictionPacket(StrictModel):
    schema_version: Literal["0.2.0"]
    jurisdiction_id: str = Field(pattern=r"^[A-Z0-9]{2,}(?:-[A-Z0-9]+)*$")
    display_name: str
    parent_jurisdiction_id: str | None = None
    publication_status: PublicationStatus
    operational: bool = False
    reviewed_at: date | None = None
    next_review_due: date | None = None
    reviewer_roles: list[str] = Field(default_factory=list)
    coverage: dict[CoverageArea, CoverageStatus]
    routes: list[Route] = Field(default_factory=list)
    requirements: list[Requirement] = Field(default_factory=list)
    obligations: list[Obligation] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    local_review_questions: list[str] = Field(default_factory=list)
    legal_notice: str

    @staticmethod
    def _ensure_unique(items: list[StrictModel], field: str, label: str) -> None:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for item in items:
            value = getattr(item, field)
            if value in seen:
                duplicates.add(value)
            seen.add(value)
        if duplicates:
            raise ValueError(f"duplicate {label} IDs: {sorted(duplicates)}")

    @staticmethod
    def _find_dependency_cycle(requirements: list[Requirement]) -> list[str] | None:
        graph = {item.requirement_id: item.depends_on for item in requirements}
        visiting: list[str] = []
        visited: set[str] = set()

        def visit(node: str) -> list[str] | None:
            if node in visiting:
                start = visiting.index(node)
                return visiting[start:] + [node]
            if node in visited:
                return None
            visiting.append(node)
            for dependency in graph.get(node, []):
                cycle = visit(dependency)
                if cycle:
                    return cycle
            visiting.pop()
            visited.add(node)
            return None

        for node in graph:
            cycle = visit(node)
            if cycle:
                return cycle
        return None

    @model_validator(mode="after")
    def enforce_integrity(self) -> "JurisdictionPacket":
        if self.publication_status == PublicationStatus.ILLUSTRATIVE and self.operational:
            raise ValueError("illustrative packets cannot be operational")
        if self.publication_status == PublicationStatus.REVIEWED and not self.operational:
            raise ValueError("reviewed packets must be explicitly operational")
        if self.publication_status == PublicationStatus.REVIEWED:
            if self.reviewed_at is None or self.next_review_due is None or not self.reviewer_roles:
                raise ValueError(
                    "reviewed packets require reviewed_at, next_review_due, and reviewer_roles"
                )
        if self.reviewed_at and self.next_review_due and self.next_review_due <= self.reviewed_at:
            raise ValueError("packet next_review_due must be after reviewed_at")

        self._ensure_unique(self.sources, "source_id", "source")
        self._ensure_unique(self.claims, "claim_id", "claim")
        self._ensure_unique(self.routes, "route_id", "route")
        self._ensure_unique(self.requirements, "requirement_id", "requirement")
        self._ensure_unique(self.obligations, "obligation_id", "obligation")

        source_map = {source.source_id: source for source in self.sources}
        route_map = {route.route_id: route for route in self.routes}
        requirement_map = {requirement.requirement_id: requirement for requirement in self.requirements}

        for route in self.routes:
            stage_ids = [stage.id for stage in route.stages]
            if len(stage_ids) != len(set(stage_ids)):
                duplicates = sorted({stage_id for stage_id in stage_ids if stage_ids.count(stage_id) > 1})
                raise ValueError(f"route {route.route_id} has duplicate stage IDs: {duplicates}")
            missing = set(route.source_ids) - source_map.keys()
            if missing:
                raise ValueError(f"route {route.route_id} references missing sources: {sorted(missing)}")
            if route.verified_at and route.next_review_due and route.next_review_due <= route.verified_at:
                raise ValueError(f"route {route.route_id} next_review_due must be after verified_at")
            if route.review_status == ReviewStatus.LOCAL_EXPERT_REVIEWED and route.next_review_due is None:
                raise ValueError(
                    f"route {route.route_id} needs next_review_due for local expert review"
                )
            self._validate_review_gate(
                label=f"route {route.route_id}",
                review_status=route.review_status,
                verified_at=route.verified_at,
                reviewer_roles=route.reviewer_roles,
                source_ids=route.source_ids,
                source_map=source_map,
            )

        for claim in self.claims:
            missing = set(claim.source_ids) - source_map.keys()
            if missing:
                raise ValueError(f"claim {claim.claim_id} references missing sources: {sorted(missing)}")
            missing_routes = set(claim.route_ids) - route_map.keys()
            if missing_routes:
                raise ValueError(f"claim {claim.claim_id} references missing routes: {sorted(missing_routes)}")
            self._validate_review_gate(
                label=f"claim {claim.claim_id}",
                review_status=claim.review_status,
                verified_at=claim.verified_at,
                reviewer_roles=claim.reviewer_roles,
                source_ids=claim.source_ids,
                source_map=source_map,
            )

        for requirement in self.requirements:
            missing_sources = set(requirement.source_ids) - source_map.keys()
            if missing_sources:
                raise ValueError(
                    f"requirement {requirement.requirement_id} references missing sources: {sorted(missing_sources)}"
                )
            route = route_map.get(requirement.route_id)
            if route is None:
                raise ValueError(
                    f"requirement {requirement.requirement_id} references unknown route {requirement.route_id}"
                )
            if requirement.stage_id not in {stage.id for stage in route.stages}:
                raise ValueError(
                    f"requirement {requirement.requirement_id} references unknown stage "
                    f"{requirement.stage_id} in route {requirement.route_id}"
                )
            missing_dependencies = set(requirement.depends_on) - requirement_map.keys()
            if missing_dependencies:
                raise ValueError(
                    f"requirement {requirement.requirement_id} has missing dependencies: "
                    f"{sorted(missing_dependencies)}"
                )
            cross_route = [
                dependency
                for dependency in requirement.depends_on
                if requirement_map[dependency].route_id != requirement.route_id
            ]
            if cross_route:
                raise ValueError(
                    f"requirement {requirement.requirement_id} has cross-route dependencies: "
                    f"{sorted(cross_route)}"
                )
            self._validate_review_gate(
                label=f"requirement {requirement.requirement_id}",
                review_status=requirement.review_status,
                verified_at=requirement.verified_at,
                reviewer_roles=requirement.reviewer_roles,
                source_ids=requirement.source_ids,
                source_map=source_map,
            )

        cycle = self._find_dependency_cycle(self.requirements)
        if cycle:
            raise ValueError(f"requirement dependency cycle: {' -> '.join(cycle)}")

        for obligation in self.obligations:
            missing_sources = set(obligation.source_ids) - source_map.keys()
            if missing_sources:
                raise ValueError(
                    f"obligation {obligation.obligation_id} references missing sources: "
                    f"{sorted(missing_sources)}"
                )
            missing_routes = set(obligation.route_ids) - route_map.keys()
            if missing_routes:
                raise ValueError(
                    f"obligation {obligation.obligation_id} references missing routes: "
                    f"{sorted(missing_routes)}"
                )
            self._validate_review_gate(
                label=f"obligation {obligation.obligation_id}",
                review_status=obligation.review_status,
                verified_at=obligation.verified_at,
                reviewer_roles=obligation.reviewer_roles,
                source_ids=obligation.source_ids,
                source_map=source_map,
            )

        return self

    @staticmethod
    def _validate_review_gate(
        *,
        label: str,
        review_status: ReviewStatus,
        verified_at: date | None,
        reviewer_roles: list[str],
        source_ids: list[str],
        source_map: dict[str, Source],
    ) -> None:
        if review_status not in {ReviewStatus.SOURCE_CHECKED, ReviewStatus.LOCAL_EXPERT_REVIEWED}:
            return
        if verified_at is None:
            raise ValueError(f"{label} needs verified_at for {review_status.value}")

        sources = [source_map[source_id] for source_id in source_ids]
        checked = [
            source
            for source in sources
            if source.source_tier != SourceTier.UNVERIFIED_LEAD
            and source.verified_at is not None
            and source.verified_at <= verified_at
            and source.freshness_days is not None
            and (source.effective_to is None or source.effective_to >= verified_at)
        ]
        if not checked:
            raise ValueError(
                f"{label} needs a verified, freshness-scoped source for {review_status.value}"
            )

        if review_status == ReviewStatus.LOCAL_EXPERT_REVIEWED:
            if not reviewer_roles:
                raise ValueError(f"{label} needs reviewer_roles for local expert review")
            official = [
                source
                for source in checked
                if source.source_tier in {SourceTier.OFFICIAL_PRIMARY, SourceTier.OFFICIAL_INTERPRETIVE}
            ]
            if not official:
                raise ValueError(f"{label} needs an official source")
            if not any(source.locator or source.excerpt for source in official):
                raise ValueError(f"{label} needs a precise official locator or excerpt")


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]
