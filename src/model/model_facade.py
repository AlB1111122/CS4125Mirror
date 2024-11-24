from src.model import model_factory
from src.model.model_registry import ModelRegistry
from src.preprocess.dataset_creator import ScratchDatasetCreator, LoadProcessedDatasetCreator
from src.model.model import Model

class ModelFacade():
    def __init__(self):
        self.model_registry = ModelRegistry()
        self.model = None

    def create_model(self, model_type: str):
        self.model = model_factory.NewModelFactory.create_model(model_type)
        return self.model
    
    def load_model(self, model_name: str):
        self.model = model_factory.LoadModelFactory.create_model(model_name)
        return self.model
    
    def register_model(self, model_name: str, model_class: str):
        return self.model_registry.register_model(model_name, model_class)
    
    def list_model_registry(self):
        return self.model_registry.list_registries()
    
    def save_model(self, model_name: str):
        return self.model.save_model(model_name)
    
    def train_model(self, X_train, y_train):
        return self.model.train(X_train, y_train)
    
    def test_model(self, X_test, y_test, file_name: str):
        return self.model.test_model(X_test, y_test, file_name)
    
    def predict_model(self, X_test, y_test):
        return self.model.predict(X_test, y_test)
    
    def create_train_test(self, creator_type: str, file_name: str):
        if creator_type == "scratch":
            creator = ScratchDatasetCreator()
        elif creator_type == "load":
            creator = LoadProcessedDatasetCreator()
        d = creator.create_train_test(file_name)
        return d
 
   
