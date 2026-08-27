# Contributing

Research Centre Atlas accepts technical, editorial, source, translation, and jurisdiction contributions. Substantive legal content has a higher review bar than ordinary documentation.

## Before opening a pull request

- Identify the legally meaningful jurisdiction scope.
- Identify the route(s), stage(s), and structured IDs affected by the change.
- Use official primary or official interpretive sources where available.
- Put each substantive legal proposition in structured data rather than hiding it only in prose.
- Record source publisher, URL, access date, precise locator or excerpt, verification date, and a justified freshness interval when the source supports current reviewed material.
- Preserve uncertainty and unresolved local-review questions.
- Do not upload passports, signatures, beneficial-owner records, incorporation documents containing personal data, or other sensitive personal information.
- Do not add instructions intended to evade registration, tax, sanctions, AML/CFT, disclosure, fundraising, or other controls.

## Review levels

`draft` → `source_checked` → `local_expert_reviewed`

A status can also move to `stale` or `withdrawn`. A contributor must not self-certify local expertise merely because a source was found.

`source_checked` requires verified, freshness-scoped evidence. `local_expert_reviewed` additionally requires scoped reviewer roles and verified official support with a precise locator or excerpt. See `docs/local-review-rubric.md`.

## Requirements graph

Requirements are bound to a specific `route_id` and `stage_id`. Dependencies must stay within the route and remain acyclic. If a real jurisdiction needs a dependency that cannot be represented under those constraints, open a schema-design issue rather than encoding the relationship ambiguously.

## Pull request checklist

- [ ] Scope and jurisdiction are explicit.
- [ ] Affected route/claim/requirement/obligation IDs are named.
- [ ] Claims and routes have source IDs and controlled statuses.
- [ ] Sources are classified, dated, and freshness-scoped where required.
- [ ] Requirement dependencies are encoded where ordering matters.
- [ ] Uncertainty and local/specialist-review triggers are preserved.
- [ ] Conflicts relevant to local review are disclosed.
- [ ] Examples are clearly marked non-operational.
- [ ] No sensitive personal or incorporation-document data is included.
- [ ] `python scripts/validate_corpus.py` passes.
- [ ] `python scripts/check_freshness.py` passes.
- [ ] `pytest` passes.
- [ ] Generated JSON Schema is current.

See `docs/editorial-standard.md`, `docs/source-policy.md`, `docs/local-review-rubric.md`, and `docs/legal-safety-policy.md`.
