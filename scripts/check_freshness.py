from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import yaml
from pydantic import ValidationError
from research_centre_atlas.schemas.models import JurisdictionPacket, PublicationStatus, ReviewStatus


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATTERNS = (
    "data/examples/*.yaml",
    "data/jurisdictions/**/packet.yaml",
)
CURRENT_REVIEW_STATUSES = {ReviewStatus.SOURCE_CHECKED, ReviewStatus.LOCAL_EXPERT_REVIEWED}


def packet_paths() -> list[Path]:
    paths: set[Path] = set()
    for pattern in PACKET_PATTERNS:
        paths.update(ROOT.glob(pattern))
    return sorted(paths)


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


def main() -> int:
    failures = 0
    today = date.today()

    for path in packet_paths():
        try:
            payload = yaml.safe_load(path.read_text())
            packet = JurisdictionPacket.model_validate(payload)
        except (yaml.YAMLError, ValidationError, ValueError) as exc:
            failures += 1
            print(f"ERR {path.relative_to(ROOT)} cannot be freshness-checked\n{exc}")
            continue

        packet_failures = freshness_failures(packet, today=today)
        if packet_failures:
            failures += len(packet_failures)
            for failure in packet_failures:
                print(f"STALE {path.relative_to(ROOT)}: {failure}")
        else:
            print(f"fresh {path.relative_to(ROOT)}")

    if failures:
        print(f"{failures} freshness failure(s)")
        return 1

    print("freshness checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
