# OpenProduct agent entry point

Work in this repository. Begin with the current Git/worktree state and the actual delta.

## Execution authority: Backlog.md

`backlog/` is the single writable record for engineering backlog, readiness, doing,
blockers, completion, dependencies, ownership, plans and progress. Use the native
Backlog.md CLI; do not maintain parallel Issue checklists, `todos/`, execution plans
under `docs/plans/`, or progress tables in documentation. This instruction supersedes
the historical execution-tracker mappings above and the Issue work-authority wording
in `.harness/AGENT.md`; it does not bypass integration gates.

Run `npx backlog.md@1.53.0 instructions overview` and read its matching creation,
execution or finalization guide before managing work. Prefer an already installed
Backlog.md 1.53.0 binary when available; do not install duplicate copies.
Search/list/view before creating a task. Read its requirement references and
dependencies, assign yourself and set Doing before implementation. Record the plan
and progress through `task edit`; set Blocked with the exact reason and unblock
condition when work cannot continue. Check acceptance criteria only against objective
verification, record the final summary, and set Done when those criteria are met.
Integration-dependent work stays open until its integration criterion is met.

Product Model objects, `/spec` and product decisions own meaning and requirements.
Tasks reference those owners and never redefine them. Backlog's document/decision
features are not additional product authorities. See [execution usage](docs/execution.md)
for native commands, migrated work and the remaining OpenHarness compatibility gap.

Read [the contract index](spec/README.md), then only the owners relevant to the task. The index routes product boundaries, authority, representation, revisions, diffs, context, errors, golden cases, and implementation obligations. Compiled `/spec` is the daily contract authority after the Stage 1 audit passes.

For compilation status and evidence, read [the audit](docs/compilation/README.md) and its validation report. Semantic compilation and runtime enforcement are separate. Run `python -X utf8 scripts/validate_contract_compilation.py` for changes to the compiled environment. This is a compilation audit, not `openproduct check` or a runtime acceptance proof.

Stage 1 is closed and committed separately at `8291a35a45da80b04334171a8f2c2c95437d0784`. The current goal is Stage 2 implementation. Read the frozen [execution order](docs/implementation-contract.md#s-041), [constraints](docs/implementation-contract.md#s-042), and [acceptance](docs/implementation-contract.md#s-043); inspect existing capabilities before building the delta. [Implementation readiness](docs/implementation/readiness.md) records the current first-step specification dependency. Stage 1 audit records are historical evidence, not a live runtime enforcement report.

Architecture and contract semantics are frozen. For the compilation task, report contradictions with exact clause anchors, why both cannot hold, and the minimum affected surface; do not resolve them. The compilation request governs this representation-only task. The frozen implementation constraints govern a subsequent implementation goal. Implementation inconvenience is not evidence for reopening.

Load [immutable provenance](docs/provenance/openproduct-v0.1-frozen.md) only for traceability, suspected compilation error, semantic loss, contradiction, or necessary historical rationale. It is not a second daily authority. Do not normalize or rewrite its bytes. Missing schema details in the source are preserved specification obligations, not permission to invent them during compilation. See [the retained boundaries](docs/compilation/README.md#retained-boundaries).

<!-- OpenHarness entry -->
Read `.harness/AGENT.md` and run `openharness --repo . entry` before managed work.
