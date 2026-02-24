import re
from typing import List, Dict, Any, Optional

class CoordinateAugmenter:
    """
    Utility to augment (instruction, code) pairs with explicit coordinates.
    """
    def __init__(self):
        # Pattern to find .shift(), .move_to(), or [x,y,z] in code
        self.shift_pattern = re.compile(r'\.shift\((.*?)\)')
        self.move_to_pattern = re.compile(r'\.move_to\((.*?)\)')
        self.vector_pattern = re.compile(r'np\.array\(\[(.*?)\]\)|\[\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\]')

    def augment_instruction(self, instruction: str, code: str) -> str:
        """
        Attempts to extract coordinates from code and append to instruction.
        """
        coords = self.extract_coordinates(code)
        if not coords:
            return instruction
        
        coord_strings = [f"[{c[0]:.2f}, {c[1]:.2f}]" for c in coords]
        spatial_note = " with coordinates: " + ", ".join(coord_strings)
        
        return instruction + spatial_note

    def extract_coordinates(self, code: str) -> List[List[float]]:
        """
        Basic extraction of coordinates from Manim code.
        Supports .shift(), .move_to(), and explicit lists [x, y, z].
        """
        coords = []
        
        # 1. Simple coordinate lists [x, y, z]
        vec_matches = self.vector_pattern.findall(code)
        for match in vec_matches:
            # match is a tuple (array_content, x, y, z)
            if match[1]: # Literal [x,y,z]
                coords.append([float(match[1]), float(match[2]), float(match[3])])
            elif match[0]: # np.array([x,y,z])
                # Try to split by comma
                inner = match[0].split(',')
                if len(inner) >= 2:
                    try:
                        coords.append([float(i.strip()) for i in inner[:3]])
                    except:
                        pass

        # 2. Heuristics for named directions (approximation)
        if "LEFT" in code: coords.append([-1.0, 0.0, 0.0])
        if "RIGHT" in code: coords.append([1.0, 0.0, 0.0])
        if "UP" in code: coords.append([0.0, 1.0, 0.0])
        if "DOWN" in code: coords.append([0.0, -1.0, 0.0])
        if "ORIGIN" in code: coords.append([0.0, 0.0, 0.0])

        # Remove duplicates while preserving order
        unique_coords = []
        for c in coords:
            if c not in unique_coords:
                unique_coords.append(c)
                
        return unique_coords[:5] # Limit to 5 for instruction brevity

if __name__ == "__main__":
    augmenter = CoordinateAugmenter()
    test_code = "circle.shift(LEFT * 2 + UP).move_to([0.5, -0.2, 0])"
    test_inst = "Draw a circle."
    print(augmenter.augment_instruction(test_inst, test_code))
