import unittest
from openproduct import engine
from openproduct.parser import parse_object
from openproduct.fingerprint import digest
import json

class HistoryDepth(unittest.TestCase):
    def test_1100_accepted_transitions_do_not_consume_recursive_stack(self):
        config={'schemaVersion':'0.1','project':{'canonicalRef':'refs/heads/product'}}
        class HistoryRepo:
            def __init__(self,n): self.n=n; self.snaps={}; self.records={}
            def config(self): return config
            def resolve(self,ref): return 'p'+str(self.n)
            def rank(self,c): return 2*int(c[1:])-(c[0]=='s')
            def git(self,*args,optional=False):
                if args[0]=='reflog': return ''
                c=args[2] if args[-2:]==('--','.openproduct') else args[-1]
                end=self.rank(c.rstrip('^'))-c.endswith('^')
                return '\n'.join(('p' if x%2==0 else 's')+str((x+1)//2) for x in range(end,0,-1))
            def ancestor(self,a,b): return self.rank(a)<=self.rank(b)
            def snapshot(self,c):
                i=int(c[1:])
                if i not in self.snaps:
                    front=dict(id='why',type='direction',revision=i,title='Why')
                    obj=parse_object('---\n'+json.dumps(front)+'\n---\n## Intent\nstate'+str(i),'objects/directions/why.md')
                    self.snaps[i]=(config,{'why':obj})
                return self.snaps[i]
            def proofs(self,c):
                if c[0]=='s': return []
                if c not in self.records:
                    i=int(c[1:]); identity=checker.identities(*self.snapshot(c))
                    proof=dict(checkedCommit='s'+str(i),**identity,result='PASS',revisionBaseline='p'+str(i-1) if i>1 else None)
                    name=digest([proof[k] for k in ('productStateFingerprint','specFingerprint','checkerBuild')])
                    self.records[c]=[('.openproduct/checkproofs/'+name+'.json',proof)]
                return self.records[c]
            def history(self,c): return self.git('rev-list',c).splitlines()
        repo=HistoryRepo(1100); checker=engine.Checker(repo)
        self.assertIsNotNone(checker.recognized('p1100'))

    def test_code_only_history_reuses_a_single_proven_product_transition(self):
        config={'schemaVersion':'0.1','project':{'canonicalRef':'refs/heads/product'}}
        obj=parse_object('---\n'+json.dumps(dict(id='why',type='direction',revision=1,title='Why'))+'\n---\n## Intent\nStable','objects/directions/why.md')
        class CodeHistory:
            def __init__(self,n): self.n=n; self.proof_reads=0
            def config(self): return config
            def resolve(self,ref): return 'c'+str(self.n)
            def git(self,*args,optional=False):
                if args[0]=='reflog': return ''
                if args[-2:]==('--','.openproduct'): return 'c1'
                if args[-1].endswith('^'): return ''
                return '\n'.join('c'+str(i) for i in range(self.n,0,-1))
            def ancestor(self,a,b): return int(a[1:])<=int(b[1:])
            def snapshot(self,c): return config,{'why':obj}
            def proofs(self,c):
                self.proof_reads+=1
                identity=checker.identities(config,{'why':obj})
                proof=dict(checkedCommit='c1',**identity,result='PASS',revisionBaseline=None)
                name=digest([proof[k] for k in ('productStateFingerprint','specFingerprint','checkerBuild')])
                return [('.openproduct/checkproofs/'+name+'.json',proof)]
            def history(self,c): return self.git('rev-list',c).splitlines()
        repo=CodeHistory(800); checker=engine.Checker(repo)
        self.assertIsNotNone(checker.recognized('c800'))
        self.assertLessEqual(repo.proof_reads,2)
