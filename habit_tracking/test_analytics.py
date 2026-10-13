import unittest
import os
import tempfile

from database import Database
from habit_manager import HabitManager
from analytics import Analytics


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()

        self.database = Database(self.test_db.name)
        self.manager = HabitManager(self.database)
        self.analytics = Analytics(self.database)

    def tearDown(self):
        os.remove(self.test_db.name)

    def test_filter_by_periodicity(self):
        self.manager.create_habit(
            "Exercise",
            "Workout",
            "daily"
        )

        self.manager.create_habit(
            "Clean House",
            "Weekly cleaning",
            "weekly"
        )

        daily = self.analytics.get_habits_by_periodicity("daily")
        weekly = self.analytics.get_habits_by_periodicity("weekly")

        self.assertEqual(len(daily), 1)
        self.assertEqual(len(weekly), 1)

    def test_longest_streak(self):
        self.manager.create_habit(
            "Exercise",
            "Workout",
            "daily"
        )

        habits = self.manager.get_habits()
        habit_id = habits[0][0]

        self.manager.complete_habit(habit_id, "2026-09-01")
        self.manager.complete_habit(habit_id, "2026-09-02")
        self.manager.complete_habit(habit_id, "2026-09-03")

        streak = self.analytics.longest_streak(habit_id)

        self.assertEqual(streak, 3)


if __name__ == "__main__":
    unittest.main()