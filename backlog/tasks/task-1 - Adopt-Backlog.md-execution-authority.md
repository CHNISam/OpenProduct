---
id: TASK-1
title: Adopt Backlog.md execution authority
status: Blocked
assignee:
  - '@codex'
created_date: '2026-09-26 16:54'
updated_date: '2026-09-26 17:02'
labels: []
dependencies:
  - TASK-5
references:
  - 'https://github.com/CHNISam/OpenProduct/issues/11'
documentation:
  - spec/README.md
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
User-authorized migration to one execution authority. Preserve Product meaning, existing dirty work, and protected PR integration. GitHub Issue 11 is the legacy gate binding only.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Current actionable work is migrated without duplication or loss
- [x] #2 Agent guidance routes execution state exclusively to Backlog
- [x] #3 Real runtime task lifecycle is verified
- [ ] #4 Enforced workflow accepts Backlog as sole work authority
- [ ] #5 Changes are committed through legitimate workflow
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Inventory live work; initialize native CLI; migrate work and retire trackers; verify a contract-backed runtime fix; submit a bound PR. Keep Product and integration authorities intact.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Native enforcement gap: OpenHarness model.AUTHORITIES fixes work to github-issues and validate_config rejects Backlog; ci.candidate_context requires an open Issue. Do not claim enforced sole authority until a supported upstream profile exists. Protected AGENTS change additionally needs exact-head/base owner approval after PR submission.

Native Backlog doctor reports no duplicate IDs, self dependencies or cycles. Original meaning-closure plan text equality verified using native JSON output before retiring the competing plan. TASK-5 reached Done after red/green and full 71-test acceptance. Remaining: OpenHarness fixed authority profile cannot attest Backlog; exact-head/base owner approval required for protected AGENTS PR. Unblock enforcement through a supported upstream profile; unblock PR integration through native owner approval and trusted acceptance.
<!-- SECTION:NOTES:END -->
