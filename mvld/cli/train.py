import typer

app = typer.Typer()

@app.command()
def rft(
    num_samples: int = typer.Option(5, "--num-samples", "-n", help="Number of samples to process"),
    output_dir: str = typer.Option("results/rft", "--output-dir", "-o", help="Output directory"),
):
    """
    Run Rejection Fine-Tuning pipeline.
    """
    from mvld.pipeline.rft import RFTPipeline
    
    pipeline = RFTPipeline(output_dir=output_dir)
    pipeline.run_baseline(num_samples=num_samples)

