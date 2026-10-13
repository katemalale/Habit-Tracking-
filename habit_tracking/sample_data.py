from datetime import date, timedelta


PREDEFINED_HABITS = [
    {
        "name": "Exercise",
        "description": "Complete a workout session.",
        "periodicity": "daily"
    },
    {
        "name": "Read",
        "description": "Read for at least 30 minutes.",
        "periodicity": "daily"
    },
    {
        "name": "Drink Water",
        "description": "Drink at least 2 litres of water.",
        "periodicity": "daily"
    },
    {
        "name": "Clean the House",
        "description": "Complete the weekly house cleaning routine.",
        "periodicity": "weekly"
    },
    {
        "name": "Review Finances",
        "description": "Review personal finances and expenses.",
        "periodicity": "weekly"
    }
]


def add_sample_data(manager):
    """Create predefined habits and four weeks of sample completion data."""

    existing_habits = manager.get_habits()

    if existing_habits:
        return

    for habit in PREDEFINED_HABITS:
        manager.create_habit(
            habit["name"],
            habit["description"],
            habit["periodicity"]
        )

    habits = manager.get_habits()

    start_date = date.today() - timedelta(days=27)

    for habit_id, name, description, periodicity, created_date in habits:

        if periodicity == "daily":
            for day in range(28):
                completion_date = start_date + timedelta(days=day)

                # Deliberately leave some days incomplete
                if day % 5 != 0:
                    manager.complete_habit(
                        habit_id,
                        completion_date.isoformat()
                    )

        elif periodicity == "weekly":
            for week in range(4):
                completion_date = start_date + timedelta(days=week * 7)

                manager.complete_habit(
                    habit_id,
                    completion_date.isoformat()
                )