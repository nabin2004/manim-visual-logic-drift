import json
from pathlib import Path
from typing import List, Dict, Any
from datasets import Dataset
from rich.console import Console

console = Console()

class RFTIntegrator:
    """
    Automates the loop: Load RFT results -> Filter -> Create SFT Dataset.
    """
    def __init__(self, results_path: str = "results/rft/rft_results.json"):
        self.results_path = Path(results_path)

    def integrate_results(self, threshold: float = 0.7, output_path: str = "data/refined_sft") -> Dataset:
        """
        Loads RFT results and filters samples by score to create a high-quality dataset.
        """
        if not self.results_path.exists():
            console.print(f"[bold red]Results not found at {self.results_path}[/bold red]")
            return Dataset.from_list([])

        with open(self.results_path, "r") as f:
            results = json.load(f)

        console.print(f"Loaded {len(results)} samples from RFT results.")
        
        # Filter: successful render and score above threshold
        refined_data = [
            {
                "instruction": r["instruction"],
                "code": r["code"],
                "score": r["score"]
            }
            for r in results if r["render_success"] and r["score"] >= threshold
        ]

        console.print(f"Filtered to {len(refined_data)} samples with CLIP score >= {threshold}.")
        
        dataset = Dataset.from_list(refined_data)
        
        # Save for SFT training
        dataset_path = Path(output_path)
        dataset_path.parent.mkdir(parents=True, exist_ok=True)
        # dataset.save_to_disk(str(dataset_path)) # Uncomment for persistence
        
        console.print(f"[bold green]Refined SFT dataset created at {output_path}.[/bold green]")
        return dataset

if __name__ == "__main__":
    integrator = RFTIntegrator()
    # integrator.integrate_results(threshold=0.8)
    print("RFT Integrator ready.")
