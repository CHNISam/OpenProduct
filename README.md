# OpenProduct

OpenProduct v0.1 is a structured Markdown and Git Product graph with deterministic checks, revision-scoped proof and task-relevant context for generic coding agents.

## Install

Install directly from GitHub:

```powershell
python -m pip install "git+https://github.com/CHNISam/OpenProduct.git@main"
openproduct --help
```

For reproducible automation, replace `main` with a reviewed commit or release tag. The installed package includes the canonical runtime specification; consuming repositories do not need an OpenProduct source checkout or `PYTHONPATH`.

Start with [usage](docs/usage.md), [the canonical contract](spec/README.md), or [repository agent instructions](AGENTS.md). OpenProduct v0.1 runtime acceptance is closed; OpenHarness owns repository execution and integration guarantees.

```powershell
openproduct --help
python -X utf8 scripts/validate_contract_compilation.py --self-test
```

The frozen source and Stage 1 compilation evidence are preserved under `docs/provenance` and `docs/compilation`. Runtime evidence is separate.
