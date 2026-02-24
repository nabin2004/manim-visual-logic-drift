from datasets import Dataset
import jsonlines
from pathlib import Path
from typing import List, Dict, Any

class MVLDDataset:
    """
    Handles loading and versioning of datasets for training and evaluation.
    """
    def __init__(self, data_path: str = None):
        self.data_path = Path(data_path) if data_path else None

    def create_dummy_dataset(self, num_samples: int = 5) -> Dataset:
        """
        Creates a dummy dataset for testing the pipeline.
        """
        data = []
        for i in range(num_samples):
            data.append({
                "instruction": f"Draw a blue square and a red circle at index {i}.",
                "code": "from mvld.sandbox.base import MVLDScene\nfrom manim import *\nclass Scene(MVLDScene):\n    def construct(self):\n        self.add(Square(color=BLUE).shift(LEFT))\n        self.add(Circle(color=RED).shift(RIGHT))",
                "metadata": {"source": "synthetic"}
            })
        
        return Dataset.from_list(data)


    def save_to_jsonl(self, dataset: List[Dict[str, Any]], output_path: str):
        with jsonlines.open(output_path, mode='w') as writer:
            writer.write_all(dataset)

    def load_from_jsonl(self, input_path: str) -> List[Dict[str, Any]]:
        with jsonlines.open(input_path) as reader:
            return list(reader)
