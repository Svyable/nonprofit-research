# Contributing

Research Centre Atlas accepts technical, editorial, source, translation, and jurisdiction contributions. Substantive legal content has a higher review bar than ordinary documentation.

## Before opening a pull request

- Identify the legally meaningful jurisdiction scope.
- Use official primary or official interpretive sources where available.
- Put each substantive legal proposition in a structured claim rather than hiding it only in prose.
- Record the source publisher, URL, access date, precise locator or excerpt, and review status.
- Do not upload passports, signatures, beneficial-owner records, incorporation documents containing personal data, or other sensitive personal information.
- Do not add instructions intended to evade registration, tax, sanctions, AML/CFT, disclosure, fundraising, or other controls.

## Review levels

`draft` → `source_checked` → `local_expert_reviewed`

A status can also move to `stale` or `withdrawn`. A contributor must not self-certify local expertise merely because a source was found.

## Pull request checklist

- [ ] Scope and jurisdiction are explicit.
- [ ] Claims have source IDs and controlled statuses.
- [ ] Sources are classified and dated.
- [ ] Dependencies are encoded where ordering matters.
- [ ] Uncertainty and local-review triggers are preserved.
- [ ] Examples are clearly marked non-operational.
- [ ] `python scripts/validate_corpus.py` passes.
- [ ] `pytest` passes.

See `docs/editorial-standard.md`, `docs/source-policy.md`, and `docs/legal-safety-policy.md`.
