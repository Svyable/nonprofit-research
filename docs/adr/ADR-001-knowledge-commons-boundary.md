# ADR-001: Knowledge commons, not incorporation service

- **Status:** Accepted for foundation phase
- **Date:** 2026-08-27
- **Decision owners:** Project maintainers

## Context

The institutional goal is portable: make independent, curiosity-driven, public-benefit research centres easier to establish and operate. The legal implementation is not portable. Jurisdictions differ on entity form, charitable or tax recognition, fundraising registration, governance, reporting, employment, banking, cross-border activity, and the level of government that controls each question.

A product framed as "form a nonprofit anywhere" would collapse legally distinct concepts and create pressure to turn uncertain public research into personalized legal conclusions.

## Decision

Research Centre Atlas is a **versioned legal-operations knowledge commons**.

Its primary unit is a jurisdiction packet that can:

1. state exactly where the packet applies;
2. describe one or more candidate legal/regulatory routes;
3. separate entity formation from tax, charity, fundraising, and recurring compliance;
4. encode requirements and dependencies as an auditable graph;
5. attach claim-level evidence and freshness metadata;
6. expose review state and unresolved local-review questions; and
7. produce a counsel-handoff research packet without determining an individual user's legal eligibility.

The platform may explain why a route is `potentially_suitable`, `unknown`, `local_review_required`, or `specialist_review_required`. It must not present a route as a personalized legal recommendation.

## Out of scope for the foundation product

- automated incorporation or government filing submission;
- personalized legal, tax, accounting, banking, immigration, employment, fundraising, sanctions, or data-protection conclusions;
- instructions to evade registration, tax, disclosure, AML/CFT, sanctions, export-control, or similar requirements;
- storage of passports, signatures, beneficial-owner records, or sensitive incorporation documents;
- a conversational legal agent that can outrank the reviewed corpus.

## Consequences

- Corpus quality, source provenance, and review tooling precede UI breadth.
- Real jurisdiction packets require local review before being represented as locally expert reviewed.
- Product interfaces must preserve uncertainty and citation visibility.
- Global expansion happens through jurisdiction-specific editorial work, not by extending generic rules to new countries.
- The independent-research-centre archetype may be shared globally, while legal routes remain local implementations.

## Revisit triggers

Revisit this ADR before adding filing automation, user-specific eligibility scoring, document ingestion, a conversational answer layer, or any workflow that converts research content into an individualized legal action.
