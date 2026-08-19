from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st


from lagrange import SystemParameters,lagrange_points,routh_stable,simulate_orbit,  


st.set_page_config(
    page_title="Lagrange Points Explorer",
    page_icon="🪐",
    layout="wide",
)

st.title("🪐 Lagrange Points Explorer")
st.caption("REBOUND + NumPy + SciPy + Plotly + Streamlit — a Python-only hackathon simulation")

with st.sidebar:
    st.header("System controls")
    m1 = st.number_input("Planet 1 mass", min_value=0.01, value=1.0, step=0.1)
    m2 = st.number_input("Planet 2 mass", min_value=0.0001, value=0.1, step=0.01)
    separation = st.slider("Planet separation", 2.0, 30.0, 10.0, 0.5)

    st.header("Satellite experiment")
    point_name = st.selectbox("Place satellite near", ["L1", "L2", "L3", "L4", "L5"])
    perturbation = st.slider(
        "Perturbation (% of separation)",
        0.0, 2.0, 0.25, 0.05,
        help="A small offset reveals the stability behavior.",
    ) / 100.0
    duration_periods = st.slider("Simulation duration (orbital periods)", 0.25, 8.0, 2.0, 0.25)

    run = st.button("🚀 Run REBOUND simulation", type="primary", use_container_width=True)

p = SystemParameters(m1=m1, m2=m2, separation=separation)
points = lagrange_points(p)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mass ratio μ", f"{p.mu:.5f}")
c2.metric("Angular speed ω", f"{p.omega:.5f}")
c3.metric("Orbital period", f"{p.period:.3f}")
c4.metric("L4/L5 stable?", "YES" if routh_stable(p) else "NO")

st.info(
    "L1–L3 are collinear equilibrium points and are dynamically unstable. "
    "L4/L5 are conditionally stable: the classical Routh criterion requires "
    "μ < 0.0385209."
)

left, right = st.columns([1.7, 1.0])

with left:
    fig = go.Figure()

    # Primary and secondary.
    x1 = -p.mu * separation
    x2 = (1.0 - p.mu) * separation
    fig.add_trace(go.Scatter(
        x=[x1], y=[0], mode="markers+text",
        marker=dict(size=22), text=["Planet 1"], textposition="bottom center",
        name="Planet 1",
    ))
    fig.add_trace(go.Scatter(
        x=[x2], y=[0], mode="markers+text",
        marker=dict(size=15), text=["Planet 2"], textposition="bottom center",
        name="Planet 2",
    ))

    for name, xy in points.items():
        is_selected = name == point_name
        fig.add_trace(go.Scatter(
            x=[xy[0]], y=[xy[1]],
            mode="markers+text",
            marker=dict(size=14 if is_selected else 10, symbol="diamond"),
            text=[name],
            textposition="top center",
            name=name,
        ))

    if run:
        result = simulate_satellite(
            p,
            point_name,
            perturbation=perturbation,
            duration_periods=duration_periods,
        )
        traj = result["trajectory"]
        fig.add_trace(go.Scatter(
            x=traj[:, 0], y=traj[:, 1],
            mode="lines",
            line=dict(width=3),
            name="Satellite trajectory",
        ))
        fig.add_trace(go.Scatter(
            x=[traj[0, 0], traj[-1, 0]],
            y=[traj[0, 1], traj[-1, 1]],
            mode="markers",
            marker=dict(size=8),
            name="Start / end",
        ))

    lim = 1.45 * separation
    fig.update_layout(
        title="Rotating-frame view",
        xaxis_title="x",
        yaxis_title="y",
        xaxis=dict(range=[-lim, lim], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-lim, lim]),
        height=680,
        legend=dict(orientation="h"),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Lagrange point coordinates")
    rows = []
    for name, xy in points.items():
        rows.append({
            "Point": name,
            "x": round(float(xy[0]), 5),
            "y": round(float(xy[1]), 5),
            "Type": "Collinear" if name in ("L1", "L2", "L3") else "Triangular",
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.subheader("Physics")
    st.markdown(
        f"""
**Primary:** `{m1:g}` mass units  
**Secondary:** `{m2:g}` mass units  
**Separation:** `{separation:g}` distance units  
**μ = m₂/(m₁+m₂):** `{p.mu:.6f}`

The dashboard uses the **center-of-mass rotating frame**. The two planets remain
fixed in this frame while the satellite is integrated by REBOUND in the inertial
frame and transformed back for display.
"""
    )

    if run:
        st.subheader("Experiment result")
        st.metric("Maximum distance from selected L-point", f"{result['max_displacement']:.4f}")
        st.metric("Final distance", f"{result['final_displacement']:.4f}")
        if point_name in ("L4", "L5"):
            status = "Classically stable regime" if routh_stable(p) else "Above Routh threshold"
        else:
            status = "Unstable equilibrium"
        st.write(f"**Expected behavior:** {status}")

st.divider()
st.subheader("What to demonstrate to judges")
st.markdown(
    """
- **L1:** satellite drifts away after a tiny perturbation.
- **L2/L3:** same qualitative instability on the outer sides.
- **L4/L5:** satellite can remain bounded around the triangular point when the mass ratio satisfies the Routh condition.
- **Mass control:** changing the secondary mass changes μ and therefore the geometry and L4/L5 stability.
- **Distance control:** changing separation scales the point coordinates and changes the orbital period.
- **Scientific correctness:** the actual satellite trajectory comes from an N-body integrator, not a pre-drawn animation.
"""
)
