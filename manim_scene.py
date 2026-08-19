from manim import *
import numpy as np


class LagrangePointsIntro(Scene):
    def construct(self):
        title = Text("Lagrange Points", font_size=48)
        subtitle = Text("Gravity + orbital motion → rotating-frame equilibria", font_size=26)
        self.play(Write(title))
        self.play(FadeIn(subtitle.next_to(title, DOWN)))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=10,
            y_length=6.5,
            tips=False,
        )
        self.play(Create(axes))

        primary = Dot(axes.c2p(-2, 0), radius=0.18)
        secondary = Dot(axes.c2p(2, 0), radius=0.13)
        p1 = Text("Planet 1", font_size=22).next_to(primary, DOWN)
        p2 = Text("Planet 2", font_size=22).next_to(secondary, DOWN)

        self.play(FadeIn(primary), FadeIn(secondary), Write(p1), Write(p2))

        # A clean pedagogical normalized diagram.
        pts = {
            "L1": (-0.25, 0),
            "L2": (3.05, 0),
            "L3": (-3.05, 0),
            "L4": (0, 2.25),
            "L5": (0, -2.25),
        }

        labels = VGroup()
        dots = VGroup()
        for name, (x, y) in pts.items():
            d = Dot(axes.c2p(x, y), radius=0.09)
            lab = Text(name, font_size=24).next_to(d, UP if y >= 0 else DOWN)
            dots.add(d)
            labels.add(lab)

        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.12))
        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.12))
        self.wait(1)

        note = Text(
            "L1–L3: unstable   |   L4/L5: conditionally stable",
            font_size=28,
        ).to_edge(DOWN)
        self.play(Write(note))
        self.wait(2)

        eq = MathTex(
            r"\omega=\sqrt{\frac{G(m_1+m_2)}{a^3}}",
            font_size=36,
        ).to_edge(UP)
        self.play(Write(eq))
        self.wait(2)

        final = Text(
            "Interactive demo: REBOUND + NumPy + SciPy + Plotly",
            font_size=26,
        ).to_edge(DOWN)
        self.play(Transform(note, final))
        self.wait(2)
