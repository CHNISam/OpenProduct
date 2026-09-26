# Stage 1 compilation audit

This document and the JSON registers are non-normative compilation evidence. The canonical product contract owners are indexed by [spec/README.md](../../spec/README.md). The frozen operational clauses have one canonical owner in [implementation-contract.md](../implementation-contract.md), outside product ruleset identity. These surfaces retain source text; the audit does not restate normative clauses.

## Source and reconciliation

The input is the complete frozen implementation contract, supplied as a stable readable attachment. Input SHA-256 and byte length were recorded before copying. The repository provenance copy was compared immediately after copying. [source-integrity.json](source-integrity.json) contains the before-compilation baseline; the checker recomputes it from current bytes.

[compilation-map.json](compilation-map.json) records every heading, subheading, and named golden-case region. The 44 top-level regions partition the complete input. Four second-level headings and 23 golden cases are independently reconciled: 71 reviewed regions and 69 source units. Command subcontracts have separate units. The golden policy and 23 cases have disjoint source ranges. Named definitions, invariant lists, and constraint/acceptance blocks stay within their bounded section units; explanatory prose is not split into sentences.

Every region was read during semantic review. All contain decision-relevant requirements or references, including the initial repository instructions, implementation gates, and recap. None was discarded as wholly non-normative. Units can contain rationale/examples: that does not upgrade those passages to rules. `Why revision MUST be included` preserves the example and consequence as an explanation/reference to the state identity rule. Repeated rules are routed by [ownership.json](ownership.json); conformance cases own their scenarios, not duplicate underlying product rules.

The script proves complete structural enumeration, source-range coverage, one declared owner per compiled unit, owner existence, exact verbatim clause identity, explicit independent enforcement dispositions, all G-01 through G-23, navigation anchors, and integrity. Text identity is stronger than a paraphrase-equivalence assertion. Natural-language unitization and rule identity still require semantic review: a green script alone cannot prove every possible semantic omission or detect all conceivable redundant formulations.

## Retained boundaries

The source specifies obligations to freeze field keys/types/cardinality/normalization, per-type sections, deletion/lifecycle treatment, canonical serialization/ordering, impact traversal, and relevant context policies. It does not supply all their concrete values, algorithms, or tables. Compilation preserves those obligations exactly. It does not invent answers, claim schemas are executable, or claim two runtime implementations already have sufficient details for interoperability. These are retained specification deltas in the frozen execution sequence, not lost source semantics and not contradictions established by this audit.

The standalone "latest Operation Protocol" was referenced but not separately supplied or found in the repository. This compilation follows the provided repository instructions and the complete Stage 1 task; it makes no claim to have read an unavailable protocol document.

## Enforcement and stage boundary

At initial inspection, HEAD was `c8a0774` on `main`, the only worktree was this repository, origin was `https://github.com/CHNISam/OpenProduct.git`, and the clean repository contained only `LICENSE`. No existing spec, runtime, harness, routing, or relevant mechanical validation existed: Proof L is `NONE` for pre-existing validation.

Product-contract units have no executable enforcement in this repository. The map distinguishes `COMPILED` from `DEFERRED_TO_IMPLEMENTATION` and `NOT_APPLICABLE`. The G-01 through G-23 cases, revisions, CheckProof, and Context Isolation are compiled and deferred. No product unit is claimed `ENFORCED`. The compilation checker enforces audit bookkeeping/integrity only; it does not implement a parser, graph, fingerprint runtime, checker, CLI, or product test harness.

## Verification

Run from the repository root:

```powershell
python -X utf8 scripts/validate_contract_compilation.py
python -X utf8 scripts/validate_contract_compilation.py --self-test
git diff --check
```

The second command tests rejection of malformed audit states in temporary copies. [validation-report.json](validation-report.json) records the actual run and proof outcomes. The source attachment is checked when still accessible; the repository baseline remains the durable integrity boundary when that external attachment is unavailable later.

Proofs F, H, I, J, and K combine reviewed boundaries, route checks, exact retained execution clauses, and the actual changed-file scope. They do not claim runtime behavior, golden execution, or dogfood. A and B are byte identity checks; C, D, E, and G combine structural checks with the documented semantic review. Compilation acceptance closes only Stage 1. Future implementation must start from actual repository state and its remaining delta; no Stage 2 implementation prompt is prescribed here.
