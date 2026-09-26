"""Dependency-free command line for generic coding agents."""
import argparse
import json
from pathlib import Path
from .parser import ProductError, definition
from .repository import Repository
from .engine import accepted, check
from .context import compile_context, find, rebuild_current, show

def main(argv=None):
    parser = argparse.ArgumentParser(prog='openproduct')
    parser.add_argument('--repo',default='.')
    commands = parser.add_subparsers(dest='command',required=True)
    p = commands.add_parser('init')
    p.add_argument('--canonical-ref',required=True)
    p.add_argument('--name')
    p = commands.add_parser('check')
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--all',action='store_true')
    modes.add_argument('--changed',action='store_true')
    modes.add_argument('--against',choices=['canonical'])
    p.add_argument('--save-proof',action='store_true')
    commands.add_parser('accepted')
    p = commands.add_parser('show')
    p.add_argument('id')
    p = commands.add_parser('find')
    p.add_argument('query',nargs='?',default='')
    p.add_argument('--type')
    p = commands.add_parser('context')
    p.add_argument('ids',nargs='*')
    p.add_argument('--whole',action='store_true')
    p = commands.add_parser('current')
    p.add_argument('action',choices=['rebuild'])
    p.add_argument('ids',nargs='*')
    p = commands.add_parser('copy-for-agent')
    p.add_argument('ids',nargs='*')
    p.add_argument('--whole',action='store_true')
    p = commands.add_parser('studio')
    p.add_argument('--output',required=True)
    p.add_argument('--whole',action='store_true')
    p = commands.add_parser('migrate-nanopm')
    p.add_argument('source')
    p = commands.add_parser('diff')
    p.add_argument('--base',default='HEAD')
    args = parser.parse_args(argv)
    try:
        root = Path(args.repo).resolve()
        if args.command == 'init':
            base = root / '.openproduct'
            if base.exists():
                raise ProductError('SCHEMA_INVALID','Product directory already exists; init never overwrites it')
            repo = Repository(root)
            if repo.git('check-ref-format',args.canonical_ref,optional=True) is None:
                raise ProductError('SCHEMA_INVALID','Use a fully qualified canonical Git ref')
            base.mkdir(parents=True)
            project = dict(canonicalRef=args.canonical_ref)
            if args.name:
                project['name'] = args.name
            (base / 'config.yml').write_text(json.dumps(dict(schemaVersion='0.1',project=project),indent=2)+'\n',encoding='utf-8')
            for rule in definition('object-schema/types.json')['types'].values():
                (base / 'objects' / rule['directory']).mkdir(parents=True)
            result = rebuild_current(root,[])
        elif args.command == 'check':
            result = check(root,'all' if args.all else 'changed' if args.changed else 'against',args.save_proof)
        elif args.command == 'copy-for-agent':
            from .compiler import copy_for_agent
            print(copy_for_agent(root,args.ids,args.whole),end='')
            return 0
        elif args.command == 'studio':
            from .studio import build
            result = build(root,args.output,args.whole)
        elif args.command == 'migrate-nanopm':
            from .migration import migrate
            result = migrate(args.source,root)
        elif args.command == 'accepted':
            result = accepted(root)
        elif args.command == 'show':
            result = show(root,args.id)
        elif args.command == 'find':
            result = find(root,args.query,args.type)
        elif args.command == 'context':
            result = compile_context(root,args.ids,args.whole)
        elif args.command == 'current':
            result = rebuild_current(root,args.ids)
        else:
            repo = Repository(root)
            commit = repo.resolve(args.base)
            if not commit:
                raise ProductError('SCHEMA_INVALID','Unknown diff base')
            _, old = repo.snapshot(commit)
            _, new = repo.snapshot()
            result = [dict(id=id,before=old.get(id),after=new.get(id)) for id in sorted(set(old)|set(new)) if old.get(id) != new.get(id)]
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if isinstance(result,dict) and result.get('result') == 'FAIL' else 0
    except ProductError as failure:
        print(json.dumps(dict(result='FAIL',errors=[failure.record()]),ensure_ascii=False,indent=2))
        return 2
    except (OSError,UnicodeError) as failure:
        print(json.dumps(dict(result='FAIL',errors=[ProductError('SCHEMA_INVALID',str(failure)).record()]),indent=2))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
