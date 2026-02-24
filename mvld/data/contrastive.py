import re
import random
from typing import List, Dict, Any, Tuple

class ErrorSeeder:
    """
    Introduces "visual logic bugs" into Manim code to create contrastive pairs.
    """
    def __init__(self):
        # Swap mappings for common visual logic
        self.swaps = {
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
            "UP": "DOWN",
            "DOWN": "UP",
            "BLUE": "RED",
            "RED": "BLUE",
            "GREEN": "YELLOW",
            "YELLOW": "GREEN",
            "Circle": "Square",
            "Square": "Circle",
            "shift": "move_to",
            "move_to": "next_to"
        }

    def generate_negative(self, code: str) -> Tuple[str, str]:
        """
        Takes valid code and returns a (negative_code, error_description) pair.
        """
        negative_code = code
        applied_errors = []
        
        # Try to replace at least one occurrence of a swappable keyword
        for key, val in self.swaps.items():
            if key in negative_code and random.random() > 0.5:
                # Replace only one occurrence to keep it subtle
                negative_code = negative_code.replace(key, val, 1)
                applied_errors.append(f"Swapped {key} with {val}")
                break # Just one error for now
        
        if not applied_errors:
            # Fallback: Just jitter a number
            num_match = re.search(r'([-+]?\d*\.?\d+)', negative_code)
            if num_match:
                val = float(num_match.group(1))
                new_val = val + random.choice([-1.0, 1.0, 2.0])
                negative_code = negative_code.replace(str(val), f"{new_val:.1f}", 1)
                applied_errors.append(f"Jittered coordinate {val} to {new_val}")

        return negative_code, "; ".join(applied_errors)

class ContrastiveGenerator:
    """
    Creates (prompt, positive_code, negative_code) triplets.
    """
    def __init__(self):
        self.seeder = ErrorSeeder()

    def create_triplet(self, prompt: str, code: str) -> Dict[str, str]:
        negative_code, error = self.seeder.generate_negative(code)
        return {
            "prompt": prompt,
            "chosen": code,
            "rejected": negative_code,
            "error_type": error
        }

if __name__ == "__main__":
    cg = ContrastiveGenerator()
    test_code = "obj.shift(LEFT).set_color(BLUE)"
    triplet = cg.create_triplet("Move object left and make it blue", test_code)
    print("Chosen:", triplet["chosen"])
    print("Rejected:", triplet["rejected"])
    print("Reason:", triplet["error_type"])
