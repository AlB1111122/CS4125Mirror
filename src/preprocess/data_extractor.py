from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sympy.codegen.ast import continue_

from src.pickler import Pickler

class IDataExtractor(ABC):
    """Abstract class to manage extracting good data from the raw input data"""
    @staticmethod
    @abstractmethod
    def extract_data(data, lang,min_val):
        pass

class DataExtractor(IDataExtractor):
    def extract_data(self,data, lang, min_val):
        vocab = None
        try:
            vocab = Pickler.read_dump("vocab/vocab_data.pkl")
            tfidfconverter = TfidfVectorizer(max_features=2000, min_df=4, max_df=0.90, vocabulary=vocab)
        except FileNotFoundError:
            tfidfconverter = TfidfVectorizer(max_features=2000, min_df=4, max_df=0.90)
            combined_text = data["Interaction content"] + " " + data["ts_" + lang]
            #make a combined vocab set
            tfidfconverter.fit_transform(combined_text)

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
        if vocab is None:
            Pickler.dump( "vocab/vocab_data.pkl",tfidfconverter.get_feature_names_out())
        return X_good, y_good
