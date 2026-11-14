from ml.candidates import nb_pmf, pause_deviation


def test_predictive_distribution_sums_to_one():
    assert abs(sum(nb_pmf(k, 5.2, 8.0) for k in range(200)) - 1.0) < 1e-9


def test_usual_pause_count_scores_zero_and_unusual_scores_high():
    hist = [0, 1, 0, 1, 1, 0, 1, 0]
    assert pause_deviation(hist, 1) == 0.0
    assert pause_deviation(hist, 7) > pause_deviation(hist, 4) > 0.5


def test_more_history_makes_the_same_surprise_larger():
    # with only 2 sessions the prior dominates, so 5 pauses is less surprising than after 12 quiet sessions
    assert pause_deviation([0] * 12, 5) > pause_deviation([0, 0], 5)
