# OpenProduct v0.1 — relation-schema

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-015 -->
<a id="s-015"></a>
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


<!-- END S-015 -->

<!-- BEGIN S-034 -->
<a id="s-034"></a>
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


<!-- END S-034 -->
