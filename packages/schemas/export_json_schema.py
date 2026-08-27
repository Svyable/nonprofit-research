from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_centre_atlas.schemas import JurisdictionPacket


OUTPUT = Path(__file__).parent / "generated" / "jurisdiction-packet.schema.json"


def render() -> str:
    return json.dumps(JurisdictionPacket.model_json_schema(), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != rendered:
            print(f"{OUTPUT} is out of date; run this script without --check")
            return 1
        print(f"{OUTPUT} is current")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(rendered)
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
