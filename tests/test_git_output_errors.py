import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from openproduct.__main__ import main
from openproduct.parser import ProductError
from openproduct.repository import Repository


class GitOutputErrors(unittest.TestCase):
    def test_non_utf8_stdout_is_structured_even_for_optional_git(self):
        result = subprocess.CompletedProcess(['git'], 0, b'\xff', b'')
        with patch('openproduct.repository.subprocess.run', return_value=result):
            for optional in (False, True):
                with self.subTest(optional=optional):
                    with self.assertRaises(ProductError) as caught:
                        Repository('.').git('status', optional=optional)
                    record = caught.exception.record()
                    self.assertEqual(record['code'], 'SCHEMA_INVALID')
                    self.assertIn('UTF-8', record['explanation'])
                    self.assertTrue(record['nextAction'])

    def test_cli_non_utf8_git_output_returns_error_json(self):
        result = subprocess.CompletedProcess(['git'], 0, b'\xff', b'')
        with tempfile.TemporaryDirectory() as root:
            output = io.StringIO()
            with patch('openproduct.repository.subprocess.run', return_value=result):
                with contextlib.redirect_stdout(output):
                    status = main(['--repo', root, 'init', '--canonical-ref', 'refs/heads/product'])
            self.assertEqual(status, 2)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload['errors'][0]['code'], 'SCHEMA_INVALID')
            self.assertIn('UTF-8', payload['errors'][0]['explanation'])


if __name__ == '__main__':
    unittest.main()
