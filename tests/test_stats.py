"""The statistics helpers against values computed independently."""
import math

import pytest

from eval.stats import fisher_exact, wilson


def test_fisher_extreme_table():
    # 18/18 vs 0/18: only the observed table and its mirror are as unlikely, so p = 2 / C(36, 18)
    assert fisher_exact(18, 0, 0, 18) == pytest.approx(2 / math.comb(36, 18))


def test_fisher_no_difference_is_one():
    assert fisher_exact(5, 5, 5, 5) == pytest.approx(1.0)


def test_fisher_known_value():
    # the classic tea-tasting table [[3, 1], [1, 3]]: two-sided p = 34/70
    assert fisher_exact(3, 1, 1, 3) == pytest.approx(34 / 70)


def test_wilson_bounds():
    lo, hi = wilson(0, 18)
    assert lo == 0.0 and hi == pytest.approx(0.1759, abs=1e-3)
    lo, hi = wilson(18, 18)
    assert hi == 1.0 and lo == pytest.approx(0.8241, abs=1e-3)
    lo, hi = wilson(9, 18)
    assert lo < 0.5 < hi
