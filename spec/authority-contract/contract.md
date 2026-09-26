# OpenProduct v0.1 — authority-contract

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-005 -->
<a id="s-005"></a>
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


<!-- END S-005 -->

<!-- BEGIN S-007 -->
<a id="s-007"></a>
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


<!-- END S-007 -->

<!-- BEGIN S-008 -->
<a id="s-008"></a>
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


<!-- END S-008 -->

<!-- BEGIN S-009 -->
<a id="s-009"></a>
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


<!-- END S-009 -->

<!-- BEGIN S-010 -->
<a id="s-010"></a>
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


<!-- END S-010 -->

<!-- BEGIN S-022 -->
<a id="s-022"></a>
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


<!-- END S-022 -->

<!-- BEGIN S-023 -->
<a id="s-023"></a>
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


<!-- END S-023 -->

<!-- BEGIN S-024 -->
<a id="s-024"></a>
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


<!-- END S-024 -->

<!-- BEGIN S-025 -->
<a id="s-025"></a>
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


<!-- END S-025 -->

<!-- BEGIN S-026 -->
<a id="s-026"></a>
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


<!-- END S-026 -->

<!-- BEGIN S-027 -->
<a id="s-027"></a>
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


<!-- END S-027 -->

<!-- BEGIN S-028 -->
<a id="s-028"></a>
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


<!-- END S-028 -->

<!-- BEGIN S-031 -->
<a id="s-031"></a>
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


<!-- END S-031 -->
