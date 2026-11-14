"""
Pause model v2: how surprising is today's pause count FOR THIS PERSON?

pause_count is a small count that is usually 0 or 1, so a median/MAD z-score is the wrong tool (the MAD
is often 0 and one ordinary pause then looks huge). We model it as a negative binomial per person:
  * mean: the person's own recent average, shrunk toward a prior of PRIOR_MEAN
  * burstiness (dispersion): estimated from their own history, shrunk toward PRIOR_DISPERSION, then
    widened by 1/a for uncertainty in the mean (approximate)
and report the mid-p tail probability of today's count, converted to a z-equivalent (capped) so it sits
on the same deviation scale as every other feature.

ILLUSTRATIVE constants. Measured effect (synthetic, docs/ML_RESULTS.md): fewer false alerts at equal
sensitivity than median/MAD, robust to a wrong PRIOR_DISPERSION. Known loss: pause_total_ms (one very long
pause) is not scored in this model. Pure functions; no database access. Owner: Member 2 (Data & ML).
"""
from __future__ import annotations

from math import exp, lgamma, log
from statistics import NormalDist

DEVIATION_CAP = 4.0
PRIOR_MEAN = 0.8           # pauses per session, stand-in for the crew average
PRIOR_STRENGTH = 4.0       # sessions of evidence the prior is worth
PRIOR_DISPERSION = 0.5     # variance = mean + phi * mean^2
DISPERSION_STRENGTH = 8.0

_N = NormalDist()


def nb_pmf_mean(x: int, mu: float, phi: float) -> float:
    """Negative binomial by mean and dispersion (phi -> 0 is Poisson)."""
    phi = max(phi, 1e-6)
    r = 1.0 / phi
    return exp(lgamma(x + r) - lgamma(r) - lgamma(x + 1) + r * log(r / (r + mu)) + x * log(mu / (r + mu)))


def tail_probability(history_counts: list, today: int) -> float:
    n = len(history_counts)
    a = PRIOR_MEAN * PRIOR_STRENGTH + sum(history_counts)
    mu = a / (PRIOR_STRENGTH + n)
    if n >= 2:
        m = sum(history_counts) / n
        var = sum((c - m) ** 2 for c in history_counts) / (n - 1)
        phi_hat = max(0.0, (var - m) / max(m * m, 1e-9)) if m > 0 else 0.0
    else:
        phi_hat = PRIOR_DISPERSION
    phi = (DISPERSION_STRENGTH * PRIOR_DISPERSION + n * phi_hat) / (DISPERSION_STRENGTH + n)
    phi += 1.0 / a
    below = sum(nb_pmf_mean(k, mu, phi) for k in range(today))
    return max(1e-9, 1.0 - below - 0.5 * nb_pmf_mean(today, mu, phi))   # mid-p: P(X > x) + 0.5 P(X = x)


def pause_deviation_nb(history_counts: list, today: int) -> float:
    return min(max(0.0, _N.inv_cdf(1.0 - tail_probability(history_counts, today))), DEVIATION_CAP)
