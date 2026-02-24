import typer
from rich.console import Console
from pathlib import Path

app = typer.Typer()
console = Console()

@app.command()
def file(
    script: Path = typer.Option(..., "--script", "-s", help="Path to Manim script"),
    scene: str = typer.Option(None, "--scene", "-c", help="Scene class name"),
    output_dir: Path = typer.Option("media", "--output-dir", "-o", help="Output directory"),
):
    """
    Render a Manim script and capture metadata.
    """
    from mvld.sandbox.executor import ManimSandbox
    import json
    
    console.print(f"[bold green]Rendering {script}...[/bold green]")
    sandbox = ManimSandbox(output_dir=str(output_dir))
    result = sandbox.run_script(script, scene_name=scene)
    
    if result["success"]:
        console.print(f"[bold blue]Success![/bold blue] Image saved to: {result['image_path']}")
        # Save structured output
        meta_path = Path(output_dir) / f"{script.stem}_meta.json"
        with open(meta_path, "w") as f:
            json.dump(result, f, indent=2)
        console.print(f"Metadata saved to: {meta_path}")
    else:
        console.print("[bold red]Render Failed![/bold red]")
        console.print(result["error"])
        raise typer.Exit(code=1)

