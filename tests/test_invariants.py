import unittest
import copy
from test_graph import obj
import test_golden
from openproduct.graph import ProductGraph
from openproduct.parser import ProductError

class Invariants(unittest.TestCase):
    def graph(self):
        return test_golden.Golden.proof_graph(self)

    def test_selected_solution_needs_active_not_superseded_selector(self):
        solution=obj('solution','selected','Approach',status='Selected')
        decision=obj('decision','selector','Choice',status='Superseded',topic='choice',relations=[dict(kind='selects',target='selected'),dict(kind='basis',target='ev')])
        objects={'selected':solution,'selector':decision,'ev':obj('evidence','ev','Observation')}
        self.assertIn('INVALID_DERIVED_STATE',{e['code'] for e in ProductGraph(objects).validate({})})
        decision['frontmatter']['status']='Active'
        self.assertEqual(ProductGraph(objects).validate({}),[])

    def test_current_requires_previously_accepted_realization(self):
        objects=self.graph()
        baseline=copy.deepcopy(objects)
        baseline['cap']['frontmatter']['realizations'][0]['status']='Proposed'
        self.assertIn('INVALID_CURRENT_REALIZATION',{e['code'] for e in ProductGraph(objects).validate(baseline)})

    def test_unknown_or_stale_evidence_cannot_close_a_gap(self):
        objects=self.graph()
        objects['verify']['frontmatter']['result']='UNKNOWN'
        self.assertIn('INVALID_DERIVED_STATE',{e['code'] for e in ProductGraph(objects).validate(objects)})
        objects['verify']['frontmatter']['result']='PASS'
        objects['ev']['frontmatter']['revision']=2
        self.assertFalse(ProductGraph(objects).applicable('verify'))
        self.assertIn('INVALID_DERIVED_STATE',{e['code'] for e in ProductGraph(objects).validate(objects)})

    def test_supported_outcome_requires_current_judgment(self):
        outcome=obj('outcome','aim','Success Criteria',status='Supported')
        evidence=obj('evidence','ev','Observation')
        judgment=obj('judgment','judge','Conclusion',binding=dict(outcomeRevision=1),relations=[dict(kind='supports',target='aim'),dict(kind='basis',target='ev',revision=1)])
        objects={'aim':outcome,'ev':evidence,'judge':judgment}
        self.assertEqual(ProductGraph(objects).validate({}),[])
        outcome['frontmatter']['revision']=2
        self.assertIn('INVALID_DERIVED_STATE',{e['code'] for e in ProductGraph(objects).validate({})})

    def test_undefined_proof_scope_axis_is_not_a_normative_field(self):
        with self.assertRaises(ProductError):
            obj('verification','proof','Method',result='PASS',binding=dict(targetRevision=1,realization='run',scope='extra-axis'),relations=[dict(kind='verifies',target='cap'),dict(kind='evidence',target='ev',revision=1)])
