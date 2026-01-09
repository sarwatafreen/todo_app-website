# Quickstart Guide: Phase I Todo Console Application

## Running the Application

1. Ensure Python 3.10+ is installed on your system
2. Navigate to the project directory containing `todo_app.py`
3. Run the application:
   ```bash
   python todo_app.py
   ```

## Using the Application

### Main Menu
The application presents a numbered menu with 7 options:
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

### Adding Tasks
1. Select option 1 from the main menu
2. Enter your task description when prompted
3. The task will be added with a unique ID and "incomplete" status

### Viewing Tasks
1. Select option 2 from the main menu
2. All tasks will be displayed with their ID, completion status, and description
3. Format: `{ID}. [{Status}] {Description}`
   - Status: ✓ for complete, ○ for incomplete

### Updating Tasks
1. Select option 3 from the main menu
2. Enter the ID of the task you want to update
3. Enter the new description for the task
4. The task description will be updated

### Deleting Tasks
1. Select option 4 from the main menu
2. Enter the ID of the task you want to delete
3. Confirm deletion when prompted
4. The task will be removed from the list

### Marking Tasks Complete/Incomplete
1. Select option 5 (Complete) or 6 (Incomplete) from the main menu
2. Enter the ID of the task you want to update
3. The task status will be changed accordingly

### Exiting
1. Select option 7 from the main menu
2. The application will terminate

## Error Handling
- Invalid menu choices will display an error message and return to the main menu
- Invalid task IDs will display an error message
- Empty task descriptions will be rejected
- Operations on non-existent tasks will display an error message
- Empty task lists will display appropriate messages

## Limitations
- Data is stored only in memory and will be lost when the application exits
- Single user only
- No persistence beyond runtime
- Maximum recommended task count: 1000 tasks (for optimal performance)