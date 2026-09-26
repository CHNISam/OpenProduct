import json
from pathlib import Path
import subprocess,sys
from unittest.mock import patch
import test_git
from test_graph import obj
from openproduct import engine
from openproduct.parser import parse_object,ProductError
from openproduct.graph import ProductGraph

class ReviewRegressions(test_git.GitFixture):
    def test_revalidate_after_checker_identity_change(self):
        self.bootstrap()
        with patch('openproduct.engine.checker_build',return_value='a'*64):
            self.assertEqual(engine.accepted(self.root)['result'],'FAIL')
            result=engine.check(self.root,save=True)
            self.assertEqual(result['result'],'PASS',result)
            self.commit('revalidated proof under changed checker')
            self.assertEqual(engine.accepted(self.root)['result'],'PASS')

    def test_failed_and_uncommitted_proofs_do_not_block_bootstrap(self):
        self.write(2)
        self.commit('invalid bootstrap revision')
        self.assertEqual(engine.check(self.root,save=True)['result'],'FAIL')
        self.commit('diagnostic FAIL artifact')
        self.write(1)
        result=engine.check(self.root,save=True)
        self.assertEqual(result['result'],'PASS',result)
        self.assertIsNone(result['proof']['checkedCommit'])
        self.commit('corrected inputs with uncommitted-state PASS')
        self.assertEqual(engine.accepted(self.root)['result'],'FAIL')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('commit-bound bootstrap proof')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')

    def test_wrong_verification_endpoint_returns_errors(self):
        target=obj('direction','wrong','Intent')
        proof=obj('verification','proof','Method',result='PASS',binding=dict(targetRevision=1,realization='none'),relations=[dict(kind='verifies',target='wrong'),dict(kind='evidence',target='ev',revision=1)])
        errors=ProductGraph({'wrong':target,'proof':proof,'ev':obj('evidence','ev','Observation')}).validate({})
        self.assertIn('INVALID_RELATION',{e['code'] for e in errors})

    def test_normalized_relation_uniqueness(self):
        with self.assertRaises(ProductError) as failure:
            obj('outcome','aim','Success Criteria',relations=[dict(kind='requires',target='cap'),dict(kind='requires',target=' cap ')])
        self.assertEqual(failure.exception.code,'DUPLICATE_RELATION_AUTHORITY')

    def test_four_backtick_fence_does_not_close_with_three(self):
        text='---\n{"id":"why","type":"direction","revision":1,"title":"Why"}\n---\n## Intent\nTools\n## Notes\n````markdown\n```\n## Intent\nExample only\n````\n'
        self.assertEqual(parse_object(text,'objects/directions/why.md')['sections'],{'Intent':'Tools'})

    def test_executable_cache_does_not_invalidate_accepted_state(self):
        self.bootstrap()
        directory=self.root / '.openproduct/cache'
        directory.mkdir()
        (directory/'helper').write_text('excluded cache')
        self.git('add','.')
        self.git('update-index','--chmod=+x','.openproduct/cache/helper')
        self.git('commit','-m','non-normative executable cache')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')

    def test_frozen_current_rebuild_interface(self):
        command=[sys.executable,'-m','openproduct','--repo',str(self.root),'current','rebuild','why']
        result=subprocess.run(command,capture_output=True,text=True,cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        self.assertIn('why',(self.root/'.openproduct/current.md').read_text())

    def test_repeated_revalidation_keeps_the_same_accepted_transition(self):
        self.bootstrap()
        for build in ('a'*64,'b'*64,'c'*64):
            with patch('openproduct.engine.checker_build',return_value=build):
                self.assertEqual(engine.accepted(self.root)['result'],'FAIL')
                result=engine.check(self.root,save=True)
                self.assertEqual(result['result'],'PASS',result)
                self.commit('revalidate same accepted state')
                self.assertEqual(engine.accepted(self.root)['result'],'PASS')
