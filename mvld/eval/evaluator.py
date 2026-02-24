import torch
import clip
from PIL import Image
from pathlib import Path
from typing import List, Union, Dict, Any
from mvld.eval.base import BaseEvaluator, EvaluatorRegistry

@EvaluatorRegistry.register("clip")
class CLIPScorer(BaseEvaluator):
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

@EvaluatorRegistry.register("spatial")
class SpatialEvaluator(BaseEvaluator):
    """
    Evaluates layout and spatial constraints.
    """
    def evaluate(self, scene_graph: List[Dict[str, Any]], expected_constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates the scene graph against constraints.
        """
        if not scene_graph:
            return {"spatial_drift_score": 1.0, "error": "No scene graph data"}

        # Basic check: Object count
        obj_count = len(scene_graph)
        expected_count = expected_constraints.get("count")
        
        counts_match = True
        if expected_count is not None:
            counts_match = obj_count == expected_count

        # Heuristic: Compare specific types if requested
        type_constraints = expected_constraints.get("types", {})
        type_match = True
        for t, count in type_constraints.items():
            actual = len([m for m in scene_graph if m["type"].lower() == t.lower()])
            if actual != count:
                type_match = False
                break
        
        drift_score = 0.0 if (counts_match and type_match) else 1.0

        return {
            "spatial_drift_score": drift_score,
            "object_count": obj_count,
            "counts_match": counts_match,
            "type_match": type_match,
            "mobjects": [m["type"] for m in scene_graph]
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
            
        # Combine scores (heuristic: penalize CLIP score if spatial constraints fail)
        final_score = clip_score
        if spatial_results.get("spatial_drift_score", 0.0) > 0:
            final_score *= 0.5 # Penalty for spatial drift

        return {
            "clip_similarity": clip_score,
            "spatial": spatial_results,
            "overall_score": final_score
        }

