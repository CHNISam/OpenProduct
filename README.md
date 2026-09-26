# OpenProduct

OpenProduct v0.1 is a structured Markdown and Git Product graph with deterministic checks, revision-scoped proof and task-relevant context for generic coding agents.

Start with [usage](docs/usage.md), [the canonical contract](spec/README.md), or [repository agent instructions](AGENTS.md). [Backlog.md](docs/execution.md) owns engineering execution state; the [frozen implementation obligations](docs/implementation-contract.md) retain product implementation requirements. OpenHarness retains protected integration and evidence gates, with its legacy work-authority compatibility gap tracked in Backlog.

```powershell
python -m openproduct --help
python -X utf8 scripts/validate_contract_compilation.py --self-test
```

The frozen source and Stage 1 compilation evidence are preserved under `docs/provenance` and `docs/compilation`. Runtime evidence is separate.
