from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError
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
    paths = packet_paths()
    if not paths:
        print("no packets found")
        return 1

    for path in paths:
        try:
            payload = yaml.safe_load(path.read_text())
            JurisdictionPacket.model_validate(payload)
            print(f"ok  {path.relative_to(ROOT)}")
        except (yaml.YAMLError, ValidationError, ValueError) as exc:
            failures += 1
            print(f"ERR {path.relative_to(ROOT)}\n{exc}")

    if failures:
        print(f"{failures} packet(s) failed validation")
        return 1

    print(f"validated {len(paths)} packet(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
