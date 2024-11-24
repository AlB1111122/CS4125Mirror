from abc import ABC
from src.preprocess.data_cleaner import CSVDataCleaner
from src.preprocess.data_loader import CSVDataLoader
from src.preprocess.translator import StanzaTranslator

class IPreprocessor(ABC):
    def __init__(self, translator, data_loader, data_cleaner):
        self.translator = translator
        self.data_loader = data_loader
        self.data_cleaner = data_cleaner

    def translate_text(self, texts):
        pass

    def load_and_label_data(self, input_file_name):
        pass

    def clean_data(self,data_frame):
        pass

    def process(self, file_name):
        pass

class Preprocessor(IPreprocessor):
    def __init__(self, translator = StanzaTranslator("en"), data_loader = CSVDataLoader(),data_cleaner = CSVDataCleaner() ):
        super().__init__(translator, data_loader, data_cleaner)
        self.file_path = None

    def process(self, file_name):
        """Load and process the data"""
        data = self.data_loader.load_data(file_name)
        data = self.data_cleaner.clean_data(data)
        data["ts_"+self.translator.lang] = self.translator.translate(data["ts"].to_list())
        print(data)
        return data
