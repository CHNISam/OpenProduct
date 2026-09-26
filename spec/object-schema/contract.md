# OpenProduct v0.1 — object-schema

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-004 -->
<a id="s-004"></a>
# Product Boundary

OpenProduct owns：

```text
Direction
Principle
Constraint

Outcome
Opportunity
Solution

Assumption
Experiment

Capability

Evidence
Claim
Judgment

Decision
Risk

Verification
Validation
```

OpenProduct does NOT own：

```text
Task
Backlog lifecycle
Assignee
Sprint
Branch lifecycle
PR lifecycle
Build lifecycle
Developer workload
```

Invariant：

> **Product ≠ Execution**

Execution 只通过 reference / trace 进入 Product Model。

---


<!-- END S-004 -->

<!-- BEGIN S-006 -->
<a id="s-006"></a>
# Canonical Representation

项目级 Product State 位于：

```text
.openproduct/
├── config.yml
├── current.md
└── objects/
    ├── directions/
    ├── principles/
    ├── constraints/
    ├── outcomes/
    ├── opportunities/
    ├── solutions/
    ├── assumptions/
    ├── experiments/
    ├── capabilities/
    ├── evidence/
    ├── claims/
    ├── judgments/
    ├── decisions/
    ├── risks/
    ├── verifications/
    └── validations/
```

定义：

```text
Canonical Product Representation
=
normative .openproduct project data
```

但：

```text
Canonical Representation
≠
Accepted Product State
```

---


<!-- END S-006 -->

<!-- BEGIN S-033 -->
<a id="s-033"></a>
# Core Semantic Invariants

```text
Capability ≠ Implementation

Accepted ≠ Current

Verification ≠ Validation

Evidence ≠ Claim ≠ Judgment

Product ≠ Execution

Projection ≠ Authority

Unknown ≠ Failed

Proof is revision-scoped

Relations have one canonical owner

No silent semantic latest-write-wins
```

Accepted Product State 不得存在：

```text
Closed Gap without applicable PASS Verification

Selected Solution without active selecting Decision

Selected Solution whose selecting Decision is Superseded

Supported Outcome without applicable Judgment

Current Realization without explicit selection

Current Realization whose realization was never Accepted

Active Decision without Basis

Dangling relation

Unsurfaced incompatible Decisions

Silent Capability target winner

Proof silently reused across incompatible revision
```

---


<!-- END S-033 -->

<!-- BEGIN S-035 -->
<a id="s-035"></a>
# Proof Scope

Verification：

```text
Realization
+
Criteria / Target Revision
+
Evidence
```

Validation：

```text
Outcome Revision
+
Success Criteria / Measurement
+
Evidence
```

因此：

```text
Tests PASS
≠
Outcome Proven
```

旧 Proof 可以保留历史意义，但不得自动证明新 Revision。

---


<!-- END S-035 -->
