from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml
from pydantic import ValidationError
from research_centre_atlas.freshness import freshness_failures
from research_centre_atlas.schemas import JurisdictionPacket


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATTERNS = (
    "data/examples/*.yaml",
    "data/jurisdictions/**/packet.yaml",
)


def packet_paths() -> list[Path]:
    paths: set[Path] = set()
    for pattern in PACKET_PATTERNS:
        paths.update(ROOT.glob(pattern))
    return sorted(paths)


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
