from functools import wraps
from src.preprocess.preprocessor import Preprocessor
from sklearn.model_selection import train_test_split

class IDatasetCreator:
    def __init__(self, preprocessor,data_extractor):
        self.preprocessor=preprocessor
        self.data_extractor=data_extractor

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
    def __init__(self, preprocessor=Preprocessor(),data_extractor=DataExtractor()):
        super().__init__(preprocessor,data_extractor)

    def autoprocessed(func):
        def wrapper(instance, *args, **kwargs):
            file_name = args[0]
            print(f"Processing file: {file_name}")

            p = instance.preprocessor
            # Preprocess the data using the instance's preprocessor
            data = p.process(file_name)
            if data.empty:
                print("The DataFrame is empty.")
                return
            X_good, y_good = instance.data_extractor.extract_data(data=data,lang=p.translator.lang,min_val=10)
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
