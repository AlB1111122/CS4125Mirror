from abc import abstractmethod, ABC
from src.model.model import Model
from src.model.model_registry import ModelRegistry
from src.model.model_loader import ModelLoader

class AbstractModelFactory(ABC):
    #contract allowing creation of models from new and loaded
    @staticmethod
    @abstractmethod
    def create_model(model_type: str) -> Model:
        ...

class NewModelFactory(AbstractModelFactory):
    @staticmethod
    def create_model(model_type: str) -> Model:
        registry = ModelRegistry()
        classifier = registry.get_model(model_type)
        return Model(classifier)

class LoadModelFactory(AbstractModelFactory):
    @staticmethod
    def create_model(model_name: str) -> Model:
        return ModelLoader.create_model_from_dump(model_name)