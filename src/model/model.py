from abc import ABC
from sklearn.metrics import confusion_matrix, classification_report
from src.util import Util
from src.pickler import Pickler
import pandas as pd

class IModel(ABC):
    """Define a template model which can be used in concrete classes."""
    def __init__(self, s_model) -> None:
        self.classifier = s_model

    def train(self, X_train, y_train) -> None:
        """Train the model"""
        pass

    def predict(self, data):
        """Use the trained model to predict what new inputs are classified as."""
        pass

    def save_model(self, model_name):
        """Save teh model to the disk for future use."""
        pass

    def test_model(self, X_test, y_test, file_name):
        """Test teh model against training data"""
        pass

class Model(IModel):
    """Main model of the AI models we are running"""
    def __init__(self, s_model) -> None:
        super().__init__(s_model)
    
    def train(self,X_train, y_train) -> None:
        self.classifier.fit(X_train, y_train)

    def predict(self, data):
       return self.classifier.predict(data)

    def save_model(self,model_name):
        Pickler.dump("models/"+model_name,self.classifier)
    
    def test_model(self,X_test,y_test,file_name):
        y_pred = self.classifier.predict(X_test)
        p_result = pd.DataFrame(self.classifier.predict_proba(X_test))
        p_result.columns = self.classifier.classes_
        with open(Util().get_project_dir() +'/saves/test_results/'+file_name, 'w') as file:
            print(p_result, file=file)
            print(confusion_matrix(y_test, y_pred), file=file)
            print(classification_report(y_test, y_pred), file=file)
