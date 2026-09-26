---
id: TASK-2
title: Complete standalone CLI distribution integration
status: Blocked
assignee: []
created_date: '2026-09-26 16:54'
updated_date: '2026-09-26 17:01'
labels: []
dependencies: []
references:
  - 'https://github.com/CHNISam/OpenProduct/issues/9'
  - 'https://github.com/CHNISam/OpenProduct/pull/10'
documentation:
  - docs/usage.md
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Migrated open Issue 9. Existing PR 10 already implements packaging, bundled runtime spec, console entry point and installed-artifact smoke test; its candidate check failed. Resolve that failure and integrate the existing implementation, without starting another packaging task. No source assignee.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Installed CLI works outside checkout with canonical runtime spec
- [ ] #2 Existing PR passes trusted candidate checks and integrates
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Observed existing PR 10 head 8a5756355d3eae31c79807d97118e73be5d5c3d2: trusted verify and openharness / candidate failed; publish succeeded. Unblock by reproducing that candidate failure, correcting the existing PR, and passing trusted checks.

Exact failed candidate cause from trusted run 36251414517: test_built_package_runs_outside_source_checkout_with_spec invokes setup.py in the credential-free sandbox; setuptools is unavailable (ModuleNotFoundError). Preserve standard packaging; address build-test dependency availability through the legitimate verification environment or a compatible smoke-test design.
<!-- SECTION:NOTES:END -->
