"""Task-scoped text compilation for any coding agent."""
import json
from .context import compile_context

def render_context(context):
    header = '# OpenProduct task context\n\nThis is a scoped projection. Context does not establish acceptance; verify Product state through the configured canonical ref and CheckProof.\n\n'
    header += 'contextFingerprint: ' + context['contextFingerprint'] + '\n'
    header += 'contextObjectSet: ' + ', '.join(context['contextObjectSet']) + '\n\n'
    header += 'Edit source-owned fields and canonical sections directly; compare revisions to the accepted baseline. Verification is not Validation. Tests alone do not prove an Outcome.\n\n'
    for obj in context['objects']:
        front = obj['frontmatter']
        header += '## ' + front['id'] + ' (' + front['type'] + ')\n\n'
        header += '```json\n' + json.dumps(front,ensure_ascii=False,sort_keys=True,indent=2) + '\n```\n\n'
        for name,text in sorted(obj['sections'].items()):
            header += '### ' + name + '\n\n' + text + '\n\n'
    return header

def copy_for_agent(root,seeds,whole=False):
    return render_context(compile_context(root,seeds,whole))
