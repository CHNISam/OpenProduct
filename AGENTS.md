# OpenProduct agent entry point

Work in this repository. Begin with the current Git/worktree state and the actual delta.

Read [the contract index](spec/README.md), then only the owners relevant to the task. The index routes product boundaries, authority, representation, revisions, diffs, context, errors, golden cases, and implementation obligations. Compiled `/spec` is the daily contract authority after the Stage 1 audit passes.

For compilation status and evidence, read [the audit](docs/compilation/README.md) and its validation report. Semantic compilation and runtime enforcement are separate. Run `python -X utf8 scripts/validate_contract_compilation.py` for changes to the compiled environment. This is a compilation audit, not `openproduct check` or a runtime acceptance proof.

The current task is Stage 1 only: stop after compilation acceptance. Parser, checker, CLI, migrations, dogfood, context runtime, and Studio belong to a separate implementation goal. For that goal, read the frozen [execution order](docs/implementation-contract.md#s-041), [constraints](docs/implementation-contract.md#s-042), and [acceptance](docs/implementation-contract.md#s-043); inspect existing capabilities before building the delta.

Architecture and contract semantics are frozen. For the compilation task, report contradictions with exact clause anchors, why both cannot hold, and the minimum affected surface; do not resolve them. The compilation request governs this representation-only task. The frozen implementation constraints govern a subsequent implementation goal. Implementation inconvenience is not evidence for reopening.

Load [immutable provenance](docs/provenance/openproduct-v0.1-frozen.md) only for traceability, suspected compilation error, semantic loss, contradiction, or necessary historical rationale. It is not a second daily authority. Do not normalize or rewrite its bytes. Missing schema details in the source are preserved specification obligations, not permission to invent them during compilation. See [the retained boundaries](docs/compilation/README.md#retained-boundaries).
