# Lagrange Points Explorer — Python Hackathon

A Python-only interactive simulation for the **Lagrange Points (L1–L5)** using:

- **REBOUND** — N-body gravitational integration
- **NumPy** — numerical calculations
- **SciPy** — Lagrange-point root solving
- **Plotly** — interactive rotating-frame visualization
- **Streamlit** — live parameter controls
- **Manim** — polished explanatory animation

## What the project demonstrates

1. Two customizable massive bodies orbit their common center of mass.
2. The five Lagrange points are computed for the current mass ratio and separation.
3. A massless satellite can be placed near any Lagrange point.
4. REBOUND integrates the satellite's real gravitational motion.
5. The display is transformed to the rotating frame, where ideal Lagrange points remain fixed.
6. Small perturbations show the difference between the unstable collinear points (L1–L3) and the conditionally stable triangular points (L4–L5).
7. Changing either planet mass or separation updates the locations and orbital timescale.

## Run the interactive app

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Render the Manim explanation

```bash
manim -pqh manim_scene.py LagrangePointsIntro
```

For a faster preview:

```bash
manim -pql manim_scene.py LagrangePointsIntro
```

## Suggested hackathon demo flow

1. Start with equal-ish masses and separation = 10 units.
2. Select **L4** and use a tiny perturbation.
3. Show the satellite remaining near the triangular point in the rotating frame.
4. Select **L1** with the same perturbation and show the displacement growing.
5. Increase the secondary mass until the L4/L5 stability condition is violated.
6. Change the separation and show that the dimensionless geometry is similar while the orbital period changes.
7. Use the Manim animation as the 60–90 second project introduction.

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
