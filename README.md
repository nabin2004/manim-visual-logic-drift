# Manim Visual Logic Drift (MVLD) Post-Training System

Fixing visual logic drift in Manim code generation by grounding models in visual and spatial feedback.

## 🚀 Quick Start

### 1. Setup Environment
```bash
make setup
```

### 2. Generate Synthetic Training Data
```bash
make gen-data
```

### 3. Run Post-Training Algorithms
```bash
# Run RFT (Rejection Fine-Tuning)
make train-rft

# Run generic algorithm from the registry
mvld train algorithm rft --num-samples 10
```

### 4. Visualize Results
```bash
make dashboard
```

## 🛠 Features

- **Isolated Execution**: `ManimSandbox` for safe code rendering.
- **Visual Grounding**: CLIP-based visual alignment & VLM-as-Judge qualitative feedback.
- **Extensible Architecture**: Registry-based plugin system for new algorithms and evaluators.
- **Spatial Awareness**: Coordinate-augmented SFT and automated scene graph extraction.

## 📁 Project Structure

- `mvld/sandbox/`: Rendering and metadata extraction.
- `mvld/eval/`: Evaluator suite (CLIP, Spatial, VLM, Directional).
- `mvld/pipeline/`: Training pipelines (RFT, SFT, DPO, MCTS, Refinement).
- `mvld/data/`: Loaders (TikZ, SVG), generators, and augmenters.
- `docs/DEVELOPMENT.md`: Guide for adding new algorithms.

## 📊 Research Automation

Use the `Makefile` for streamlined research workflows:
- `make evaluate`: Score the latest renders.
- `make report`: Generate summary performance metrics.
- `make test`: Run the verification suite.
- `make lint`: Maintain code quality.
