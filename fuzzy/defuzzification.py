import numpy as np

def centroid(universe, aggregated):
    universe = np.asarray(universe, dtype=float)
    aggregated = np.asarray(aggregated, dtype=float)
    denom = np.sum(aggregated)
    if denom == 0:
        return 0.0
    return float(np.sum(universe * aggregated) / denom)
