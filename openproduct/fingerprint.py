"""Deterministic identities; none depend on Git or projections."""
import copy
import hashlib
import json
import re
from pathlib import Path
from .parser import SPEC, normalize

NON_NORMATIVE = {'$comment', 'description', 'examples'}

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def semantic(obj):
    value = copy.deepcopy(obj)
    value['frontmatter'].pop('revision', None)
    return digest(value)

def product_state(config, objects):
    return digest({'config':config, 'objects':sorted([
        {'id':key, 'type':obj['frontmatter']['type'], 'revision':obj['frontmatter']['revision'], 'semanticFingerprint':semantic(obj)}
        for key, obj in objects.items()], key=lambda x:(x['type'], x['id']))})

def checked_tree(config, objects):
    return digest({'config':config, 'objects':sorted(objects.values(), key=lambda x:(x['frontmatter']['type'], x['frontmatter']['id']))})

def normative_content(value):
    if isinstance(value, dict):
        return {k:normative_content(v) for k,v in value.items() if k not in NON_NORMATIVE}
    if isinstance(value, list):
        return [normative_content(v) for v in value]
    return normalize(value)

def spec_identity(root=SPEC):
    files = {}
    policy = json.loads((Path(root) / 'semantic-diff/serialization.json').read_text(encoding='utf-8-sig'))
    exclusions = policy.get('markdownExcludedRegions', {})
    for path in sorted(Path(root).rglob('*')):
        if path.suffix == '.json':
            files[path.relative_to(root).as_posix()] = normative_content(json.loads(path.read_text(encoding='utf-8-sig')))
        elif path.name in ('contract.md', 'golden-tests.md'):
            source = path.read_text(encoding='utf-8-sig')
            sections = {}
            for match in re.finditer(r'<!-- BEGIN (S-\d+) -->(.*?)<!-- END \1 -->', source, re.S):
                if match[1] == 'S-023':
                    continue  # frozen rationale owner, not executable product semantics
                text = match[2]
                for region in exclusions.get(match[1], []):
                    text = re.sub(region, '', text, flags=re.S)
                text = re.sub(r'^#{1,6} .*$','',text,flags=re.M)
                text = re.sub(r'<a\s+[^>]+></a>', '', text)
                text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
                sections[match[1]] = normalize(re.sub(r'[*`#]', '', text))
            files[path.relative_to(root).as_posix()] = sections
    return digest(files)

def checker_build(root=None):
    root = Path(root or Path(__file__).parent)
    return digest({p.relative_to(root).as_posix():p.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
                   for p in sorted(root.rglob('*.py'))})
