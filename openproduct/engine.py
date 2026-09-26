"""CheckProof authority and the three frozen check modes."""
from pathlib import Path
from . import __version__
from .parser import ProductError, definition
from .fingerprint import canonical, digest, checked_tree, product_state, spec_identity, checker_build
from .graph import ProductGraph, error, validate_revisions
from .repository import Repository

class Checker:
    def __init__(self, repo, config=None):
        self.repo = repo
        self.spec = spec_identity()
        self.build = checker_build()
        self.canonical_ref = (config or repo.config())['project']['canonicalRef']
        self.canonical_tip = repo.resolve(self.canonical_ref)
        history = repo.git('rev-list', '--first-parent', self.canonical_tip) if self.canonical_tip else ''
        self.canonical_line = history.splitlines()
        self.canonical_history = set(self.canonical_line)
        self.history_primed = False
        self.prior_accepted = {}
        changes = repo.git('rev-list', '--first-parent', self.canonical_tip, '--', '.openproduct') if self.canonical_tip else ''
        self.product_commits = set(changes.splitlines())
        positions = (repo.git('reflog', 'show', '--format=%H', self.canonical_ref, optional=True) or '').splitlines()
        # Native ref observations corroborate local history; merge first-parent history
        # remains the portable canonical line, excluding proposal-only merge parents.
        self.ref_positions = set(positions)
        self.ref_window_start = positions[-1] if positions else None
        self.validated = {}
        self.active = set()

    def identities(self, config, objects):
        return dict(checkedTree=checked_tree(config, objects), productStateFingerprint=product_state(config, objects),
                    specFingerprint=self.spec, checkerVersion=__version__, checkerBuild=self.build)

    def canonical_position(self, commit):
        if commit not in self.canonical_history:
            return False
        if self.ref_window_start and self.repo.ancestor(self.ref_window_start, commit):
            return commit in self.ref_positions
        return True

    def recognized(self, commit, historical=False):
        if not self.history_primed:
            # Prove older canonical dependencies first, without a call frame per
            # accepted transition. This is per-invocation derived state only.
            self.history_primed = True
            latest = None
            for older in reversed(self.canonical_line):
                self.prior_accepted[older] = latest
                if older not in self.product_commits and latest and self.canonical_position(older):
                    # No Product input changed on this first-parent transition.
                    # The previously proved state/proof is inherited verbatim.
                    self.validated[(older, True)] = latest
                else:
                    witness = self.recognized(older, historical=True)
                    if witness:
                        latest = witness
                if (older, True) in self.validated and self.validated[(older, True)]:
                    latest = self.validated[(older, True)]
        if historical and not self.canonical_position(commit):
            return None
        key = (commit, historical)
        if key in self.validated:
            return self.validated[key]
        if not historical and commit in self.canonical_history and commit not in self.product_commits:
            inherited = self.validated.get((commit, True))
            if inherited and inherited.get('specFingerprint') == self.spec and inherited.get('checkerBuild') == self.build:
                self.validated[key] = inherited
                return inherited
        if key in self.active:
            return None
        self.active.add(key)
        result = None
        try:
            config, objects = self.repo.snapshot(commit)
            if config['project']['canonicalRef'] != self.canonical_ref:
                return None
            identity = self.identities(config, objects)
            for path, proof in self.repo.proofs(commit):
                if type(proof) is not dict or set(proof) != set(definition('authority-contract/proof.json')['checkProofFields']):
                    continue
                bindings = ('checkedTree','productStateFingerprint') if historical else ('checkedTree','productStateFingerprint','specFingerprint','checkerBuild')
                if proof['result'] != 'PASS' or any(proof.get(k) != identity[k] for k in bindings):
                    continue
                expected_path = '.openproduct/checkproofs/' + digest([proof[k] for k in ('productStateFingerprint','specFingerprint','checkerBuild')]) + '.json'
                if path != expected_path:
                    continue
                checked = proof['checkedCommit']
                if not checked or not self.repo.ancestor(checked, commit):
                    continue
                checked_config, checked_objects = self.repo.snapshot(checked)
                if self.identities(checked_config, checked_objects) != identity:
                    continue
                baseline_commit = proof['revisionBaseline']
                baseline = {}
                if baseline_commit:
                    if baseline_commit == checked or not self.canonical_position(baseline_commit) or not self.recognized(baseline_commit, historical=True):
                        continue
                    if commit in self.canonical_history and not self.repo.ancestor(baseline_commit, commit):
                        continue
                    _, baseline = self.repo.snapshot(baseline_commit)
                if commit in self.canonical_history:
                    previous = self.prior_accepted.get(commit)
                    baseline_state = product_state(*self.repo.snapshot(baseline_commit)) if baseline_commit else None
                    # The last recognized canonical Product state, not merely the
                    # candidate branch ancestry, is the integration baseline.
                    if previous and previous['productStateFingerprint'] not in {baseline_state, identity['productStateFingerprint']}:
                        continue
                    if baseline_commit and previous is None:
                        continue
                elif baseline_commit and not self.repo.ancestor(baseline_commit, self.canonical_tip):
                    continue
                errors = validate_revisions(objects, baseline) + ProductGraph(objects).validate(baseline)
                if not errors:
                    result = proof
                    break
        except (ProductError, KeyError, TypeError, ValueError):
            result = None
        finally:
            self.active.remove(key)
        self.validated[key] = result
        return result

    def baseline(self, target, head):
        if target and self.recognized(target):
            return target, self.repo.snapshot(target)[1]
        if target and target != head:
            raise ProductError('CANONICAL_STATE_INVALID', 'Canonical tip has no current valid CheckProof')
        if target:
            historic = self.recognized(target, historical=True)
            if historic:
                # Explicit canonical revalidation replays the original accepted transition.
                # Historical replay is never returned by accepted() as a current PASS.
                parent = historic['revisionBaseline']
                return parent, self.repo.snapshot(parent)[1] if parent else {}
            for commit in self.repo.history(target):
                if commit != target and self.recognized(commit, historical=True):
                    return commit, self.repo.snapshot(commit)[1]
        return None, {}

    def proof(self, config, objects, errors, baseline_commit, head):
        identity = self.identities(config, objects)
        if not errors and head:
            existing = self.recognized(head)
            if existing and all(existing.get(k) == v for k,v in identity.items()):
                return existing
        checked = None
        if head:
            try:
                if self.identities(*self.repo.snapshot(head)) == identity:
                    checked = head
            except ProductError:
                pass
        return dict(checkedCommit=checked, **identity, result='FAIL' if errors else 'PASS', revisionBaseline=baseline_commit)

def accepted(root):
    try:
        repo = Repository(root)
        checker = Checker(repo)
        target = repo.resolve(repo.config()['project']['canonicalRef'])
        if target and repo.config(target)['project']['canonicalRef'] != checker.canonical_ref:
            raise ProductError('CANONICAL_STATE_INVALID', 'Selected canonical ref is outside the validated configuration')
        proof = checker.recognized(target) if target else None
        if not proof:
            raise ProductError('CANONICAL_STATE_INVALID', 'Canonical ref is unvalidated or its CheckProof is stale')
        return dict(result='PASS', errors=[], commit=target, proof=proof)
    except ProductError as failure:
        return dict(result='FAIL', errors=[failure.record()])

def check(root, mode='all', save=False):
    try:
        if mode not in ('all','changed','against'):
            raise ProductError('SCHEMA_INVALID', 'Unknown check mode')
        repo = Repository(root)
        head = repo.resolve('HEAD')
        if mode == 'against' and not head:
            raise ProductError('CANONICAL_STATE_INVALID', 'Against-canonical requires a committed proposal HEAD')
        config, objects = repo.snapshot(head if mode == 'against' else None)
        checker = Checker(repo, config)
        target = repo.resolve(config['project']['canonicalRef'])
        baseline_commit, baseline = checker.baseline(target, head)
        graph = ProductGraph(objects)
        errors = []
        checked_ids = sorted(objects)
        merge_base = None
        if mode == 'changed':
            previous = repo.snapshot(head)[1] if head else {}
            seeds = {id for id in set(objects) | set(previous) if objects.get(id) != previous.get(id)}
            checked_ids = graph.impact(seeds, ProductGraph(previous))
        elif mode == 'against':
            if not target or not checker.recognized(target) or not head:
                raise ProductError('CANONICAL_STATE_INVALID', 'Against-canonical requires a validated canonical commit')
            merge_base = repo.git('merge-base', head, target)
            _, ancestor = repo.snapshot(merge_base)
            _, canonical_objects = repo.snapshot(target)
            proposal_objects = objects
            for id in sorted(set(ancestor) | set(canonical_objects) | set(proposal_objects)):
                if canonical_objects.get(id) != ancestor.get(id) and proposal_objects.get(id) != ancestor.get(id) and proposal_objects.get(id) != canonical_objects.get(id):
                    errors.append(error('STALE_OBJECT', [id], 'Canonical and proposal changed this object since their real merge base'))
                    errors.append(error('SEMANTIC_CONFLICT', [id], 'Concurrent unequal product changes require explicit resolution'))
            seeds = {id for id in set(objects) | set(baseline) if objects.get(id) != baseline.get(id)}
            checked_ids = graph.impact(seeds, ProductGraph(baseline))
        findings = validate_revisions(objects, baseline) + graph.validate(baseline)
        if mode != 'all':
            findings = [e for e in findings if set(e['objects']) & set(checked_ids)]
        errors.extend(findings)
        proof = checker.proof(config, objects, errors, baseline_commit, head)
        # Partial checks never create an all-state acceptance proof.
        if save:
            if mode != 'all':
                raise ProductError('SCHEMA_INVALID', 'Only check --all may persist an acceptance CheckProof')
            directory = repo.root / '.openproduct/checkproofs'
            directory.mkdir(parents=True, exist_ok=True)
            name = digest([proof[k] for k in ('productStateFingerprint','specFingerprint','checkerBuild')]) + '.json'
            (directory / name).write_bytes(canonical(proof) + b'\n')
        return dict(result=proof['result'], errors=errors, proof=proof, checkedObjects=checked_ids, mergeBase=merge_base)
    except ProductError as failure:
        return dict(result='FAIL', errors=[failure.record()])
