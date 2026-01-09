"""
CLI interface for the Todo Console Application.

This module handles user interface, menu display, and input collection.
"""

def display_menu():
    """Display the main menu options to the user."""
    print("\n" + "="*40)
    print("TODO APPLICATION - MAIN MENU")
    print("="*40)
    print("1. Add Task")
    print("2. View Task List")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Mark Task Incomplete")
    print("7. Exit")
    print("="*40)
    print("Choose an option (1-7): ", end="")


def get_user_choice():
    """Get and validate user menu choice."""
    choice = input().strip()
    if is_valid_menu_choice(choice):
        return choice
    return None


def is_valid_menu_choice(choice):
    """Validate if the menu choice is a valid option (1-7)."""
    try:
        choice_num = int(choice)
        return 1 <= choice_num <= 7
    except ValueError:
        return False


def is_valid_task_description(description):
    """Validate if the task description is not empty."""
    return description.strip() != ""


def is_valid_task_id(task_manager, task_id_str):
    """Validate if the task ID exists in the task manager."""
    try:
        task_id = int(task_id_str)
        return task_manager.get_task_by_id(task_id) is not None
    except ValueError:
        return False


def handle_add_task(task_manager):
    """Handle the Add Task functionality."""
    print("\n--- ADD TASK ---")
    description = input("Enter task description: ").strip()

    if not is_valid_task_description(description):
        print("Error: Task description cannot be empty.")
        return

    task = task_manager.add_task(description)
    print(f"Task added successfully with ID {task.id}: {task.description}")


def handle_view_tasks(task_manager):
    """Handle the View Task List functionality."""
    print("\n--- VIEW TASK LIST ---")
    tasks = task_manager.get_all_tasks()

    if not tasks:
        print("Your task list is empty.")
        return

    print(f"Total tasks: {len(tasks)}")
    for task in tasks:
        print(task)


def handle_update_task(task_manager):
    """Handle the Update Task functionality."""
    print("\n--- UPDATE TASK ---")

    if not task_manager.get_all_tasks():
        print("Your task list is empty. Cannot update any tasks.")
        return

    task_id_input = input("Enter task ID to update: ").strip()

    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Task ID must be a number.")
        return

    # Check if the task ID exists
    if not task_manager.get_task_by_id(task_id):
        print(f"Error: Task with ID {task_id} not found.")
        return

    task = task_manager.get_task_by_id(task_id)
    print(f"Current task: {task}")
    new_description = input("Enter new task description: ").strip()

    if not is_valid_task_description(new_description):
        print("Error: Task description cannot be empty.")
        return

    success = task_manager.update_task(task_id, new_description)
    if success:
        print(f"Task {task_id} updated successfully: {new_description}")
    else:
        print(f"Error: Could not update task {task_id}.")


def handle_delete_task(task_manager):
    """Handle the Delete Task functionality."""
    print("\n--- DELETE TASK ---")

    if not task_manager.get_all_tasks():
        print("Your task list is empty. Cannot delete any tasks.")
        return

    task_id_input = input("Enter task ID to delete: ").strip()

    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Task ID must be a number.")
        return

    # Check if the task ID exists
    if not task_manager.get_task_by_id(task_id):
        print(f"Error: Task with ID {task_id} not found.")
        return

    task = task_manager.get_task_by_id(task_id)
    print(f"Task to delete: {task}")
    confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()

    if confirm in ['y', 'yes']:
        success = task_manager.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Could not delete task {task_id}.")
    else:
        print("Task deletion cancelled.")


def handle_mark_complete(task_manager):
    """Handle the Mark Complete functionality."""
    print("\n--- MARK TASK COMPLETE ---")

    if not task_manager.get_all_tasks():
        print("Your task list is empty. No tasks to mark as complete.")
        return

    task_id_input = input("Enter task ID to mark as complete: ").strip()

    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Task ID must be a number.")
        return

    # Check if the task ID exists
    if not task_manager.get_task_by_id(task_id):
        print(f"Error: Task with ID {task_id} not found.")
        return

    task = task_manager.get_task_by_id(task_id)
    if task.completed:
        print(f"Task {task_id} is already marked as complete.")
        return

    success = task_manager.mark_task_complete(task_id)
    if success:
        print(f"Task {task_id} marked as complete: {task.description}")
    else:
        print(f"Error: Could not mark task {task_id} as complete.")


def handle_mark_incomplete(task_manager):
    """Handle the Mark Incomplete functionality."""
    print("\n--- MARK TASK INCOMPLETE ---")

    if not task_manager.get_all_tasks():
        print("Your task list is empty. No tasks to mark as incomplete.")
        return

    task_id_input = input("Enter task ID to mark as incomplete: ").strip()

    try:
        task_id = int(task_id_input)
    except ValueError:
        print("Error: Task ID must be a number.")
        return

    # Check if the task ID exists
    if not task_manager.get_task_by_id(task_id):
        print(f"Error: Task with ID {task_id} not found.")
        return

    task = task_manager.get_task_by_id(task_id)
    if not task.completed:
        print(f"Task {task_id} is already marked as incomplete.")
        return

    success = task_manager.mark_task_incomplete(task_id)
    if success:
        print(f"Task {task_id} marked as incomplete: {task.description}")
    else:
        print(f"Error: Could not mark task {task_id} as incomplete.")


def handle_exit():
    """Handle the Exit functionality."""
    print("\nThank you for using the Todo Application. Goodbye!")