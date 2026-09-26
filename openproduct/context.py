"""Progressive routing and deterministic task-relevant context."""
from pathlib import Path
from .parser import ProductError, definition, normalize, parse_object, strict_json, validate
from .repository import Repository
from .fingerprint import digest, normative_content

def metadata(repo):
    result = {}
    for path in repo.paths():
        if not path.startswith('.openproduct/objects/') or not path.endswith('.md'):
            continue
        # Stop reading at the frontmatter boundary: no unrelated narrative body is read.
        try:
            with (repo.root / path).open(encoding='utf-8-sig') as stream:
                if stream.readline().rstrip('\r\n') != '---':
                    raise ProductError('SCHEMA_INVALID','Missing frontmatter',path)
                lines = []
                for line in stream:
                    if line.rstrip('\r\n') == '---':
                        break
                    lines.append(line)
                else:
                    raise ProductError('SCHEMA_INVALID','Unclosed frontmatter',path)
            front = normalize(strict_json(''.join(lines),path))
            validate(front,definition('frontmatter-schema/schema.json'),path)
            if not isinstance(front,dict) or type(front.get('id')) is not str or type(front.get('relations',[])) is not list:
                raise ProductError('SCHEMA_INVALID','Invalid routing metadata',path)
            id = front['id']
            if id in result or Path(path).stem != id:
                raise ProductError('OBJECT_ID_MISMATCH','Duplicate or mismatched routing identity',path,[id])
            front = normalize(front)
            result[id] = dict(frontmatter=front,path=path)
        except (OSError,UnicodeError) as failure:
            raise ProductError('SCHEMA_INVALID','Cannot read UTF-8 routing metadata',path) from failure
    return result

def compile_context(root, seeds, whole=False):
    repo = Repository(root)
    repo.config()
    routes = metadata(repo)
    policy = definition('context-contract/policy.json')
    seeds = sorted(set(seeds))
    if not seeds and not whole:
        raise ProductError('SCHEMA_INVALID','Context requires explicit task object IDs; use --whole only for an intentional whole-graph request')
    if set(seeds) - routes.keys():
        raise ProductError('DANGLING_REFERENCE','Unknown context seed',objects=sorted(set(seeds) - routes.keys()))
    relevant = set(routes) if whole else set(seeds)
    incoming = {}
    for id, route in routes.items():
        for relation in route['frontmatter'].get('relations',[]):
            if not isinstance(relation,dict) or not isinstance(relation.get('target'),str):
                raise ProductError('INVALID_RELATION','Invalid routing relation',route['path'],[id])
            if relation.get('kind') in policy['edgeKinds']:
                incoming.setdefault(relation['target'],set()).add(id)
    if not whole:
        for _ in range(policy['maxHops']):
            expanded = set(relevant)
            for id in relevant:
                expanded.update(incoming.get(id,()))
                if id in routes:
                    expanded.update(r['target'] for r in routes[id]['frontmatter'].get('relations',[]) if r.get('kind') in policy['edgeKinds'])
            relevant = expanded
    if relevant - routes.keys():
        raise ProductError('DANGLING_REFERENCE','Relevant object is missing',objects=sorted(relevant - routes.keys()))
    objects = [parse_object(repo.read(routes[id]['path']),routes[id]['path']) for id in sorted(relevant)]
    value = dict(policyFingerprint=digest(normative_content(policy)), seeds=seeds, whole=whole, objects=objects)
    return dict(contextObjectSet=sorted(relevant),contextFingerprint=digest(value),**value)

def find(root, query='', kind=None):
    routes = metadata(Repository(root))
    return [dict(id=id,type=r['frontmatter'].get('type'),title=r['frontmatter'].get('title'),path=r['path'])
            for id,r in sorted(routes.items()) if (not kind or r['frontmatter'].get('type') == kind)
            and query.casefold() in (id + ' ' + r['frontmatter'].get('title','')).casefold()]

def show(root, id):
    repo = Repository(root)
    routes = metadata(repo)
    if id not in routes:
        raise ProductError('DANGLING_REFERENCE','Unknown object',objects=[id])
    return parse_object(repo.read(routes[id]['path']),routes[id]['path'])

def rebuild_current(root, focus):
    repo = Repository(root)
    routes = metadata(repo)
    ids = sorted(set(focus)) if focus else [id for id,r in sorted(routes.items()) if r['frontmatter'].get('type') == 'outcome' and r['frontmatter'].get('status') == 'Active']
    if set(ids) - routes.keys():
        raise ProductError('DANGLING_REFERENCE','Unknown current focus',objects=sorted(set(ids)-routes.keys()))
    text = '# Current product route\n\nGenerated navigation only. Objects and validated canonical state own authority.\n\n'
    for id in ids:
        route = routes[id]
        title = route['frontmatter'].get('title',id).replace('[','').replace(']','')
        text += '- [' + id + ': ' + title + '](' + route['path'].removeprefix('.openproduct/') + ')\n'
    (repo.root / '.openproduct/current.md').write_text(text,encoding='utf-8')
    return dict(result='PASS',focus=ids)
