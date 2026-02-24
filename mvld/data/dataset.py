from datasets import Dataset
import jsonlines
from pathlib import Path
from typing import List, Dict, Any
import random


class MVLDDataset:
    """
    Handles loading and versioning of datasets for training and evaluation.
    """
    def __init__(self, data_path: str = None):
        self.data_path = Path(data_path) if data_path else None

    def create_dummy_dataset(self, num_samples: int = 5, augment: bool = True) -> Dataset:
        """
        Creates a dummy dataset for testing the pipeline.
        """
        from mvld.data.augmenter import CoordinateAugmenter
        augmenter = CoordinateAugmenter()
        
        data = []
        for i in range(num_samples):
            instruction = f"Draw a blue square and a red circle at index {i}."
            code = "from mvld.sandbox.base import MVLDScene\nfrom manim import *\nclass Scene(MVLDScene):\n    def construct(self):\n        self.add(Square(color=BLUE).shift(LEFT))\n        self.add(Circle(color=RED).shift(RIGHT))"
            
            if augment:
                instruction = augmenter.augment_instruction(instruction, code)
                
            data.append({
                "instruction": instruction,
                "code": code,
                "metadata": {"source": "synthetic", "augmented": augment}
            })
        
        return Dataset.from_list(data)



    def generate_bulk_synthetic(self, num_samples: int = 100) -> Dataset:
        """
        Generates a large number of synthetic samples using the generator.
        """
        from mvld.data.generator import SyntheticGenerator
        from mvld.data.augmenter import CoordinateAugmenter
        
        gen = SyntheticGenerator()
        augmenter = CoordinateAugmenter()
        data = []
        
        for i in range(num_samples):
            # Mix random and relational scenes
            if random.random() > 0.3:
                sample = gen.generate_random_scene(num_objects=random.randint(1, 4))
            else:
                sample = gen.generate_relational_scene()
            
            # Augment with coordinates
            sample["instruction"] = augmenter.augment_instruction(sample["instruction"], sample["code"])
            
            data.append({
                "instruction": sample["instruction"],
                "code": sample["code"],
                "metadata": {"id": i, "source": "synthetic_bulk"}
            })
            
        return Dataset.from_list(data)

    def save_to_jsonl(self, dataset: List[Dict[str, Any]], output_path: str):

        with jsonlines.open(output_path, mode='w') as writer:
            writer.write_all(dataset)

    def load_from_jsonl(self, input_path: str) -> List[Dict[str, Any]]:
        with jsonlines.open(input_path) as reader:
            return list(reader)
