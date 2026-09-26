# /goal — Implement OpenProduct v0.1

按当前最新 Operation Protocol 工作。

你现在已经位于 **OpenProduct 仓库根目录**。

该仓库：

```text
already exists
already has Git initialized
already has remote configured
```

不要：

```text
create another repository
re-initialize Git
replace existing remote
create a parallel project
move implementation into another repository
```

先读取当前仓库真实状态，再在**当前仓库**内推进。

---

# Bottom Line

OpenProduct v0.1 Architecture / Contract 已完成设计冻结。

不要重新进行 Architecture Review。

当前阶段：

```text
Contract Freeze
→ Implementation
→ Golden Tests
→ Real Git / Agent Dogfood
```

只有真实实现证据证明 Contract 存在 contradiction 时，才允许重新打开对应的局部 Delta。

核心原则：

```text
Strong semantics,
minimal infrastructure.

Large State,
Small Context.

Flexible proposals,
strict semantic admission.

Stop when sufficient.
Build the Delta.
```

---

# Objective

实现 OpenProduct v0.1：

> 一个面向 Solo Builder + 多个本地 / 云端 AI Agents 的轻量、repo-native、Agent-native Product State & Decision System。

目标状态：

```text
Architecture             CLOSED
Product Boundary         CLOSED
Authority Contract       CLOSED
Representation Contract  CLOSED
Revision Contract        CLOSED
Semantic Diff Contract   CLOSED
CheckProof Contract      CLOSED
Context Contract         CLOSED

Implementation           READY → IMPLEMENTED
```

---

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

# Runtime

OpenProduct v0.1：

```text
Structured Markdown
+
Git
+
Semantic Compiler
+
Progressive Context
+
Direct Repository Editing
+
Lightweight Studio
```

明确不需要：

```text
SQLite
Canonical Database
Remote Database
daemon
Mandatory MCP
Mandatory Command API
Event Store
Full Event Sourcing
Kafka
Saga
Cloud Account
Custom Sync Service
```

Generic Coding Agent 最低只依赖：

```text
Read Files
Edit Files
Git
```

---

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

# Contract A — Product State Authority

## canonicalRef

项目必须拥有唯一：

```yaml
project:
  canonicalRef: refs/heads/main
```

具体 ref 以仓库真实配置为准。

不要擅自假设一定是 `main`。

定义：

```text
canonicalRef
=
designated acceptance boundary
```

不是：

```text
canonicalRef tip
=
automatically Accepted Product State
```

---

# Accepted Product State

设 commit 为 `C`。

只有：

```text
canonicalRef points to C
+
current valid CheckProof
validates exact Product State C
=
PASS
```

才被 OpenProduct 识别为：

```text
Accepted Product State
```

即：

```text
canonicalRef@C
+
ValidCheckProof(C)
=
Accepted Product State
```

如果 canonicalRef 指向：

```text
invalid state
or
state without valid current CheckProof
```

则：

```text
CANONICAL_STATE_INVALID
```

核心：

> **canonicalRef is the acceptance boundary, not the acceptance proof.**

---

# State Classes

```text
Working Tree
=
Draft


Commit on non-canonical branch
=
Proposal Snapshot


Feature Branch / Worktree
=
Proposed Product State


PR
=
Integration Proposal


Validated canonicalRef commit
=
Accepted Product State
```

原则：

> **One Accepted Product State, many proposed states.**

Agent 可以产生非法 Proposal。

Agent 不能让非法 Proposal 被识别为 Accepted。

---

# Acceptance Flow

```text
Draft
 ↓
Proposal
 ↓
Candidate Merge Result
 ↓
openproduct check --all
 ↓
CheckProof
 ↓
┌──────────────┴──────────────┐
│                             │
FAIL                         PASS
│                             │
Revise                canonicalRef may advance
                              │
                              ▼
                     Accepted Product State
```

因此：

```text
commit ≠ accepted
PR ≠ accepted
branch PASS ≠ accepted
```

---

# Contract B — Normative Product Representation

每个 Product Object：

```text
OBJECT.md
├── Frontmatter
│   └── Normative Structural Semantics
├── Canonical Sections
│   └── Normative Product Semantics
└── Free-form Markdown
    └── Non-normative Explanation
```

在当前仓库建立：

```text
/spec/
├── authority-contract/
├── object-schema/
├── frontmatter-schema/
├── canonical-markdown-grammar/
├── relation-schema/
├── revision-rules/
├── semantic-diff/
├── context-contract/
└── errors/
```

目标：

> **两个独立实现面对同一个合法 OpenProduct Project，必须得到相同 Product Semantics。**

---

# Frontmatter Contract

Canonical path：

```text
.openproduct/objects/<type>/<id>.md
```

要求：

```text
filename ID
=
frontmatter ID
```

否则：

```text
OBJECT_ID_MISMATCH
```

Frontmatter specification 必须冻结：

```text
required keys
optional keys
allowed keys
value types
cardinality
unknown-field policy
relation attributes
normalization
ordering
multiline rules
```

未知 normative field：

```text
UNKNOWN_NORMATIVE_FIELD
```

不得自行猜测语义。

---

# Canonical Sections

每种 Object Type 必须定义：

```text
required sections
optional sections
section names
multiplicity
semantic meaning
normalization
```

原则：

> **Each semantic field has exactly one canonical serialization.**

不得让两个等价权威表示同时存在。

---

# Free-form Markdown

例如：

```text
Notes
Background
Discussion
```

默认：

```text
NON-NORMATIVE
```

Parser 禁止：

```text
NLP arbitrary prose
→ infer hidden canonical state
```

---

# Relation Authority

关系只存一次。

例如：

```text
OUT-012
└── requires → CAP-042
```

只由：

```text
OUT-012.md
```

保存。

禁止在 `CAP-042.md` 再保存：

```text
requiredBy: OUT-012
```

Invariant：

> **Relation intent is stored only on the source object's canonical representation.**

反向关系全部 Derived。

---

# current.md

```text
current.md
=
Non-authoritative Context Router
```

允许：

```text
Current Release
Current Focus
Object IDs
Short Labels
Navigation Pointers
Execution References
```

不得成为：

```text
Outcome Authority
Decision Authority
Solution Authority
Capability Authority
Evidence Authority
Proof Authority
Derived State Authority
```

冲突时：

```text
Object wins.
current.md loses.
```

实现：

```bash
openproduct current rebuild
```

使 `current.md` 可从 authoritative state 重建。

---

# SemanticFingerprint(object)

定义：

```text
SemanticFingerprint(object)
=
hash(
  CanonicalSerialize(
    normalized normative frontmatter
    excluding revision
    +
    normalized canonical sections
    +
    normalized source-owned relations
  )
)
```

`revision` **必须排除**。

原因：

```text
SemanticFingerprint
=
What product semantics does this object express?
```

若包含 revision，会形成 revision 与 fingerprint 的循环定义。

同时排除：

```text
formatting
whitespace
non-normative prose
non-semantic ordering
storage formatting noise
```

Canonical serialization 必须 deterministic。

---

# Revision Contract

唯一规则：

```text
SemanticFingerprint changed
→ revision MUST increment exactly by 1

SemanticFingerprint unchanged
→ revision MUST remain unchanged
```

新 Object：

```text
revision = 1
```

已有 Object：

```text
baseline revision = N

fingerprint changed
→ candidate revision = N + 1

fingerprint unchanged
→ candidate revision = N
```

非法情况：

```text
fingerprint changed
+
revision unchanged
→ SEMANTIC_REVISION_ERROR
```

以及：

```text
fingerprint unchanged
+
revision changed
→ SEMANTIC_REVISION_ERROR
```

不要让机器判断：

```text
“只是拼写修改”
“意义应该没变化”
```

只认 normalized fingerprint。

---

# RevisionBaseline

Revision Validation 必须与明确 baseline 比较。

定义：

```text
RevisionBaseline
=
the currently recognized Accepted Product State
immediately preceding candidate acceptance
```

因此：

```text
Accepted Baseline
        vs
Candidate Product State
```

对每个 Candidate Object：

```text
Object absent in baseline
→ new Object
→ revision MUST equal 1


Object exists
+
SemanticFingerprint unchanged
→ revision MUST remain baseline revision


Object exists
+
SemanticFingerprint changed
→ revision MUST equal baseline revision + 1
```

Object deletion 按明确 lifecycle / deletion schema 处理。

如果 canonicalRef 当前没有有效 Accepted State：

```text
CANONICAL_STATE_INVALID
```

不得作为 RevisionBaseline。

---

# Bootstrap

首次没有 Accepted Product State：

```text
RevisionBaseline = NONE
```

所有首批 Object：

```text
revision = 1
```

Bootstrap State 必须：

```text
openproduct check --all
→ PASS
→ valid CheckProof
```

之后才能成为第一个 Accepted Product State。

---

# Relation Change and Revision

任何 source-owned normative relation 改变：

```text
relation added
relation removed
relation target changed
relation attribute changed
```

都会改变：

```text
SemanticFingerprint(sourceObject)
```

因此：

```text
source Object revision +1
```

---

# ProductStateFingerprint — Final Definition

这是整个 Product State 的**精确状态身份**。

与 `SemanticFingerprint(object)` 不同：

```text
SemanticFingerprint
=
object semantic meaning


ProductStateFingerprint
=
exact normative Product State identity
```

正式定义：

```text
ProductStateFingerprint
=
hash(
  CanonicalSerialize(
    normalized normative project configuration
    +
    sorted ObjectStateIdentity[]
  )
)
```

其中：

```text
ObjectStateIdentity
=
{
  id,
  type,
  revision,
  SemanticFingerprint(object)
}
```

**revision 必须包含在 ObjectStateIdentity 中。**

这是硬约束。

---

# Why revision MUST be included

例如合法状态：

```text
content = X
revision = 5
SemanticFingerprint = ABC
```

非法修改：

```text
content = X
revision = 6
SemanticFingerprint = ABC
```

虽然 Object semantics 没变，但：

```text
exact Product State changed
```

因此必须：

```text
ProductStateFingerprint(A)
≠
ProductStateFingerprint(B)
```

从而：

```text
old CheckProof
≠
proof for illegal revision state
```

---

# ProductStateFingerprint Included Scope

必须包含：

```text
normative project configuration

all canonical Product Objects

object id

object type

object revision

object SemanticFingerprint
```

任何：

```text
Object added
Object removed
Object revision changed
Object semantics changed
normative project configuration changed
```

都必须改变：

```text
ProductStateFingerprint
```

Object 顺序使用 `/spec` 中冻结的 deterministic ordering，例如：

```text
type
then id
```

---

# ProductStateFingerprint Excluded Scope

排除：

```text
current.md

non-normative Markdown

formatting / whitespace

unrelated repository files

game / application source code

build artifacts

Git metadata

PR metadata

external Execution state
unless explicitly represented as normative Product State
```

因此：

```text
unrelated source-code change
≠
ProductStateFingerprint change
```

---

# checkedTree Scope

`CheckProof.checkedTree` 不代表整个 Git repository tree。

正式 scope：

```text
checkedTree
=
exact normalized normative OpenProduct input tree
used by the checker
```

它包含：

```text
normative project configuration
+
canonical Product Object representations
including revision
```

排除：

```text
current.md
unrelated repository files
non-normative files
build outputs
```

`checkedCommit` 用于 Git provenance。

Acceptance 的 semantic identity 主要由：

```text
ProductStateFingerprint
+
specFingerprint
+
checkerBuild
```

决定。

---

# CheckProof

```text
CheckProof
├── State Identity
│   ├── checkedCommit
│   ├── checkedTree
│   └── productStateFingerprint
│
├── Ruleset Identity
│   └── specFingerprint
│
├── Checker Identity
│   ├── checkerVersion
│   └── checkerBuild
│
└── result
```

Invariant：

> **A PASS is valid only for the exact Product State, Semantic Ruleset, and Checker Implementation that produced it.**

任意变化：

```text
ProductStateFingerprint changes
specFingerprint changes
checkerBuild changes
```

都会使旧 PASS 无法满足当前 Acceptance Requirement。

---

# specFingerprint

必须是 normative `/spec` 的 deterministic identity。

至少覆盖：

```text
object schema
frontmatter schema
Markdown grammar
relation schema
revision rules
semantic diff rules
authority rules
context rules
validation-relevant error semantics
```

Non-normative documentation 不参与。

---

# Git Diff ≠ Semantic Diff

正式规则：

```text
Git Diff
≠
Semantic Diff
```

例如：

```text
text changed
+
SemanticFingerprint unchanged
=
no Object semantic change
```

而：

```text
SemanticFingerprint changed
=
Object semantic change
```

同时：

```text
revision-only illegal mutation
```

虽然不改变 SemanticFingerprint，

仍然：

```text
ProductStateFingerprint changes
```

从而不能复用旧 CheckProof。

---

# Check Command Contract

## `openproduct check --changed`

Baseline：

```text
Working Tree
vs
HEAD
```

用途：

```text
fast local feedback
```

过程：

```text
Changed Files
↓
Changed Objects
↓
Semantic / Revision Diff
↓
Affected Objects
↓
Semantic Impact Closure
↓
Relevant Invariants
```

如果涉及 Revision correctness，必须使用适用的：

```text
RevisionBaseline
```

而不是只观察当前文件。

---

## `openproduct check --against canonical`

设：

```text
B = merge-base(HEAD, canonicalRef)
T = canonicalRef tip
H = proposal HEAD
```

首先确认：

```text
T
=
currently recognized Accepted Product State
```

否则：

```text
CANONICAL_STATE_INVALID
```

然后比较：

```text
B → T
vs
B → H
```

用于：

```text
STALE_OBJECT
SEMANTIC_CONFLICT
revision conflict
proposal-vs-canonical conflict
```

---

## `openproduct check --all`

定义：

> **Validate the complete current Product Graph against the current spec/checker and, when evaluating a candidate for acceptance, validate revisions against the current RevisionBaseline.**

因此：

```text
check --all
=
Current-State Validation
+
Baseline-Relative Revision Validation
```

Bootstrap 除外。

---

# Exact-State Binding

一次 CheckProof 只对：

```text
ProductStateFingerprint
specFingerprint
checkerBuild
```

的精确组合有效。

如果 Candidate Merge Result、Spec 或 Checker 改变：

```text
previous PASS
=
invalid
```

必须重新执行。

---

# Semantic Impact Closure

不能：

```text
changed file
=
only thing checked
```

必须：

```text
Changed Semantic Objects
↓
Relevant outgoing dependencies
+
Relevant incoming dependencies
↓
Affected Objects
↓
Affected Derived States
↓
Applicable Invariants
```

例如：

```text
Outcome.successCriteria changes
```

可能影响：

```text
Validation applicability
Judgment applicability
Decision basis
Outcome derived state
Capability requirements
```

具体：

```text
relation / field change
→ affected semantic edges
→ applicable checks
```

必须冻结进：

```text
/spec/semantic-diff/
```

不要让实现自行猜 traversal。

---

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

# Capability Target Conflict

`requires` MAY carry：

```text
requestedTarget
scope
criticality
```

v0.1：

```text
Conflict Detection
=
REQUIRED


Automatic Resolution
=
DEFERRED
```

不兼容请求：

```text
Outcome A → CAP-X Target A
Outcome B → CAP-X Target B
```

必须：

```text
CAPABILITY_TARGET_CONFLICT
```

禁止：

```text
first writer wins
latest writer wins
```

如果已有：

```text
Target X
+
valid scoped PASS Verification
```

后来出现冲突 Target Y：

```text
existing Proof remains valid for X
+
new Conflict surfaced separately
```

---

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

# Low-Token Contract

原则：

> **Large State, Small Context.**

OpenProduct 保证：

> **OpenProduct-provided context surfaces MUST scale with task relevance, not total Product State size.**

默认：

```text
Repository Instructions
↓
current.md
↓
Relevant Product Objects
↓
Relevant Decision / Capability / Evidence
↓
Raw Sources only when necessary
```

Whole Graph 是 explicit exceptional operation。

---

# Context Compiler

定义：

```text
RelevantClosure(Task, ProductState, ContextPolicy)
=
R
```

默认 Context 只能由 `R` 生成。

定义：

```text
ContextObjectSet
ContextFingerprint
```

Serialization 必须 deterministic。

---

# Context Isolation

Given：

```text
Task = T
ContextPolicy = P
RelevantClosure(T, StateA, P) = R
```

When：

```text
StateB
=
StateA
+
any number of unrelated Product Objects
```

且：

```text
RelevantClosure(T, StateB, P) = R
```

Then：

```text
ContextObjectSet(A)
=
ContextObjectSet(B)
```

并且：

```text
ContextFingerprint(A)
=
ContextFingerprint(B)
```

且不得出现 unrelated object。

---

# Golden Tests

至少实现：

```text
G-01
Valid state + current valid CheckProof
→ Accepted PASS


G-02
canonicalRef points to invalid/unvalidated state
→ CANONICAL_STATE_INVALID


G-03
Bootstrap Object
→ revision = 1


G-04
Accepted baseline fingerprint A
Candidate fingerprint B
revision unchanged
→ SEMANTIC_REVISION_ERROR


G-05
SemanticFingerprint unchanged
revision incremented
→ SEMANTIC_REVISION_ERROR


G-06
Relation semantic change
→ source Object revision +1 required


G-07
Formatting/non-normative change
→ SemanticFingerprint unchanged


G-08
Duplicate relation authority
→ rejected


G-09
current.md contradicts Object
→ Object remains authority


G-10
Git-clean conflicting Decisions
→ DECISION_CONFLICT


G-11
Stale proposal changes same semantic Object
→ STALE_OBJECT


G-12
Two proposals individually PASS
but merged Product State conflicts
→ check --all FAIL


G-13
Unrelated repository code changes
→ ProductStateFingerprint unchanged


G-14
Canonical Object added / removed / semantics changed
→ ProductStateFingerprint changes


G-15
CheckProof bound to old ProductStateFingerprint
→ invalid for new state


G-16
Unrelated Product Graph growth
→ ContextObjectSet unchanged
→ ContextFingerprint unchanged


G-17
Same Product State
+
specFingerprint changes
→ old PASS invalid


G-18
Same Product State + Spec
+
checkerBuild changes
→ old PASS invalid


G-19
Capability requested targets conflict
→ CAPABILITY_TARGET_CONFLICT


G-20
New conflicting Capability consumer
→ existing scoped valid Proof remains valid


G-21
Old Validation
→ does not prove new Outcome revision


G-22
Generic Coding Agent operates without
SQLite / daemon / MCP / proprietary API


G-23
SemanticFingerprint unchanged
+
revision illegally changes
→ ProductStateFingerprint changes
→ previous CheckProof invalid
→ SEMANTIC_REVISION_ERROR
```

**G-23 是必须的。**

它证明：

```text
Semantic meaning unchanged
≠
exact Product State unchanged
```

---

# Error Model

最低：

```text
CANONICAL_STATE_INVALID

SCHEMA_INVALID
OBJECT_ID_MISMATCH
UNKNOWN_NORMATIVE_FIELD

DANGLING_REFERENCE
INVALID_RELATION
DUPLICATE_RELATION_AUTHORITY

SEMANTIC_REVISION_ERROR

STALE_OBJECT
SEMANTIC_CONFLICT

DECISION_CONFLICT
CAPABILITY_TARGET_CONFLICT

INVALID_CURRENT_REALIZATION

INVALID_VERIFICATION_BINDING
INVALID_VALIDATION_BINDING
PROOF_REVISION_MISMATCH

INVALID_DERIVED_STATE
```

每个 Error：

```text
code
affected object(s)
source location
human explanation
recommended next action
```

---

# Execution Order

你已经位于现有 OpenProduct 仓库根目录。

**不要创建仓库。**

**不要重新初始化 Git。**

**不要替换已有 remote。**

首先：

```text
Inspect repository
↓
Locate current real state
↓
Read existing instructions / code / specs
↓
Identify actual Delta
```

然后按依赖推进：

```text
1. Complete /spec
   ├── authority-contract
   ├── object-schema
   ├── frontmatter-schema
   ├── canonical-markdown-grammar
   ├── relation-schema
   ├── revision-rules
   ├── semantic-diff
   ├── context-contract
   └── errors

2. Implement parser

3. Implement SemanticFingerprint(object)

4. Implement ProductStateFingerprint
   including object revision

5. Implement specFingerprint

6. Implement Product Graph

7. Implement RevisionBaseline resolution

8. Implement invariant engine

9. Implement CheckProof

10. Implement check --changed

11. Implement check --against canonical

12. Implement check --all

13. Implement Semantic Impact Closure

14. Implement Golden Tests G-01…G-23

15. Implement show / find / context

16. Implement NanoPM migration

17. Dogfood on Nameless Reach
    with generic Coding Agents

18. Implement Context Compiler / Copy for Agent

19. Build Studio

20. Retire NanoPM Studio / Viewer
    only after real dogfood gate
```

Do not mechanically redo anything already correctly present in the repository.

Reuse proven capability and build only the Delta.

---

# Constraints

Do NOT:

```text
reopen Architecture Review

create a new repository

reinitialize Git

replace existing remote

introduce SQLite

introduce daemon

introduce Event Sourcing

introduce mandatory MCP

introduce task management

introduce enterprise capabilities

expand ontology for completeness

create duplicate authority

use AI interpretation where deterministic rules suffice
```

如果实现发现真实 contradiction：

```text
Observed Failure
↓
Locate exact violated Contract
↓
Identify minimum required semantic Delta
↓
Fix only that Delta
↓
Re-run proof
```

不要因为局部实现不方便而重构整个系统。

---

# Acceptance

完成条件：

```text
Authority Contract
PASS

Representation Contract
PASS

Revision Contract
PASS

RevisionBaseline
PASS

SemanticFingerprint
PASS

ProductStateFingerprint
PASS

CheckProof
PASS

Semantic Diff
PASS

Semantic Impact Closure
PASS

Context Isolation
PASS

Golden Tests G-01…G-23
PASS

Generic-Agent Dogfood
PASS
```

最终：

```text
Architecture
= CLOSED

Contract Semantics
= CLOSED

Implementation
= PASS
```

---

# Required Final Recap

最终只汇报：

```text
Closed
- ...

Implemented
- ...

Proof
- ...

Dogfood
- ...

Remaining
- ...

Blockers
- None / exact blocker
```

不要重新讲一遍 Architecture。

不要提出 Architecture vNext。

如果 Contract 与全部 Acceptance 已成立：

> **OpenProduct v0.1 Contract is frozen. Continue only with implementation evidence and real-world dogfood.**