from __future__ import annotations

import numpy as np


def rolling_variance(values: np.ndarray, window: int = 10) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if window < 2 or window > values.size:
        raise ValueError("window must be between 2 and the number of observations")
    return np.array(
        [np.var(values[i - window + 1 : i + 1]) for i in range(window - 1, values.size)]
    )


def rolling_autocorrelation(values: np.ndarray, window: int = 10) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if window < 3 or window > values.size:
        raise ValueError("window must be between 3 and the number of observations")
    result = []
    for i in range(window - 1, values.size):
        x = values[i - window + 1 : i + 1]
        if np.std(x[:-1]) == 0 or np.std(x[1:]) == 0:
            result.append(np.nan)
        else:
            result.append(float(np.corrcoef(x[:-1], x[1:])[0, 1]))
    return np.asarray(result)


def relaxation_rate(values: np.ndarray) -> float:
    """Simple lag-1 recovery proxy; not a universal critical-slowing-down estimator."""
    values = np.asarray(values, dtype=float)
    if values.size < 3:
        raise ValueError("at least three observations are required")
    x = values[:-1]
    y = values[1:]
    slope = np.polyfit(x - np.mean(x), y - np.mean(y), 1)[0]
    return float(1.0 - slope)
