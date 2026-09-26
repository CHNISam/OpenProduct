import copy
from unittest.mock import patch
import test_git
from test_graph import obj
from openproduct.context import compile_context,find
from openproduct.parser import ProductError,definition

class InputRegressions(test_git.GitFixture):
    def test_normalized_unique_arrays_reject_duplicates(self):
        with self.assertRaises(ProductError):
            obj('direction','why','Intent',labels=['tag',' tag '])

    def test_invalid_routing_title_is_structured_error(self):
        path=self.root/'.openproduct/objects/directions/why.md'
        path.write_text(path.read_text().replace('"Why"','42'))
        with self.assertRaises(ProductError):
            find(self.root,'why')

    def test_non_normative_policy_comment_does_not_change_context(self):
        before=compile_context(self.root,['why'])
        policy=copy.deepcopy(definition('context-contract/policy.json'))
        policy['$comment']='Unrelated explanation, not semantic policy'
        with patch('openproduct.context.definition',side_effect=lambda path: policy if path == 'context-contract/policy.json' else definition(path)):
            self.assertEqual(before,compile_context(self.root,['why']))
