from mvld.sandbox.executor import ManimSandbox
from mvld.eval.vlm_judge import VLMJudge
from rich.console import Console

console = Console()

class RefinementLoop:
    """
    Orchestrates a loop between a Coder (LLM) and a Critic (VLM).
    """
    def __init__(self, output_dir: str = "results/refinement"):
        self.sandbox = ManimSandbox(output_dir=output_dir)
        self.judge = VLMJudge()
        self.max_iterations = 3

    def run_refinement(self, prompt: str, initial_code: str):
        """
        Iteratively refines code based on visual feedback.
        """
        current_code = initial_code
        history = []

        for i in range(self.max_iterations):
            console.print(f"[bold cyan]Iteration {i+1}:[/bold cyan] Rendering and Judging...")
            
            # 1. Render
            temp_script = Path("temp_refine.py")
            temp_script.write_text(current_code)
            res = self.sandbox.run_script(temp_script)
            
            if not res["success"]:
                feedback = f"Execution Error: {res['error']}"
                score = 0.0
            else:
                # 2. Judge (Critic)
                judge_res = self.judge.judge_render(res["image_path"], prompt)
                feedback = judge_res["feedback"]
                score = judge_res["score"]

            console.print(f"Score: [green]{score}[/green] | Feedback: {feedback}")
            
            history.append({
                "iteration": i,
                "code": current_code,
                "score": score,
                "feedback": feedback
            })

            if score >= 0.95:
                console.print("[bold green]Threshold met![/bold green]")
                break

            # 3. Request Fix (Simulated call to Coder LLM)
            current_code = self._mock_llm_fix(current_code, feedback)

        return history

    def _mock_llm_fix(self, code: str, feedback: str) -> str:
        """
        Simulates an LLM providing a fix based on feedback.
        """
        # In a real system, this would call an LLM API
        console.print("[italic]Requesting fix from Coder LLM...[/italic]")
        return code + "\n# Fix applied based on feedback: " + feedback

if __name__ == "__main__":
    loop = RefinementLoop()
    # loop.run_refinement("A red circle on the LEFT", "from manim import *; class S(Scene): def construct(self): self.add(Circle(color=RED))")
    print("Refinement Loop ready.")
