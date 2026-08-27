from __future__ import annotations

from datetime import date, timedelta

from .schemas.models import JurisdictionPacket, PublicationStatus, ReviewStatus


CURRENT_REVIEW_STATUSES = {ReviewStatus.SOURCE_CHECKED, ReviewStatus.LOCAL_EXPERT_REVIEWED}


def current_source_ids(packet: JurisdictionPacket) -> set[str]:
    source_ids: set[str] = set()
    for item in [*packet.routes, *packet.claims, *packet.requirements, *packet.obligations]:
        if item.review_status in CURRENT_REVIEW_STATUSES:
            source_ids.update(item.source_ids)
    return source_ids


def freshness_failures(packet: JurisdictionPacket, *, today: date) -> list[str]:
    if not packet.operational:
        return []

    failures: list[str] = []
    if (
        packet.publication_status == PublicationStatus.REVIEWED
        and packet.next_review_due is not None
        and today > packet.next_review_due
    ):
        failures.append(
            f"packet {packet.jurisdiction_id} review expired on {packet.next_review_due.isoformat()}"
        )

    for route in packet.routes:
        if (
            route.review_status in CURRENT_REVIEW_STATUSES
            and route.next_review_due is not None
            and today > route.next_review_due
        ):
            failures.append(
                f"route {route.route_id} review expired on {route.next_review_due.isoformat()}"
            )

    referenced = current_source_ids(packet)
    for source in packet.sources:
        if source.source_id not in referenced:
            continue
        if source.verified_at is None or source.freshness_days is None:
            continue
        due = source.verified_at + timedelta(days=source.freshness_days)
        if today > due:
            failures.append(
                f"source {source.source_id} verification expired on {due.isoformat()}"
            )

    return failures
