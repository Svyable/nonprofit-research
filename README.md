# Research Centre Atlas

**Working repository name:** `nonprofit-research`  
**Product name:** `research-centre-atlas`

Research Centre Atlas is a global legal-operations knowledge commons for people building independent, public-benefit research institutions. It publishes versioned, evidence-backed jurisdiction packets describing what organizational forms exist, where a packet applies, the order of filings and dependencies, official costs and recurring obligations, the evidence supporting each claim, and the packet's review status.

The project is **not an incorporation service and not a substitute for local legal, tax, accounting, banking, employment, immigration, fundraising, sanctions, or data-protection advice**. It does not determine personalized legal eligibility, submit government forms, or recommend ways to evade registration, tax, disclosure, sanctions, AML/CFT, or other controls.

## Product thesis

The primary artifact is a **jurisdiction packet**, not a blog post. A packet may describe multiple candidate routes and must separate:

- entity formation from tax or charitable recognition;
- fundraising registration from ordinary corporate registration;
- domestic operations from cross-border grants, donors, staff, and data;
- portable governance practices from locally mandatory rules; and
- official primary sources from interpretive or secondary material.

Routes are described as `potentially_suitable`, `local_review_required`, `unknown`, or similar controlled statuses. The project does not endorse a route for a particular user.

The institutional archetype is an independent, curiosity-driven research centre with minimal teaching and administrative overhead, inspired in part by the London Institute for Mathematical Sciences. That institutional goal is portable; the legal implementation is local and reviewed.

## Repository principles

1. **Corpus first.** Schemas, evidence, and editorial controls precede product interfaces.
2. **Claim-level evidence.** Every substantive legal claim is separable from prose and linked to scoped source metadata.
3. **Review is explicit.** Draft, source-checked, local-expert-reviewed, stale, and withdrawn content are visibly different states.
4. **No false globality.** Coverage is published as complete, partial, draft, stale, or not started.
5. **Readable and forkable.** Legal content and structured data remain independent from the application layer.
6. **Read-only first.** The initial product exposes researched information and exports; it does not file forms or hold sensitive incorporation documents.

## Initial layout

```text
docs/                    Project, safety, editorial, source, and data standards
packages/schemas/        Pydantic contract and generated JSON Schema
data/archetypes/         Portable research-centre archetypes
data/jurisdictions/      Canonical jurisdiction index and reviewed packets
data/examples/            Non-operational packets used to exercise the schema
scripts/                  Corpus validation and maintenance utilities
tests/                    Schema and review-gate tests
.github/workflows/        CI validation
```

The broader monorepo (`apps/`, additional `packages/`, source registry, API, UI, worker, and infrastructure) will be added only as those layers become executable. Empty application directories are deliberately not scaffolded in this PR.

## Development

Requires Python 3.12+.

```bash
python -m pip install -e "packages/schemas[dev]"
python scripts/validate_corpus.py
pytest
python packages/schemas/export_json_schema.py --check
```

## Licensing intent

- Code: AGPL-3.0-or-later
- Editorial/content material: CC-BY-4.0
- Structured jurisdiction data: ODbL-1.0

Exact canonical license texts must be vendored before the first public content release. See `LICENSES/README.md`.

## Status

Foundation phase. The example packets in `data/examples/` are **illustrative and non-operational**. No jurisdiction packet is yet represented as reviewed legal guidance.
