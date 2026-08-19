from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple
import math

import numpy as np
import rebound
from scipy.optimize import brentq


@dataclass
class SystemParameters:
    m1: float = 1.0
    m2: float = 0.1
    separation: float = 10.0
    G: float = 1.0

    @property
    def total_mass(self) -> float:
        return self.m1 + self.m2

    @property
    def mu(self) -> float:
        return self.m2 / self.total_mass

    @property
    def omega(self) -> float:
        return math.sqrt(self.G * self.total_mass / self.separation**3)

    @property
    def period(self) -> float:
        return 2.0 * math.pi / self.omega


def body_positions(p: SystemParameters) -> Tuple[float, float]:
    """Return rotating-frame x positions of primary and secondary."""
    x1 = -p.mu * p.separation
    x2 = (1.0 - p.mu) * p.separation
    return x1, x2


def _collinear_equation(x: float, *args, p: SystemParameters) -> float:
    """dOmega/dx = 0 for a point on the rotating x-axis."""
    x1, x2 = body_positions(p)
    return (
        p.omega**2 * x
        - p.G * p.m1 * (x - x1) / abs(x - x1) ** 3
        - p.G * p.m2 * (x - x2) / abs(x - x2) ** 3
    )


def _safe_root(f, lo: float, hi: float,args=(), maxiter=300) -> float:
    # Avoid singularities at the two massive bodies.
    eps = max(1e-10, (hi - lo) * 1e-10)
    return brentq(f, lo + eps, hi - eps,args=args, maxiter=maxiter)


def lagrange_points(p: SystemParameters) -> Dict[str, np.ndarray]:
    """Compute L1-L5 in the rotating frame."""
    x1, x2 = body_positions(p)
    a = p.separation

    # Collinear points.
    l1 = _safe_root(_collinear_equation, x1, x2)
    l2 = brentq(_collinear_equation, x2 + 1e-10 * a, x2 + 100.0 * a)
    l3 = brentq(_collinear_equation, x1 - 100.0 * a, x1 - 1e-10 * a)

    # Triangular points.
    xt = a * (0.5 - p.mu)
    yt = math.sqrt(3.0) * a / 2.0

    return {
        "L1": np.array([l1, 0.0]),
        "L2": np.array([l2, 0.0]),
        "L3": np.array([l3, 0.0]),
        "L4": np.array([xt, yt]),
        "L5": np.array([xt, -yt]),
    }


def routh_stable(p: SystemParameters) -> bool:
    """Classical linear stability criterion for L4/L5."""
    return p.mu < 0.0385208965


def make_rebound(p: SystemParameters) -> rebound.Simulation:
    """Create a circular two-body REBOUND system in the inertial frame."""
    sim = rebound.Simulation()
    sim.G = p.G
    sim.add(m=p.m1)
    sim.add(m=p.m2)

    # Move the pair to their center-of-mass frame and make a circular orbit.
    sim.move_to_com()
    sim.integrator = "ias15"

    # After move_to_com, particles are already on a circular binary only if
    # initial orbital elements were supplied, so reset them explicitly.
    r1 = -p.mu * p.separation
    r2 = (1.0 - p.mu) * p.separation
    v1 = p.omega * abs(r1)
    v2 = p.omega * abs(r2)

    primary, secondary = sim.particles[0], sim.particles[1]
    primary.x, primary.y = r1, 0.0
    secondary.x, secondary.y = r2, 0.0
    primary.vx, primary.vy = 0.0, -v1
    secondary.vx, secondary.vy = 0.0, v2
    primary.vz = secondary.vz = 0.0

    return sim


def rotating_to_inertial(xy: np.ndarray, t: float, omega: float) -> Tuple[float, float]:
    """Convert a rotating-frame coordinate to inertial coordinates."""
    c, s = math.cos(omega * t), math.sin(omega * t)
    x, y = xy
    return c * x - s * y, s * x + c * y


def inertial_to_rotating(x: float, y: float, t: float, omega: float) -> Tuple[float, float]:
    """Convert an inertial coordinate to rotating-frame coordinates."""
    c, s = math.cos(omega * t), math.sin(omega * t)
    return c * x + s * y, -s * x + c * y


def simulate_satellite(
    p: SystemParameters,
    point_name: str,
    perturbation: float = 0.02,
    duration_periods: float = 2.0,
    samples: int = 600,
) -> dict:
    """
    Integrate the satellite near an L point using REBOUND.

    perturbation is a fraction of the planet separation.
    """
    points = lagrange_points(p)
    target = points[point_name]
    offset = np.array([perturbation * p.separation, 0.0])

    # A slight tangential perturbation is useful for visualizing stability.
    if point_name in ("L4", "L5"):
        offset = np.array([perturbation * p.separation, 0.35 * perturbation * p.separation])

    initial_rot = target + offset
    x0, y0 = rotating_to_inertial(initial_rot, 0.0, p.omega)
    vx0, vy0 = -p.omega * y0, p.omega * x0

    sim = make_rebound(p)
    sim.add(m=0.0, x=x0, y=y0, vx=vx0, vy=vy0, r=0.0)

    t_end = duration_periods * p.period
    times = np.linspace(0.0, t_end, samples)
    xr, yr = [], []

    for t in times:
        sim.integrate(float(t))
        sat = sim.particles[2]
        x, y = inertial_to_rotating(sat.x, sat.y, t, p.omega)
        xr.append(x)
        yr.append(y)

    trajectory = np.column_stack([xr, yr])
    displacement = np.linalg.norm(trajectory - target, axis=1)

    return {
        "times": times,
        "trajectory": trajectory,
        "target": target,
        "points": points,
        "max_displacement": float(np.max(displacement)),
        "final_displacement": float(displacement[-1]),
        "period": p.period,
        "mu": p.mu,
    }
