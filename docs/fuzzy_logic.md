# Fuzzy Logic

Inputs: urgency, importance, time pressure, difficulty, each on 0–100.

Each input is fuzzified with overlapping triangular/trapezoidal membership functions. Rules use the minimum t-norm for fuzzy AND. Consequent sets are clipped by rule firing strength and combined with maximum aggregation.

The final priority is calculated by centroid defuzzification:

score = Σ(x × μ(x)) / Σμ(x)

The result is a crisp 0–100 score and a descriptive level.
