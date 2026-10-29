"""Physically grounded image and point-cloud perturbations for SOTIF triggering conditions.

Each function changes one condition of the scene or the sensor, with parameters in
physical units, so that the performance of a perception component can be measured
as a function of that parameter (ISO 21448 performance insufficiencies). The models
are deliberately simple and transparent; their limitations are stated per function.

Conventions
-----------
* Images are ``H x W x 3`` ``uint8`` sRGB arrays (as loaded by :mod:`avsafety.data`).
  Physical light models are applied in linear RGB (IEC 61966-2-1 sRGB transfer curve).
* Distances are in metres, along the line of sight from the camera.
* Randomness only through a caller-supplied ``numpy.random.Generator``, so results are
  reproducible (the benchmark seeds one generator per frame).

References
----------
Koschmieder, H. (1924). Theorie der horizontalen Sichtweite. *Beiträge zur Physik der
    freien Atmosphäre* 12, 33-53 (original not consulted; cited after Sakaridis et al. 2018).
Sakaridis, C., Dai, D., Van Gool, L. (2018). Semantic Foggy Scene Understanding with
    Synthetic Data. *International Journal of Computer Vision* 126, 973-992.
    https://doi.org/10.1007/s11263-018-1072-8
Foi, A., Trimeche, M., Katkovnik, V., Egiazarian, K. (2008). Practical Poissonian-Gaussian
    Noise Modeling and Fitting for Single-Image Raw-Data. *IEEE Transactions on Image
    Processing* 17(10), 1737-1754. https://doi.org/10.1109/TIP.2008.2001399
Hahner, M., Sakaridis, C., Dai, D., Van Gool, L. (2021). Fog Simulation on Real LiDAR Point
    Clouds for 3D Object Detection in Adverse Weather. *ICCV 2021*, 15263-15272.
    https://doi.org/10.1109/ICCV48922.2021.01500
"""
from __future__ import annotations

import numpy as np

#: Contrast threshold that defines meteorological visibility (5 %, Koschmieder).
CONTRAST_THRESHOLD = 0.05

#: Default atmospheric light (linear RGB, uniform grey) used for synthetic fog.
AIRLIGHT = 0.8

#: Received-power threshold of the LiDAR link-budget model: a 10 %-reflective target
#: is just detected at 50 m (Velodyne HDL-64E specification of the KITTI car).
LIDAR_P_MIN = 0.10 / 50.0 ** 2


# --------------------------------------------------------------------------- colour
def srgb_to_linear(x):
    """sRGB-encoded values in [0, 1] to linear light (IEC 61966-2-1)."""
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(x):
    """Linear light to sRGB encoding; values are clipped to [0, 1] first."""
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * x ** (1 / 2.4) - 0.055)


# --------------------------------------------------------------------------- fog
def extinction_coefficient(visibility_m: float) -> float:
    """Extinction coefficient beta (1/m) for a meteorological visibility V (m).

    V is the distance at which the contrast of a black object against the horizon sky
    falls to 5 %: beta = -ln(0.05) / V, approximately 3 / V. Clear air (V = inf) gives 0.
    """
    if visibility_m <= 0:
        raise ValueError("visibility must be positive")
    return -np.log(CONTRAST_THRESHOLD) / visibility_m


def transmission(distance_m, visibility_m: float):
    """Koschmieder transmission t = exp(-beta d) for distance(s) d (m) at visibility V (m).

    Equals 1 for clear air (V = inf) and 0.05 at d = V.
    """
    if not np.isfinite(visibility_m):
        return np.ones_like(np.asarray(distance_m, dtype=float))
    return np.exp(np.log(CONTRAST_THRESHOLD) / visibility_m * np.asarray(distance_m, dtype=float))


def dense_range(frame, cell: int = 4) -> np.ndarray:
    """Per-pixel line-of-sight distance (m) from a frame's projected LiDAR scan.

    ``frame`` is an :class:`avsafety.data.KittiFrame` with image, points and calibration.
    The scan is projected into the image; the nearest return per ``cell x cell`` pixel
    block is kept, empty blocks take the nearest valid block, a 5 x 5 median filter
    removes speckle, and the grid is resampled to full resolution.

    Limitations: pixels above the highest LiDAR beam (sky, upper façades) take the depth
    of the highest return in their column (a vertical-surface assumption); thin
    structures and object edges inherit the depth of their neighbours; the camera and
    LiDAR are not perfectly synchronised in KITTI. Road users within ~40 m are well
    covered by the 64-beam scan, which is what matters for the benchmark.
    """
    from scipy import ndimage

    H, W = frame.image.shape[:2]
    rect = frame.velo_to_rect(frame.points)
    rect = rect[rect[:, 2] > 1.0]                                  # in front of the camera
    uv = frame.rect_to_image(rect)
    dist = np.linalg.norm(rect, axis=1)                            # distance along the line of sight
    ok = (uv[:, 0] >= 0) & (uv[:, 0] < W) & (uv[:, 1] >= 0) & (uv[:, 1] < H)
    gh, gw = -(-H // cell), -(-W // cell)
    grid = np.full((gh, gw), np.inf)
    np.minimum.at(grid, ((uv[ok, 1] // cell).astype(int), (uv[ok, 0] // cell).astype(int)), dist[ok])
    for c in range(gw):                                            # above the top beam: copy upwards
        rows = np.flatnonzero(np.isfinite(grid[:, c]))
        if len(rows):
            grid[:rows[0], c] = grid[rows[0], c]
    idx = ndimage.distance_transform_edt(~np.isfinite(grid), return_distances=False, return_indices=True)
    grid = ndimage.median_filter(grid[tuple(idx)], size=5)
    return ndimage.zoom(grid, (H / gh, W / gw), order=1)[:H, :W]


def fog(img: np.ndarray, distance_m: np.ndarray, visibility_m: float, airlight: float = AIRLIGHT) -> np.ndarray:
    """Homogeneous fog by Koschmieder's law, I = J t + A (1 - t), t = exp(-beta d).

    Parameters
    ----------
    img : H x W x 3 uint8 sRGB image J (clear air).
    distance_m : H x W per-pixel distance d in metres (e.g. :func:`dense_range`).
    visibility_m : meteorological visibility V in metres; ``inf`` returns ``img`` unchanged.
        Meteorology calls V < 1 km fog; the German StVO § 3 (1) caps speed at 50 km/h
        below 50 m visibility.
    airlight : atmospheric light A in linear RGB (uniform grey).

    Limitations: homogeneous fog only (no patches or height dependence); no forward
    scattering blur or glow around light sources; no reaction of the camera's exposure
    control; A is uniform, whereas real airlight varies with sun position. Sakaridis
    et al. (2018) use the same optical model to create Foggy Cityscapes.
    """
    if not np.isfinite(visibility_m):
        return img
    t = np.exp(np.log(CONTRAST_THRESHOLD) / visibility_m * distance_m)[..., None]
    out = srgb_to_linear(img / 255.0) * t + airlight * (1 - t)
    return (linear_to_srgb(out) * 255 + 0.5).astype(np.uint8)


# --------------------------------------------------------------------------- low light
def low_light(img: np.ndarray, light_factor: float, rng: np.random.Generator,
              full_well: float = 4000.0, read_noise: float = 4.0) -> np.ndarray:
    """Less scene light at equal exposure time, brightness restored by gain.

    The linear signal of each pixel is scaled to ``light_factor * full_well`` electrons
    at full scale; photon shot noise (Poisson) and read noise (Gaussian, ``read_noise``
    electrons rms) are added, and a gain of ``1 / light_factor`` restores the mean
    brightness: the image looks similar but is noisier (Poisson-Gaussian model,
    Foi et al. 2008).

    Parameters
    ----------
    light_factor : k, scene light relative to the original exposure (e.g. 1/64).
    full_well : full-well capacity in electrons (illustrative: 4000 e-).
    read_noise : read noise in electrons rms (illustrative: 4 e-).

    Limitations: k is a relative exposure, not calibrated to lux; no dark current, fixed
    pattern noise, motion blur from longer exposure, demosaicing, tone mapping, colour
    shift of street lighting or headlight beam pattern. The original KITTI image is
    treated as noise-free, which slightly underestimates the noise. At very low light
    (k <= 1/256) clipping of negative values biases dark pixels upwards.
    """
    electrons = rng.poisson(srgb_to_linear(img / 255.0) * full_well * light_factor) + rng.normal(0, read_noise, img.shape)
    return (linear_to_srgb(electrons / (full_well * light_factor)) * 255 + 0.5).astype(np.uint8)


# --------------------------------------------------------------------------- lens dirt
def dirt_mask(shape, coverage: float, rng: np.random.Generator) -> np.ndarray:
    """Opacity map (0 ... 0.9) of out-of-focus dirt blobs covering ``coverage`` of the image.

    Discs of radius 25-70 px are placed uniformly at random until the fraction of pixels
    with opacity > 0.5 reaches ``coverage``; a Gaussian blur (sigma 12 px) gives the soft
    edges of dirt that lies far out of the focal plane.
    """
    from scipy import ndimage

    H, W = shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    mask = np.zeros((H, W))
    while (mask > 0.5).mean() < coverage:
        cy, cx, r = rng.uniform(0, H), rng.uniform(0, W), rng.uniform(25, 70)
        mask = np.maximum(mask, ((yy - cy) ** 2 + (xx - cx) ** 2 < r ** 2).astype(float))
    return 0.9 * ndimage.gaussian_filter(mask, 12)


def lens_dirt(img: np.ndarray, alpha: np.ndarray, colour=(0.28, 0.22, 0.16)) -> np.ndarray:
    """Blend semi-opaque, defocused dirt of opacity ``alpha`` (H x W) and RGB ``colour`` into ``img``.

    Under the dirt the scene is half blurred and half replaced by the dirt colour.
    Limitations: a visual model of mud, not of water droplets (refraction) or ice; it is
    not derived from optics of a particular lens.
    """
    from scipy import ndimage

    J = img / 255.0
    blurred = ndimage.gaussian_filter(J, (6, 6, 0))
    out = (1 - alpha[..., None]) * J + alpha[..., None] * (0.5 * blurred + 0.5 * np.array(colour))
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)


# --------------------------------------------------------------------------- LiDAR in fog
def lidar_fog(points: np.ndarray, visibility_m: float, p_min: float = LIDAR_P_MIN) -> np.ndarray:
    """Remove LiDAR returns whose two-way attenuated power falls below the detection threshold.

    Link budget: rho exp(-2 beta R) / R^2 >= p_min, with the stored intensity as
    reflectivity rho (raised where needed so that every recorded return passes in clear
    air). ``points`` is N x 4 (x, y, z, intensity) in the sensor frame, ranges in metres.

    Limitations: no backscatter clutter from droplets, no receiver saturation or
    multi-echo behaviour, extinction at 905 nm taken equal to the visible one; Hahner et
    al. (2021) model these effects.
    """
    if not np.isfinite(visibility_m):
        return points
    R = np.linalg.norm(points[:, :3], axis=1).clip(0.5)
    rho = np.maximum(points[:, 3], p_min * R ** 2)
    beta = -np.log(CONTRAST_THRESHOLD) / visibility_m
    return points[rho * np.exp(-2 * beta * R) / R ** 2 >= p_min]
