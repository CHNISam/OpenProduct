import json
from unittest.mock import patch
import test_git
from openproduct import engine
from openproduct.repository import Repository
from openproduct.parser import ProductError,parse_object
from openproduct.context import find,compile_context
from openproduct.fingerprint import canonical,digest,semantic

class AuthorityRegressions(test_git.GitFixture):
    def forge_proposal_baseline(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(2,'proposal first')
        self.commit('first proposal')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        proposal_baseline=self.commit('proposal proof, never canonical')
        self.write(3,'proposal second')
        head=self.commit('second proposal')
        repo=Repository(self.root)
        config,objects=repo.snapshot()
        proof=engine.Checker(repo).proof(config,objects,[],proposal_baseline,head)
        directory=self.root/'.openproduct/checkproofs'
        name=digest([proof[k] for k in ('productStateFingerprint','specFingerprint','checkerBuild')])+'.json'
        (directory/name).write_bytes(canonical(proof)+b'\n')
        return self.commit('forged proposal-only baseline')

    def test_proposal_ancestor_is_not_an_accepted_revision_baseline(self):
        head=self.forge_proposal_baseline()
        self.assertIsNone(engine.Checker(Repository(self.root)).recognized(head))
        self.git('checkout','product')
        self.git('merge','--no-ff','proposal','-m','merge counterfeit baseline fixture')
        self.assertEqual(engine.accepted(self.root)['result'],'FAIL')

    def test_fast_forward_cannot_promote_intermediate_proposal_baselines(self):
        head=self.forge_proposal_baseline()
        self.git('update-ref','refs/heads/product',head)
        self.assertEqual(engine.accepted(self.root)['result'],'FAIL')

    def test_unvalidated_config_cannot_redirect_acceptance(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(2,'changed')
        self.commit('proposal')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('proposal proof')
        path=self.root/'.openproduct/config.yml'
        config=json.loads(path.read_text())
        config['project']['canonicalRef']='refs/heads/proposal'
        path.write_text(json.dumps(config))
        self.assertEqual(engine.accepted(self.root)['result'],'FAIL')

    def test_fenced_lexical_characters_remain_semantic(self):
        a='---\n{"id":"why","type":"direction","revision":1,"title":"Why"}\n---\n## Intent\n```text\n**literal**\n- item\n```'
        b=a.replace('**literal**','literal').replace('- item','item')
        self.assertNotEqual(semantic(parse_object(a,'objects/directions/why.md')),semantic(parse_object(b,'objects/directions/why.md')))

    def test_bom_is_accepted_consistently_by_routing(self):
        path=self.root/'.openproduct/objects/directions/why.md'
        path.write_bytes(b'\xef\xbb\xbf'+path.read_bytes())
        self.assertEqual(engine.check(self.root)['result'],'PASS')
        self.assertEqual(find(self.root,'why')[0]['id'],'why')
        self.assertEqual(compile_context(self.root,['why'])['contextObjectSet'],['why'])

    def test_pruned_ref_history_does_not_invalidate_older_canonical_baselines(self):
        self.bootstrap()
        self.write(2,'accepted change')
        self.commit('new canonical normative state')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('new canonical proof')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')
        positions=self.git('reflog','show','--format=%H','refs/heads/product').splitlines()
        for index in range(len(positions)-1,1,-1):
            self.git('reflog','delete','--rewrite','refs/heads/product@{'+str(index)+'}')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')

    def test_unrelated_malformed_proof_archive_is_not_authority(self):
        self.bootstrap()
        (self.root/'.openproduct/checkproofs/unrelated.json').write_text('{ broken archive')
        self.commit('unrelated malformed mechanical archive')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')

    def test_intervening_canonical_acceptance_invalidates_stale_proposal_proof(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(2,'proposal state')
        self.commit('proposal normative state')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('proposal proof against initial baseline')
        self.git('checkout','product')
        self.write(2,'different canonical state')
        self.commit('canonical normative change')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('canonical accepted proof')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')
        self.git('merge','--no-ff','proposal','-s','ours','-m','native merge retaining proposal objects')
        self.git('checkout','proposal','--','.openproduct')
        self.commit('merged proposal state with stale proof')
        self.assertEqual(engine.accepted(self.root)['result'],'FAIL')

    def test_illustrative_contract_text_is_not_ruleset_identity(self):
        import shutil
        from openproduct.parser import SPEC
        from openproduct.fingerprint import spec_identity
        copy=self.root/'copied-spec'
        shutil.copytree(SPEC,copy)
        before=spec_identity(copy)
        path=copy/'authority-contract/contract.md'
        text=path.read_text(encoding='utf-8')
        self.assertIn('type\nthen id',text)
        path.write_text(text.replace('type\nthen id','illustrative alternate order'),encoding='utf-8')
        self.assertEqual(spec_identity(copy),before)
        path.write_text(path.read_text(encoding='utf-8').replace('revision 必须包含','revision 禁止包含'),encoding='utf-8')
        self.assertNotEqual(spec_identity(copy),before)

    def test_stale_bootstrap_proof_cannot_replace_an_accepted_product(self):
        self.git('checkout','-b','initial-proposal')
        self.write(1,'proposed bootstrap')
        head=self.commit('proposal initial state')
        repo=Repository(self.root)
        config,objects=repo.snapshot()
        proof=engine.Checker(repo).proof(config,objects,[],None,head)
        directory=self.root/'.openproduct/checkproofs'
        directory.mkdir(exist_ok=True)
        name=digest([proof[k] for k in ('productStateFingerprint','specFingerprint','checkerBuild')])+'.json'
        (directory/name).write_bytes(canonical(proof)+b'\n')
        self.commit('unadmitted bootstrap proposal proof')
        self.git('checkout','product')
        self.bootstrap()
        self.git('merge','--no-ff','initial-proposal','-s','ours','-m','merge initial proposal fixture')
        self.git('checkout','initial-proposal','--','.openproduct')
        self.commit('stale bootstrap proof reused after another acceptance')
        self.assertEqual(engine.accepted(self.root)['result'],'FAIL')

    def test_uncommitted_resolution_does_not_hide_committed_head_conflict(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(2,'proposal')
        self.commit('committed proposal')
        self.git('checkout','product')
        self.write(2,'canonical')
        self.commit('canonical change')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('canonical proof')
        self.git('checkout','proposal')
        self.write(2,'canonical')
        codes={e['code'] for e in engine.check(self.root,'against')['errors']}
        self.assertIn('STALE_OBJECT',codes)
        self.assertIn('SEMANTIC_CONFLICT',codes)

    def test_code_only_accepted_baseline_allows_next_product_transition(self):
        self.bootstrap()
        self.write(2,'accepted change')
        self.commit('second normative state')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        self.commit('second accepted proof')
        (self.root/'app.py').write_text('app_change = True')
        self.commit('unrelated application-only accepted tip')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')
        self.git('checkout','-b','proposal')
        self.write(3,'next proposed product change')
        self.commit('third normative state')
        self.assertEqual(engine.check(self.root,save=True)['result'],'PASS')
        head=self.commit('third proposal proof')
        self.assertIsNotNone(engine.Checker(Repository(self.root)).recognized(head))
        self.git('checkout','product')
        self.git('merge','--no-ff','proposal','-m','integrate after unrelated code commit')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')

    def test_against_canonical_validates_committed_revisions_not_only_repairs(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(1,'illegal committed semantic change')
        self.commit('proposal with missing revision increment')
        self.write(2,'illegal committed semantic change')
        self.assertEqual(engine.check(self.root,'all')['result'],'PASS')
        codes={e['code'] for e in engine.check(self.root,'against')['errors']}
        self.assertIn('SEMANTIC_REVISION_ERROR',codes)

    def test_same_state_canonical_revalidation_after_branch_point_is_valid_baseline(self):
        self.bootstrap()
        self.git('checkout','-b','proposal')
        self.write(2,'next state')
        self.commit('proposal state')
        self.git('checkout','product')
        (self.root/'app.py').write_text('new_code = True')
        baseline=self.commit('canonical code-only state')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')
        self.git('checkout','proposal')
        proof=engine.check(self.root,save=True)
        self.assertEqual(proof['result'],'PASS',proof)
        self.assertEqual(proof['proof']['revisionBaseline'],baseline)
        self.commit('proposal proof against later same-state baseline')
        self.git('checkout','product')
        self.git('merge','--no-ff','proposal','-m','native merge')
        self.assertEqual(engine.accepted(self.root)['result'],'PASS')
