from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BasePipeline(ABC):
    """
    Abstract base class for all MVLD training pipelines.
    """
    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        pass

class PipelineRegistry:
    """
    Registry for managing training pipelines.
    """
    _pipelines = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(pipeline_cls):
            cls._pipelines[name] = pipeline_cls
            return pipeline_cls
        return wrapper

    @classmethod
    def get(cls, name: str) -> BasePipeline:
        if name not in cls._pipelines:
            raise ValueError(f"Pipeline '{name}' not found in registry.")
        return cls._pipelines[name]()

    @classmethod
    def list_pipelines(cls) -> List[str]:
        return list(cls._pipelines.keys())
