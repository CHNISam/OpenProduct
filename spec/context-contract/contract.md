# OpenProduct v0.1 — context-contract

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-016 -->
<a id="s-016"></a>
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


<!-- END S-016 -->

<!-- BEGIN S-036 -->
<a id="s-036"></a>
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


<!-- END S-036 -->

<!-- BEGIN S-037 -->
<a id="s-037"></a>
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


<!-- END S-037 -->

<!-- BEGIN S-038 -->
<a id="s-038"></a>
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


<!-- END S-038 -->
