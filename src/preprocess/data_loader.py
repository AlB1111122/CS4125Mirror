from src.util import Util
import pandas as pd

class IDataLoader:
    def load_data(self, file_name):
        pass

class CSVDataLoader(IDataLoader):
    def __init__(self):
        self.file_path = None

    def load_data(self,input_file_name):
        self.file_path = Util().get_project_dir()+"/data/"+input_file_name
        df = pd.read_csv(self.file_path)

        # convert the dtype object to unicode string
        df['Interaction content'] = df['Interaction content'].values.astype('U')
        df['Ticket Summary'] = df['Ticket Summary'].values.astype('U')

        # Optional: rename variable names for remebering easily
        df["y1"] = df["Type 1"]
        df["y2"] = df["Type 2"]
        df["y3"] = df["Type 3"]
        df["y4"] = df["Type 4"]
        df["x"] = df['Interaction content']

        df["y"] = df["y2"]

        # remove empty y
        df = df.loc[(df["y"] != '') & (~df["y"].isna()),]
        print(df.shape)
        return df
