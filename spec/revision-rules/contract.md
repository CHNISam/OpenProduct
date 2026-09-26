# OpenProduct v0.1 — revision-rules

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-018 -->
<a id="s-018"></a>
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


<!-- END S-018 -->

<!-- BEGIN S-019 -->
<a id="s-019"></a>
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


<!-- END S-019 -->

<!-- BEGIN S-020 -->
<a id="s-020"></a>
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


<!-- END S-020 -->

<!-- BEGIN S-021 -->
<a id="s-021"></a>
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


<!-- END S-021 -->
