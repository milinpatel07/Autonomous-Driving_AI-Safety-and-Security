"""Physics checks for avsafety.perturb (offline, synthetic inputs)."""
import numpy as np
import pytest

from avsafety import perturb as P


@pytest.mark.parametrize("V", [25.0, 50.0, 100.0, 300.0])
def test_transmission_matches_koschmieder(V):
    d = np.linspace(0, 2 * V, 50)
    t = P.transmission(d, V)
    np.testing.assert_allclose(t, np.exp(-3 * d / V), rtol=0.01)   # -ln(0.05) = 2.996 ~ 3
    assert P.transmission(V, V) == pytest.approx(0.05)               # definition of visibility
    assert P.extinction_coefficient(V) == pytest.approx(-np.log(0.05) / V)


def test_clear_air_is_identity():
    rng = np.random.default_rng(0)
    img = rng.integers(0, 256, (20, 30, 3), dtype=np.uint8)
    depth = rng.uniform(1, 80, (20, 30))
    assert P.fog(img, depth, np.inf) is img
    np.testing.assert_array_equal(P.transmission(depth, np.inf), 1.0)
    pts = rng.normal(0, 20, (100, 4)).astype(np.float32)
    assert P.lidar_fog(pts, np.inf) is pts


def test_fog_blends_towards_airlight_with_distance():
    img = np.zeros((1, 3, 3), np.uint8)                     # black object
    depth = np.array([[1.0, 50.0, 1000.0]])
    out = P.fog(img, depth, 50.0, airlight=0.8).astype(float)
    assert out[0, 0, 0] < out[0, 1, 0] < out[0, 2, 0]
    # at d = V the linear radiance is A (1 - 0.05)
    lin = P.srgb_to_linear(out[0, 1, 0] / 255)
    assert lin == pytest.approx(0.8 * 0.95, abs=0.01)
    assert P.srgb_to_linear(out[0, 2, 0] / 255) == pytest.approx(0.8, abs=0.01)


def test_srgb_round_trip():
    x = np.linspace(0, 1, 101)
    np.testing.assert_allclose(P.linear_to_srgb(P.srgb_to_linear(x)), x, atol=1e-12)


def test_low_light_keeps_mean_and_adds_noise_that_grows_as_light_falls():
    img = np.full((200, 200, 3), 128, np.uint8)
    a = P.low_light(img, 1 / 16, np.random.default_rng(1)).astype(float)
    b = P.low_light(img, 1 / 256, np.random.default_rng(1)).astype(float)
    assert abs(a.mean() - 128) < 3                 # gain restores the brightness
    assert 0 < a.std() < b.std()                   # but the noise grows as the light falls
    np.testing.assert_array_equal(P.low_light(img, 1 / 64, np.random.default_rng(5)),
                                  P.low_light(img, 1 / 64, np.random.default_rng(5)))   # reproducible


def test_low_light_shot_noise_follows_poisson():
    lin = 0.5
    img = np.full((300, 300, 3), int(round(P.linear_to_srgb(lin) * 255)), np.uint8)
    k, fw = 1 / 64, 4000.0
    out = P.low_light(img, k, np.random.default_rng(2), full_well=fw, read_noise=0.0)
    electrons = P.srgb_to_linear(out / 255.0) * fw * k
    mean_e = P.srgb_to_linear(img[0, 0, 0] / 255.0) * fw * k
    assert electrons.var() == pytest.approx(mean_e, rel=0.15)        # Poisson: variance = mean


def test_dirt_mask_coverage_and_lens_dirt_locality():
    rng = np.random.default_rng(3)
    alpha = P.dirt_mask((120, 200, 3), 0.25, rng)
    assert (alpha > 0.5).mean() >= 0.2 and alpha.max() <= 0.9 + 1e-9
    img = np.full((120, 200, 3), 200, np.uint8)
    out = P.lens_dirt(img, alpha)
    clean = alpha < 1e-3
    np.testing.assert_array_equal(out[clean], img[clean])
    assert out[alpha > 0.8].mean() < 150


def test_lidar_fog_removes_far_returns_first():
    r = np.array([5.0, 20.0, 40.0, 80.0])
    pts = np.column_stack([r, np.zeros(4), np.zeros(4), np.full(4, 0.5)]).astype(np.float32)
    kept = P.lidar_fog(pts, 25.0)[:, 0]
    assert 5.0 in kept and 80.0 not in kept
    assert len(P.lidar_fog(pts, 25.0)) <= len(P.lidar_fog(pts, 100.0))
