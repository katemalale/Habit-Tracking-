import unittest
import os
import tempfile

from database import Database
from habit_manager import HabitManager


class TestHabitManager(unittest.TestCase):

    def setUp(self):
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()

        self.database = Database(self.test_db.name)
        self.manager = HabitManager(self.database)

    def tearDown(self):
        os.remove(self.test_db.name)

    def test_create_habit(self):
        self.manager.create_habit(
            "Exercise",
            "Complete a workout",
            "daily"
        )

        habits = self.manager.get_habits()

        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0][1], "Exercise")
        self.assertEqual(habits[0][3], "daily")

    def test_invalid_periodicity(self):
        with self.assertRaises(ValueError):
            self.manager.create_habit(
                "Exercise",
                "Complete a workout",
                "monthly"
            )

    def test_complete_habit(self):
        self.manager.create_habit(
            "Read",
            "Read for 30 minutes",
            "daily"
        )

        habits = self.manager.get_habits()
        habit_id = habits[0][0]

        self.manager.complete_habit(
            habit_id,
            "2026-09-21"
        )

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM habit_events WHERE habit_id = ?",
            (habit_id,)
        )

        count = cursor.fetchone()[0]
        connection.close()

        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()