import subprocess
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import tempfile

class ManimSandbox:
    def __init__(self, output_dir: str = "media"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_script(self, script_path: Path, scene_name: str = None) -> Dict[str, Any]:
        """
        Runs a Manim script and returns the result metadata.
        """
        if not scene_name:
            # Try to infer scene name or use -a for all
            scene_arg = ""
        else:
            scene_arg = scene_name

        # Command to run manim
        # We use -v ERROR to reduce noise
        # We use --format png --write_to_movie False to get the last frame as image
        cmd = [
            "manim", 
            str(script_path), 
            scene_arg,
            "-v", "ERROR",
            "--format", "png",
            "--write_to_movie", "False",
            "--media_dir", str(self.output_dir)
        ]

        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            success = result.returncode == 0
            error_log = result.stderr if not success else ""
            
            # Find the output image
            # Manim usually puts it in media/images/<script_name>/<scene_name>.png
            image_path = self._find_latest_image(script_path.stem)

            return {
                "success": success,
                "error": error_log,
                "image_path": str(image_path) if image_path else None,
                "stdout": result.stdout
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "image_path": None
            }

    def _find_latest_image(self, script_stem: str) -> Optional[Path]:
        image_dir = self.output_dir / "images" / script_stem
        if not image_dir.exists():
            return None
        
        png_files = list(image_dir.glob("*.png"))
        if not png_files:
            return None
        
        # Return the most recently modified png
        return max(png_files, key=os.path.getmtime)

    def extract_scene_graph(self, script_content: str) -> List[Dict[str, Any]]:
        """
        Mocked scene graph extraction. 
        In a real scenario, we might use AST or a modified Manim base class to log mobjects.
        """
        # Placeholder: Basic regex or simply return dummy data for now
        # We will refine this to use a custom Manim Scene that exports JSON
        return [{"type": "Circle", "color": "RED", "pos": [0,0,0]}]

if __name__ == "__main__":
    # Test snippet
    sandbox = ManimSandbox()
    test_code = """
from manim import *
class TestScene(Scene):
    def construct(self):
        circle = Circle(color=RED)
        self.add(circle)
    """
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
        tmp.write(test_code)
        tmp_path = Path(tmp.name)
    
    print(f"Running test on {tmp_path}")
    res = sandbox.run_script(tmp_path, "TestScene")
    print(json.dumps(res, indent=2))
    os.unlink(tmp_path)
