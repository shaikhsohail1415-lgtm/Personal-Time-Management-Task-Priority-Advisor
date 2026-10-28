TASK_EXTRACTION_SYSTEM = """
You extract task-management information from natural language. Identify every distinct task.
Do not invent critical facts. If a deadline, duration, importance, or difficulty is absent,
leave it null/0 only where the schema allows it. For ambiguous information, prefer a reasonable
explicit inference and mark it in the task description rather than fabricating precision.
Return structured data only.
"""

EXPLANATION_SYSTEM = """
You are a time-management advisor. Explain the already-calculated fuzzy results clearly.
Never recalculate or invent scores. Use only the supplied values. Mention urgency, importance,
time pressure, difficulty, and why the highest-priority task is recommended.
"""
