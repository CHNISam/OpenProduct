import importlib
import unittest
import test_git
from test_graph import obj
from openproduct.context import compile_context

class Projection(test_git.GitFixture):
    def test_copy_for_agent_is_scoped_and_stable(self):
        try:
            compiler = importlib.import_module('openproduct.compiler')
        except ModuleNotFoundError:
            self.fail('Copy for Agent is not implemented')
        before = compiler.copy_for_agent(self.root,['why'])
        path = self.root / '.openproduct/objects/directions/unrelated.md'
        path.write_text('---\n{"id":"unrelated","type":"direction","revision":1,"title":"other"}\n---\n## Intent\nUnrelated growth')
        self.assertEqual(before,compiler.copy_for_agent(self.root,['why']))
        self.assertIn('contextFingerprint',before)
        self.assertNotIn('Unrelated growth',before)

    def test_studio_requires_explicit_whole_and_escapes_data(self):
        try:
            studio = importlib.import_module('openproduct.studio')
        except ModuleNotFoundError:
            self.fail('Lightweight Studio is not implemented')
        path = self.root / '.openproduct/objects/directions/why.md'
        path.write_text(path.read_text().replace('"Why"','"</script><script>alert(1)</script>"'))
        with self.assertRaises(Exception):
            studio.build(self.root,self.root / 'index.html')
        studio.build(self.root,self.root / 'index.html',whole=True)
        html = (self.root / 'index.html').read_text()
        self.assertNotIn('</script><script>alert(1)</script>',html)
        self.assertIn('Copy for Agent',html)
        self.assertIn('contextFingerprint',html)
