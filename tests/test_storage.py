"""Tests for storage behavior: add, delete (exact + prefix), env var path."""

from __future__ import annotations

import os
import tempfile
import unittest

from gigtrack.models import Shift
from gigtrack.storage import Storage, default_storage_path, ENV_STORAGE_PATH


def _make_shift(shift_id: str, date: str = "2026-10-30") -> Shift:
    return Shift(
        id=shift_id,
        date=date,
        job="Job A",
        shift_type="gig",
        hours=8.0,
        rate=20.0,
        earnings=160.0,
        expenses=0.0,
    )


class StorageDeleteTests(unittest.TestCase):
    def test_delete_exact_id(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = tmp.name
        try:
            storage = Storage(path)
            storage.add(_make_shift("abc12345"))
            storage.add(_make_shift("def67890"))
            self.assertTrue(storage.delete("abc12345"))
            self.assertEqual(len(storage.load()), 1)
            self.assertEqual(storage.load()[0].id, "def67890")
        finally:
            os.unlink(path)

    def test_delete_by_prefix(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = tmp.name
        try:
            storage = Storage(path)
            storage.add(_make_shift("abc12345"))
            storage.add(_make_shift("def67890"))
            self.assertTrue(storage.delete("abc12"))
            self.assertEqual(len(storage.load()), 1)
            self.assertEqual(storage.load()[0].id, "def67890")
        finally:
            os.unlink(path)

    def test_delete_ambiguous_prefix(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = tmp.name
        try:
            storage = Storage(path)
            storage.add(_make_shift("abc12345"))
            storage.add(_make_shift("abc12367"))
            self.assertFalse(storage.delete("abc12"))
            self.assertEqual(len(storage.load()), 2)
        finally:
            os.unlink(path)

    def test_delete_nonexistent(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = tmp.name
        try:
            storage = Storage(path)
            storage.add(_make_shift("abc12345"))
            self.assertFalse(storage.delete("zzz99999"))
            self.assertEqual(len(storage.load()), 1)
        finally:
            os.unlink(path)


class EnvVarStorageTests(unittest.TestCase):
    def test_env_var_overrides_default(self):
        old = os.environ.pop(ENV_STORAGE_PATH, None)
        try:
            os.environ[ENV_STORAGE_PATH] = "/tmp/kilo/gigtrack-env-test.json"
            self.assertEqual(default_storage_path(), "/tmp/kilo/gigtrack-env-test.json")
        finally:
            if old is None:
                os.environ.pop(ENV_STORAGE_PATH, None)
            else:
                os.environ[ENV_STORAGE_PATH] = old


if __name__ == "__main__":
    unittest.main()
