from models.task import Task

def validate_task(task: Task):
    if not task.name.strip():
        raise ValueError("Task name cannot be empty.")
    if task.estimated_hours <= 0:
        raise ValueError("Estimated hours must be positive.")
    if not 0 <= task.importance <= 100:
        raise ValueError("Importance must be between 0 and 100.")
    if not 0 <= task.difficulty <= 100:
        raise ValueError("Difficulty must be between 0 and 100.")
    return True
