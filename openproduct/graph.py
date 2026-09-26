"""Source-owned graph, revision predicates and derived product invariants."""
from itertools import combinations
from .parser import ProductError, definition
from .fingerprint import semantic

def error(code, ids, explanation, field=''):
    return ProductError(code, explanation, '.openproduct/objects', sorted(ids), field).record()

def validate_revisions(objects, baseline):
    errors = []
    for id, obj in objects.items():
        front = obj['frontmatter']
        old = baseline.get(id)
        expected = 1 if old is None else old['frontmatter']['revision'] + (semantic(obj) != semantic(old))
        if front['revision'] != expected or (old and front['type'] != old['frontmatter']['type']):
            errors.append(error('SEMANTIC_REVISION_ERROR', [id], 'Expected revision ' + str(expected) + '; existing identity/type is immutable', 'revision'))
        if front['type'] == 'capability':
            target_changed = old is not None and any(obj['sections'].get(k) != old['sections'].get(k) for k in ('Target', 'Criteria'))
            target_expected = 1 if old is None else old['frontmatter']['targetRevision'] + target_changed
            if front['targetRevision'] != target_expected:
                errors.append(error('SEMANTIC_REVISION_ERROR', [id], 'Capability targetRevision must track Target/Criteria changes exactly', 'targetRevision'))
    for id, old in baseline.items():
        if id not in objects:
            incoming = [key for key, obj in objects.items() if any(r['target'] == id for r in obj['frontmatter']['relations'])]
            if old['frontmatter']['status'] != 'Retired' or incoming:
                errors.append(error('SEMANTIC_REVISION_ERROR', [id] + incoming, 'Hard deletion requires retired baseline and no remaining references'))
    return errors

class ProductGraph:
    def __init__(self, objects):
        self.objects = objects
        self.outgoing = {id:obj['frontmatter']['relations'] for id,obj in objects.items()}
        self.incoming = {id:[] for id in objects}
        for id, relations in self.outgoing.items():
            for relation in relations:
                self.incoming.setdefault(relation['target'], []).append((id, relation))

    def edges(self, id, kind):
        return [r for r in self.outgoing.get(id, []) if r['kind'] == kind]

    def applicable(self, id):
        """Historical proof objects remain readable, but cannot prove changed targets."""
        obj = self.objects[id]
        front = obj['frontmatter']
        kind = front['type']
        relation = {'verification':'verifies', 'validation':'validates', 'judgment':'supports'}.get(kind)
        if not relation or (kind != 'judgment' and front['result'] != 'PASS'):
            return False
        targets = self.edges(id, relation)
        if len(targets) != 1 or targets[0]['target'] not in self.objects:
            return False
        target = self.objects[targets[0]['target']]['frontmatter']
        binding = front['binding']
        if kind == 'verification':
            if binding['targetRevision'] != target.get('targetRevision'):
                return False
            if binding['realization'] not in {r['id'] for r in target.get('realizations', []) if r['status'] == 'Accepted'}:
                return False
            if target.get('currentRealization') != binding['realization']:
                return False
        elif binding['outcomeRevision'] != target['revision']:
            return False
        bound_edges = self.edges(id, 'evidence') + self.edges(id, 'basis')
        return bool(bound_edges) and all(r['target'] in self.objects and
            ('revision' not in r or r['revision'] == self.objects[r['target']]['frontmatter']['revision']) for r in bound_edges)

    def validate(self, baseline):
        errors = []
        rules = definition('relation-schema/schema.json')
        decisions = []
        for id, obj in self.objects.items():
            front = obj['frontmatter']
            kind, status = front['type'], front['status']
            for relation in self.outgoing[id]:
                target = self.objects.get(relation['target'])
                if target is None:
                    errors.append(error('DANGLING_REFERENCE', [id, relation['target']], 'Referenced object does not exist', 'relations'))
                elif target['frontmatter']['type'] not in rules['relations'][relation['kind']]['target']:
                    errors.append(error('INVALID_RELATION', [id, relation['target']], 'Target type is not legal for relation', 'relations'))
            for relation, count in rules['cardinality'].get(kind, {}).items():
                actual = len(self.edges(id, relation))
                if (count == 'one-or-more' and actual < 1) or (type(count) is int and actual != count):
                    code = {'verification':'INVALID_VERIFICATION_BINDING', 'validation':'INVALID_VALIDATION_BINDING'}.get(kind, 'INVALID_RELATION')
                    errors.append(error(code, [id], 'Invalid ' + relation + ' cardinality', 'relations'))
            if kind == 'decision' and status == 'Active':
                decisions.append(id)
                if not self.edges(id, 'basis'):
                    errors.append(error('INVALID_DERIVED_STATE', [id], 'An Active Decision requires Basis'))
            if kind == 'solution' and status == 'Selected':
                selectors = [source for source, r in self.incoming.get(id, []) if r['kind'] == 'selects' and self.objects[source]['frontmatter']['status'] == 'Active']
                if not selectors:
                    errors.append(error('INVALID_DERIVED_STATE', [id], 'Selected Solution requires an Active selecting Decision'))
            if kind == 'outcome' and status == 'Supported':
                if not any(r['kind'] == 'supports' and self.applicable(source) for source,r in self.incoming.get(id, [])):
                    errors.append(error('INVALID_DERIVED_STATE', [id], 'Supported Outcome requires applicable Judgment'))
            if kind == 'capability':
                current = front.get('currentRealization')
                if current:
                    realization = next((r for r in front.get('realizations', []) if r['id'] == current), None)
                    historic = baseline.get(id, {}).get('frontmatter', {}).get('realizations', [])
                    selectors = [source for source,r in self.incoming.get(id, []) if r['kind'] == 'selectsRealization' and r.get('realization') == current and self.objects[source]['frontmatter']['status'] == 'Active']
                    if not realization or realization['status'] != 'Accepted' or not selectors or not any(r['id'] == current and r['status'] == 'Accepted' for r in historic):
                        errors.append(error('INVALID_CURRENT_REALIZATION', [id] + selectors, 'Current requires explicit selection and previously Accepted realization'))
                if status == 'Closed' and not any(r['kind'] == 'verifies' and self.applicable(source) for source,r in self.incoming.get(id, [])):
                    errors.append(error('INVALID_DERIVED_STATE', [id], 'Closed Gap requires an applicable PASS Verification'))
                consumers = [(source,r) for source,r in self.incoming.get(id, []) if r['kind'] == 'requires' and 'requestedTarget' in r]
                for (a, left), (b, right) in combinations(consumers, 2):
                    scopes = (left.get('scope','global'), right.get('scope','global'))
                    if left['requestedTarget'] != right['requestedTarget'] and (scopes[0] == scopes[1] or 'global' in scopes):
                        errors.append(error('CAPABILITY_TARGET_CONFLICT', [id,a,b], 'Overlapping consumers require incompatible targets; no winner is inferred'))
            if kind in ('verification', 'validation'):
                targets = self.edges(id, 'verifies' if kind == 'verification' else 'validates')
                if targets and targets[0]['target'] in self.objects:
                    target = self.objects[targets[0]['target']]['frontmatter']
                    expected_type = 'capability' if kind == 'verification' else 'outcome'
                    if target['type'] != expected_type:
                        continue
                    binding = front['binding']
                    if kind == 'verification' and binding['realization'] not in {r['id'] for r in target.get('realizations', [])}:
                        errors.append(error('INVALID_VERIFICATION_BINDING', [id, targets[0]['target']], 'Unknown realization binding'))
                    expected = target.get('targetRevision') if kind == 'verification' else target['revision']
                    observed = binding.get('targetRevision') if kind == 'verification' else binding.get('outcomeRevision')
                    if observed > expected:
                        errors.append(error('PROOF_REVISION_MISMATCH', [id, targets[0]['target']], 'Proof binds a future revision'))
        for a,b in combinations(decisions, 2):
            left,right = self.objects[a],self.objects[b]
            explicit = any(r['target'] == b for r in self.edges(a, 'conflictsWith')) or any(r['target'] == a for r in self.edges(b, 'conflictsWith'))
            choices = lambda id: sorted((r['kind'], r['target'], r.get('realization','')) for r in self.outgoing[id] if r['kind'] in ('selects','selectsRealization'))
            incompatible = left['frontmatter']['topic'] == right['frontmatter']['topic'] and (left['sections']['Choice'] != right['sections']['Choice'] or choices(a) != choices(b))
            if explicit or incompatible:
                errors.append(error('DECISION_CONFLICT', [a,b], 'Active Decisions are incompatible; supersede or explicitly resolve before acceptance'))
        return errors

    def impact(self, seeds, previous=None):
        """Fixed-point closure over the explicit impact policy, including removed edges."""
        allowed = set(definition('semantic-diff/impact.json')['edgeKinds'])
        result = set(seeds)
        graphs = [self] + ([previous] if previous else [])
        while True:
            expanded = set(result)
            for graph in graphs:
                for id in result:
                    expanded.update(r['target'] for r in graph.outgoing.get(id, []) if r['kind'] in allowed)
                    expanded.update(source for source,r in graph.incoming.get(id, []) if r['kind'] in allowed)
            if expanded == result:
                return sorted(result)
            result = expanded
