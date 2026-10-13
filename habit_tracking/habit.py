from datetime import date


class Habit:
    """Represents a habit tracked by the application."""

    def __init__(self, name, description, periodicity, created_date=None):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_date = created_date or date.today().isoformat()

    def __str__(self):
        return f"{self.name} ({self.periodicity})"