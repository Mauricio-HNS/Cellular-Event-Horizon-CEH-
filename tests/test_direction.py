import pytest
from ceh.direction import DIMENSIONS, DirectionSnapshot, direction_report

def snap(value, timestamp="t"):
    return DirectionSnapshot(timestamp, {k: value for k in DIMENSIONS})

def test_direction_index_and_change():
    previous = snap(0.40, "t0")
    current = snap(0.60, "t1")
    report = direction_report(current, previous)
    assert report.direction_index == pytest.approx(0.60)
    assert all(v == pytest.approx(0.20) for v in report.changes.values())
    assert set(report.improving) == set(DIMENSIONS)
    assert not report.declining

def test_decline_is_visible():
    previous = snap(0.80, "t0")
    current = snap(0.70, "t1")
    report = direction_report(current, previous)
    assert set(report.declining) == set(DIMENSIONS)

def test_invalid_range_rejected():
    values = {k: 0.5 for k in DIMENSIONS}
    values["novelty"] = 1.1
    with pytest.raises(ValueError):
        direction_report(DirectionSnapshot("t", values))
