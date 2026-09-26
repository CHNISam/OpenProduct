"""Executable canonical G-01 through G-23; real commits where authority matters."""
import copy
import importlib
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import test_git
from test_graph import obj
from openproduct import engine
from openproduct.fingerprint import product_state, semantic, spec_identity, checker_build
from openproduct.graph import ProductGraph, validate_revisions
from openproduct.parser import ProductError, parse_object, SPEC

class Golden(test_git.GitFixture):
    def codes(self, result):
        return {e['code'] for e in result['errors']}

    def test_G01_valid_canonical_state(self):
        self.bootstrap()

    def test_G02_unvalidated_canonical_ref(self):
        self.assertIn('CANONICAL_STATE_INVALID', self.codes(engine.accepted(self.root)))

    def test_G03_bootstrap_revision_one(self):
        self.assertEqual(engine.check(self.root)['result'], 'PASS')
        self.write(2)
        self.assertIn('SEMANTIC_REVISION_ERROR', self.codes(engine.check(self.root)))

    def test_G04_changed_semantics_requires_increment(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(1, 'changed')
        self.assertIn('SEMANTIC_REVISION_ERROR', self.codes(engine.check(self.root)))

    def test_G05_unchanged_semantics_forbids_increment(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(2)
        self.assertIn('SEMANTIC_REVISION_ERROR', self.codes(engine.check(self.root)))

    def test_G06_source_owned_relation_changes_revision(self):
        a = obj('outcome','aim','Success Criteria')
        b = obj('outcome','aim','Success Criteria',relations=[dict(kind='requires',target='cap')])
        self.assertNotEqual(semantic(a), semantic(b))
        self.assertEqual({e['code'] for e in validate_revisions({'aim':b},{'aim':a})}, {'SEMANTIC_REVISION_ERROR'})
        b['frontmatter']['revision'] = 2
        self.assertEqual(validate_revisions({'aim':b},{'aim':a}), [])

    def test_G07_formatting_and_non_normative_text(self):
        text = (self.root / '.openproduct/objects/directions/why.md').read_text()
        a = parse_object(text, 'objects/directions/why.md')
        b = parse_object(text.replace('Tools','**Tools**') + '\n## Notes\ncompletely different', 'objects/directions/why.md')
        self.assertEqual(semantic(a), semantic(b))

    def test_G08_duplicate_relation_authority(self):
        text = '---\n' + json.dumps(dict(id='why',type='direction',title='why',revision=1,requiredBy=['other'])) + '\n---\n## Intent\nTools'
        with self.assertRaises(ProductError) as failure:
            parse_object(text, 'objects/directions/why.md')
        self.assertEqual(failure.exception.code, 'DUPLICATE_RELATION_AUTHORITY')

    def test_G09_current_is_non_authoritative(self):
        self.bootstrap()
        before = engine.accepted(self.root)['proof']['productStateFingerprint']
        (self.root / '.openproduct/current.md').write_text('why revision 999 is retired')
        self.commit('contradictory projection')
        after = engine.accepted(self.root)
        self.assertEqual(after['result'], 'PASS')
        self.assertEqual(after['proof']['productStateFingerprint'], before)

    def decisions(self):
        basis = obj('evidence','basis','Observation')
        a = obj('decision','a','Choice','X',status='Active',topic='topic',relations=[dict(kind='basis',target='basis')])
        b = obj('decision','b','Choice','Y',status='Active',topic='topic',relations=[dict(kind='basis',target='basis')])
        return basis,a,b

    def put(self, object):
        from openproduct.parser import definition
        front = object['frontmatter']
        directory = self.root / '.openproduct/objects' / definition('object-schema/types.json')['types'][front['type']]['directory']
        directory.mkdir(parents=True, exist_ok=True)
        (directory / (front['id'] + '.md')).write_text('---\n' + json.dumps(front) + '\n---\n' + '\n'.join('## ' + k + '\n' + v for k,v in object['sections'].items()), encoding='utf-8')

    def test_G10_git_clean_semantic_conflict(self):
        self.bootstrap()
        for object in self.decisions():
            self.put(object)
        self.commit('textually valid conflicting product decisions')
        self.assertEqual(self.git('status','--porcelain'), '')
        self.assertIn('DECISION_CONFLICT', self.codes(engine.check(self.root)))

    def test_G11_stale_object_real_merge_base(self):
        test_git.GitContract.test_real_merge_base_detects_concurrent_changes(self)

    def test_G12_individually_valid_proposals_conflict_after_merge(self):
        self.bootstrap()
        basis,a,b = self.decisions()
        self.put(basis)
        self.commit('shared basis')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('shared basis proof')
        self.git('checkout','-b','left')
        self.put(a)
        self.commit('left choice')
        self.assertEqual(engine.check(self.root)['result'],'PASS')
        self.git('checkout','product')
        self.git('checkout','-b','right')
        self.put(b)
        self.commit('right choice')
        self.assertEqual(engine.check(self.root)['result'],'PASS')
        self.git('merge','left','--no-edit')
        self.assertIn('DECISION_CONFLICT',self.codes(engine.check(self.root)))

    def test_G13_unrelated_git_code_preserves_state(self):
        self.bootstrap()
        before = engine.accepted(self.root)['proof']['productStateFingerprint']
        (self.root / 'game.py').write_text('print(123)')
        self.commit('unrelated code')
        self.assertEqual(engine.accepted(self.root)['proof']['productStateFingerprint'],before)

    def test_G14_object_add_delete_change_changes_state(self):
        from openproduct.repository import Repository
        config, objects = Repository(self.root).snapshot()
        original = product_state(config,objects)
        changed = copy.deepcopy(objects)
        changed['why']['sections']['Intent'] = 'other'
        self.assertNotEqual(product_state(config,changed),original)
        changed = dict(objects, other=obj('direction','other','Intent'))
        self.assertNotEqual(product_state(config,changed),original)
        self.assertNotEqual(product_state(config,{}),original)

    def test_G15_old_proof_cannot_accept_new_state(self):
        self.bootstrap()
        self.write(2, 'new intent')
        self.commit('unvalidated changed state')
        self.assertIn('CANONICAL_STATE_INVALID', self.codes(engine.accepted(self.root)))

    def context_api(self):
        try:
            return importlib.import_module('openproduct.context')
        except ModuleNotFoundError:
            self.fail('Task-relevant context is not implemented')

    def test_G16_unrelated_graph_growth_preserves_context(self):
        context = self.context_api()
        before = context.compile_context(self.root, ['why'])
        self.put(obj('direction','unrelated','Intent'))
        # Unrelated body is intentionally malformed: task context must not parse it.
        path = self.root / '.openproduct/objects/directions/unrelated.md'
        path.write_text(path.read_text().replace('## Intent','## Freeform'))
        after = context.compile_context(self.root, ['why'])
        self.assertEqual(before, after)
        self.assertEqual(after['contextObjectSet'], ['why'])

    def test_G17_changed_normative_spec_invalidates_proof(self):
        self.bootstrap()
        with tempfile.TemporaryDirectory() as temp:
            import shutil
            shutil.copytree(SPEC, Path(temp) / 'spec')
            root = Path(temp) / 'spec'
            path = root / 'context-contract/policy.json'
            data = json.loads(path.read_text())
            data['maxHops'] = 3
            path.write_text(json.dumps(data))
            changed = spec_identity(root)
        self.assertNotEqual(changed, spec_identity())
        with patch('openproduct.engine.spec_identity', return_value=changed):
            self.assertIn('CANONICAL_STATE_INVALID',self.codes(engine.accepted(self.root)))

    def test_G18_changed_checker_build_invalidates_proof(self):
        self.bootstrap()
        with tempfile.TemporaryDirectory() as temp:
            import shutil
            source = Path(__file__).resolve().parents[1] / 'openproduct'
            shutil.copytree(source,Path(temp) / 'runtime')
            path = Path(temp) / 'runtime/graph.py'
            path.write_text(path.read_text(encoding='utf-8-sig') + '\nBUILD_DELTA = True\n')
            changed = checker_build(Path(temp) / 'runtime')
        self.assertNotEqual(changed,checker_build())
        with patch('openproduct.engine.checker_build',return_value=changed):
            self.assertIn('CANONICAL_STATE_INVALID',self.codes(engine.accepted(self.root)))

    def proof_graph(self):
        cap = obj('capability','cap','Target','X',targetRevision=1,status='Closed',realizations=[dict(id='run',status='Accepted',executionRefs=['git:abc'])],currentRealization='run')
        proof = obj('verification','verify','Method',status='Active',result='PASS',binding=dict(targetRevision=1,realization='run'),relations=[dict(kind='verifies',target='cap'),dict(kind='evidence',target='ev',revision=1)])
        evidence = obj('evidence','ev','Observation')
        decision = obj('decision','choice','Choice','run',status='Active',topic='realization',relations=[dict(kind='basis',target='ev'),dict(kind='selectsRealization',target='cap',realization='run')])
        consumer = obj('outcome','x','Success Criteria',relations=[dict(kind='requires',target='cap',requestedTarget='X')])
        return {o['frontmatter']['id']:o for o in (cap,proof,evidence,decision,consumer)}

    def test_G19_conflicting_capability_targets(self):
        objects = self.proof_graph()
        objects['y'] = obj('outcome','y','Success Criteria',relations=[dict(kind='requires',target='cap',requestedTarget='Y')])
        self.assertIn('CAPABILITY_TARGET_CONFLICT', {e['code'] for e in ProductGraph(objects).validate(objects)})

    def test_G20_existing_scoped_proof_remains_applicable(self):
        objects = self.proof_graph()
        self.assertEqual(ProductGraph(objects).validate(objects), [])
        self.assertTrue(ProductGraph(objects).applicable('verify'))
        objects['y'] = obj('outcome','y','Success Criteria',relations=[dict(kind='requires',target='cap',requestedTarget='Y')])
        graph = ProductGraph(objects)
        self.assertTrue(graph.applicable('verify'))
        self.assertIn('CAPABILITY_TARGET_CONFLICT', {e['code'] for e in graph.validate(objects)})

    def test_G21_validation_is_revision_scoped(self):
        outcome = obj('outcome','aim','Success Criteria')
        evidence = obj('evidence','ev','Observation')
        validation = obj('validation','validate','Measurement',result='PASS',binding=dict(outcomeRevision=1),relations=[dict(kind='validates',target='aim'),dict(kind='evidence',target='ev',revision=1)])
        objects = {'aim':outcome,'ev':evidence,'validate':validation}
        self.assertTrue(ProductGraph(objects).applicable('validate'))
        outcome['frontmatter']['revision'] = 2
        self.assertFalse(ProductGraph(objects).applicable('validate'))
        validation['frontmatter']['result'] = 'UNKNOWN'
        outcome['frontmatter']['revision'] = 1
        self.assertFalse(ProductGraph(objects).applicable('validate'))

    def test_G22_generic_agent_file_and_git_interface(self):
        import os, subprocess, sys
        command = [sys.executable,'-m','openproduct','--repo',str(self.root),'check','--all']
        result = subprocess.run(command,capture_output=True,text=True,cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(result.returncode,0,result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)['result'],'PASS')
        # The package must import/run with only Python's standard library and Git.
        result = subprocess.run([sys.executable,'-S',*command[1:]],capture_output=True,text=True,cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(result.returncode,0,result.stderr + result.stdout)

    def test_G23_revision_only_invalidates_state_and_proof(self):
        self.bootstrap()
        from openproduct.repository import Repository
        config, before = Repository(self.root).snapshot()
        proof = engine.accepted(self.root)['proof']
        self.git('checkout','-b','proposal')
        self.write(2)
        _, after = Repository(self.root).snapshot()
        self.assertEqual(semantic(before['why']),semantic(after['why']))
        self.assertNotEqual(product_state(config,before),product_state(config,after))
        self.assertNotEqual(proof['productStateFingerprint'],product_state(config,after))
        self.assertIn('SEMANTIC_REVISION_ERROR',self.codes(engine.check(self.root,mode='changed')))
        self.commit('illegal revision')
        self.git('update-ref','refs/heads/product','HEAD')
        self.assertIn('CANONICAL_STATE_INVALID',self.codes(engine.accepted(self.root)))
