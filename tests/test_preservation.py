import importlib
import tempfile
from pathlib import Path
import unittest
from test_graph import obj
from openproduct.parser import parse_object
from openproduct.fingerprint import semantic

class Preservation(unittest.TestCase):
    def test_lexical_underscores_are_semantic(self):
        self.assertNotEqual(semantic(obj('direction','why','Intent','a_b')), semantic(obj('direction','why','Intent','ab')))

    def test_migration_preserves_source_and_does_not_promote_status(self):
        try:
            migration = importlib.import_module('openproduct.migration')
        except ModuleNotFoundError:
            self.fail('NanoPM migration is not implemented')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'old/wiki/entities/solutions'
            source.mkdir(parents=True)
            data = b'---\nid: idea\ntype: solution\ntitle: "Idea"\nstatus: selected\n---\n## Pitch\nA useful change.\n## Notes\nPrivate origin\n'
            (source / 'idea.md').write_bytes(data)
            target = root / 'new'
            target.mkdir()
            (target / '.openproduct').mkdir()
            (target / '.openproduct/config.yml').write_text('{"schemaVersion":"0.1","project":{"canonicalRef":"refs/heads/product"}}')
            result = migration.migrate(root / 'old',target)
            self.assertEqual(result['result'],'PASS')
            path = target / '.openproduct/objects/solutions/idea.md'
            migrated = parse_object(path.read_text(),'objects/solutions/idea.md')
            self.assertEqual(migrated['frontmatter']['status'],'Draft')
            self.assertEqual(migrated['sections']['Approach'],'A useful change.')
            originals = list((target / '.openproduct/migration-sources').glob('*.md'))
            self.assertEqual(originals[0].read_bytes(),data)
            with self.assertRaises(Exception):
                migration.migrate(root / 'old',target)
