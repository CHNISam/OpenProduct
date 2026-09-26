# OpenProduct

OpenProduct v0.1 is a structured Markdown and Git Product graph with deterministic checks, revision-scoped proof and task-relevant context for generic coding agents.

Start with [usage](docs/usage.md), [the canonical contract](spec/README.md), or [repository agent instructions](AGENTS.md). The [frozen implementation obligations](docs/implementation-contract.md) govern the remaining acceptance work. OpenHarness owns repository execution and integration guarantees.

```powershell
python -m openproduct --help
python -X utf8 scripts/validate_contract_compilation.py --self-test
```

The frozen source and Stage 1 compilation evidence are preserved under `docs/provenance` and `docs/compilation`. Runtime evidence is separate.
