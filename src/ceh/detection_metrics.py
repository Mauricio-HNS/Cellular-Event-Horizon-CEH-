"""Metrics for evaluating blind horizon detections."""
from __future__ import annotations
import numpy as np

def lead_time(detected_time: int, transition_time: int) -> int:
    return int(transition_time - detected_time)

def within_window(detected_time: int, transition_time: int, tolerance: int) -> bool:
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    return abs(int(detected_time) - int(transition_time)) <= tolerance

def detection_rate(detections: list[int | None], transition_time: int,
                   tolerance: int) -> float:
    if not detections:
        return 0.0
    hits = sum(
        d is not None and within_window(d, transition_time, tolerance)
        for d in detections
    )
    return float(hits / len(detections))
