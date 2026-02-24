# Manim Visual Logic Drift (MVLD) Post-Training System

Fixing visual logic drift in Manim code generation where code runs but renders the wrong scene.

## Core Features

- **Manim Execution Sandbox**: Isolated rendering of Manim code with metadata capture.
- **Visual Evaluation**: CLIP-based similarity scores between prompt and rendered frame.
- **RFT Baseline**: Rejection Fine-Tuning pipeline for collecting high-quality code-render pairs.
- **Structured CLI**: Powerful commands for rendering, evaluation, and training.

## Installation

```bash
make setup
source venv/bin/activate
```

## Usage

### Render a script
```bash
mvld render file --script samples/simple_scene.py
```

### Evaluate visual similarity
```bash
mvld evaluate visual --prompt "A blue square and a red circle" --image media/images/simple_scene/SimpleScene.png
```

### Run RFT Baseline
```bash
mvld train rft --num-samples 5
```

## Project Structure

- `mvld/sandbox/`: Execution and scene graph extraction.
- `mvld/eval/`: CLIP and spatial metrics.
- `mvld/pipeline/`: Training pipelines (RFT, DPO).
- `mvld/cli/`: CLI implementation.
