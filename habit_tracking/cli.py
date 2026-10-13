class CLI:
    """Command Line Interface for the Habit Tracking Application."""

    def __init__(self, manager, analytics):
        self.manager = manager
        self.analytics = analytics

    def display_habits(self):
        habits = self.manager.get_habits()

        if not habits:
            print("\nNo habits found.")
            return

        print("\n--- Your Habits ---")

        for habit in habits:
            habit_id, name, description, periodicity, created_date = habit

            print(
                f"{habit_id}. {name} | "
                f"{periodicity} | "
                f"Created: {created_date}"
            )

    def create_habit(self):
        print("\n--- Create Habit ---")

        name = input("Habit name: ")
        description = input("Description: ")
        periodicity = input("Periodicity (daily/weekly): ").lower()

        try:
            self.manager.create_habit(
                name,
                description,
                periodicity
            )
            print("Habit created successfully.")

        except ValueError as error:
            print(f"Error: {error}")

    def complete_habit(self):
        self.display_habits()

        try:
            habit_id = int(input("\nEnter habit ID to check off: "))
            self.manager.complete_habit(habit_id)
            print("Habit completed successfully.")

        except ValueError:
            print("Please enter a valid habit ID.")

    def delete_habit(self):
        self.display_habits()

        try:
            habit_id = int(input("\nEnter habit ID to delete: "))
            self.manager.delete_habit(habit_id)
            print("Habit deleted successfully.")

        except ValueError:
            print("Please enter a valid habit ID.")

    def show_analytics(self):
        print("\n--- Habit Analytics ---")

        habits = self.analytics.get_all_habits()

        print(f"\nTotal habits: {len(habits)}")

        daily = self.analytics.get_habits_by_periodicity("daily")
        weekly = self.analytics.get_habits_by_periodicity("weekly")

        print(f"Daily habits: {len(daily)}")
        print(f"Weekly habits: {len(weekly)}")

        longest = self.analytics.longest_streak_all_habits()

        if longest:
            print(
                f"Longest streak: {longest[0]} "
                f"({longest[1]} days)"
            )
        else:
            print("No completion data available.")

    def run(self):
        while True:
            print("\n==============================")
            print("      HABIT TRACKER")
            print("==============================")
            print("1. View habits")
            print("2. Create habit")
            print("3. Check off habit")
            print("4. Delete habit")
            print("5. View analytics")
            print("6. Exit")

            choice = input("\nChoose an option: ")

            if choice == "1":
                self.display_habits()

            elif choice == "2":
                self.create_habit()

            elif choice == "3":
                self.complete_habit()

            elif choice == "4":
                self.delete_habit()

            elif choice == "5":
                self.show_analytics()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")