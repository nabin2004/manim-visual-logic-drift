import wandb
from typing import Dict, Any, Optional

class WandBLogger:
    """
    Wrapper for Weights & Biases logging in the MVLD project.
    """
    def __init__(self, project_name: str = "manim-visual-drift", experiment_name: Optional[str] = None):
        self.project_name = project_name
        self.experiment_name = experiment_name

    def start_run(self, config: Dict[str, Any]):
        wandb.init(project=self.project_name, name=self.experiment_name, config=config)

    def log_metrics(self, metrics: Dict[str, Any], step: Optional[int] = None):
        wandb.log(metrics, step=step)

    def log_render(self, image_path: str, caption: str):
        wandb.log({
            "render": wandb.Image(image_path, caption=caption)
        })

    def finish(self):
        wandb.finish()

if __name__ == "__main__":
    # logger = WandBLogger()
    # logger.start_run({"learning_rate": 0.001})
    # logger.log_metrics({"clip_score": 0.8})
    print("WandB Logger ready.")
