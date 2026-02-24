import json
from pathlib import Path
from typing import Dict, Any
import matplotlib.pyplot as plt

class ReportGenerator:
    """
    Generates summary reports and plots for research presentations.
    """
    def generate_summary(self, results_path: str = "results/rft/rft_results.json", output_dir: str = "results/reports"):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        
        with open(results_path, "r") as f:
            results = json.load(f)

        scores = [r["score"] for r in results if r["render_success"]]
        
        # Plot distribution
        plt.figure(figsize=(10, 6))
        plt.hist(scores, bins=20, color='skyblue', edgecolor='black')
        plt.title("Distribution of Visual Alignment (CLIP) Scores")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.savefig(out / "score_distribution.png")
        
        # Summary text
        summary = {
            "total_samples": len(results),
            "render_success_rate": len(scores) / len(results) if results else 0,
            "mean_clip_score": sum(scores) / len(scores) if scores else 0
        }
        
        with open(out / "summary_metrics.json", "w") as f:
            json.dump(summary, f, indent=2)
            
        print(f"Report generated in {output_dir}")

if __name__ == "__main__":
    gen = ReportGenerator()
    # gen.generate_summary()
    print("Report Generator ready.")
