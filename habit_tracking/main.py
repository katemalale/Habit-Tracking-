from database import Database
from habit_manager import HabitManager
from analytics import Analytics
from cli import CLI
from sample_data import add_sample_data


def main():
    database = Database()

    manager = HabitManager(database)
    analytics = Analytics(database)

    add_sample_data(manager)

    application = CLI(manager, analytics)
    application.run()


if __name__ == "__main__":
    main()