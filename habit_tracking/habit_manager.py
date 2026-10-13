from datetime import date
from habit import Habit


class HabitManager:
    """Manages habits and their completion events."""

    def __init__(self, database):
        self.database = database

    def create_habit(self, name, description, periodicity):
        if periodicity not in ("daily", "weekly"):
            raise ValueError("Periodicity must be daily or weekly.")

        habit = Habit(name, description, periodicity)

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO habits
            (name, description, periodicity, created_date)
            VALUES (?, ?, ?, ?)
        """, (
            habit.name,
            habit.description,
            habit.periodicity,
            habit.created_date
        ))

        connection.commit()
        connection.close()

    def get_habits(self):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, description, periodicity, created_date
            FROM habits
            ORDER BY id
        """)

        habits = cursor.fetchall()
        connection.close()

        return habits

    def complete_habit(self, habit_id, completion_date=None):
        completion_date = completion_date or date.today().isoformat()

        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO habit_events
            (habit_id, completion_date)
            VALUES (?, ?)
        """, (habit_id, completion_date))

        connection.commit()
        connection.close()

    def delete_habit(self, habit_id):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM habit_events WHERE habit_id = ?",
            (habit_id,)
        )

        cursor.execute(
            "DELETE FROM habits WHERE id = ?",
            (habit_id,)
        )

        connection.commit()
        connection.close()