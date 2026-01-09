# CLI Interface Contract: Phase I Todo Console Application

## Overview
This document defines the command-line interface contract for the todo console application, specifying the user interaction patterns, input/output formats, and error handling behavior.

## Menu Interface

### Main Menu Display
**Output Format**:
```
========================================
TODO APPLICATION - MAIN MENU
========================================
1. Add Task
2. View Task List
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit
========================================
Choose an option (1-7):
```

### Menu Selection
**Input**: Single numeric character (1-7)
**Validation**: Must be a number between 1 and 7
**Error Response**: "Invalid choice. Please select a number between 1 and 7."

## Task Display Format
**Output Format**: `{ID}. [{Status}] {Description}`
- ID: Sequential integer starting from 1
- Status: ✓ (complete) or ○ (incomplete)
- Description: User-provided task description

## Operation Contracts

### Add Task
**Input Flow**:
1. Prompt: "Enter task description: "
2. Input: Text description (non-empty)
3. Output: "Task added successfully with ID {ID}: {description}"

**Error Cases**:
- Empty description: "Error: Task description cannot be empty."

### View Task List
**Output Flow**:
1. Output: "Total tasks: {count}"
2. Output: Each task in display format
3. If empty: "Your task list is empty."

### Update Task
**Input Flow**:
1. Prompt: "Enter task ID to update: "
2. Input: Valid task ID
3. Prompt: "Enter new task description: "
4. Input: New description (non-empty)
5. Output: "Task {ID} updated successfully: {new_description}"

**Error Cases**:
- Invalid ID: "Error: Task with ID {ID} not found."
- Empty description: "Error: Task description cannot be empty."
- Non-numeric ID: "Error: Task ID must be a number."

### Delete Task
**Input Flow**:
1. Prompt: "Enter task ID to delete: "
2. Input: Valid task ID
3. Display: "Task to delete: {task_info}"
4. Prompt: "Are you sure you want to delete this task? (y/N): "
5. Input: Confirmation (y/yes or N/no)
6. Output: "Task {ID} deleted successfully." (if confirmed)

**Error Cases**:
- Invalid ID: "Error: Task with ID {ID} not found."
- Non-numeric ID: "Error: Task ID must be a number."
- Cancelled: "Task deletion cancelled."

### Mark Complete/Incomplete
**Input Flow**:
1. Prompt: "Enter task ID to mark as {complete/incomplete}: "
2. Input: Valid task ID
3. Output: "Task {ID} marked as {complete/incomplete}: {description}"

**Error Cases**:
- Invalid ID: "Error: Task with ID {ID} not found."
- Already correct status: "Task {ID} is already marked as {complete/incomplete}."
- Non-numeric ID: "Error: Task ID must be a number."

## Error Handling Standards

### Input Validation
- All numeric inputs must be integers
- All task descriptions must be non-empty after trimming whitespace
- All task IDs must exist in the current task list

### Error Message Format
- Format: "Error: {descriptive message}"
- Error messages should be actionable and clear
- Errors should not crash the application

### Application State
- All operations should maintain application stability
- Invalid operations should return to main menu without changing state
- Empty list conditions should be handled gracefully