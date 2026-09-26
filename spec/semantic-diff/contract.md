# OpenProduct v0.1 — semantic-diff

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-017 -->
<a id="s-017"></a>
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


<!-- END S-017 -->

<!-- BEGIN S-029 -->
<a id="s-029"></a>
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


<!-- END S-029 -->

<!-- BEGIN S-030 -->
<a id="s-030"></a>
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


<!-- END S-030 -->

<!-- BEGIN S-032 -->
<a id="s-032"></a>
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


<!-- END S-032 -->
