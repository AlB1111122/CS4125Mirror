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
    def extract_data(self,data,lang):
        pass
    @staticmethod
    def autoprocessed(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            pass

class CSVDatasetCreator(IDatasetCreator):

    @staticmethod
    def extract_data(data,lang,min_val):
        tfidfconverter = TfidfVectorizer(max_features=2000, min_df=4, max_df=0.90)
        x1 = tfidfconverter.fit_transform(data["Interaction content"]).toarray()
        x2 = tfidfconverter.fit_transform(data["ts_" + lang]).toarray()  # make that mod
        X = np.concatenate((x1, x2), axis=1)
        good_y1 = data.y1.value_counts()[data.y1.value_counts() > min_val].index
        data = data.loc[data.y1.isin(good_y1)]
        y = data.y.to_numpy()
        # rm bad test cases
        y_series = pd.Series(y)
        good_y_value = y_series.value_counts()[y_series.value_counts() >= 3].index
        y_good = y[y_series.isin(good_y_value)]
        X_good = X[y_series.isin(good_y_value)]
        return X_good,y_good

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
            X_good, y_good = CSVDatasetCreator.extract_data(data,p.translator.lang,10)
            # Call the original function with updated arguments
            return func(instance,X_good=X_good,y_good=y_good, *args, **kwargs)

        return wrapper

    @autoprocessed
    def create_train_test(self,file_name,X_good,y_good,test_size=.2):
        X_train, X_test, y_train, y_test = train_test_split(X_good, y_good, test_size=test_size, random_state=0)
        return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

    @autoprocessed
    def create_dataset(self,file_name,use,X_good,y_good):
        return {"X_"+use: X_good,"y_"+use: y_good}
