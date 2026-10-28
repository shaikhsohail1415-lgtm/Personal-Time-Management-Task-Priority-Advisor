import numpy as np

def triangular(x, a, b, c):
    x = float(x)
    if x <= a or x >= c:
        return 0.0 if x != b else 1.0
    if x == b:
        return 1.0
    return (x-a)/(b-a) if x < b else (c-x)/(c-b)

def trapezoidal(x, a, b, c, d):
    x = float(x)
    if x < a or x > d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if a <= x < b:
        return (x-a)/(b-a) if b != a else 1.0
    return (d-x)/(d-c) if d != c else 1.0

INPUT_SETS = {
    "urgency": {
        "Low": lambda x: trapezoidal(x, 0, 0, 20, 40),
        "Medium": lambda x: triangular(x, 20, 50, 70),
        "High": lambda x: trapezoidal(x, 50, 70, 100, 100),
    },
    "importance": {
        "Low": lambda x: trapezoidal(x, 0, 0, 20, 40),
        "Medium": lambda x: triangular(x, 20, 50, 70),
        "High": lambda x: trapezoidal(x, 50, 70, 100, 100),
    },
    "time_pressure": {
        "Low": lambda x: trapezoidal(x, 0, 0, 20, 40),
        "Medium": lambda x: triangular(x, 20, 50, 70),
        "High": lambda x: trapezoidal(x, 50, 70, 100, 100),
    },
    "difficulty": {
        "Easy": lambda x: trapezoidal(x, 0, 0, 20, 40),
        "Moderate": lambda x: triangular(x, 20, 50, 70),
        "Difficult": lambda x: trapezoidal(x, 50, 70, 100, 100),
    },
}

OUTPUT_SETS = {
    "Very Low": lambda x: trapezoidal(x, 0, 0, 10, 25),
    "Low": lambda x: triangular(x, 10, 25, 40),
    "Medium": lambda x: triangular(x, 30, 50, 65),
    "High": lambda x: triangular(x, 55, 70, 85),
    "Very High": lambda x: trapezoidal(x, 75, 90, 100, 100),
}

def fuzzify(variable, value):
    return {name: float(fn(value)) for name, fn in INPUT_SETS[variable].items()}
