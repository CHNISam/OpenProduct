# OpenProduct v0.1 usage

Run from this source checkout with Python 3.11+ and Git:

```powershell
python -m openproduct --repo PATH init --canonical-ref refs/heads/product
python -m openproduct --repo PATH find
python -m openproduct --repo PATH show OBJECT_ID
python -m openproduct --repo PATH context OBJECT_ID
python -m openproduct --repo PATH check --changed
python -m openproduct --repo PATH check --against canonical
python -m openproduct --repo PATH check --all
```

`PYTHONPATH` may point at this checkout when operating in another repository. No database, daemon, MCP, network service or private Product API is required. `check --changed` compares Working Tree with HEAD; `check --all` validates the complete Working Tree. `check --against canonical` evaluates committed proposal HEAD against its real merge base and the accepted canonical tip; commit a draft resolution before using that mode to verify it. CLI output is JSON. Exit 0 is success, 2 reports an invalid Product state/input. Diagnostics contain codes, affected objects, source locators, explanations and next actions.

The project explicitly configures its canonical Git ref; `main` is not assumed. Objects live at `.openproduct/objects/<type-directory>/<id>.md`. The [canonical definitions](../spec/README.md) specify every type, allowed field, status, section and relation. Frontmatter and config use JSON-form YAML 1.2 with exact `---` frontmatter delimiters. Ordinary YAML shorthand is outside this v0.1 grammar. Duplicate keys and unknown normative fields are rejected.

```markdown
---
{
  "id": "useful-tools",
  "type": "direction",
  "revision": 1,
  "title": "Useful tools",
  "status": "Draft"
}
---
## Intent
Make useful tools.

## Notes
This section is non-normative.
```

A semantic change increments an existing object's revision exactly once against the accepted canonical baseline. A formatting or non-normative edit does not increment it. Relations are authored once on their source object; inverse edges are derived. Capability criteria have their own `targetRevision`. Historical Verification and Validation records remain readable but apply only to their bound criteria/outcome and evidence revisions. Tests alone do not establish Outcome proof.

Bootstrap starts with all objects at revision 1. Commit the normative state, run `check --all --save-proof`, then commit the generated CheckProof. `accepted` recognizes only the configured canonical ref and a current valid proof. A branch check, commit, worktree or PR remains proposed. In an existing product, make changes on a proposal branch, run all three checks, commit the state, generate and commit its all-state proof, and integrate through that repository's actual integration authority. OpenProduct does not own its execution mechanism.

```powershell
python -m openproduct --repo PATH check --all --save-proof
python -m openproduct --repo PATH accepted
python -m openproduct --repo PATH diff --base HEAD
python -m openproduct --repo PATH current rebuild OBJECT_ID
python -m openproduct --repo PATH migrate-nanopm PATH_TO_NANOPM
```

Migration requires an empty initialized target and separate source directory. Explicit NanoPM objective/opportunity/solution section mappings create Draft Product objects. Source-authored opportunity references become source-owned `addresses` relations when both endpoints are mapped. Other source material becomes Evidence of source existence. Original supported files are preserved byte-for-byte under `migration-sources`; imported source claims are never automatically accepted or promoted to PASS.

Normal context requires explicit task object IDs and uses the canonical bounded relevance policy. `--whole` is an intentional exceptional whole-graph request. Neither unrelated graph size nor total Product state enters the context fingerprint. `current rebuild` creates navigation only; it cannot override objects or canonical proof.

Repository verification runs the historical compilation audit and the executable runtime suite. Its source-preservation audit is distinct from Product runtime acceptance and from OpenHarness execution guarantees.

## Context Compiler and Studio

```powershell
python -m openproduct --repo PATH copy-for-agent OBJECT_ID
python -m openproduct --repo PATH studio --whole --output PATH_TO_STUDIO.html
```

Studio is a standalone static HTML projection. Open the generated HTML locally; no server or service is required. It supports object/title search, type filters, source-owned and derived incoming relation navigation, check findings, canonical acceptance status, and task-scoped Copy for Agent/download. The bundle is also readable in the object's details. Regenerate Studio after edits; its displayed state is the generation-time snapshot, never live authority.

After a normative specification or checker build change, old evidence is not current acceptance. On the canonical checkout, rerun `check --all --save-proof` and commit the replacement evidence. Historical baseline provenance is replayed to establish the original transition; FAIL and uncommitted-state artifacts do not constitute acceptance. Revalidation cannot silently reset revisions or skip a different accepted Product state.
