import pandas as pd
from functools import wraps
from src.preprocess.preprocessor import Preprocessor
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

class IDatasetCreator:
    def create_dataset(self,file_name,use):
        pass
    def create_train_test(self):
        pass
    @staticmethod
    def autoprocessed(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            pass

class CSVDatasetCreator(IDatasetCreator):

    @staticmethod
    def autoprocessed(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            p = Preprocessor()
            # Extract the filename (assumed to be the second argument here)
            file_name = args[0]
            print(f"Processing file: {file_name}")

            # Preprocess the data using the instance's preprocessor
            data = p.process(file_name)
            if data.empty:
                print("The DataFrame is empty.")
                return
            # Call the original function with updated arguments
            return func(instance,data=data,lang=p.translator.lang, *args, **kwargs)

        return wrapper

    @autoprocessed # dont supply vaues for data or lang
    def create_train_test(self,file_name,data,lang):
        tfidfconverter = TfidfVectorizer(max_features=2000, min_df=4, max_df=0.90)
        x1 = tfidfconverter.fit_transform(data["Interaction content"]).toarray()
        x2 = tfidfconverter.fit_transform(data["ts_"+lang]).toarray()#make that mod
        X = np.concatenate((x1, x2), axis=1)
        good_y1 = data.y1.value_counts()[data.y1.value_counts() > 10].index
        data = data.loc[data.y1.isin(good_y1)]
        y = data.y.to_numpy()
        # rm bad test cases
        y_series = pd.Series(y)
        good_y_value = y_series.value_counts()[y_series.value_counts() >= 3].index
        y_good = y[y_series.isin(good_y_value)]
        X_good = X[y_series.isin(good_y_value)]
        test_size = X.shape[0] * 0.2 / X_good.shape[0]
        X_train, X_test, y_train, y_test = train_test_split(X_good, y_good, test_size=test_size, random_state=0)
        return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

    @autoprocessed # dont supply values for data or lang
    def create_dataset(self,file_name,use,data,lang):
        tfidfconverter = TfidfVectorizer(max_features=2000, min_df=4, max_df=0.90)
        x1 = tfidfconverter.fit_transform(data["Interaction content"]).toarray()
        x2 = tfidfconverter.fit_transform(data["ts_"+lang]).toarray()#make that mod
        X = np.concatenate((x1, x2), axis=1)
        good_y1 = data.y1.value_counts()[data.y1.value_counts() > 10].index
        data = data.loc[data.y1.isin(good_y1)]
        y = data.y.to_numpy()
        # rm bad test cases
        y_series = pd.Series(y)
        good_y_value = y_series.value_counts()[y_series.value_counts() >= 3].index
        y_good = y[y_series.isin(good_y_value)]
        X_good = X[y_series.isin(good_y_value)]
        return {"X_"+use: X_good,"y_"+use: y_good}
