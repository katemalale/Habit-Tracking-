from collections import defaultdict
from datetime import date, timedelta


class Analytics:
    """Provides functional-style analysis of habit data."""

    def __init__(self, database):
        self.database = database

    def get_all_habits(self):
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

    def get_habits_by_periodicity(self, periodicity):
        habits = self.get_all_habits()

        return list(
            filter(
                lambda habit: habit[3].lower() == periodicity.lower(),
                habits
            )
        )

    def get_events(self, habit_id):
        connection = self.database.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT completion_date
            FROM habit_events
            WHERE habit_id = ?
            ORDER BY completion_date
        """, (habit_id,))

        events = [row[0] for row in cursor.fetchall()]
        connection.close()

        return events

    def longest_streak(self, habit_id):
        events = self.get_events(habit_id)

        if not events:
            return 0

        dates = sorted(
            set(date.fromisoformat(event) for event in events)
        )

        longest = 1
        current = 1

        for previous, current_date in zip(dates, dates[1:]):
            if current_date == previous + timedelta(days=1):
                current += 1
            else:
                current = 1

            longest = max(longest, current)

        return longest

    def longest_streak_all_habits(self):
        habits = self.get_all_habits()

        streaks = list(
            map(
                lambda habit: (
                    habit[1],
                    self.longest_streak(habit[0])
                ),
                habits
            )
        )

        if not streaks:
            return None

        return max(streaks, key=lambda item: item[1])