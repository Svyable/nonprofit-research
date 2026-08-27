# Editorial standard

## Unit of publication

The canonical unit is a jurisdiction packet for one legally meaningful place. A packet may reference a parent jurisdiction and may contain multiple organizational routes.

A packet is not a general country article. Its `jurisdiction_id`, coverage map, routes, review dates, and unresolved questions define the exact boundary of what is being represented.

## Claim atomization

Every substantive legal statement that drives a checklist, comparison, applicability result, cost, filing, dependency, or recurring obligation must be representable as structured data with source IDs.

Prose may explain claims, but prose is not allowed to silently outrank structured data. Route suitability is also evidence-bearing and therefore routes carry source IDs.

## Requirements graph

Requirements are route-scoped nodes. Each requirement names both `route_id` and `stage_id`; a stage name that happens to exist on another route does not make it applicable.

Dependencies must:

- point to existing requirement IDs;
- remain within the same route unless the data model is deliberately extended to represent an external/cross-route dependency; and
- form an acyclic graph.

These constraints prevent a renderer from inventing ordering from prose or from accidentally combining two legal routes.

## Review promotion

A reviewable item may be `draft`, `source_checked`, `local_expert_reviewed`, `stale`, or `withdrawn`.

To become `source_checked`, an item must have a verification date and at least one supporting source that is not an `unverified_lead`, has itself been verified, and has an explicit freshness interval.

To become `local_expert_reviewed`, the source-checked requirements still apply and the item must also have:

- at least one official primary or official interpretive supporting source;
- a precise official locator or excerpt; and
- at least one reviewer role appropriate to the scoped proposition.

See `docs/local-review-rubric.md` for what local review does and does not certify.

## Packet publication

- `illustrative` packets exist only to exercise the schema and must be non-operational.
- `draft` packets may contain research in progress and must not be represented as reviewed guidance.
- `reviewed` packets must be explicitly operational and record packet-level review date, next review date, and reviewer roles.
- `stale` material remains available for auditability but must not be presented as current guidance.
- `withdrawn` material is retained only where useful for history and correction tracing.

## Freshness

Freshness is explicit at two levels:

- reviewed packets and routes can carry a `next_review_due` date; and
- verified sources used by current reviewed items carry `freshness_days`.

CI checks operational packets against those dates. A failed freshness check is a maintenance signal, not proof that the underlying law changed.

## Corrections

Corrections should name the affected claim, route, requirement, or obligation IDs, explain what changed, update evidence metadata, and preserve review history in Git and the pull-request discussion.

Never erase an inconvenient prior state by reusing an identifier for a materially different proposition. Withdraw or supersede it instead.
