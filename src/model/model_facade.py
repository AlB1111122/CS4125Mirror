from src.model import model_factory
from src.model.model_registry import ModelRegistry
from src.preprocess.dataset_creator import ScratchDatasetCreator, LoadProcessedDatasetCreator
from src.model.model import Model

class ModelFacade:
    """Class to control all teh complex processes of the model"""
    def __init__(self):
        self.model_registry = ModelRegistry()
        self.model = None

    def create_model(self, model_type: str):
        """Create a specified module"""
        self.model = model_factory.NewModelFactory.create_model(model_type)
        return self.model
    
    def load_model(self, model_name: str):
        """Load a specified module from file"""
        self.model = model_factory.LoadModelFactory.create_model(model_name)
        return self.model
    
    def register_model(self, model_name: str, model_class: str):
        """register the model to the model registry"""
        return self.model_registry.register_model(model_name, model_class)
    
    def list_model_registry(self):
        """Get the list of modules from the model registry"""
        return self.model_registry.list_registries()
    
    def save_model(self, model_name: str):
        """Save teh trained module to disk"""
        return self.model.save_model(model_name)
    
    def train_model(self, X_train, y_train):
        """Train the model with teh specified data"""
        return self.model.train(X_train, y_train)
    
    def test_model(self, X_test, y_test, file_name: str):
        """Test the model with the specified data"""
        return self.model.test_model(X_test, y_test, file_name)
    
    def predict_model(self, X_test):
        """Use a trained module to predict classification of new data"""
        return self.model.predict(X_test)
