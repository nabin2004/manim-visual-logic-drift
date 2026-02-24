# MVLD Development Guide: Extending the System

This guide explains how to add new features to the Manim Visual Logic Drift (MVLD) project with minimal friction.

## Adding a New Algorithm (Pipeline)

To add a new post-training algorithm (e.g., a new RL survey method or a specialized SFT):

1.  **Create a new file** in `mvld/pipeline/`.
2.  **Inherit** from `BasePipeline` and **Register** it.

```python
from mvld.pipeline.base import BasePipeline, PipelineRegistry

@PipelineRegistry.register("my_new_algorithm")
class MyNewAlgorithm(BasePipeline):
    def run(self, **kwargs):
        # Implementation here
        return {"status": "success"}
```

3.  **Automatic CLI Participation**: The CLI will now automatically list `my_new_algorithm` as a choice for training.

## Adding a New Evaluator

To add a new visual or spatial metric:

1.  **Create/Modify a file** in `mvld/eval/`.
2.  **Inherit** from `BaseEvaluator` and **Register** it.

```python
from mvld.eval.base import BaseEvaluator, EvaluatorRegistry

@EvaluatorRegistry.register("color_diversity")
class ColorDiversityEvaluator(BaseEvaluator):
    def evaluate(self, scene_graph=None, **kwargs):
        # Logic to calculate diversity
        return {"score": 0.9}
```

## Modular Design Principles

- **Registsries**: Use `PipelineRegistry` and `EvaluatorRegistry` to decouple implementation from selection.
- **Independence**: Evaluators should operate on the `scene_graph` or `image_path` independently.
- **Reporting**: Always return a dictionary from `evaluate()` or `run()` for standardized logging.
