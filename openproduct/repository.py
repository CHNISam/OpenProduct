"""Actual Git snapshots, never branch-name heuristics or simulated merge bases."""
from pathlib import Path, PurePosixPath
import subprocess
from .parser import ProductError, normalize, parse_object, strict_json

def is_input(path):
    return path == '.openproduct/config.yml' or path.startswith('.openproduct/objects/') or (path.startswith('.openproduct/checkproofs/') and path.endswith('.json'))

class Repository:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self._snapshots = {}
        self._proofs = {}

    def git(self, *args, optional=False):
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True)
        if result.returncode:
            if optional:
                return None
            raise ProductError('SCHEMA_INVALID', 'Git operation failed: ' + args[0])
        try:
            return result.stdout.decode('utf-8', errors='strict').strip()
        except UnicodeDecodeError as error:
            raise ProductError('SCHEMA_INVALID', 'Git output is not valid UTF-8: ' + args[0]) from error

    def resolve(self, ref):
        if not isinstance(ref, str) or not ref or ref.startswith('-') or '\n' in ref:
            raise ProductError('SCHEMA_INVALID', 'Invalid Git revision')
        return self.git('rev-parse', '--verify', ref + '^{commit}', optional=True)

    def ancestor(self, older, newer):
        if not self.resolve(older) or not self.resolve(newer):
            return False
        return self.git('merge-base', '--is-ancestor', older, newer, optional=True) is not None

    def paths(self, commit=None):
        if commit:
            records = self.git('ls-tree', '-r', '-z', commit, '--', '.openproduct') or ''
            result = []
            for record in records.split('\0'):
                if not record:
                    continue
                meta, path = record.split('\t', 1)
                mode, kind, blob = meta.split()
                if is_input(path) and (mode not in ('100644','100755') or kind != 'blob'):
                    raise ProductError('SCHEMA_INVALID', 'Product inputs must be ordinary files', path)
                result.append(path)
            return result
        base = self.root / '.openproduct'
        if base.is_symlink():
            raise ProductError('SCHEMA_INVALID', 'Product directory cannot be a symlink')
        result = []
        for path in sorted(base.rglob('*')):
            relative = path.relative_to(self.root).as_posix()
            if path.is_symlink():
                if is_input(relative) or relative in ('.openproduct/objects','.openproduct/checkproofs'):
                    raise ProductError('SCHEMA_INVALID', 'Product inputs cannot be symlinks', relative)
                continue
            if path.is_file():
                result.append(path.relative_to(self.root).as_posix())
        return result

    def read(self, path, commit=None):
        try:
            if commit:
                result = subprocess.run(['git','-C',str(self.root),'show',commit + ':' + path], capture_output=True)
                if result.returncode:
                    raise ProductError('SCHEMA_INVALID', 'Required product input missing', path)
                return result.stdout.decode('utf-8', errors='strict')
            return (self.root / path).read_text(encoding='utf-8', errors='strict')
        except (OSError, UnicodeError) as error:
            raise ProductError('SCHEMA_INVALID', 'Cannot read UTF-8 product input', path) from error

    def config(self, commit=None):
        path = '.openproduct/config.yml'
        config = strict_json(self.read(path, commit), path)
        if type(config) is not dict or set(config) != {'schemaVersion','project'} or config['schemaVersion'] != '0.1':
            raise ProductError('SCHEMA_INVALID', 'Config requires schemaVersion 0.1 and project only', path)
        project = config['project']
        if type(project) is not dict or 'canonicalRef' not in project or set(project) - {'canonicalRef','name'}:
            raise ProductError('SCHEMA_INVALID', 'Project requires a unique canonicalRef', path)
        if any(type(v) is not str or not v.strip() for v in project.values()):
            raise ProductError('SCHEMA_INVALID', 'Project fields must be nonempty strings', path)
        ref = project['canonicalRef']
        if self.git('check-ref-format', ref, optional=True) is None:
            raise ProductError('SCHEMA_INVALID', 'canonicalRef must be a fully qualified Git ref', path)
        return normalize(config)

    def snapshot(self, commit=None):
        if commit and commit in self._snapshots:
            return self._snapshots[commit]
        config = self.config(commit)
        objects = {}
        for path in self.paths(commit):
            if path.startswith('.openproduct/objects/'):
                if len(PurePosixPath(path).parts) != 4 or not path.endswith('.md'):
                    raise ProductError('SCHEMA_INVALID', 'Object path must be objects/type/id.md', path)
                obj = parse_object(self.read(path, commit), path)
                id = obj['frontmatter']['id']
                if id in objects:
                    raise ProductError('SCHEMA_INVALID', 'Duplicate object id', path, [id])
                objects[id] = obj
        result = (config, objects)
        if commit:
            self._snapshots[commit] = result
        return result

    def proofs(self, commit):
        if commit not in self._proofs:
            records = []
            for path in self.paths(commit):
                if not path.startswith('.openproduct/checkproofs/') or not path.endswith('.json'):
                    continue
                try:
                    records.append((path, strict_json(self.read(path, commit), path)))
                except ProductError:
                    # A broken unrelated archive is not Product or proof authority.
                    # If the exact current key is broken, no valid matching proof exists.
                    continue
            self._proofs[commit] = records
        return self._proofs[commit]

    def history(self, commit):
        return (self.git('rev-list', commit) or '').splitlines()
