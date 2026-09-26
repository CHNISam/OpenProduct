"""NanoPM import with explicit structural mappings and byte-preserved provenance."""
import hashlib
import json
import re
from pathlib import Path
from .parser import ProductError, definition, parse_object
from .repository import Repository

def _header(text):
    lines = text.splitlines()
    values, sections = {}, {}
    if lines and lines[0] == '---':
        try:
            end = lines.index('---',1)
        except ValueError:
            return {}, {}
        for line in lines[1:end]:
            match = re.fullmatch(r'([A-Za-z_][A-Za-z0-9_]*):\s*(.*)',line)
            if match:
                key, value = match.groups()
                if key in values:
                    raise ProductError('SCHEMA_INVALID','Duplicate NanoPM metadata key',field=key)
                if value.startswith('"'):
                    try:
                        value = json.loads(value)
                    except ValueError:
                        continue
                values[key] = value
        lines = lines[end + 1:]
    current = None
    for line in lines:
        if line.startswith('## '):
            current = line[3:]
            sections[current] = []
        elif current:
            sections[current].append(line)
    return values, {k:'\n'.join(v).strip() for k,v in sections.items()}

def migrate(source, root):
    source, root = Path(source).resolve(),Path(root).resolve()
    Repository(root).config()
    if not source.is_dir() or source.is_symlink() or source == root or source in root.parents or root in source.parents:
        raise ProductError('SCHEMA_INVALID','Use separate existing NanoPM source and initialized target directories')
    base = root / '.openproduct'
    if any((base / 'objects').rglob('*.md')) or (base / 'migration-sources').exists():
        raise ProductError('SCHEMA_INVALID','Migration requires an empty initialized product; never overwrite existing Product data')
    rules = definition('object-schema/migration.json')
    copies, planned, mapping, warnings = {}, {}, {}, []
    for path in sorted(source.rglob('*')):
        if path.is_symlink():
            raise ProductError('SCHEMA_INVALID','Migration does not follow symlinks',str(path))
        if not path.is_file() or path.suffix not in ('.md','.json','.jsonl','.yml','.yaml'):
            continue
        raw = path.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        name = sha + path.suffix
        copies[name] = raw
        relative = path.relative_to(source).as_posix()
        meta, sections = _header(raw.decode('utf-8',errors='strict')) if path.suffix == '.md' else ({},{})
        rule = rules['mappings'].get(meta.get('type')) if relative.startswith('wiki/entities/') else None
        id = meta.get('id','')
        matched = bool(rule and re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,95}',id) and sections.get(rule['sourceSection']))
        if matched:
            kind = rule['type']
            body = '## ' + rule['section'] + '\n' + sections[rule['sourceSection']]
            if id in planned:
                raise ProductError('SCHEMA_INVALID','Duplicate source Product identity',relative,[id])
        else:
            id,kind = 'source-' + sha[:24], 'evidence'
            body = '## Observation\nImported source ' + relative + '; byte identity SHA256 ' + sha + '. This records source existence, not verified Product claims.\n'
            if rule:
                warnings.append(dict(source=relative,reason='Missing usable canonical source section; retained as Evidence'))
        front = dict(id=id,type=kind,revision=1,title=meta.get('title',relative) if matched else relative,status='Draft',sourceRefs=['migration-sources/' + name])
        directory = definition('object-schema/types.json')['types'][kind]['directory']
        destination = 'objects/' + directory + '/' + id + '.md'
        document = '---\n' + json.dumps(front,ensure_ascii=False,indent=2) + '\n---\n' + body + '\n\n## Original source\nByte-preserved at ../' + front['sourceRefs'][0] + '\n'
        try:
            parse_object(document,destination)
        except ProductError:
            if matched:
                warnings.append(dict(source=relative,reason='Source section outside canonical grammar; retained as Evidence'))
                id,kind = 'source-' + sha[:24], 'evidence'
                front.update(id=id,type=kind,title=relative)
                destination = 'objects/evidence/' + id + '.md'
                document = '---\n' + json.dumps(front,ensure_ascii=False,indent=2) + '\n---\n## Observation\nImported source ' + relative + '; SHA256 ' + sha + '.\n'
                matched = False
            else:
                raise
        planned[id] = (destination,document,meta)
        if matched:
            mapping[meta['id']] = id
    # Add only source-authored opportunity references whose imported target is known.
    for id,(destination,document,meta) in list(planned.items()):
        if meta.get('type') == 'solution' and meta.get('opportunity') in mapping and destination.startswith('objects/solutions/'):
            front, rest = document.split('\n---\n',1)
            fields = json.loads(front.removeprefix('---\n'))
            target = mapping[meta['opportunity']]
            if planned[target][0].startswith('objects/opportunities/'):
                fields['relations'] = [dict(kind='addresses',target=target)]
                document = '---\n' + json.dumps(fields,ensure_ascii=False,indent=2) + '\n---\n' + rest
                planned[id] = (destination,document,meta)
    if not planned:
        raise ProductError('SCHEMA_INVALID','No supported source files found')
    for id,(destination,document,meta) in planned.items():
        parse_object(document,destination)
    originals = base / 'migration-sources'
    originals.mkdir()
    for name,raw in copies.items():
        (originals / name).write_bytes(raw)
    for destination,document,meta in planned.values():
        path = base / destination
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(document,encoding='utf-8')
    return dict(result='PASS',objects=len(planned),sourceCopies=len(copies),mappedProductObjects=len(mapping),warnings=warnings)
