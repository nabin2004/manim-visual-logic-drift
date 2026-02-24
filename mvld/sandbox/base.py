from manim import *
import json
from pathlib import Path

class MVLDScene(Scene):
    """
    Custom Scene class that automatically extracts the scene graph 
    metadata after rendering.
    """
    def tear_down(self):
        super().tear_down()
        self.extract_scene_graph()

    def extract_scene_graph(self):
        """
        Introspects the current mobjects in the scene and saves 
        their metadata to a JSON file.
        """
        scene_graph = []
        for mobject in self.mobjects:
            # We skip mobjects that are likely internal or background
            if hasattr(mobject, "is_background") and mobject.is_background:
                continue
            
            # Extract basic data
            data = {
                "type": mobject.__class__.__name__,
                "position": mobject.get_center().tolist(),
                "color": self._get_color_str(mobject),
                "width": mobject.width,
                "height": mobject.height,
                "z_index": mobject.z_index
            }
            
            # Handle specialized attributes
            if isinstance(mobject, Circle):
                data["radius"] = mobject.radius
            
            scene_graph.append(data)

        # Save to file
        # Manim's media_dir can be accessed via config
        output_path = Path(config.media_dir) / "scene_graph.json"
        
        # Ensure directory exists (might not if no media was saved)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(scene_graph, f, indent=2)
        
        # print(f"Scene graph saved to {output_path}")

    def _get_color_str(self, mobject) -> str:
        if hasattr(mobject, "color"):
            try:
                # Return hex or string representation
                return str(mobject.color)
            except:
                return "unknown"
        return "none"
