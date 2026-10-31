"""Local JSON storage for shift records."""

from __future__ import annotations

import json
import os
from typing import Optional

from .models import Shift

DEFAULT_STORAGE_PATH = os.path.join(os.path.expanduser("~"), ".gigtrack", "shifts.json")
ENV_STORAGE_PATH = "GIGTRACK_STORAGE"


def default_storage_path() -> str:
    """Return the storage path, honoring the GIGTRACK_STORAGE env var."""
    return os.environ.get(ENV_STORAGE_PATH, DEFAULT_STORAGE_PATH)


class Storage:
    """Reads and writes shift records to a local JSON file."""

    def __init__(self, path: str | None = None) -> None:
        self.path = path or default_storage_path()

    def load(self) -> list[Shift]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as handle:
            content = handle.read().strip()
        if not content:
            return []
        data = json.loads(content)
        return [Shift.from_dict(item) for item in data]

    def save(self, shifts: list[Shift]) -> None:
        directory = os.path.dirname(self.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump([shift.to_dict() for shift in shifts], handle, indent=2)

    def add(self, shift: Shift) -> None:
        shifts = self.load()
        shifts.append(shift)
        self.save(shifts)

    def delete(self, shift_id: str) -> bool:
        """Delete a shift by exact id or unambiguous prefix.

        If ``shift_id`` does not match a full id, shifts whose id starts with
        ``shift_id`` are considered. Deletion proceeds only when exactly one
        shift matches the prefix; otherwise no deletion occurs and False is
        returned.
        """
        shifts = self.load()
        exact = [s for s in shifts if s.id == shift_id]
        if exact:
            filtered = [s for s in shifts if s.id != shift_id]
            self.save(filtered)
            return True
        matches = [s for s in shifts if s.id.startswith(shift_id)]
        if len(matches) == 1:
            filtered = [s for s in shifts if s.id != matches[0].id]
            self.save(filtered)
            return True
        return False
