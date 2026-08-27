# Data model

The schema is designed around evidence-bearing assertions rather than page-shaped content.

Current foundation schema: `0.2.0`.

## Main objects

- **Jurisdiction packet** — scope, publication state, coverage, packet review dates, routes, requirements, obligations, sources, claims, and unresolved local-review questions.
- **Route** — one candidate entity/regulatory path, its ordered stages, suitability labels, evidence, and review state.
- **Requirement** — a route-scoped node in the dependency graph.
- **Obligation** — a recurring or event-driven post-launch duty, optionally scoped to one or more routes.
- **Claim** — an atomic proposition linked to one or more sources and optionally to relevant routes.
- **Source** — classified evidence with provenance, effective-date, verification, freshness, checksum, and snapshot metadata.

## Why requirements are route-scoped

Stage IDs such as `design`, `form`, or `tax` are intentionally reusable across routes. A requirement therefore carries both `route_id` and `stage_id`. This prevents a requirement from accidentally attaching to the wrong route merely because two routes use the same stage name.

Dependencies are currently restricted to requirements in the same route. If future research demonstrates a need for cross-route or parent-jurisdiction dependencies, that should be introduced as an explicit new dependency type rather than silently weakening the invariant.

## Reviewable evidence

Routes, claims, requirements, and obligations have independent review states. `source_checked` and `local_expert_reviewed` are not cosmetic labels: the executable schema requires verified, freshness-scoped supporting evidence, and local expert review additionally requires official evidence with a precise locator or excerpt plus reviewer roles.

Sources can record:

- `accessed_at`;
- `effective_from` / `effective_to`;
- `verified_at`;
- `freshness_days`;
- `locator` / short `excerpt`;
- SHA-256 `checksum`; and
- `snapshot_ref`.

## Core invariants

- IDs are unique within their object class in a packet.
- Every route, claim, requirement, and obligation references source IDs that exist in the same packet.
- Every route stage ID is unique within that route.
- Every requirement identifies an existing route and a stage on that route.
- Requirement dependencies reference existing requirements on the same route and form an acyclic graph.
- Route references on claims and obligations must resolve.
- `local_expert_reviewed` items require verified official evidence, a locator/excerpt, verification date, freshness interval, and reviewer roles.
- `reviewed` packets must be operational and carry packet-level review dates and reviewer roles.
- Example packets are `illustrative` and must never be operational.
- Coverage areas, claim types, applicability states, source tiers, and review/publication states use controlled vocabularies.

The Pydantic model in `packages/schemas/` is the executable contract. Its generated JSON Schema is checked into the repository for non-Python consumers, and CI verifies that the checked-in schema and controlled-vocabulary file have not drifted from the executable model.
