# /goal — Compile the Frozen OpenProduct v0.1 Contract into the Repository

按当前最新 Operation Protocol 工作。

你现在已经位于 **OpenProduct 现有仓库根目录**。

先读取当前仓库真实状态，包括：

- repository-local instructions；
- Git / branch / worktree 状态；
- 已有 spec；
- 已有 docs；
- 已有 tests / validation；
- 已有 implementation；
- 已有 Agent / harness / routing mechanism。

不要：

- 创建另一个 repository；
- re-initialize Git；
- replace existing remote；
- 创建 parallel project；
- 将本任务迁移到其他 repository。

先定位真实状态，再在**当前仓库**内推进。

---

# Bottom Line

本轮不是：

> **Implement OpenProduct v0.1**

本轮只完成一件事：

> **将已经完成多轮评审并正式冻结的 OpenProduct v0.1 Architecture / Contract，无损编译为当前仓库内部持久、repo-native、Agent-native、可导航、可验证的 Canonical Contract Environment。**

提供给你的完整：

> **`/goal — Implement OpenProduct v0.1` Frozen Contract**

是本轮唯一上游设计源。

Architecture / Contract 已完成设计冻结。

不要重新进行 Architecture Review。

当前阶段是：

```text
Frozen Architecture / Contract
            ↓
Stage 1
Contract Compilation
            ↓
Durable Repository Contract Environment
            ↓
STOP
```

OpenProduct v0.1 runtime implementation 属于下一次独立 `/goal`。

---

# Authority

本轮必须严格区分：

```text
Frozen Source
=
upstream design authority for this compilation
```

与：

```text
Compiled Repository Contract
=
future runtime authority after successful compilation
```

本任务没有权限重新设计 Frozen Contract。

你拥有：

```text
representation / materialization authority
```

但不拥有：

```text
semantic modification authority
```

因此：

> **Representation may change. Semantics may not.**

---

# Non-Negotiable Preservation Rule

本轮 Compilation 必须是：

> **semantics-preserving transformation**

Frozen Contract 中所有 decision-relevant semantics：

```text
MUST PRESERVE
```

禁止：

```text
删除语义

弱化语义

增强语义

泛化语义

收窄语义

重新解释语义

为了实现方便修改语义

合并两个不同 distinction

拆分后改变原有 boundary

自行补充新的 normative requirement

自行解决 Frozen Contract 没有解决的问题

将 rationale 意外升级为 normative rule

将 normative rule 降级为普通 explanation
```

不要因为：

```text
实现起来更方便
结构看起来更漂亮
你认为另一种设计更现代
已有代码采用不同模式
某个 schema 更容易写
```

而修改 Frozen Contract。

如果无法证明转换前后等价：

```text
DO NOT GUESS.
```

保留原语义，并记录 exact blocker。

---

# Frozen Source Materialization

在任何 Compilation transformation 发生之前，首先确定提供给当前执行环境的 Frozen Contract 是否存在一个**可稳定读取的原始文件 / byte source**。

分两种情况处理。

## Case A — Stable Input Byte Source Exists

如果 Frozen Contract 以当前 Agent 可读取的稳定原始文件存在：

在任何复制、转换、重新格式化或 repository materialization 之前，记录：

```text
InputFrozenSourceFingerprint
=
SHA-256(exact input source bytes)
```

以及：

```text
InputFrozenSourceByteLength
=
exact input source byte length
```

然后将其 faithful materialize 到当前 repository 内唯一的 canonical provenance location。

优先复用仓库已有符合要求的 provenance / historical-source convention。

不要为了本任务创建不必要的新文档体系。

materialization 后必须计算：

```text
RepositoryFrozenSourceFingerprint
=
SHA-256(exact repository provenance file bytes)
```

以及：

```text
RepositoryFrozenSourceByteLength
=
exact repository provenance file byte length
```

必须证明：

```text
RepositoryFrozenSourceFingerprint
=
InputFrozenSourceFingerprint
```

并且：

```text
RepositoryFrozenSourceByteLength
=
InputFrozenSourceByteLength
```

否则：

```text
COMPILATION_SOURCE_MATERIALIZATION_MISMATCH
→ Compilation FAIL
```

---

## Case B — No Stable Input Byte Source

如果 Frozen Contract 只通过：

```text
conversation text
host-provided context
or another representation without stable readable source bytes
```

提供，

则：

```text
DO NOT fabricate
InputFrozenSourceFingerprint
```

明确记录：

```text
Pre-materialization byte-level source proof
=
UNAVAILABLE
```

此时，首次 faithful repository materialization 后建立的 provenance file，成为后续能够机械验证的 integrity boundary。

`UNAVAILABLE`：

```text
≠ PASS
≠ FAIL
```

它只表示执行环境无法获得 materialization 前的 byte-level identity。

---

# Frozen Source Preservation

无论 Case A 或 Case B，repository provenance file 一旦建立：

它必须保存提供的完整 Frozen Contract。

不得：

```text
rewrite

summarize in place

normalize wording

correct wording

reformat source

delete sections

reorder sections

replace with a shorter version
```

如果仓库已经存在与输入 Frozen Contract 完全对应的 provenance source：

```text
reuse it
```

不要创建第二份竞争副本。

Frozen Source 用于：

```text
provenance

traceability

historical design source

compilation audit

future contradiction investigation
```

Successful Compilation 后，它不再是普通 Agent 日常执行所需的 runtime authority。

---

# Frozen Source Integrity Baseline

repository provenance file 一旦 materialized 并确认：

记录：

```text
FrozenSourceFingerprint
=
SHA-256(exact provenance file bytes)
```

以及：

```text
FrozenSourceByteLength
=
exact provenance file byte length
```

从这一刻开始：

```text
Frozen Source
=
immutable provenance
```

不得：

```text
normalize line endings

rewrite

regenerate

reformat

auto-correct

silently repair

replace
```

该 provenance source。

Compilation 完成后重新计算：

```text
SHA-256(current provenance file bytes)
```

并证明：

```text
current SHA-256
=
FrozenSourceFingerprint
```

同时：

```text
current byte length
=
FrozenSourceByteLength
```

任一不一致：

```text
COMPILATION_SOURCE_MUTATED
→ Compilation FAIL
```

---

# Compilation Objective

将 Frozen Contract 中不同性质的信息，编译到其正确的 durable repository surface。

核心原则：

> **One semantic rule → one effective canonical owner.**

不得通过复制 normative prose 的方式制造多个权威来源。

Compiled environment 应当最终支持：

> **Large State, Small Context.**

未来 Coding Agent 不应需要每次重新读取完整 Frozen Source 才能正确工作。

---

# Compilation Surfaces

## A. Normative Contract Semantics

Frozen Contract 中属于 OpenProduct v0.1 normative semantics 的内容，应进入它自己已经冻结的 canonical `/spec` contract structure。

包括原 Frozen Contract 已明确规定的：

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

不要为了所谓：

```text
better taxonomy
cleaner organization
more modern architecture
```

而修改这套 Frozen structure。

如果仓库已经存在正确内容：

```text
KEEP
```

如果只存在部分：

```text
COMPILE MISSING DELTA
```

如果与 Frozen Contract 冲突：

```text
SURFACE EXACT CONFLICT
```

---

## B. Repository Agent Routing

检查当前仓库已有：

```text
Agent instructions
skills
harness
routing
repository conventions
```

优先：

```text
reuse existing repository convention
```

不要创建 parallel operating system。

Agent routing surface 的职责只是帮助未来 Agent 回答：

```text
当前任务应该读什么？

canonical contract 在哪里？

什么是 frozen？

什么可以变化？

什么 validation 必须运行？

什么证据才允许 reopen？

什么算 completion？

什么才是真正 blocker？
```

它不是 OpenProduct Contract 的第二份副本。

因此：

> **AGENTS.md / equivalent is a map, not the territory.**

不要把 Frozen Contract 全量复制到 always-on instructions。

---

## C. Normative vs Non-Normative

必须忠实保持 Frozen Contract 已经建立的：

```text
Normative
≠
Non-Normative
```

例如：

```text
schema semantics
authority rules
canonical sections
revision rules
semantic invariants
error semantics
```

可以是 normative。

而：

```text
background
rationale
discussion
examples
historical explanation
```

不得因为 Compilation 被偷偷升级为 normative。

反之亦然。

---

## D. Provenance / Rationale

原始 Frozen Source 保持为：

```text
provenance
traceability
historical rationale
compilation audit
contradiction investigation
```

successful Compilation 后：

```text
must not remain a competing runtime authority
```

普通 Coding Agent 默认不需要完整加载它。

只有以下情况才应深入读取：

```text
traceability investigation

possible compilation error

possible semantic loss

possible contract contradiction

historical rationale genuinely required
```

---

# Required Semantic Coverage

Compilation 必须覆盖 Frozen Contract 的全部 decision-relevant semantics。

至少包括：

```text
Product Boundary

Runtime Boundary

Canonical Representation

Product State Authority

canonicalRef

Accepted Product State

State Classes

Acceptance Flow

Normative Product Representation

Frontmatter Contract

Canonical Sections

Free-form Markdown boundary

Relation Authority

current.md authority boundary

SemanticFingerprint

Revision Contract

RevisionBaseline

Bootstrap

Relation Change and Revision

ProductStateFingerprint

ProductStateFingerprint included scope

ProductStateFingerprint excluded scope

checkedTree scope

CheckProof

specFingerprint

Git Diff ≠ Semantic Diff

check --changed

check --against canonical

check --all

Exact-State Binding

Semantic Impact Closure

Core Semantic Invariants

Capability Target Conflict

Verification / Validation Proof Scope

Low-Token Contract

Context Compiler contract

Context Isolation

Golden Tests G-01…G-23

Error Model

Execution Order

Constraints

Acceptance

Required Final Recap
```

这是：

```text
coverage checklist
```

不是重新设计邀请。

此 checklist 不是完整性的唯一证明。

完整性还必须通过后续：

```text
Source Section Reconciliation
+
Source Unit Inventory
+
Compilation Map
```

验证。

---

# Source Section Reconciliation

Source Unit Inventory 本身必须接受完整性检查。

不能仅通过：

```text
UNMAPPED Source Units = 0
```

推断整个 Frozen Source 已完整覆盖。

因为：

```text
a decision-relevant semantic
that was never inventoried
```

不会表现为 `UNMAPPED`。

因此，在建立完整 Source Unit Inventory 前，必须首先对 Frozen Source **全部结构化 source regions** 进行 reconciliation。

一个 source region 应由稳定结构边界识别，例如：

```text
heading
subheading
named contract block
named test block
named invariant block
or equivalent stable source region
```

不要任意按句子切割。

对于 Frozen Source 中每一个 source region，都必须显式记录：

```text
SECTION_REVIEWED
```

然后进一步解析为：

```text
contains Source Units:
- ...
- ...
```

或者，当该 region 确实不承载 decision-relevant semantics 时：

```text
SECTION_NON_NORMATIVE
```

---

# SECTION_NON_NORMATIVE Rule

`SECTION_NON_NORMATIVE` 只能用于明确属于：

```text
rationale

background

example

discussion

historical explanation

navigation-only material

presentation-only material
```

的 section。

不得使用 `SECTION_NON_NORMATIVE` 跳过任何会改变：

```text
authority

meaning

behavior

constraint

acceptance

proof

state identity

revision semantics

validation semantics

error semantics

future implementation requirement

execution-order requirement

reopen condition

completion condition
```

的内容。

---

# Section Reconciliation Invariant

Compilation Acceptance 必须满足：

```text
Unreviewed Frozen Source Sections
=
0
```

以及：

```text
Decision-relevant Sections
without inventoried Source Units
=
0
```

除非该 section 被显式、合理标记为：

```text
SECTION_NON_NORMATIVE
```

任何：

```text
Frozen Source Section
→ neither inventoried nor SECTION_NON_NORMATIVE
```

必须产生：

```text
COMPILATION_SECTION_UNREVIEWED
→ Compilation FAIL
```

因此 Coverage Proof 必须形成：

```text
Frozen Source
        ↓
Every Section Reconciled
        ↓
Every Decision-Relevant Semantic Inventoried
        ↓
Every Source Unit Dispositioned
        ↓
Every COMPILED Normative Unit Has One Canonical Owner
```

---

# Source Unit Inventory

在完成 Section Reconciliation 后，建立一个 compact、auditable 的 Source Unit Inventory。

每个 Source Unit 必须有稳定来源 anchor。

至少包含：

```text
Source Section

Stable Heading / Identifier

Source Range
or equivalent stable locator

Short semantic identity
```

不要把普通 explanatory prose 机械拆成大量 Source Unit。

Unitization 的目标是：

> **覆盖所有可能改变 authority、meaning、behavior、acceptance、proof、constraint、state identity、reopen boundary 或 future implementation 的 decision-relevant semantics。**

第一次 Source Unit Inventory 的完整性属于 semantic review surface。

不要假装自然语言 unitization 本身可以完全通过 hash 自动证明。

但是一旦 Source Unit Inventory 建立：

```text
mapping completeness

disposition completeness

canonical-owner uniqueness
```

应当尽可能机械检查。

---

# Compilation Map

建立 compact Compilation Map：

```text
Frozen Source Unit
→ Canonical Owner
→ Semantic Disposition
→ Enforcement Status
→ Notes / blocker when required
```

Compilation Map：

```text
is traceability
≠ normative authority
```

不得成为第二份 Contract。

---

# Compilation Coverage Model

必须严格区分两个不同维度：

```text
1. Semantic Compilation
2. Enforcement / Implementation Status
```

不要将二者压成一个状态。

---

# Axis 1 — Semantic Disposition

每一个 decision-relevant Frozen Source Unit 必须且只能解析为：

```text
COMPILED
```

或：

```text
BLOCKED
```

对于明确不承载 decision-relevant semantics 的 material，可标记：

```text
NON_NORMATIVE
```

---

## COMPILED

表示：

```text
该语义已经拥有明确 canonical repository owner
```

`COMPILED` 只声明：

```text
semantic contract has been durably represented
```

它不声明：

```text
runtime implementation exists
```

也不声明：

```text
mechanical enforcement exists
```

---

## BLOCKED

表示：

```text
无法在不改变 Frozen semantics 的前提下完成 faithful compilation
```

必须给出：

```text
exact source anchor

exact blocker

why faithful compilation cannot currently complete

minimum affected semantic surface
```

---

## NON_NORMATIVE

仅适用于：

```text
rationale

example

background

discussion

historical explanation

presentation-only content
```

不得使用 `NON_NORMATIVE` 逃避 normative semantic coverage。

---

# Axis 2 — Enforcement Status

对每个 mechanically relevant Source Unit，独立记录：

```text
ENFORCED

DEFERRED_TO_IMPLEMENTATION

NOT_APPLICABLE

BLOCKED
```

---

## ENFORCED

当前 repository 已存在且能够指向实际证据的：

```text
schema

validator

test

lint

guard

runtime check

policy gate

or equivalent deterministic enforcement
```

存在文件本身：

```text
≠ ENFORCED
```

如果声称 `ENFORCED`，必须能够指出它如何对真实 violating state 产生 rejection / failure。

---

## DEFERRED_TO_IMPLEMENTATION

表示：

```text
semantic contract 已经 COMPILED
```

但对应：

```text
runtime

checker

validator

test implementation

CLI

or other enforcement
```

属于 Frozen Execution Order 后续 Stage 2 implementation。

---

## NOT_APPLICABLE

该 Source Unit：

```text
does not require mechanical enforcement
```

例如纯粹的 non-mechanical Human/Product judgment boundary。

---

## BLOCKED

存在真实阻碍，使 enforcement status 无法正确确定或验证。

必须说明 exact blocker。

---

# Critical Distinctions

必须保持：

```text
COMPILED
≠
ENFORCED
```

以及：

```text
DEFERRED_TO_IMPLEMENTATION
≠
semantic contract missing
```

例如：

```text
G-23 semantics
=
COMPILED
```

而：

```text
G-23 executable test implementation
=
DEFERRED_TO_IMPLEMENTATION
```

如果真实 repository 尚未实现它。

不要为了让 Coverage 看起来完整而提前实现 runtime。

---

# Compilation Coverage Invariants

Compilation 必须最终满足：

```text
Unreviewed Frozen Source Sections
=
0
```

```text
Decision-relevant Sections
without inventoried Source Units
=
0
```

```text
UNMAPPED decision-relevant Source Units
=
0
```

```text
decision-relevant COMPILED units
without CanonicalOwner
=
0
```

```text
duplicate effective normative owners
=
0
```

```text
silent semantic omissions
=
0
```

任何：

```text
decision-relevant Source Unit
→ no Semantic Disposition
```

属于：

```text
Compilation FAIL
```

任何：

```text
one semantic rule
→ multiple competing effective normative owners
```

属于：

```text
Compilation FAIL
```

---

# Golden Tests G-01…G-23

Frozen Contract 定义的 G-01…G-23：

```text
MUST preserve semantics exactly.
```

本轮必须确保每一个 Golden Test 都有：

```text
explicit

unique

discoverable

canonical contract representation
```

但本轮不是：

> **implementation of the full test harness**

因此：

如果 executable test 已正确存在：

```text
inspect
preserve
reference
validate when appropriate
```

如果尚未存在：

```text
SemanticDisposition
=
COMPILED
```

并且：

```text
EnforcementStatus
=
DEFERRED_TO_IMPLEMENTATION
```

不要因为本轮名称叫 Contract Compilation，就提前实施 Frozen Contract 已定义在后续 Execution Order 中的：

```text
parser

checker

runtime

CLI

dogfood

Studio
```

---

# Execution Order Preservation

Frozen Contract 已经定义 Implementation Execution Order。

该顺序属于 Frozen Source 的 decision-relevant execution contract。

必须：

```text
preserve
```

不得：

```text
reorder

replace

optimize

reinterpret

collapse

expand into another roadmap
```

本轮只做 Contract Compilation 所必需的 repository materialization。

不要继续进入其后续完整 implementation sequence。

如果某一步已经存在正确 implementation：

```text
inspect

preserve

route

reference
```

不要重做。

---

# Existing Work / Build the Delta

在创建或修改任何 durable surface 前：

```text
Inspect repository
        ↓
Locate current real state
        ↓
Identify existing relevant closure
        ↓
Identify actual compilation Delta
```

对每个需要的 surface 判断：

```text
already correct
→ KEEP

partially correct
→ COMPILE MISSING DELTA

conflicting with Frozen Contract
→ SURFACE EXACT CONFLICT

duplicate authority
→ consolidate only if semantics can be preserved exactly
```

不要机械重做已有正确工作。

遵守：

> **Build the Delta.**

---

# No Architecture Reopen

OpenProduct v0.1 Architecture / Contract：

```text
CLOSED
```

以下都不是 reopen 理由：

```text
implementation inconvenience

repository organization inconvenience

schema complexity

personal design preference

another pattern looks cleaner

another architecture seems more modern

existing implementation differs

tool limitation that can be handled without semantic change
```

只有发现：

```text
Frozen Contract clause A
logically contradicts
Frozen Contract clause B
```

并且两者无法通过 faithful representation 同时成立时，

才允许报告：

```text
CONTRACT_COMPILATION_BLOCKER
```

必须包含：

```text
exact source anchors

exact conflicting semantics

why both cannot simultaneously hold

minimum affected semantic surface
```

本轮：

```text
DO NOT resolve the contradiction yourself.
```

因为本轮没有 semantic modification authority。

---

# Progressive Disclosure

Compilation 完成后，未来普通 Agent 的正常读取路径应当类似：

```text
Repository Instructions
        ↓
Current task / state
        ↓
Task-relevant canonical spec
        ↓
Task-relevant implementation / tests / evidence
        ↓
Deeper source only when necessary
```

而不是：

```text
every task
↓
read entire Frozen Contract
```

但是：

> **Compress context, not semantics.**

Progressive Disclosure 不能成为删除、弱化或隐藏 Contract semantics 的理由。

---

# Explicit Stage 1 Non-Goals

本轮不要执行：

```text
OpenProduct v0.1 runtime implementation

full parser implementation

SemanticFingerprint runtime implementation

ProductStateFingerprint runtime implementation

specFingerprint runtime implementation

Product Graph runtime

RevisionBaseline runtime

invariant engine runtime

CheckProof runtime

check --changed implementation

check --against canonical implementation

check --all implementation

Semantic Impact Closure runtime

full G-01…G-23 executable implementation

show / find / context implementation

NanoPM migration

Nameless Reach dogfood

Context Compiler runtime

Copy for Agent runtime

Studio implementation

NanoPM Studio / Viewer retirement
```

除非某能力已经在当前 repository 正确存在。

此时只能：

```text
inspect

preserve

route

reference

validate where appropriate
```

不要为了本轮重新实现。

---

# Explicit Architecture Non-Goals

不要：

```text
reopen Architecture Review

redesign Product Boundary

redesign authority model

redesign representation model

redesign revision model

redesign semantic diff model

redesign CheckProof

redesign Context Contract

expand ontology for completeness

introduce SQLite

introduce canonical database

introduce remote database

introduce daemon

introduce Event Sourcing

introduce Full Event Sourcing

introduce Kafka

introduce Saga

introduce mandatory MCP

introduce mandatory Command API

introduce Cloud Account

introduce Custom Sync Service

introduce task-management ownership

change Product ≠ Execution

create duplicate authority

use AI interpretation where Frozen deterministic semantics already exist
```

---

# Compilation Proof

不要把：

```text
files created
```

或者：

```text
Agent says preserved
```

当作完成证据。

必须实际验证 Compilation Result。

---

# Proof A — Input-to-Provenance Integrity

如果存在稳定 Input Frozen Source byte source：

证明：

```text
InputFrozenSourceFingerprint
=
RepositoryFrozenSourceFingerprint
```

以及：

```text
InputFrozenSourceByteLength
=
RepositoryFrozenSourceByteLength
```

结果：

```text
PASS
```

如果不存在稳定 pre-materialization byte source：

明确报告：

```text
Pre-materialization byte-level source proof
=
UNAVAILABLE
```

不得伪造 PASS。

---

# Proof B — Frozen Source Post-Compilation Integrity

证明：

```text
FrozenSourceFingerprint before compilation
=
FrozenSourceFingerprint after compilation
```

以及：

```text
FrozenSourceByteLength before compilation
=
FrozenSourceByteLength after compilation
```

必须：

```text
PASS
```

---

# Proof C — Source Section Reconciliation

证明：

```text
Unreviewed Frozen Source Sections
=
0
```

以及：

```text
Decision-relevant Sections
without inventoried Source Units
=
0
```

不得只证明 Unit Map，而不证明 Source Sections 已全部 review。

---

# Proof D — Semantic Coverage

证明：

```text
UNMAPPED decision-relevant Source Units
=
0
```

```text
decision-relevant COMPILED units
without CanonicalOwner
=
0
```

```text
silent semantic omissions
=
0
```

---

# Proof E — Single Authority

证明：

```text
duplicate effective normative owners
=
0
```

每个 COMPILED normative Source Unit：

```text
exactly one effective CanonicalOwner
```

引用、索引和 derived projection 不算 competing authority。

---

# Proof F — Normative Boundary

检查：

```text
normative semantics
没有降级为 explanation
```

以及：

```text
non-normative rationale
没有升级为 hidden normative semantics
```

---

# Proof G — Semantic / Enforcement Separation

证明没有把：

```text
COMPILED
```

错误等价为：

```text
ENFORCED
```

同时没有把：

```text
DEFERRED_TO_IMPLEMENTATION
```

错误解释为：

```text
semantic contract missing
```

抽查至少包括：

```text
G-01…G-23

Revision rules

CheckProof

Context Isolation
```

等关键 contract surface。

---

# Proof H — Agent Discoverability

从 repository-local Agent entry point 出发，

证明一个未来 Agent 可以：

```text
locate the relevant canonical contract owner
```

而无需默认全文读取 Frozen Source。

---

# Proof I — Context Discipline

证明普通任务默认路径：

```text
does not require whole Frozen Contract
```

同时：

```text
all Frozen semantics remain discoverable
```

---

# Proof J — Execution Order Preservation

证明 Frozen Contract 中已有：

```text
Execution Order
```

被忠实保存。

没有：

```text
reorder

replacement

silent optimization

stage collapse
```

---

# Proof K — No Premature Implementation

检查本轮 diff。

证明：

```text
没有越权进入 Stage 2 runtime implementation
```

除非只是：

```text
inspect

preserve

reference

validate
```

已有实现。

---

# Proof L — Existing Repository Validation

运行当前 repository 已存在且与本次 Contract Compilation 直接相关的：

```text
validation

lint

schema check

test

guard

or equivalent relevant check
```

如果不存在适用 mechanical validation：

```text
report NONE
```

不得伪造：

```text
PASS
```

---

# Compilation Acceptance

只有以下全部成立，本轮才允许关闭：

```text
Frozen Source
= materialized once

Input-to-Provenance Integrity
= PASS or honestly UNAVAILABLE where pre-materialization bytes do not exist

Frozen Source post-compilation integrity
= PASS

Architecture semantics
= unchanged

Contract semantics
= unchanged

Unreviewed Frozen Source Sections
= 0

Decision-relevant Sections without Source Units
= 0

UNMAPPED decision-relevant Source Units
= 0

decision-relevant COMPILED units without CanonicalOwner
= 0

Duplicate effective normative authority
= 0

Silent semantic omission
= 0

Normative / non-normative boundary
= preserved

Semantic / Enforcement distinction
= preserved

G-01…G-23 semantics
= preserved

Execution Order
= preserved

Repository Agent routing
= compact and sufficient

Progressive Disclosure
= established

Unauthorized Architecture change
= 0

Unauthorized semantic modification
= 0

Unauthorized Stage 2 implementation
= 0
```

最终应达到：

```text
Frozen Contract
        ↓
semantics-preserving compilation
        ↓
durable repository-native Contract Environment
        ↓
future GPT-6 implementation can start from
a small task-specific /goal
without losing the original design
```

---

# Stop Condition

当且仅当全部 Compilation Acceptance 成立：

```text
Contract Compilation
=
CLOSED
```

然后：

```text
STOP
```

不要继续进入 OpenProduct v0.1 runtime implementation。

不要因为已经理解后续工作而主动开始 Stage 2。

Stage 2 属于下一次独立 `/goal`。

Stage 2 必须根据 Stage 1 完成后的：

```text
real repository state

compiled canonical owners

actual enforcement state

existing implementation

remaining Delta
```

重新编译。

不要现在预设 Stage 2 的详细执行 Prompt。

---

# Required Final Recap

最终只汇报：

```text
Compiled
- ...

Canonical Owners
- ...

Routing
- ...

Section Reconciliation
- Frozen Source Sections: <number>
- Unreviewed Sections: <number>
- Decision-relevant Sections without Source Units: <number>

Coverage
- Source Units: <number>
- UNMAPPED: <number>
- COMPILED without CanonicalOwner: <number>
- Duplicate normative owners: <number>
- Silent omissions: <number>

Enforcement
- ENFORCED: ...
- DEFERRED_TO_IMPLEMENTATION: ...
- NOT_APPLICABLE: ...
- BLOCKED: ...

Source Integrity
- InputFrozenSourceFingerprint: <hash / UNAVAILABLE>
- FrozenSourceFingerprint: <hash>
- FrozenSourceByteLength: <bytes>
- Input-to-Provenance Integrity: PASS / UNAVAILABLE / FAIL
- Post-Compilation Integrity: PASS / FAIL

Preserved
- ...

Proof
- ...

Remaining
- ...

Blockers
- None / exact blocker
```

不要重新讲一遍 OpenProduct Architecture。

不要提出 Architecture vNext。

不要开始 Stage 2 Implementation。

如果全部 Compilation Acceptance 成立：

> **OpenProduct v0.1 Contract Compilation is closed. The frozen design is now durably represented by the repository contract environment. Continue only through a separate implementation goal derived from the resulting real repository state.**