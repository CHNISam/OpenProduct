---
id: TASK-5
title: Return structured errors for non-UTF8 Git output
status: Done
assignee:
  - '@codex'
created_date: '2026-09-26 16:54'
updated_date: '2026-09-26 17:02'
labels: []
dependencies: []
references:
  - openproduct/repository.py
documentation:
  - spec/errors/contract.md#s-040
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Repository.git strictly decodes Git stdout but raises UnicodeDecodeError to library callers. The CLI generic UnicodeError fallback loses Git operation context. Error contract S-040 requires structured diagnostics; translate malformed Git output into ProductError at its boundary without lossy replacement.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Non-UTF8 Git stdout produces SCHEMA_INVALID through ProductError
- [x] #2 CLI returns error JSON and exit 2; full candidate checks pass
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Reproduce malformed UTF-8 at Git subprocess boundary; translate decoder failure into ProductError; assert CLI JSON/exit 2; run candidate checks in isolated clean baseline.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Red regression confirmed: direct Repository.git raises UnicodeDecodeError for both optional and required calls; CLI fallback loses operation context. The dedicated two-test suite fails before the fix.

Verification in bound clean baseline: dedicated two-test regression passes; python -X utf8 scripts/validate_contract_compilation.py --self-test passes 71 runtime tests, G-01 through G-23 and 13 compilation rejection cases; git diff --check passes. Original source/provenance intact. CLI fallback existed previously but library callers now receive ProductError with Git operation context.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed contract S-040 runtime task: Ready to Doing with owner and plan, reproduced malformed UTF-8 error, translated it to SCHEMA_INVALID ProductError, verified CLI JSON/exit 2 and full candidate suite. Two regression tests and all 71 runtime checks pass.
<!-- SECTION:FINAL_SUMMARY:END -->
