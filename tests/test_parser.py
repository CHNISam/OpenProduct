import unittest
from pathlib import Path
import importlib

class ParserContract(unittest.TestCase):
    def api(self):
        try:
            return importlib.import_module('openproduct.parser')
        except ModuleNotFoundError:
            self.fail('The contract parser is not implemented')

    def test_normalization_and_non_normative_text(self):
        p = self.api()
        a = '---\n{"id":"why","type":"direction","revision":1,"title":"Why"}\n---\n## Intent\n**Make**   useful tools.\n## Notes\nfirst'
        b = a.replace('**Make**   useful', 'Make useful').replace('first', 'second')
        self.assertEqual(p.parse_object(a, 'objects/directions/why.md'), p.parse_object(b, 'objects/directions/why.md'))

    def test_unknown_field_and_id_mismatch(self):
        p = self.api()
        a = '---\n{"id":"why","type":"direction","revision":1,"title":"Why","surprise":true}\n---\n## Intent\nTools'
        with self.assertRaises(p.ProductError) as failure:
            p.parse_object(a, 'objects/directions/why.md')
        self.assertEqual(failure.exception.code, 'UNKNOWN_NORMATIVE_FIELD')
        with self.assertRaises(p.ProductError) as failure:
            p.parse_object(a.replace(',"surprise":true', ''), 'objects/directions/other.md')
        self.assertEqual(failure.exception.code, 'OBJECT_ID_MISMATCH')

    def test_duplicate_key_and_boolean_revision_rejected(self):
        p = self.api()
        for fields in ('"revision":true', '"revision":1,"revision":2'):
            a = '---\n{"id":"why","type":"direction",' + fields + ',"title":"Why"}\n---\n## Intent\nTools'
            with self.assertRaises(p.ProductError):
                p.parse_object(a, 'objects/directions/why.md')

if __name__ == '__main__':
    unittest.main()
