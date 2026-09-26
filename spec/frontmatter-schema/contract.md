# OpenProduct v0.1 — frontmatter-schema

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-012 -->
<a id="s-012"></a>
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


<!-- END S-012 -->
