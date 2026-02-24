import json
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console

console = Console()

class NegativeMiner:
    """
    Identifies "hard negatives": samples where code runs but visual output is wrong.
    """
    def __init__(self, results_path: str = "results/rft/rft_results.json"):
        self.results_path = Path(results_path)

    def mine_hard_negatives(self, max_score: float = 0.5, output_path: str = "results/hard_negatives.json") -> List[Dict[str, Any]]:
        """
        Filters RFT results for successful renders with low CLIP similarity.
        """
        if not self.results_path.exists():
            console.print(f"[bold red]Results not found at {self.results_path}[/bold red]")
            return []

        with open(self.results_path, "r") as f:
            results = json.load(f)

        hard_negatives = [
            r for r in results 
            if r["render_success"] and r["score"] <= max_score
        ]

        console.print(f"Mined {len(hard_negatives)} hard negatives (Score <= {max_score}) out of {len(results)} total samples.")
        
        # Save results
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            json.dump(hard_negatives, f, indent=2)
            
        console.print(f"[bold blue]Hard negatives saved to {output_path}[/bold blue]")
        return hard_negatives

if __name__ == "__main__":
    miner = NegativeMiner()
    # miner.mine_hard_negatives(max_score=0.4)
    print("Negative Miner ready.")
