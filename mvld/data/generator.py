import random
from typing import List, Dict, Any, Tuple
import json

class SyntheticGenerator:
    """
    Programmatically generates Manim scene code and instructions for training.
    """
    def __init__(self):
        self.shapes = ["Circle", "Square", "Triangle", "Rectangle", "Star", "Pentagon"]
        self.colors = ["RED", "BLUE", "GREEN", "YELLOW", "ORANGE", "PURPLE", "PINK", "WHITE"]
        self.directions = ["LEFT", "RIGHT", "UP", "DOWN", "ORIGIN"]
        self.grid_extents = 3.0 # Manim default grid is roughly -7 to 7, but let's stay safer

    def generate_random_scene(self, num_objects: int = 3) -> Dict[str, str]:
        """
        Generates a scene with N random objects at random positions.
        """
        objs = []
        instruction_parts = []
        
        for i in range(num_objects):
            shape = random.choice(self.shapes)
            color = random.choice(self.colors)
            # Random position [x, y, 0]
            pos = [
                round(random.uniform(-self.grid_extents, self.grid_extents), 2),
                round(random.uniform(-self.grid_extents, self.grid_extents), 2),
                0.0
            ]
            
            objs.append({
                "type": shape,
                "color": color,
                "pos": pos
            })
            instruction_parts.append(f"a {color.lower()} {shape.lower()} at {pos[:2]}")

        instruction = "Draw " + ", ".join(instruction_parts[:-1]) + " and " + instruction_parts[-1] + "."
        code = self._assemble_code(objs)
        
        return {
            "instruction": instruction,
            "code": code
        }

    def generate_relational_scene(self) -> Dict[str, str]:
        """
        Generates a scene with two objects and a relational instruction.
        """
        shape_a = random.choice(self.shapes)
        shape_b = random.choice(self.shapes)
        color_a = random.choice(self.colors)
        color_b = random.choice(self.colors)
        
        rel = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])
        
        objs = [
            {"type": shape_a, "color": color_a, "pos": [0,0,0], "label": "obj_a"},
            {"type": shape_b, "color": color_b, "pos": [0,0,0], "label": "obj_b", "rel": rel, "target": "obj_a"}
        ]
        
        instruction = f"Draw a {color_a.lower()} {shape_a.lower()} and place a {color_b.lower()} {shape_b.lower()} to its {rel.lower()}."
        code = self._assemble_code(objs)
        
        return {
            "instruction": instruction,
            "code": code
        }

    def _assemble_code(self, objects: List[Dict[str, Any]]) -> str:
        lines = [
            "from mvld.sandbox.base import MVLDScene",
            "from manim import *",
            "class Scene(MVLDScene):",
            "    def construct(self):"
        ]
        
        obj_refs = {}
        for i, obj in enumerate(objects):
            ref = obj.get("label", f"obj_{i}")
            obj_refs[ref] = ref
            
            line = f"        {ref} = {obj['type']}(color={obj['color']})"
            
            if "rel" in obj:
                target = obj["target"]
                line += f".next_to({target}, {obj['rel']})"
            else:
                line += f".shift([{obj['pos'][0]}, {obj['pos'][1]}, 0])"
                
            lines.append(line)
            lines.append(f"        self.add({ref})")
            
        return "\n".join(lines)

if __name__ == "__main__":
    gen = SyntheticGenerator()
    print("--- Random Scene ---")
    print(gen.generate_random_scene(2)["instruction"])
    print(gen.generate_random_scene(2)["code"])
    
    print("\n--- Relational Scene ---")
    print(gen.generate_relational_scene()["instruction"])
    print(gen.generate_relational_scene()["code"])
