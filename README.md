# 🚀 Lagrange Points Simulation

An interactive Python-based simulation of the five Lagrange points using REBOUND, NumPy, SciPy, Streamlit and Manim.

## 🎯 Hackathon Project

## What the project demonstrates

1. Two customizable massive bodies orbit their common center of mass.
2. The five Lagrange points are computed for the current mass ratio and separation.
3. A massless satellite can be placed near any Lagrange point.
4. REBOUND integrates the satellite's real gravitational motion.
5. The display is transformed to the rotating frame, where ideal Lagrange points remain fixed.
6. Small perturbations show the difference between the unstable collinear points (L1–L3) and the conditionally stable triangular points (L4–L5).
7. Changing either planet mass or separation updates the locations and orbital timescale.


This project visualizes the five Lagrange points:

- L1
- L2
- L3
- L4
- L5

Users can modify:

- Planet masses
- Planet separation
- Satellite position
- Simulation duration

## 🛠️ Technologies

Python
REBOUND
NumPy
SciPy
Streamlit
Plotly
Manim


## Core equations

For total mass `M = m1 + m2`, separation `a`, and

`mu = m2 / (m1 + m2)`,

the normalized rotating-frame coordinates place the primary at `(-mu*a, 0)` and secondary at `((1-mu)*a, 0)`.

L4/L5 are:

`x = a*(1/2 - mu)`

`y = ±sqrt(3)*a/2`

L1/L2/L3 are obtained by solving the zero-gradient condition of the effective potential along the x-axis.

The circular angular speed is:

`omega = sqrt(G*(m1+m2)/a^3)`

The classical Routh stability condition for L4/L5 is approximately:

`mu < 0.0385209`

## Project structure

- `app.py` — interactive Streamlit dashboard
- `lagrange.py` — physics and L-point calculations
- `manim_scene.py` — explanatory Manim animation
- `requirements.txt` — Python dependencies

## Important interpretation

Lagrange points are not ordinary "places where gravity is zero". They are equilibrium points **in the rotating frame**, where gravitational acceleration and the rotating-frame terms balance. A real spacecraft generally performs a small orbit around an L-point or uses station-keeping rather than sitting perfectly motionless.
