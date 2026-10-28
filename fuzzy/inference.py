import numpy as np
from .membership import fuzzify, OUTPUT_SETS
from .rules import RULES
from .defuzzification import centroid

class MamdaniFuzzySystem:
    def __init__(self):
        self.universe = np.linspace(0, 100, 1001)

    @staticmethod
    def level(score):
        if score < 20: return "Very Low"
        if score < 40: return "Low"
        if score < 60: return "Medium"
        if score < 80: return "High"
        return "Very High"

    def infer(self, urgency, importance, time_pressure, difficulty):
        values = {"urgency": urgency, "importance": importance,
                  "time_pressure": time_pressure, "difficulty": difficulty}
        memberships = {v: fuzzify(v, x) for v, x in values.items()}
        aggregated = np.zeros_like(self.universe)
        activated = []

        for idx, (antecedents, consequent, description) in enumerate(RULES, 1):
            strengths = [memberships[var][label] for var, label in antecedents.items()]
            strength = min(strengths)
            if strength > 0:
                output_curve = np.array([OUTPUT_SETS[consequent](x) for x in self.universe])
                clipped = np.minimum(strength, output_curve)
                aggregated = np.maximum(aggregated, clipped)
                activated.append({
                    "rule": idx, "description": f"IF " + " AND ".join(f"{v} is {l}" for v,l in antecedents.items()) + f" THEN priority is {consequent}",
                    "strength": round(float(strength), 4), "consequent": consequent
                })

        score = centroid(self.universe, aggregated)
        return {
            "score": score,
            "level": self.level(score),
            "memberships": memberships,
            "rules": activated,
            "aggregated": {"x": self.universe.tolist(), "mu": aggregated.tolist()}
        }
