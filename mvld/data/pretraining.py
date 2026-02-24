from pathlib import Path
from typing import List, Dict, Any
from datasets import Dataset
from mvld.data.loaders import TikZLoader, SVGLoader
import json

class LayoutPretrainingScript:
    """
    Converts a directory of TikZ/SVG files into a Hugging Face Dataset 
    for layout pretraining.
    """
    def __init__(self):
        self.tikz_loader = TikZLoader()
        self.svg_loader = SVGLoader()

    def process_directory(self, input_dir: str, file_type: str = "tikz") -> Dataset:
        path = Path(input_dir)
        samples = []
        
        # Determine extension based on type
        ext = "*.tikz" if file_type == "tikz" else "*.svg"
        files = list(path.glob(ext))
        
        print(f"Processing {len(files)} {file_type} files...")
        
        for i, file in enumerate(files):
            try:
                content = file.read_text()
                if file_type == "tikz":
                    graph = self.tikz_loader.parse_string(content)
                else:
                    graph = self.svg_loader.parse_string(content)
                
                # Instruction: Describe the layout
                # In pretraining, we often use the code as the target.
                instruction = f"Reconstruct the layout defined in this {file_type} snippet."
                
                samples.append({
                    "instruction": instruction,
                    "code": content,
                    "scene_graph": json.dumps(graph),
                    "metadata": {"source": file.name, "type": file_type}
                })
            except Exception as e:
                print(f"Error processing {file.name}: {e}")
                
        return Dataset.from_list(samples)

if __name__ == "__main__":
    # Example usage:
    # script = LayoutPretrainingScript()
    # dataset = script.process_directory("data/pretraining/tikz", "tikz")
    # dataset.save_to_disk("data/pretraining_dataset")
    print("Bulk loader ready. Run with actual data directories to generate pretraining sets.")
