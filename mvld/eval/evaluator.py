import torch
import clip
from PIL import Image
from pathlib import Path
from typing import List, Union, Dict, Any

class CLIPScorer:
    def __init__(self, model_name: str = "ViT-B/32", device: str = None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        self.model, self.preprocess = clip.load(model_name, device=self.device)

    @torch.no_grad()
    def score(self, image_path: Union[str, Path], prompt: str) -> float:
        """
        Calculates the cosine similarity between an image and a text prompt.
        """
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        text = clip.tokenize([prompt]).to(self.device)

        image_features = self.model.encode_image(image)
        text_features = self.model.encode_text(text)

        # Normalize features
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (100.0 * image_features @ text_features.T).item()
        return similarity

class SpatialEvaluator:
    """
    Evaluates layout and spatial constraints.
    """
    def evaluate(self, scene_graph: List[Dict[str, Any]], expected_constraints: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder for complex spatial logic
        # e.g., "blue square should be to the left of red circle"
        return {
            "spatial_drift_score": 0.0,
            "constraints_met": True,
            "details": "Spatial evaluation logic is currently a placeholder."
        }

class VisualEvaluator:
    def __init__(self, device: str = None):
        self.clip_scorer = CLIPScorer(device=device)
        self.spatial_evaluator = SpatialEvaluator()

    def evaluate_render(self, image_path: str, prompt: str, scene_graph: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        clip_score = self.clip_scorer.score(image_path, prompt)
        
        # Spatial evaluation if scene graph is available
        spatial_results = {}
        if scene_graph:
            spatial_results = self.spatial_evaluator.evaluate(scene_graph, {})
            
        return {
            "clip_similarity": clip_score,
            "spatial": spatial_results,
            "overall_score": clip_score # Simplified for now
        }
