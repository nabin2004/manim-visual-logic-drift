import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def visual(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Original prompt"),
    image: str = typer.Option(..., "--image", "-i", help="Path to rendered frame"),
):
    """
    Evaluate visual similarity using CLIP.
    """
    from mvld.eval.evaluator import VisualEvaluator
    import json
    
    console.print(f"[bold blue]Evaluating similarity for: {prompt}[/bold blue]")
    
    try:
        evaluator = VisualEvaluator()
        results = evaluator.evaluate_render(image, prompt)
        
        console.print(f"[bold green]Evaluation Complete![/bold green]")
        console.print(f"CLIP Similarity: [cyan]{results['clip_similarity']:.2f}[/cyan]")
        
        # Output structured JSON
        print(json.dumps(results, indent=2))
    except Exception as e:
        console.print(f"[bold red]Evaluation Error:[/bold red] {e}")
        raise typer.Exit(code=1)

