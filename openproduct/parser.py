from pathlib import Path
import copy
import json
import re
import unicodedata

PACKAGE_SPEC = Path(__file__).resolve().parent / '_spec'
SOURCE_SPEC = Path(__file__).resolve().parents[1] / 'spec'
SPEC = PACKAGE_SPEC if PACKAGE_SPEC.is_dir() else SOURCE_SPEC

def definition(path):
    return json.loads((SPEC / path).read_text(encoding='utf-8-sig'))

class ProductError(ValueError):
    def __init__(self, code, explanation, path='', objects=(), field=''):
        super().__init__(explanation)
        self.code, self.explanation = code, explanation
        self.path, self.objects, self.field = path, list(objects), field

    def record(self):
        return dict(code=self.code, objects=self.objects,
                    sourceLocation=dict(path=self.path, locator=self.field),
                    explanation=self.explanation,
                    nextAction='Correct the indicated canonical input, then rerun check.')

def strict_json(text, path=''):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate key: ' + key)
            result[key] = value
        return result
    try:
        return json.loads(text, object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except (ValueError, TypeError) as error:
        raise ProductError('SCHEMA_INVALID', str(error), path) from error

def validate(value, schema, path='', field=''):
    types = {'object': dict, 'array': list, 'string': str, 'integer': int}
    if 'type' in schema and type(value) is not types[schema['type']]:
        raise ProductError('SCHEMA_INVALID', 'Expected ' + schema['type'], path, field=field)
    if 'enum' in schema and value not in schema['enum']:
        raise ProductError('SCHEMA_INVALID', 'Value outside allowed enumeration', path, field=field)
    if isinstance(value, dict):
        missing = set(schema.get('required', [])) - value.keys()
        if missing:
            raise ProductError('SCHEMA_INVALID', 'Missing fields: ' + ', '.join(sorted(missing)), path, field=field)
        properties = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            unknown = value.keys() - properties.keys()
            if unknown:
                raise ProductError('UNKNOWN_NORMATIVE_FIELD', 'Unknown fields: ' + ', '.join(sorted(unknown)), path, field=field)
        for key, item in value.items():
            if key in properties:
                validate(item, properties[key], path, field + '.' + key)
    elif isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            raise ProductError('SCHEMA_INVALID', 'Too few items', path, field=field)
        if schema.get('uniqueItems') and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            raise ProductError('SCHEMA_INVALID', 'Duplicate items', path, field=field)
        for index, item in enumerate(value):
            validate(item, schema.get('items', {}), path, field + '[' + str(index) + ']')
    elif isinstance(value, str):
        if len(value.strip()) < schema.get('minLength', 0) or ('pattern' in schema and not re.fullmatch(schema['pattern'], value)):
            raise ProductError('SCHEMA_INVALID', 'Invalid string', path, field=field)
    elif type(value) is int and value < schema.get('minimum', value):
        raise ProductError('SCHEMA_INVALID', 'Integer below minimum', path, field=field)

def normalize(value):
    if isinstance(value, str):
        return ' '.join(unicodedata.normalize('NFC', value).split())
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    return value

def split_document(text, path=''):
    if text.startswith('\ufeff'):
        text = text[1:]
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ProductError('SCHEMA_INVALID', 'Missing frontmatter delimiter', path)
    try:
        end = lines.index('---', 1)
    except ValueError as error:
        raise ProductError('SCHEMA_INVALID', 'Unclosed frontmatter', path) from error
    return strict_json('\n'.join(lines[1:end]), path), lines[end + 1:]

def parse_object(text, path):
    front, lines = split_document(text, path)
    schema = definition('frontmatter-schema/schema.json')
    if isinstance(front, dict) and set(front) & set(schema['inverseRelationFields']):
        raise ProductError('DUPLICATE_RELATION_AUTHORITY', 'Inverse relations are derived, never authored', path)
    front = normalize(front)
    validate(front, schema, path)
    types = definition('object-schema/types.json')
    kind = front['type']
    if kind not in types['types']:
        raise ProductError('SCHEMA_INVALID', 'Unknown product object type', path)
    location = Path(path)
    if location.stem != front['id']:
        raise ProductError('OBJECT_ID_MISMATCH', 'Filename must equal id', path, [front['id']])
    if location.parent.name != types['types'][kind]['directory']:
        raise ProductError('SCHEMA_INVALID', 'Object directory must match type', path, [front['id']])
    allowed = set(types['commonFields'] + types['specialAllowed'].get(kind, []))
    if front.keys() - allowed:
        raise ProductError('UNKNOWN_NORMATIVE_FIELD', 'Fields not allowed on this object type', path, [front['id']])
    if set(types['specialRequired'].get(kind, [])) - front.keys():
        raise ProductError('SCHEMA_INVALID', 'Missing type-specific fields', path, [front['id']])
    for key, value in schema['defaults'].items():
        front.setdefault(key, copy.deepcopy(value))
    if front['status'] not in types['types'][kind]['statuses']:
        raise ProductError('SCHEMA_INVALID', 'Status not allowed on type', path, [front['id']])
    relations = definition('relation-schema/schema.json')
    intents = set()
    for relation in front['relations']:
        rule = relations['relations'].get(relation['kind'])
        if not rule or kind not in rule['source'] or set(relation) - {'kind', 'target'} - set(rule['attributes']):
            raise ProductError('INVALID_RELATION', 'Relation kind or attributes invalid for source type', path, [front['id']])
        intent = (relation['kind'], normalize(relation['target']), normalize(relation.get('scope', 'global')))
        if intent in intents:
            raise ProductError('DUPLICATE_RELATION_AUTHORITY', 'Duplicate relation intent', path, [front['id']])
        intents.add(intent)
        if kind in ('verification', 'validation') and relation['kind'] == 'evidence' and 'revision' not in relation:
            raise ProductError('INVALID_RELATION', 'Proof evidence requires revision binding', path, [front['id']])
    if kind in relations['bindings']:
        binding = relations['bindings'][kind]
        if set(binding['required']) - front['binding'].keys() or front['binding'].keys() - set(binding['required'] + binding['optional']):
            raise ProductError('SCHEMA_INVALID', 'Invalid proof binding fields', path, [front['id']])
    rule = definition('canonical-markdown-grammar/sections.json')['types'][kind]
    names = set(rule['required'] + rule['optional'])
    sections, current, fence = {}, None, None
    for line in lines:
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if marker and fence is None:
            fence = (marker[1][0], len(marker[1]))
            continue
        if marker and fence is not None and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
            fence = None
            continue
        if fence is None and line.startswith('## '):
            name = line[3:]
            current = name if name in names else None
            if current:
                if current in sections:
                    raise ProductError('SCHEMA_INVALID', 'Duplicate canonical section', path, [front['id']], current)
                sections[current] = []
            continue
        if current:
            if fence is None:
                if re.search(r'<[A-Za-z/!]', line):
                    raise ProductError('SCHEMA_INVALID', 'HTML not supported in canonical sections', path, [front['id']], current)
                line = re.sub(r'^\s*(?:[-+*]|\d+[.)])\s+', '', line)
                line = re.sub(r'(`+)(.*?)\1', r'\2', line)
                line = re.sub(r'(?<!\w)(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1(?!\w)', r'\2', line)
            sections[current].append(line)
    sections = {k: normalize('\n'.join(v)) for k, v in sections.items()}
    if any(not sections.get(k) for k in rule['required']):
        raise ProductError('SCHEMA_INVALID', 'Missing or empty canonical section', path, [front['id']])
    front = normalize(front)
    for key in ('relations', 'labels', 'sourceRefs', 'realizations'):
        if key in front:
            if key == 'realizations':
                ids = [x['id'] for x in front[key]]
                if len(set(ids)) != len(ids):
                    raise ProductError('SCHEMA_INVALID', 'Duplicate realization ids', path, [front['id']])
                for item in front[key]:
                    item['executionRefs'].sort()
            front[key].sort(key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    return dict(frontmatter=front, sections=sections)
