from manim import *
import numpy as np

class Ket11(Scene):
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
            atom2[2].animate.move_to([h_spacing/2, v_