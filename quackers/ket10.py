from manim import *
import numpy as np

class Ket10(Scene):
    def construct(self):
        # --- 1. Configuration ---
        h_spacing = 3.5  
        v_gap = 1.2      
        v_double = 2.4   
        line_length = 1.5

        def create_atom_column(x_pos, index):
            l0 = Line(LEFT, RIGHT).set_length(line_length).move_to([x_pos, -v_gap, 0])
            l1 = Line(LEFT, RIGHT).set_length(line_length).move_to([x_pos, 0, 0])
            lr = Line(LEFT, RIGHT).set_length(line_length).move_to([x_pos, v_gap, 0])
            
            t0 = MathTex(f"|0\\rangle_{index}").next_to(l0, LEFT, buff=0.2)
            t1 = MathTex(f"|1\\rangle_{index}").next_to(l1, LEFT, buff=0.2)
            tr = MathTex(f"|r\\rangle_{index}").next_to(lr, LEFT, buff=0.2)
            
            footer = Text(f"Atom {index}", font_size=30).next_to(l0, DOWN, buff=0.5)
            return VGroup(l0, l1, lr, t0, t1, tr, footer)

        # --- 2. Sequential Loading of Atoms ---
        atom1 = create_atom_column(-h_spacing/2, 1)
        atom2 = create_atom_column(h_spacing/2, 2)

        self.play(FadeIn(atom1))
        self.wait(1)
        self.play(FadeIn(atom2))
        self.wait(1)

        # --- 3. Loading Blue Labels ---
        label_r = Text("Rydberg State", color=BLUE, font_size=24).next_to(atom1[5], LEFT, buff=0.8)
        label_1 = Text("Ket 1", color=BLUE, font_size=24).next_to(atom1[4], LEFT, buff=0.8)
        label_0 = Text("Ket 0", color=BLUE, font_size=24).next_to(atom1[3], LEFT, buff=0.8)
        
        self.play(Write(label_r), Write(label_1), Write(label_0), run_time=2)
        self.wait(2) 
        self.play(FadeOut(label_r), FadeOut(label_1), FadeOut(label_0))

        # --- 4. Shift Rydberg Line Up ---
        self.play(
            atom1[2].animate.move_to([-h_spacing/2, v_double, 0]),
            atom1[5].animate.next_to([-h_spacing/2 + line_length/2, v_double, 0], LEFT, buff=0.2 + line_length),
            atom2[2].animate.move_to([h_spacing/2, v_double, 0]),
            atom2[5].animate.next_to([h_spacing/2 + line_length/2, v_double, 0], LEFT, buff=0.2 + line_length),
            run_time=1.5
        )

        # --- 5. Loading Dots ---
        dot_right = Dot(color=RED).scale(1.2).move_to(atom2[0].get_center())
        self.play(FadeIn(dot_right))
        self.wait(1)

        dot_left_core = Dot(color=GREEN).scale(1.5)
        glow = Dot(color=GREEN, fill_opacity=0.3).scale(2.5)
        dot_left = VGroup(glow, dot_left_core)
        dot_left.move_to(atom1[1].get_center())
        self.play(FadeIn(dot_left))
        self.wait(1)

        # --- 5.5 Laser Beam Animation ---
        f_width = 14 
        laser = Rectangle(width=0.01, height=v_double, color=RED, fill_opacity=0.2, stroke_width=0)
        laser.move_to([f_width/2, v_double/2, 0])
        self.play(laser.animate.stretch_to_fit_width(f_width).move_to([0, v_double/2, 0]), run_time=2, rate_func=linear)

        # --- 6. Arrow and Continuous Oscillation ---
        arrow = Arrow(start=LEFT, end=RIGHT, color=WHITE, buff=0).scale(0.2)
        arrow.move_to(dot_left.get_center() + RIGHT * 0.5)
        self.play(FadeIn(arrow))

        time_tracker = ValueTracker(0)
        freq = 1.0        # Oscillation frequency
        arrow_freq = freq / 10  # 10x slower than oscillation

        # Updater for dot movement
        dot_left.add_updater(lambda d, dt: d.move_to(
            interpolate(
                atom1[1].get_center(), 
                atom1[2].get_center(), 
                np.abs(np.sin(PI * freq * time_tracker.get_value()))
            )
        ))

        # Updater for arrow (Rotating 10x slower)
        def update_arrow(a, dt):
            t = time_tracker.get_value()
            center = dot_left.get_center()
            angle = 2 * PI * arrow_freq * t
            offset = np.array([np.cos(angle), np.sin(angle), 0]) * 0.6
            a.move_to(center + offset)
            a.set_angle(angle + PI/2)

        arrow.add_updater(update_arrow)

        self.play(time_tracker.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(1)