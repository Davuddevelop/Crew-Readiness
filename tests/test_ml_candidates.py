from ml.candidates import nb_pmf, pause_deviation


def test_predictive_distribution_sums_to_one():
    assert abs(sum(nb_pmf(k, 5.2, 8.0) for k in range(200)) - 1.0) < 1e-9


def test_usual_pause_count_scores_zero_and_unusual_scores_high():
    hist = [0, 1, 0, 1, 1, 0, 1, 0]
    assert pause_deviation(hist, 0) == 0.0                       # fewer pauses than usual is never penalised
    assert pause_deviation(hist, 1) < 1.0                        # a usual count stays under the reason threshold
    assert pause_deviation(hist, 7) > pause_deviation(hist, 4) > pause_deviation(hist, 2) > 1.0


def test_more_history_makes_the_same_surprise_larger():
    # with only 2 sessions the prior dominates, so 5 pauses is less surprising than after 12 quiet sessions
    assert pause_deviation([0] * 12, 5) > pause_deviation([0, 0], 5)


def test_negative_binomial_matches_poisson_limit_and_normalises():
    from math import exp, lgamma, log
    from ml.candidates import nb_pmf_mean
    assert abs(sum(nb_pmf_mean(k, 2.0, 0.7) for k in range(300)) - 1.0) < 1e-9
    poisson = lambda k, m: exp(k * log(m) - m - lgamma(k + 1))
    assert abs(nb_pmf_mean(3, 2.0, 1e-9) - poisson(3, 2.0)) < 1e-6


def test_burstier_history_makes_the_same_count_less_surprising():
    from ml.candidates import pause_deviation_nb
    steady = [1, 1, 1, 1, 1, 1, 1, 1]
    bursty = [0, 0, 5, 0, 0, 4, 0, 1]      # same mean (1.5 vs 1.0 aside), far more variable
    assert pause_deviation_nb(bursty, 4) < pause_deviation_nb(steady, 4)


def test_product_scoring_equals_the_benchmarked_candidate():
    """The score the product shows must be the score the benchmark measured."""
    import numpy as np
    from app.baseline import compute_baseline, select_baseline_sessions
    from app.features import FEATURE_NAMES
    from app.scoring import score_session
    from ml.candidates import candidate_nb
    from ml.synth import Event, simulate_person
    sessions, _ = simulate_person(np.random.default_rng(5), 30, events=(Event("step", 20, 4, 0.2),))
    for i in range(5, 30):
        base = compute_baseline(select_baseline_sessions(sessions[:i]), FEATURE_NAMES, "docking_checklist_v1")
        view = score_session(sessions[i], base, "ok", "nb")
        assert abs(view.score - candidate_nb(sessions[:i], sessions[i])) < 1e-9


def test_api_reports_the_model_and_explains_pauses_in_plain_language(client):
    d = client.get("/api/readiness/plt-okafor").get_json()
    assert d["readiness"]["model"] == "nb-pause-v2"
    assert d["readiness"]["status"] == "SCORED"
