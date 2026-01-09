"""
Todo Console Application - Phase I Implementation

A simple in-memory console-based todo application that allows users to:
- Add tasks
- View task list
- Update tasks
- Delete tasks
- Mark tasks as complete/incomplete

All data is stored in memory only and is lost when the application exits.
"""

from src.services.task_manager import TaskManager
from src.cli.interface import (
    display_menu, get_user_choice, handle_add_task, handle_view_tasks,
    handle_update_task, handle_delete_task, handle_mark_complete,
    handle_mark_incomplete, handle_exit
)


def main():
    """Main application loop that controls the flow of the application."""
    task_manager = TaskManager()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice is None:
            print("\nInvalid choice. Please select a number between 1 and 7.")
            continue

        if choice == "1":
            handle_add_task(task_manager)
        elif choice == "2":
            handle_view_tasks(task_manager)
        elif choice == "3":
            handle_update_task(task_manager)
        elif choice == "4":
            handle_delete_task(task_manager)
        elif choice == "5":
            handle_mark_complete(task_manager)
        elif choice == "6":
            handle_mark_incomplete(task_manager)
        elif choice == "7":
            handle_exit()
            break


# Main execution guard
if __name__ == "__main__":
    main()