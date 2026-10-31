"""Gig shift data model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Shift:
    """A single logged work shift."""

    id: str
    date: str  # ISO YYYY-MM-DD
    job: str
    shift_type: str
    hours: float
    rate: float
    earnings: float
    expenses: float
    notes: str = ""

    def net(self) -> float:
        """Earnings minus expenses, rounded to cents."""
        return round(self.earnings - self.expenses, 2)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Shift":
        return Shift(
            id=data["id"],
            date=data["date"],
            job=data["job"],
            shift_type=data["shift_type"],
            hours=float(data["hours"]),
            rate=float(data["rate"]),
            earnings=float(data["earnings"]),
            expenses=float(data["expenses"]),
            notes=data.get("notes", ""),
        )
