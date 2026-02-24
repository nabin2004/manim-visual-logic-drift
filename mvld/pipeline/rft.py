from pathlib import Path
from typing import List, Dict, Any
import json
from rich.console import Console
from rich.progress import Progress

from mvld.sandbox.executor import ManimSandbox
from mvld.eval.evaluator import VisualEvaluator
from mvld.data.dataset import MVLDDataset
from mvld.pipeline.base import BasePipeline, PipelineRegistry

console = Console()

@PipelineRegistry.register("rft")
class RFTPipeline(BasePipeline):
    def __init__(self, output_dir: str = "results/rft"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sandbox = ManimSandbox(output_dir=str(self.output_dir / "media"))
        self.evaluator = VisualEvaluator()
        self.dataset_handler = MVLDDataset()

    def run_baseline(self, num_samples: int = 5):
        """
        Runs the RFT baseline loop.
        """
        console.print(f"[bold green]Starting RFT Baseline with {num_samples} samples...[/bold green]")
        
        dataset = self.dataset_handler.create_dummy_dataset(num_samples)
        results = []

        with Progress() as progress:
            task = progress.add_task("[cyan]Processing samples...", total=num_samples)
            
            for i, item in enumerate(dataset):
                instruction = item["instruction"]
                code = item["code"]
                
                # 1. Execute
                script_path = self.output_dir / f"sample_{i}.py"
                with open(script_path, "w") as f:
                    f.write(code)
                
                render_res = self.sandbox.run_script(script_path)
                
                # 2. Evaluate
                score_res = {}
                if render_res["success"] and render_res["image_path"]:
                    score_res = self.evaluator.evaluate_render(
                        render_res["image_path"], 
                        instruction,
                        scene_graph=render_res.get("scene_graph")
                    )

                
                # 3. Collect
                entry = {
                    "id": i,
                    "instruction": instruction,
                    "code": code,
                    "render_success": render_res["success"],
                    "image_path": render_res["image_path"],
                    "score": score_res.get("clip_similarity", 0.0),
                    "full_eval": score_res
                }
                results.append(entry)
                progress.update(task, advance=1)

        # Save results
        results_path = self.output_dir / "rft_results.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        
        console.print(f"[bold blue]RFT Baseline Complete![/bold blue] Results saved to {results_path}")
        return results

if __name__ == "__main__":
    pipeline = RFTPipeline()
    pipeline.run_baseline(3)
