# Governance

The project separates technical stewardship from authority over substantive legal content.

## Roles

| Role | May do | Accountability |
| --- | --- | --- |
| Research contributor | Open source-backed drafts | Declare sources, scope, and uncertainty |
| Local reviewer | Approve local-law factual content | Relevant expertise and conflict disclosure |
| Editorial maintainer | Merge standardized packets | Enforce schema, source, style, and freshness rules |
| Safety/compliance reviewer | Review high-risk areas | Cross-border funding, sanctions, tax, political activity, regulated data |
| Technical maintainer | Ship platform changes | Must not silently change substantive legal claims |

## Decision rules

- Schema and editorial-policy changes require maintainer review.
- A change that promotes a legal claim to `local_expert_reviewed` requires a reviewer distinct from the original author where practicable.
- Technical refactors must preserve claim text, source links, review state, and history unless the PR explicitly identifies substantive edits.
- Conflicts of interest must be disclosed in the PR or review record.
- Corrections are public and do not erase prior review history.

The project may later establish regional editorial councils. Until then, absence of local expertise is represented as uncertainty, not silently substituted with centralized confidence.
