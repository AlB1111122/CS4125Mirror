from sklearn.metrics import confusion_matrix, classification_report

from src.preprocess.dataset_creator import CSVDatasetCreator
from src.util import Util
from src.pickler import Pickler
import pandas as pd

class IModel:
    def __init__(self, s_model,dataset_creator) -> None:
        self.classifier = s_model
        self.dataset_creator = dataset_creator

    def train(self, X_train, y_train) -> None:
        pass

    def predict(self, X_test, y_test):
        pass

    def save_model(self, model_name):
        pass

    def test_model(self, X_test, y_test, file_name):
        pass

class Model(IModel):

    def __init__(self, s_model, dataset_creator=CSVDatasetCreator()) -> None:
        super().__init__(s_model, dataset_creator)
    
    def train(self,X_train, y_train) -> None:
        self.classifier.fit(X_train, y_train)

    def predict(self, X_test,y_test):
        self.classifier.fit(X_test, y_test)

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
