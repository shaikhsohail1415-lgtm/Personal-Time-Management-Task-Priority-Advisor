from datetime import date, datetime
import math

def calculate_urgency(deadline):
    if deadline is None:
        return 15.0
    days = (deadline - date.today()).total_seconds() / 86400
    # Continuous exponential-style urgency curve: approaches 100 as deadline approaches/overdue.
    if days <= 0:
        return 100.0
    return round(100.0 * math.exp(-days / 3.0), 2)

def calculate_time_pressure(estimated_hours, available_hours):
    if available_hours <= 0:
        return 100.0
    ratio = estimated_hours / available_hours
    # Smooth saturation: 50% of available time -> ~39, equal -> ~63, 2x -> ~86.
    return round(100.0 * (1 - math.exp(-ratio)), 2)
