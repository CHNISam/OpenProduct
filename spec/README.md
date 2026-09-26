# OpenProduct v0.1 canonical contract

This is the compiled daily contract environment. The frozen source is immutable historical provenance. The exact clauses are distributed into the nine frozen directories; the Stage 1 compilation itself supplied no runtime. The implemented runtime and operating guide are linked below.

| Task | Canonical owner |
| --- | --- |
| Accepted state, canonicalRef, state classes, acceptance flow | [authority-contract](authority-contract/contract.md#s-007) |
| Exact state identity, checkedTree, CheckProof, ruleset identity | [authority-contract](authority-contract/contract.md#s-022) |
| Product boundary, project layout, semantic invariants, verification/validation scope | [object-schema](object-schema/contract.md) |
| Frontmatter identity, fields and unknown-field policy obligations | [frontmatter-schema](frontmatter-schema/contract.md) |
| Normative representation, canonical sections, free-form boundary | [canonical-markdown-grammar](canonical-markdown-grammar/contract.md) |
| Source-owned relations and capability target conflicts | [relation-schema](relation-schema/contract.md) |
| Revision, accepted baseline, bootstrap, relation revision changes | [revision-rules](revision-rules/contract.md) |
| Object fingerprint, semantic diff, three check modes, impact closure | [semantic-diff](semantic-diff/contract.md) |
| current.md, task relevance, context compiler, isolation | [context-contract](context-contract/contract.md) |
| Minimum error codes and error records | [errors](errors/contract.md) |
| G-01 through G-23 canonical conformance scenarios | [golden tests](authority-contract/golden-tests.md#s-039) |
| Repository constraints, execution order, implementation acceptance and recap | [implementation obligations](../docs/implementation-contract.md#s-041) |

Read only relevant rows and their dependencies. Golden cases are normative test scenarios; they refer to the underlying rules rather than becoming competing owners of those rules. Repeated formulations in the frozen clauses are retained for fidelity and interpreted as references to the single effective rule owner recorded in the [ownership register](../docs/compilation/ownership.json). The register is routing/traceability, not another source of normative prose.

Normative rules keep their force. Background, examples, rationale, diagrams, and presentation keep their original roles. In particular, the example canonicalRef value is not a mandate for `main`, and the example `type then id` ordering is not a newly selected ordering. The revision rationale illustrates the mandatory inclusion already owned by the state identity definition.

Source identifiers `S-001` through `S-044` delimit verbatim clauses. The [section/unit map](../docs/compilation/compilation-map.json) links their precise provenance line ranges and the 23 named golden cases. It is an audit index, not a contract copy.

## Concrete v0.1 definitions

The current closure goal authorizes completion of the previously unspecified definitions under the frozen owners. These are canonical normative definitions, not runtime guesses or a replacement architecture. Original source clauses and provenance remain unchanged.

- [object-schema/types.json](object-schema/types.json)
- [frontmatter-schema/schema.json](frontmatter-schema/schema.json)
- [canonical-markdown-grammar/sections.json](canonical-markdown-grammar/sections.json)
- [relation-schema/schema.json](relation-schema/schema.json)
- [revision-rules/lifecycle.json](revision-rules/lifecycle.json)
- [semantic-diff/serialization.json](semantic-diff/serialization.json)
- [semantic-diff/impact.json](semantic-diff/impact.json)
- [context-contract/policy.json](context-contract/policy.json)
- [authority-contract/proof.json](authority-contract/proof.json)
- [errors/records.json](errors/records.json)

- [object-schema/migration.json](object-schema/migration.json)

The [operating guide](../docs/usage.md) describes the source-checkout CLI. It is explanatory; the owners above define semantics.
