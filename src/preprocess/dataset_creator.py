from abc import ABC, abstractmethod
from src.preprocess.data_extractor import DataExtractor
from src.preprocess.preprocessor import Preprocessor
from sklearn.model_selection import train_test_split
from src.pickler import Pickler

class IDatasetCreator(ABC):
    def __init__(self, data_extractor):
        self.data_extractor=data_extractor

    @abstractmethod
    def autoprocessed(func):
        def wrapper(instance, *args, **kwargs):
            pass

    @abstractmethod
    def create_dataset(self,file_name,use,x,y):
        return {"X_"+use: x,"y_"+use: y}

    @abstractmethod
    def create_train_test(self,file_name,x,y,test_size=.2):
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)
        return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

class ScratchDatasetCreator(IDatasetCreator):
    def __init__(self, preprocessor=Preprocessor(), data_extractor=DataExtractor()):
        super().__init__(data_extractor)
        self.preprocessor=preprocessor

    def autoprocessed(func):
        def wrapper(instance, *args, **kwargs):
            #file_name = args[0]
            file_name = kwargs.get("file_name")
            print(f"Processing file: {file_name}")

            p = instance.preprocessor
            # Preprocess the data using the instance's preprocessor
            data = p.process(file_name)
            if data.empty:
                print("The DataFrame is empty.")
                return
            X_good, y_good = instance.data_extractor.extract_data(data=data,lang=p.translator.lang,min_val=10)
            # Call the original function with updated arguments
            return func(instance,x=X_good,y=y_good, *args, **kwargs)

        return wrapper

    @autoprocessed # x,y passed int by decorator
    def create_train_test(self,file_name,x,y,test_size=.2):
        return super().create_train_test(file_name,x,y,test_size)


    @autoprocessed # x,y passed int by decorator
    def create_dataset(self,file_name,use,x,y):
        return super().create_dataset(file_name,use,x,y)

class LoadProcessedDatasetCreator(IDatasetCreator):
    def __init__(self,lang="en",data_extractor=DataExtractor()):
        super().__init__(data_extractor)
        self.lang = lang

    def autoprocessed(func):
        def wrapper(instance, *args, **kwargs):
            file_name = kwargs.get("file_name")
            print(f"Processing file: {file_name}")
            data = Pickler.read_dump("data/"+file_name)

            if not data:
                print("The DataFrame is empty.")
                return
            #return func(instance,x=data["X_data"],y=data["y_data"], *args, **kwargs)
            return data

        return wrapper

    @autoprocessed  # x,y passed int by decorator
    def create_train_test(self,file_name,x,y,test_size=.2):
        return super().create_train_test(file_name,x,y,test_size)

    @autoprocessed  # x,y passed int by decorator
    def create_dataset(self,file_name,use,x,y,):
        return super().create_dataset(file_name,use,x,y)
