"""
Candidate detector: Gamma-Poisson model for pauses (counts), incumbent robust-z for the rest.

Why: pause_count is a small count that is usually 0 or 1, so a median/MAD z-score is the wrong tool
(MAD is often 0). Model it as Poisson(lambda) with lambda ~ Gamma(a0, b0) as a prior, update with the
person's own recent sessions, and ask: how surprising is today's count under the posterior predictive
(a negative binomial)? The tail probability is turned into a z-equivalent so it is on the same
deviation scale as every other feature and can be weighted the same way.

ILLUSTRATIVE choices (document and defend; PRIOR_* are decision material for the team):
  * prior mean 0.8 pauses/session and strength 4 sessions, a stand-in for the crew average
  * only pause_count is modelled; pause_total_ms no longer counts. KNOWN LOSS: one very long pause
    is invisible to this candidate. Extending it is the owner's job.
"""
from __future__ import annotations

from math import exp, lgamma, log
from statistics import NormalDist

from app.baseline import compute_baseline, select_baseline_sessions
from app.features import FEATURE_NAMES
from app.scoring import DEVIATION_CAP, GROUP_WEIGHTS, score_session
from app.tasks import DEFAULT_TASK_TYPE

PRIOR_MEAN = 0.8
PRIOR_STRENGTH = 4.0   # in sessions: how many sessions of evidence the prior is worth

_N = NormalDist()


def nb_pmf(x: int, a: float, b: float) -> float:
    """Posterior predictive of a Poisson count with a Gamma(a, rate b) prior on the rate."""
    return exp(lgamma(x + a) - lgamma(a) - lgamma(x + 1) + a * log(b / (b + 1)) - x * log(b + 1))


def pause_deviation(history_counts: list, today: int) -> float:
    a = PRIOR_MEAN * PRIOR_STRENGTH + sum(history_counts)
    b = PRIOR_STRENGTH + len(history_counts)
    below = sum(nb_pmf(k, a, b) for k in range(today))
    p_here = nb_pmf(today, a, b)
    tail = max(1e-9, 1.0 - below - 0.5 * p_here)       # mid-p: P(X > x) + 0.5 P(X = x)
    return min(max(0.0, _N.inv_cdf(1.0 - tail)), DEVIATION_CAP)


def candidate_pause_model(history: list, today: dict) -> "float | None":
    base_sessions = select_baseline_sessions(history)
    baseline = compute_baseline(base_sessions, FEATURE_NAMES, DEFAULT_TASK_TYPE)
    view = score_session({n: today[n] for n in FEATURE_NAMES}, baseline, today["data_quality"])
    if view.status != "SCORED":
        return None
    groups = dict(view.group_scores)
    groups["pauses"] = pause_deviation([s["pause_count"] for s in base_sessions], int(today["pause_count"]))
    return sum(GROUP_WEIGHTS[g] * s for g, s in groups.items())


# ---- v2: negative binomial with a per-person dispersion ------------------------------------------
PRIOR_DISPERSION = 0.5   # ILLUSTRATIVE: crew-level burstiness (variance = mean + phi * mean^2). Decision material.
DISPERSION_STRENGTH = 8.0


def nb_pmf_mean(x: int, mu: float, phi: float) -> float:
    """Negative binomial parameterised by mean mu and dispersion phi (phi -> 0 is Poisson)."""
    phi = max(phi, 1e-6)
    r = 1.0 / phi
    return exp(lgamma(x + r) - lgamma(r) - lgamma(x + 1) + r * log(r / (r + mu)) + x * log(mu / (r + mu)))


def pause_deviation_nb(history_counts: list, today: int) -> float:
    n = len(history_counts)
    a = PRIOR_MEAN * PRIOR_STRENGTH + sum(history_counts)
    mu = a / (PRIOR_STRENGTH + n)                                   # shrunk personal mean
    if n >= 2:
        m = sum(history_counts) / n
        var = sum((c - m) ** 2 for c in history_counts) / (n - 1)
        phi_hat = max(0.0, (var - m) / max(m * m, 1e-9)) if m > 0 else 0.0
    else:
        phi_hat = PRIOR_DISPERSION
    phi = (DISPERSION_STRENGTH * PRIOR_DISPERSION + n * phi_hat) / (DISPERSION_STRENGTH + n)   # shrunk dispersion
    phi += 1.0 / a                                                  # widen for uncertainty in mu (Gamma posterior)
    below = sum(nb_pmf_mean(k, mu, phi) for k in range(today))
    tail = max(1e-9, 1.0 - below - 0.5 * nb_pmf_mean(today, mu, phi))
    return min(max(0.0, _N.inv_cdf(1.0 - tail)), DEVIATION_CAP)


def candidate_nb(history: list, today: dict) -> "float | None":
    base_sessions = select_baseline_sessions(history)
    baseline = compute_baseline(base_sessions, FEATURE_NAMES, DEFAULT_TASK_TYPE)
    view = score_session({n: today[n] for n in FEATURE_NAMES}, baseline, today["data_quality"])
    if view.status != "SCORED":
        return None
    groups = dict(view.group_scores)
    groups["pauses"] = pause_deviation_nb([s["pause_count"] for s in base_sessions], int(today["pause_count"]))
    return sum(GROUP_WEIGHTS[g] * s for g, s in groups.items())
