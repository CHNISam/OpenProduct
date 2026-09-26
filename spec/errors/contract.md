# OpenProduct v0.1 — errors

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-040 -->
<a id="s-040"></a>
# Error Model

最低：

```text
CANONICAL_STATE_INVALID

DELIBERATELY_INVALID_PROPOSAL
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


<!-- END S-040 -->
