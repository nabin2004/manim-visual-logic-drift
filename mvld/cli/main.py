import typer
from rich.console import Console
from mvld.cli import render, evaluate, train

app = typer.Typer(
    name="mvld",
    help="Manim Visual Logic Drift (MVLD) Post-Training System",
    add_completion=False,
)

app.add_typer(render.app, name="render", help="Render Manim code")
app.add_typer(evaluate.app, name="evaluate", help="Evaluate rendered output")
# app.add_typer(train.app, name="train", help="Train post-training models")

console = Console()

@app.callback()
def main():
    """
    MVLD: Fixing visual logic drift in Manim code generation.
    """
    pass

if __name__ == "__main__":
    app()
