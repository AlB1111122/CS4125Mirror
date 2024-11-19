from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

from src.util import Util
from src.pickler import Pickler
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

class Model:

    def __init__(self, s_model) -> None:
        self.classifier = s_model
    
    def train(self,X_train, y_train) -> None:
        self.classifier.fit(X_train, y_train)

    def predict(self, X_test,y_test):
        self.classifier.fit(X_test, y_test)

    def save_model(self,model_name):
        Pickler.dump("models/"+model_name)
    
    def model_data(self,temp):
        tfidfconverter = TfidfVectorizer(max_features=2000, min_df=4, max_df=0.90)
        x1 = tfidfconverter.fit_transform(temp["Interaction content"]).toarray()
        x2 = tfidfconverter.fit_transform(temp["ts_en"]).toarray()
        X = np.concatenate((x1, x2), axis=1)
        good_y1 = temp.y1.value_counts()[temp.y1.value_counts() > 10].index
        temp = temp.loc[temp.y1.isin(good_y1)]
        y = temp.y.to_numpy()

        #rm bad test cases
        y_series = pd.Series(y)
        good_y_value = y_series.value_counts()[y_series.value_counts() >= 3].index
        y_good = y[y_series.isin(good_y_value)]
        X_good = X[y_series.isin(good_y_value)]
        y_bad = y[y_series.isin(good_y_value) == False]
        X_bad = X[y_series.isin(good_y_value) == False]
        test_size = X.shape[0] * 0.2 / X_good.shape[0]
        X_train, X_test, y_train, y_test = train_test_split(X_good, y_good,     test_size=test_size, random_state=0)
        X_train = np.concatenate((X_train, X_bad), axis=0)
        y_train = np.concatenate((y_train, y_bad), axis=0)
        return {"X_train":X_train, "X_test":X_test, "y_train":y_train, "y_test":y_test}
    
    def test_model(self,X_test,y_test,file_name):
        y_pred = self.classifier.predict(X_test)
        p_result = pd.DataFrame(self.classifier.predict_proba(X_test))
        p_result.columns = self.classifier.classes_
        with open(Util.PROJ_DIR+'/saves/test_results/'+file_name, 'w') as file:
            print(p_result, file=file)
            print(confusion_matrix(y_test, y_pred), file=file)
            print(classification_report(y_test, y_pred), file=file)
