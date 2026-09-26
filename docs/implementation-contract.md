# Frozen implementation obligations

Canonical owner of frozen operational requirements for a subsequent implementation goal.
These are not product data validation rules and are outside normative product /spec identity.
Source requirements retain their force; rationale, presentation, and examples retain their original roles.
Stage 1 only represents these obligations. It does not execute the implementation sequence.
Repeated formulations refer to the primary owner in the compilation ownership register.

<!-- BEGIN S-001 -->
<a id="s-001"></a>
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


<!-- END S-001 -->

<!-- BEGIN S-002 -->
<a id="s-002"></a>
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


<!-- END S-002 -->

<!-- BEGIN S-003 -->
<a id="s-003"></a>
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


<!-- END S-003 -->

<!-- BEGIN S-041 -->
<a id="s-041"></a>
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


<!-- END S-041 -->

<!-- BEGIN S-042 -->
<a id="s-042"></a>
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


<!-- END S-042 -->

<!-- BEGIN S-043 -->
<a id="s-043"></a>
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


<!-- END S-043 -->

<!-- BEGIN S-044 -->
<a id="s-044"></a>
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
<!-- END S-044 -->
