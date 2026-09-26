# OpenProduct v0.1 — golden

Compiled canonical owner of the clauses below. Source wording is retained verbatim.
Normative requirements retain their force; rationale, examples, background, and presentation remain non-normative.
Implementation obligations describe the subsequent implementation goal; this compilation does not execute them.
Examples do not select unspecified field values, policies, algorithms, or ordering.

<!-- BEGIN S-039 -->
<a id="s-039"></a>
# Golden Tests

至少实现：

```text
G-01
Valid state + current valid CheckProof
→ Accepted PASS


G-02
canonicalRef points to invalid/unvalidated state
→ CANONICAL_STATE_INVALID


G-03
Bootstrap Object
→ revision = 1


G-04
Accepted baseline fingerprint A
Candidate fingerprint B
revision unchanged
→ SEMANTIC_REVISION_ERROR


G-05
SemanticFingerprint unchanged
revision incremented
→ SEMANTIC_REVISION_ERROR


G-06
Relation semantic change
→ source Object revision +1 required


G-07
Formatting/non-normative change
→ SemanticFingerprint unchanged


G-08
Duplicate relation authority
→ rejected


G-09
current.md contradicts Object
→ Object remains authority


G-10
Git-clean conflicting Decisions
→ DECISION_CONFLICT


G-11
Stale proposal changes same semantic Object
→ STALE_OBJECT


G-12
Two proposals individually PASS
but merged Product State conflicts
→ check --all FAIL


G-13
Unrelated repository code changes
→ ProductStateFingerprint unchanged


G-14
Canonical Object added / removed / semantics changed
→ ProductStateFingerprint changes


G-15
CheckProof bound to old ProductStateFingerprint
→ invalid for new state


G-16
Unrelated Product Graph growth
→ ContextObjectSet unchanged
→ ContextFingerprint unchanged


G-17
Same Product State
+
specFingerprint changes
→ old PASS invalid


G-18
Same Product State + Spec
+
checkerBuild changes
→ old PASS invalid


G-19
Capability requested targets conflict
→ CAPABILITY_TARGET_CONFLICT


G-20
New conflicting Capability consumer
→ existing scoped valid Proof remains valid


G-21
Old Validation
→ does not prove new Outcome revision


G-22
Generic Coding Agent operates without
SQLite / daemon / MCP / proprietary API


G-23
SemanticFingerprint unchanged
+
revision illegally changes
→ ProductStateFingerprint changes
→ previous CheckProof invalid
→ SEMANTIC_REVISION_ERROR
```

**G-23 是必须的。**

它证明：

```text
Semantic meaning unchanged
≠
exact Product State unchanged
```

---


<!-- END S-039 -->
