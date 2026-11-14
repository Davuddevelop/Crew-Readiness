"""The harness must itself be trustworthy: ground truth is right and it can tell good from bad detectors."""
import numpy as np

from ml.evaluate import evaluate, incumbent_detector
from ml.synth import Event, simulate_person


def test_truth_labels_match_the_injected_event():
    ev = Event(shape="step", start=5, length=3, magnitude=0.2)
    _, truth = simulate_person(np.random.default_rng(1), 12, events=(ev,))
    assert [i for i, t in enumerate(truth) if t > 0] == [5, 6, 7]


def test_ramp_and_spike_shapes():
    assert [Event("ramp", 2, 4, 1.0).strength(i) for i in range(2, 6)] == [0.25, 0.5, 0.75, 1.0]
    assert [Event("spike", 3, 9, 1.0).strength(i) for i in range(5)] == [0, 0, 0, 1.0, 0]


def test_an_always_alert_detector_is_caught_by_false_alerts():
    r = evaluate(lambda h, t: 99.0, shape="step", magnitude=0.2, length=5, n_people=20)
    assert r.false_alert_rate == 1.0 and r.detection_rate == 1.0


def test_a_never_alert_detector_is_caught_by_detection_rate():
    r = evaluate(lambda h, t: 0.0, shape="step", magnitude=0.2, length=5, n_people=20)
    assert r.detection_rate == 0.0 and r.false_alert_rate == 0.0


def test_incumbent_detects_big_events_more_than_small_ones():
    small = evaluate(incumbent_detector, shape="step", magnitude=0.03, length=5, n_people=60, seed=3)
    big = evaluate(incumbent_detector, shape="step", magnitude=0.30, length=5, n_people=60, seed=3)
    assert big.detection_rate > small.detection_rate
