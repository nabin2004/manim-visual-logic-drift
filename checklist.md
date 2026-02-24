# Developer Checklist: Manim Visual Logic Drift (MVLD)

This checklist outlines the remaining implementation steps to reach full project capabilities for research and production.

## Tier 1: Foundation (Spatial SFT & Layout)
- [x] **Custom Manim Base Class**: Create a `MVLDScene` that automatically logs all mobjects, their positions, colors, and bounding boxes to a `scene_graph.json` upon rendering.
- [x] **TikZ/SVG Layout Pretraining**: Implement data loaders for TikZ/SVG datasets to teach the model basic 2D spatial relationships.
- [x] **Coordinate-Augmented SFT**: Update the SFT pipeline to include explicit coordinate annotations (e.g., `[0.5, 0.2]`) in the prompt/code training pairs.
- [x] **Synthetic Data Generator**: Build a script to generate thousands of simple scene variations (e.g., "3 circles of different sizes") to boost spatial awareness.

## Tier 2: Drift Reduction (Rejection & Contrastive Flow)
- [x] **Full RFT Integration**: Automate the generate -> render -> score -> fine-tune loop using the existing RFT pipeline.
- [x] **Error-Seeded Contrastive Pairs**: Implement a system that takes working code, introduces a "visual bug" (e.g., changing `LEFT` to `RIGHT`), and uses both as a contrastive pair.
- [x] **DPO Implementation**: Setup the Direct Preference Optimization (DPO) trainer using code-render pairs where the "preferred" sample is the one with the highest CLIP score.
- [/] **Negative Mining**: Identify samples where the code runs (exit code 0) but the CLIP score is low (< 0.6) to specifically target visual drift.

## Tier 3: Advanced Pipeline (Online RL & Tooling)
- [ ] **Online DPO/PPO**: Implement a real-time RL loop where the model learns from visual feedback during the training process.
- [ ] **VLM-as-Judge**: Integrate a Vision-Language Model (like Claude 3.5 Sonnet or GPT-4o) to provide qualitative rewards (e.g., "The objects overlap awkwardly").
- [ ] **Multi-Agent Refinement Loop**: Build a "Coder + Critic" system where the Critic agent sees the render and suggests code fixes to the Coder.
- [ ] **MCTS for Manim**: Implement Monte Carlo Tree Search for planning complex animation sequences.

## Evaluation & Infrastructure
- [ ] **Object Count Scorer**: Use a simple heuristic or a small object detection model to verify the number of objects in the frame matches the prompt.
- [ ] **Animation Order Verification**: Extract frame-by-frame scene graphs to ensure objects appear in the order specified in the instruction.
- [ ] **CLIP-Directional Similarity**: Measure if the *change* in the prompt (e.g., "moving left") matches the *change* in the visual output.
- [ ] **Benchmark Dataset**: Curate a "MVLD-Bench" with 100+ high-quality Manim prompts across 5 categories of complexity.

## Research & Presentation
- [ ] **Visualization Dashboard**: Create a simple web dashboard (e.g., Streamlit) to browse code, renders, and their corresponding scores.
- [ ] **Structured Experiment Tracking**: Integrate `WandB` or `MLflow` to track CLIP scores and win rates across different model versions.
- [ ] **Ablation Study CLI**: Commands to run training with/without specific reward signals (CLIP vs. Spatial vs. Exec).
- [ ] **Paper-Ready Export**: Ensure all result JSONs contain sufficient metadata for generating LaTeX tables and performance plots.
