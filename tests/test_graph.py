import importlib
import unittest
from openproduct.parser import parse_object
from openproduct.fingerprint import semantic

def obj(kind, id, section, content='value', **fields):
    import json
    from openproduct.parser import definition
    meta = dict(id=id, type=kind, revision=1, title=id)
    meta.update(fields)
    directory = definition('object-schema/types.json')['types'][kind]['directory']
    return parse_object('---\n' + json.dumps(meta) + '\n---\n## ' + section + '\n' + content,
                        'objects/' + directory + '/' + id + '.md')

class GraphContract(unittest.TestCase):
    def api(self):
        try:
            return importlib.import_module('openproduct.graph')
        except ModuleNotFoundError:
            self.fail('ProductGraph and revision checking are not implemented')

    def test_revision_only_change_and_new_semantics(self):
        g = self.api()
        old = obj('direction', 'why', 'Intent')
        illegal = obj('direction', 'why', 'Intent', revision=2)
        self.assertIn('SEMANTIC_REVISION_ERROR', [e['code'] for e in g.validate_revisions({'why':illegal}, {'why':old})])
        changed = obj('direction', 'why', 'Intent', 'changed')
        self.assertIn('SEMANTIC_REVISION_ERROR', [e['code'] for e in g.validate_revisions({'why':changed}, {'why':old})])
        changed['frontmatter']['revision'] = 2
        self.assertEqual(g.validate_revisions({'why':changed}, {'why':old}), [])

    def test_conflicting_targets_and_dangling_edges(self):
        g = self.api()
        cap = obj('capability', 'cap', 'Target', 'X', targetRevision=1)
        a = obj('outcome', 'a', 'Success Criteria', relations=[dict(kind='requires',target='cap',requestedTarget='X')])
        b = obj('outcome', 'b', 'Success Criteria', relations=[dict(kind='requires',target='cap',requestedTarget='Y')])
        graph = g.ProductGraph({'cap':cap,'a':a,'b':b})
        self.assertIn('CAPABILITY_TARGET_CONFLICT', [e['code'] for e in graph.validate({})])
        self.assertEqual({x[0] for x in graph.incoming['cap']}, {'a','b'})
        graph = g.ProductGraph({'a':a})
        self.assertIn('DANGLING_REFERENCE', [e['code'] for e in graph.validate({})])
