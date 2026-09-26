# OpenProduct v0.1 — canonical-markdown-grammar

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-011 -->
<a id="s-011"></a>
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


<!-- END S-011 -->

<!-- BEGIN S-013 -->
<a id="s-013"></a>
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


<!-- END S-013 -->

<!-- BEGIN S-014 -->
<a id="s-014"></a>
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


<!-- END S-014 -->
