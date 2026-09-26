import importlib
import unittest
from openproduct.parser import parse_object

class FingerprintContract(unittest.TestCase):
    def test_revision_identity_and_unrelated_inputs(self):
        try:
            f = importlib.import_module('openproduct.fingerprint')
        except ModuleNotFoundError:
            self.fail('Fingerprints are not implemented')
        a = parse_object('---\n{"id":"why","type":"direction","revision":1,"title":"Why"}\n---\n## Intent\nTools', 'objects/directions/why.md')
        b = parse_object('---\n{"id":"why","type":"direction","revision":2,"title":"Why"}\n---\n## Intent\nTools', 'objects/directions/why.md')
        config = {'schemaVersion':'0.1','project':{'canonicalRef':'refs/heads/product'}}
        self.assertEqual(f.semantic(a), f.semantic(b))
        self.assertNotEqual(f.product_state(config, {'why':a}), f.product_state(config, {'why':b}))
        self.assertNotEqual(f.checked_tree(config, {'why':a}), f.checked_tree(config, {'why':b}))
        self.assertEqual(len(f.spec_identity()), 64)
        self.assertEqual(len(f.checker_build()), 64)
