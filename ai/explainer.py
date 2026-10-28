import json
from .chains import build_explanation_chain

def explain_results(analyses, available_hours):
    payload = {
        "available_hours_today": available_hours,
        "tasks": [
            {
                "task": a.task.name,
                "priority_score": round(a.priority_score, 2),
                "priority_level": a.priority_level,
                "urgency": round(a.urgency, 2),
                "importance": a.task.importance,
                "time_pressure": round(a.time_pressure, 2),
                "difficulty": a.task.difficulty,
                "estimated_hours": a.task.estimated_hours,
                "deadline": str(a.task.deadline) if a.task.deadline else None,
            } for a in analyses
        ]
    }
    chain = build_explanation_chain()
    response = chain.invoke({"results": json.dumps(payload, indent=2)})
    return response.content if hasattr(response, "content") else str(response)
