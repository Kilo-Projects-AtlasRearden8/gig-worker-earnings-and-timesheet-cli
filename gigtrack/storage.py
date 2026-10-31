"""Local JSON storage for shift records."""

from __future__ import annotations

import json
import os
from typing import Optional

from .models import Shift

DEFAULT_STORAGE_PATH = os.path.join(os.path.expanduser("~"), ".gigtrack", "shifts.json")


class Storage:
    """Reads and writes shift records to a local JSON file."""

    def __init__(self, path: str = DEFAULT_STORAGE_PATH) -> None:
        self.path = path

    def load(self) -> list[Shift]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
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
        shifts = self.load()
        filtered = [s for s in shifts if s.id != shift_id]
        if len(filtered) == len(shifts):
            return False
        self.save(filtered)
        return True
