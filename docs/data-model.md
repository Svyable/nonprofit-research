# Data model

The schema is designed around evidence-bearing assertions rather than page-shaped content.

## Main objects

- **Jurisdiction packet** — scope, publication state, coverage, routes, requirements, obligations, sources, and claims.
- **Route** — one candidate entity/regulatory path and its ordered stages.
- **Requirement** — a node in the dependency graph.
- **Obligation** — a recurring or event-driven post-launch duty.
- **Claim** — an atomic proposition linked to one or more sources.
- **Source** — classified evidence with provenance and verification metadata.

## Invariants

- Every claim references source IDs that exist in the same packet.
- Every requirement dependency references another requirement in the packet.
- `local_expert_reviewed` claims require official evidence, a source locator/excerpt, verification date, and reviewer roles.
- Example packets are `illustrative` and must never be rendered as reviewed jurisdiction guidance.
- Applicability and suitability fields use controlled vocabularies.

The Pydantic model in `packages/schemas/` is the executable contract. Its generated JSON Schema is checked into the repository for non-Python consumers.
