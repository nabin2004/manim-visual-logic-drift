from manim import *

class SimpleScene(Scene):
    def construct(self):
        # A simple blue square and red circle
        square = Square(color=BLUE).shift(LEFT * 2)
        circle = Circle(color=RED).shift(RIGHT * 2)
        
        self.add(square, circle)
        self.wait(1)
