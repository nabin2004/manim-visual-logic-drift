from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseEvaluator(ABC):
    """
    Abstract base class for all MVLD evaluators.
    """
    @abstractmethod
    def evaluate(self, **kwargs) -> Dict[str, Any]:
        pass

class EvaluatorRegistry:
    """
    Registry for managing evaluator plugins.
    """
    _evaluators = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(eval_cls):
            cls._evaluators[name] = eval_cls
            return eval_cls
        return wrapper

    @classmethod
    def get(cls, name: str) -> BaseEvaluator:
        if name not in cls._evaluators:
            raise ValueError(f"Evaluator '{name}' not found in registry.")
        return cls._evaluators[name]()

    @classmethod
    def list_evaluators(cls) -> List[str]:
        return list(cls._evaluators.keys())
