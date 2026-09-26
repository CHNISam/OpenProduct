"""Audit the Stage 1 contract materialization, not OpenProduct runtime semantics."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile


class AuditFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def read_json(root: Path, name: str) -> dict:
    return json.loads((root / name).read_text(encoding="utf-8-sig"))


def check(root: Path, *, external_input: bool = True) -> dict:
    baseline = read_json(root, "docs/compilation/source-integrity.json")
    source = (root / baseline["provenancePath"]).read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    require(digest == baseline["FrozenSourceFingerprint"], "COMPILATION_SOURCE_MUTATED: hash")
    require(len(source) == baseline["FrozenSourceByteLength"], "COMPILATION_SOURCE_MUTATED: length")
    require(baseline["InputFrozenSourceFingerprint"] == digest == baseline["RepositoryFrozenSourceFingerprint"], "Input/provenance baseline mismatch")
    require(baseline["InputFrozenSourceByteLength"] == len(source) == baseline["RepositoryFrozenSourceByteLength"], "Input/provenance length mismatch")
    input_status = "RECORDED_PASS; external input no longer available"
    attachment = Path(baseline["inputSource"])
    if external_input and attachment.is_file():
        raw = attachment.read_bytes()
        require(raw == source, "COMPILATION_SOURCE_MATERIALIZATION_MISMATCH")
        input_status = "PASS: current external bytes rechecked"

    m = read_json(root, "docs/compilation/compilation-map.json")
    require(m["source"] == baseline["provenancePath"], "Map source mismatch")
    require(m["authority"].startswith("Traceability only"), "Map must not be normative authority")
    lines = source.splitlines(keepends=True)
    sections, units = m["sections"], m["units"]
    section_ids = [s["id"] for s in sections]
    unit_ids = [u["id"] for u in units]
    require(len(set(section_ids)) == len(section_ids), "Duplicate section ID")
    require(len(set(unit_ids)) == len(unit_ids), "Duplicate source unit")
    sec_by_id = {s["id"]: s for s in sections}
    unit_by_id = {u["id"]: u for u in units}
    top = [s for s in sections if "parent" not in s]
    actual_h1 = [(i + 1, line.decode("utf-8").strip()[2:]) for i, line in enumerate(lines) if line.startswith(b"# ")]
    require([(s["sourceRange"][0], s["heading"]) for s in top] == actual_h1, "COMPILATION_SECTION_UNREVIEWED: top headings")
    expected_regions = []
    for i, line in enumerate(lines):
        if line.startswith(b"# "):
            expected_regions.append((i + 1, line.decode("utf-8").strip()[2:]))
        elif line.startswith(b"## "):
            expected_regions.append((i + 1, line.decode("utf-8").strip()[3:]))
        elif re.fullmatch(rb"G-\d\d\r?\n", line):
            expected_regions.append((i + 1, line.decode().strip()))
    require(sorted((s["sourceRange"][0], s["heading"]) for s in sections) == sorted(expected_regions), "COMPILATION_SECTION_UNREVIEWED: nested/named regions")
    require([s["sourceRange"][1] for s in top] == [x[0] - 1 for x in actual_h1[1:]] + [len(lines)], "Source partition mismatch")

    coverage: Counter = Counter()
    canonical_files = set()
    for s in sections:
        require(s["status"] == "SECTION_REVIEWED", "COMPILATION_SECTION_UNREVIEWED")
        require(s["sourceUnits"], "Decision-relevant section has no units")
        require(all(u in unit_by_id for u in s["sourceUnits"]), "UNMAPPED source unit")
        a, z = s["sourceRange"]
        require(1 <= a <= z <= len(lines), "Invalid section range")
        if "parent" in s:
            parent = sec_by_id[s["parent"]]
            require(parent["sourceRange"][0] <= a <= z <= parent["sourceRange"][1], "Invalid nested region")
            continue
        path = s["canonicalPath"]
        require(path.startswith("spec/") or path == "docs/implementation-contract.md", "Unrecognized canonical surface")
        canonical_files.add(path)
        compiled = (root / path).read_bytes()
        start_marker = f'<!-- BEGIN {s["id"]} -->\n<a id="{s["id"].lower()}"></a>\n'.encode()
        end_marker = f'\n<!-- END {s["id"]} -->'.encode()
        require(compiled.count(start_marker) == 1 and compiled.count(end_marker) == 1, "Duplicate/missing canonical section")
        payload = compiled.split(start_marker, 1)[1].split(end_marker, 1)[0]
        original = b"".join(lines[a - 1:z])
        require(payload == original, "Canonical clause differs from frozen source")
        require(hashlib.sha256(payload).hexdigest() == s["payloadSha256"], "Payload baseline differs")

    for u in units:
        require(u["semanticDisposition"] == "COMPILED", "Source unit missing/blocked disposition")
        require(u["enforcementStatus"] in {"DEFERRED_TO_IMPLEMENTATION", "NOT_APPLICABLE"}, "Unsupported runtime enforcement claim")
        require(u["enforcementEvidence"] is None, "Fabricated product enforcement evidence")
        require(u["boundary"] == "MIXED: requirements normative; source rationale/examples/presentation remain non-normative", "Normative boundary lost")
        s = sec_by_id[u["sourceSection"]]
        require(u["id"] in s["sourceUnits"], "Unit not inventoried in its section")
        owner = u.get("canonicalOwner")
        require(isinstance(owner, dict), "COMPILED without CanonicalOwner")
        require(owner["path"] == s["canonicalPath"] and owner["anchor"] == s["id"].lower() and owner["sourceUnit"] == u["id"], "Canonical owner mismatch")
        require(len(owner["lineRanges"]) == len(u["sourceRanges"]), "Owner locators missing")
        owner_lines = (root / owner["path"]).read_bytes().splitlines(keepends=True)
        for (a, z), (oa, oz) in zip(u["sourceRanges"], owner["lineRanges"]):
            require(s["sourceRange"][0] <= a <= z <= s["sourceRange"][1], "Unit escapes source section")
            coverage.update(range(a, z + 1))
            expected = b"".join(lines[a - 1:z])
            located = b"".join(owner_lines[oa - 1:oz])
            # An input without a final newline needs one framing newline before
            # the END marker. It is not part of the exact section payload above.
            if z == len(lines) and not expected.endswith(b"\n"):
                located = located.removesuffix(b"\n")
            require(expected == located, "Unit canonical locator/text mismatch")
    require(set(coverage) == set(range(1, len(lines) + 1)), "Source lines silently omitted")
    require(all(count == 1 for count in coverage.values()), "Source units overlap")
    require({u for u in unit_ids if u.startswith("G-")} == {f"G-{i:02}" for i in range(1, 24)}, "Golden cases missing")
    for identity in [f"G-{i:02}" for i in range(1, 24)] + ["U-018", "U-019", "U-027", "U-038"]:
        require(unit_by_id[identity]["enforcementStatus"] == "DEFERRED_TO_IMPLEMENTATION", "Critical semantic/enforcement distinction lost")
    require(len(m["coverageChecklist"]) == 43 and len({r["identity"] for r in m["coverageChecklist"]}) == 43, "Coverage checklist incomplete")
    for row in m["coverageChecklist"]:
        require(row["sourceUnits"] == sec_by_id[row["sourceSection"]]["sourceUnits"], "Coverage checklist disconnected")

    ownership = read_json(root, "docs/compilation/ownership.json")
    rules = ownership["rules"]
    require(len({r["ruleIdentity"] for r in rules}) == len(rules), "Duplicate effective normative rule owner")
    for rule in rules:
        primary = sec_by_id[rule["primarySourceSection"]]
        require(rule["effectiveOwner"] == {"path": primary["canonicalPath"], "anchor": primary["id"].lower()}, "Effective rule owner invalid")
        refs = rule["referenceSourceSections"]
        require(len(refs) == len(set(refs)) and primary["id"] not in refs, "Competing effective rule owner")
        require(all(r in sec_by_id for r in refs), "Rule reference missing")

    frozen_dirs = {"authority-contract", "object-schema", "frontmatter-schema", "canonical-markdown-grammar", "relation-schema", "revision-rules", "semantic-diff", "context-contract", "errors"}
    require({p.parent.name for p in (root / "spec").glob("*/contract.md")} == frozen_dirs, "Frozen spec structure changed")
    spec_files = {p for p in canonical_files if p.startswith("spec/")}
    require({p.relative_to(root).as_posix() for p in (root / "spec").rglob("*.md")} == spec_files | {"spec/README.md"}, "Unregistered spec authority")
    for doc in [root / "AGENTS.md", root / "spec/README.md", root / "docs/provenance/README.md", root / "docs/compilation/README.md"]:
        body = doc.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            file, _, anchor = target.partition("#")
            path = (doc.parent / file).resolve()
            require(path.is_relative_to(root.resolve()) and path.is_file(), f"Broken navigation: {target}")
            if anchor.startswith("s-"):
                require(f'id="{anchor}"' in path.read_text(encoding="utf-8"), f"Missing navigation anchor: {target}")
    require("spec/README.md" in (root / "AGENTS.md").read_text(), "No agent contract entry point")
    attributes = (root / ".gitattributes").read_text()
    for guard in ["/docs/provenance/*.md -text", "/spec/*/contract.md -text", "/spec/authority-contract/golden-tests.md -text", "/docs/implementation-contract.md -text"]:
        require(guard in attributes, "Verbatim source/payload Git normalization guard missing")
    return {
        "result": "PASS",
        "sourceFingerprint": digest,
        "sourceByteLength": len(source),
        "inputToProvenanceIntegrity": input_status,
        "postCompilationIntegrity": "PASS",
        "topLevelSections": len(top),
        "frozenSourceSections": len(sections),
        "unreviewedSections": 0,
        "decisionRelevantSectionsWithoutUnits": 0,
        "sourceUnits": len(units),
        "unmapped": 0,
        "compiledWithoutCanonicalOwner": 0,
        "duplicateDeclaredEffectiveNormativeOwners": 0,
        "sourceLinesOmitted": 0,
        "canonicalFiles": len(canonical_files),
        "registeredRepeatedRuleIdentities": len(rules),
        "enforcement": dict(Counter(u["enforcementStatus"] for u in units)),
        "limitations": "Semantic unitization and underlying rule identity are reviewed judgments; structural and text checks do not independently prove natural-language completeness. No product runtime/golden execution is asserted.",
    }


def self_test(root: Path) -> list[str]:
    passed = []
    with tempfile.TemporaryDirectory(prefix="openproduct-compilation-audit-") as temp:
        dest = Path(temp) / "repo"
        def fresh():
            if dest.exists():
                require(dest.resolve().is_relative_to(Path(temp).resolve()) and dest.resolve() != Path(temp).resolve(), "Unsafe temporary cleanup target")
                shutil.rmtree(dest)
            dest.mkdir()
            for folder in ["spec", "docs"]:
                shutil.copytree(root / folder, dest / folder)
            for name in ["AGENTS.md", ".gitattributes"]:
                shutil.copy2(root / name, dest / name)
        def reject(name, mutate):
            fresh()
            mutate(dest)
            try:
                check(dest, external_input=False)
            except (AuditFailure, KeyError, FileNotFoundError):
                passed.append(name)
            else:
                raise AuditFailure(f"Self-test failed to reject: {name}")
        def alter_map(d, fn):
            path = d / "docs/compilation/compilation-map.json"
            value = read_json(d, "docs/compilation/compilation-map.json")
            fn(value)
            path.write_text(json.dumps(value), encoding="utf-8")
        reject("mutated provenance bytes", lambda d: (d / "docs/provenance/openproduct-v0.1-frozen.md").write_bytes(b"tampered"))
        reject("unreviewed source section", lambda d: alter_map(d, lambda m: m["sections"].pop()))
        reject("uninventoried decision section", lambda d: alter_map(d, lambda m: m["sections"][0].update(sourceUnits=[])))
        reject("unmapped source unit", lambda d: alter_map(d, lambda m: m["units"].pop()))
        reject("compiled without owner", lambda d: alter_map(d, lambda m: m["units"][0].pop("canonicalOwner")))
        reject("missing disposition", lambda d: alter_map(d, lambda m: m["units"][0].update(semanticDisposition="")))
        reject("invented runtime enforcement", lambda d: alter_map(d, lambda m: m["units"][0].update(enforcementStatus="ENFORCED")))
        reject("normative boundary lost", lambda d: alter_map(d, lambda m: m["units"][0].update(boundary="all normative")))
        reject("altered golden semantics", lambda d: (d / "spec/authority-contract/golden-tests.md").write_text("changed", encoding="utf-8"))
        reject("altered execution order", lambda d: (d / "docs/implementation-contract.md").write_text("changed", encoding="utf-8"))
        reject("source line omitted", lambda d: alter_map(d, lambda m: m["units"][0]["sourceRanges"][0].__setitem__(0, 2)))
        def duplicate_rule(d):
            path = d / "docs/compilation/ownership.json"
            value = read_json(d, "docs/compilation/ownership.json")
            value["rules"].append(value["rules"][0])
            path.write_text(json.dumps(value), encoding="utf-8")
        reject("duplicate effective rule owner", duplicate_rule)
        reject("broken agent route", lambda d: (d / "AGENTS.md").write_text("[bad](missing.md)", encoding="utf-8"))
    return passed


def runtime_acceptance(root: Path) -> dict:
    """The managed verification entry also requires the v0.1 runtime gate."""
    import sys
    import unittest
    sys.path.insert(0, str(root))
    loader = unittest.TestLoader()
    suite = loader.discover(str(root / "tests"))
    def cases(group):
        for test in group:
            if isinstance(test, unittest.TestSuite):
                yield from cases(test)
            else:
                yield test
    ids = [test.id() for test in cases(suite)]
    required = {f"G{number:02}" for number in range(1, 24)}
    observed = {match.group(1) for id in ids
                if (match := re.search(r"\.test_(G\d{2})_", id))}
    if not (root / "openproduct/__main__.py").is_file() or required - observed:
        raise AuditFailure("Runtime acceptance incomplete: missing CLI or Golden cases " + str(sorted(required - observed)))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise AuditFailure("Runtime acceptance FAIL")
    return {"result": "PASS", "tests": result.testsRun, "golden": sorted(required)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        result = check(root)
        if args.self_test:
            result["rejectionSelfTests"] = self_test(root)
            result["runtimeAcceptance"] = runtime_acceptance(root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (AuditFailure, KeyError, FileNotFoundError, ValueError) as error:
        parser.exit(1, f"Compilation FAIL: {error}\n")


if __name__ == "__main__":
    main()
