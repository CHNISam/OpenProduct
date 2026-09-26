---
id: TASK-3
title: Finish and verify Meaning Closure implementation
status: Doing
assignee:
  - '@codex'
created_date: '2026-09-26 16:54'
updated_date: '2026-09-26 17:02'
labels: []
dependencies: []
documentation:
  - spec/README.md
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Migrated existing uncommitted meaning-closure implementation. Source ownership was unrecorded. Preserve the current delta across runtime modules, grounding/production/Kitsu adapters, schema extension script and spec definitions; inspect current state before continuing. Existing work is not part of the Backlog integration commit.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Authorized bounded meaning closure has canonical owners and runtime conformance proof
- [ ] #2 Real Git Battle Composite, file-backed production port, SSH signatures, canonical checks, context and Studio verified
- [ ] #3 Kitsu SDK adapter contract tests pass and live instance limitations recorded
- [ ] #4 Canonical audit and legitimate integration pass
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
# Meaning Closure implementation delta

The supplied goal authorizes this bounded extension. Reuse canonical Claim, Evidence,
graph, Git revision admission, context compiler and Studio. Add one historical
`grounding` object (GroundingRelation); content-addressed Evidence represents the
immutable GroundingArtifact. ProductionCase is an adapter boundary outside Product
state, with independent context/case identity. No production schema becomes Product.

Claim dimensions explicitly distinguish REQUIRED, CLEAR, ALLOWED_VARIATION and
UNKNOWN. The resolver cannot interpret prose or certify that a scope is complete.
The configured human owner signs a current scope assessment, acceptance receipts,
and any compatibility judgment needed after uncertain change. The application only
verifies public-key signatures; it never receives the owner's private key.

Accept bytes × Claim revision × dimensions, never all artifact details. Hash real
bytes and retain immutable receipts. Exact effective meaning equality preserves
CURRENT; changed declared dimension values are STALE; other authority changes are
SUSPECT unless the owner explicitly confirms applicability for the new identity.
Unknown assessment, gaps, insufficient capability/source constraints, and missing
Acceptance/Proof contract block Compilation. Execution readiness remains OpenHarness.

Proof: one real Git Battle Composite flow, a file-backed compatible production port,
real SSH signatures, canonical checks, context and Studio, plus Kitsu SDK adapter
contract tests. Live Kitsu testing requires a configured instance. The standalone
latest Model-First Adaptive Protocol was requested but not located; path requested.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Protocol-dependent validation waits for TASK-4; independent implementation may continue. No new assignee is inferred from migration.

Additional concurrent delta observed during migration: __main__.py, compiler.py, context.py, studio.py, spec/README.md, spec/authority-contract/grounding.json and tests/test_grounding_e2e.py. These belong to the same existing implementation, not separate duplicate tasks.

Original plan migrated verbatim and verified via native JSON output. Execution readiness now lives in Backlog; original OpenHarness wording is retained only as historical plan text.

User supplied the protocol repository URL and explicitly said not to pursue it; TASK-4 is no longer a dependency of this implementation. Continuing the authorized bounded delta. Initial canonical audit PASS; baseline runtime 69 tests PASS. Fresh composite verification is running. Test admission corrected to commit the exact Product tree before saving CheckProof. Kitsu live configuration remains unavailable; compatible producer and SDK adapter proof are in scope.
<!-- SECTION:NOTES:END -->
