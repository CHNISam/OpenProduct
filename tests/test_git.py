import importlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

class GitFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.git('init', '-b', 'product')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Contract test')
        (self.root / '.openproduct/objects/directions').mkdir(parents=True)
        (self.root / '.openproduct/config.yml').write_text(json.dumps(dict(schemaVersion='0.1',project=dict(canonicalRef='refs/heads/product'))), encoding='utf-8')
        self.write()
        self.commit('initial product')

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, check=True)
        return result.stdout.decode().strip()

    def write(self, revision=1, content='Tools'):
        (self.root / '.openproduct/objects/directions/why.md').write_text('---\n' + json.dumps(dict(id='why',type='direction',revision=revision,title='Why')) + '\n---\n## Intent\n' + content, encoding='utf-8')

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-m', message)
        return self.git('rev-parse', 'HEAD')

    def api(self):
        try:
            return importlib.import_module('openproduct.engine')
        except ModuleNotFoundError:
            self.fail('Git baseline and CheckProof implementation is absent')

    def bootstrap(self):
        engine = self.api()
        result = engine.check(self.root, mode='all', save=True)
        self.assertEqual(result['result'], 'PASS', result)
        self.commit('record bootstrap proof')
        self.assertEqual(engine.accepted(self.root)['result'], 'PASS')
        return engine

class GitContract(GitFixture):
    def test_real_bootstrap_proof_and_revision_only_mutation(self):
        engine = self.bootstrap()
        self.git('checkout', '-b', 'proposal')
        self.write(2)
        result = engine.check(self.root, mode='changed')
        self.assertEqual(result['result'], 'FAIL')
        self.assertIn('SEMANTIC_REVISION_ERROR', [e['code'] for e in result['errors']])

    def test_rechecking_accepted_state_is_idempotent(self):
        engine = self.bootstrap()
        self.assertEqual(engine.check(self.root, mode='all', save=True)['result'], 'PASS')
        self.assertEqual(engine.accepted(self.root)['result'], 'PASS')

    def test_unvalidated_canonical_state_is_not_accepted(self):
        engine = self.api()
        result = engine.accepted(self.root)
        self.assertEqual(result['result'], 'FAIL')
        self.assertIn('CANONICAL_STATE_INVALID', [e['code'] for e in result['errors']])

    def test_real_merge_base_detects_concurrent_changes(self):
        engine = self.bootstrap()
        self.git('checkout', '-b', 'proposal')
        self.write(2, 'Proposal')
        self.commit('proposal change')
        self.git('checkout', 'product')
        self.write(2, 'Canonical')
        self.commit('canonical change')
        self.assertEqual(engine.check(self.root, mode='all', save=True)['result'], 'PASS')
        self.commit('canonical proof')
        self.git('checkout', 'proposal')
        result = engine.check(self.root, mode='against')
        self.assertEqual(result['result'], 'FAIL')
        self.assertIn('STALE_OBJECT', [e['code'] for e in result['errors']])
        self.assertIn('SEMANTIC_CONFLICT', [e['code'] for e in result['errors']])
