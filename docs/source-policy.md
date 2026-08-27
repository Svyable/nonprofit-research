# Source policy

## Hierarchy

1. Statutes, regulations, official gazettes, official registries, tax agencies, charity regulators, and court decisions.
2. Official forms, filing instructions, fee schedules, portals, and government guidance.
3. Reputable local professional bodies and legal/accounting guidance, labeled secondary.
4. Local nonprofit networks, community references, and user reports, useful for practical friction but not authoritative alone.

Aggregators may be used as navigation aids. They do not replace the official registry or regulator for claims about incorporation requirements.

## Required source metadata

Each source record should include:

- stable `source_id`;
- title and publisher;
- URL;
- source tier;
- legally relevant scope;
- access date;
- effective dates when the source itself is time-bounded;
- precise locator or short excerpt;
- optional SHA-256 checksum or archived snapshot reference;
- `verified_at` when the source supports source-checked or locally reviewed content; and
- a positive `freshness_days` interval when the source supports current operational guidance.

`freshness_days` expresses how long the editorial team is willing to rely on a verification before re-checking it. It is an editorial control, not a statement that law changes on that schedule. Fast-moving sources such as fee schedules, forms, thresholds, and online filing portals should normally receive shorter intervals than stable statutes.

Quotes should be as short as necessary to identify the rule or filing requirement. Store precise locators when possible rather than copying large source passages.

## Promotion rules

An item cannot be `source_checked` unless at least one supporting source is classified above `unverified_lead`, has a verification date, and has an explicit freshness interval.

An item cannot be `local_expert_reviewed` unless the source-checked condition is satisfied and at least one verified supporting source is `official_primary` or `official_interpretive` with a precise locator or excerpt. Local reviewer roles must also be recorded on the item.

## Broken, expired, or changed sources

A broken link is not proof that the law changed. Mark the source for investigation, seek the successor official source, and avoid silently changing the claim until the substance is re-verified.

For operational packets, CI treats a source as expired when `verified_at + freshness_days` is earlier than the check date and the source still supports a current `source_checked` or `local_expert_reviewed` item. Expiry should cause re-verification or an explicit move to `stale`; it must not be bypassed by merely increasing the freshness interval without editorial justification.
