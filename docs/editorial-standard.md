# Editorial standard

## Unit of publication

The canonical unit is a jurisdiction packet for one legally meaningful place. A packet may reference a parent jurisdiction and may contain multiple organizational routes.

## Claim atomization

Every substantive legal statement that drives a checklist, comparison, applicability result, cost, filing, dependency, or recurring obligation must be representable as a structured claim with source IDs.

Prose may explain claims, but prose is not allowed to silently outrank structured data.

## Review promotion

A claim may be `draft`, `source_checked`, `local_expert_reviewed`, `stale`, or `withdrawn`.

To become `local_expert_reviewed`, a claim must have:
- at least one classified source;
- at least one official primary or official interpretive source;
- a precise locator or excerpt for the supporting source;
- a verification date; and
- at least one reviewer role, or a separately documented reason expert review is unavailable (which does **not** permit the `local_expert_reviewed` label).

## Freshness

Every reviewed packet declares a review date and next-review date. Source-specific freshness may be shorter for fee schedules, forms, thresholds, or filing portals.

A stale claim remains visible for auditability but must not be presented as current guidance.

## Corrections

Corrections should name the affected claim IDs, explain what changed, update evidence metadata, and preserve review history in Git.
