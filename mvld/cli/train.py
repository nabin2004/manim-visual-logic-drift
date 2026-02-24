import typer
from mvld.pipeline.base import PipelineRegistry

app = typer.Typer()

@app.command("algorithm")
def run_pipeline(
    name: str = typer.Argument(..., help="Algorithm name from registry"),
    num_samples: int = typer.Option(10, "--num-samples", "-n", help="Number of samples to process"),
    rft_threshold: float = typer.Option(0.7, "--rft-threshold", "-t", help="Threshold for RFT algorithm"),
):
    """Run a specific training algorithm from the registry."""
    pipeline = PipelineRegistry.get(name)
    pipeline.run(num_samples=num_samples, threshold=rft_threshold)
```
