import os

from numpy.f2py.auxfuncs import throw_error

from src.model.model_facade import ModelFacade
from src.pickler import Pickler
from src.util import Util
from src.preprocess.dataset_creator import LoadProcessedDatasetCreator, ScratchDatasetCreator
import shutil

class CLI:
    def __init__(self):
        self.model_facade = ModelFacade()
        self.selected_m_name = "None"
        self.util = Util()
        self.dataset_creator = None
        self.active_dataset = None

    def select_from_dir(self, src_dir):
        directory = self.util.get_project_dir() + src_dir
        print(directory)
        # List only files in the directory
        i = 0
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for file in files:
            print(str(i) + ") " + file)
            i += 1
        response = input("Selection: ")
        return files[int(response)]

    def cli(self):
        while True:
            try:
                print(
f"""
Model selected: {self.selected_m_name}
active data selected: {self.active_dataset}
1)Create new model 
2)Load model from storage 
3)Save current model 
4)Get dataset 
5)Use model
6)Save current dataset 
q)To quit
"""
                )
                selection = input("Selection: ")
                match selection:
                    case "q":
                        print("Exiting")
                        return
                    case "1":
                        model_opts = ""
                        i = 0
                        for keys in self.model_facade.list_model_registry():
                            model_opts += str(i) + ") " + keys + "\n"
                            i += 1
                        print(model_opts)
                        model_sel = input("Model selection: ")
                        self.selected_m_name = list(self.model_facade.list_model_registry())[int(model_sel)]
                        self.model_facade.create_model(self.selected_m_name)
                    case "2":
                        model_sel = self.select_from_dir("/saves/models")
                        self.model_facade.load_model(model_sel)
                        self.selected_m_name = model_sel + "_" +str(type(self.model_facade.model.classifier))
                    case "3":
                        if self.selected_m_name == "None":
                            print("Please select a model to be able to save it")
                        else:
                            print("Enter a name to send the model under, or leave blank to use default name")
                            selection = input("Saved model name: ")
                            if selection == "":
                                selection = self.selected_m_name
                            self.model_facade.save_model(selection)
                    case "4":
                        print(
                            "Enter the dataset source: 1) Preprocessed dump of data 2) Raw CSV"
                        )
                        dataset_source = ""
                        loop = True
                        while loop:
                            match input("Selection: "):
                                case "1":
                                    self.dataset_creator = LoadProcessedDatasetCreator()
                                    dataset_source = "/saves/data"
                                case "2":
                                    self.dataset_creator = ScratchDatasetCreator()
                                    dataset_source = "/data"
                                case _:
                                    print("Invalid selection, try again")
                                    loop = False
                            if dataset_source == "":
                                throw_error(IndexError)
                            print("Pick the file you want to load from: 1)Enter full path to new file 2)Pick from known data")
                            match input("Selection: "):
                                case "1":
                                    data_sel = input("Enter absolute path to file: ")
                                    filen = os.path.basename(data_sel)
                                    try:
                                        shutil.copy(data_sel, self.util.get_project_dir()+dataset_source)
                                        data_sel = filen
                                    except shutil.SameFileError:
                                        print("File already exists")
                                        loop = False
                                case "2":
                                    print(dataset_source)
                                    data_sel = self.select_from_dir(dataset_source)
                                case _:
                                    print("Invalid selection, try again")
                                    loop = False

                            print("Pick the use you want the dataset for: 1)Single usage (train or test or predict) 2)Train and test")
                            match input("Selection: "):
                                case "1":
                                    self.active_dataset = self.dataset_creator.create_dataset(data_sel, "data")
                                case "2":
                                    train_split = float(input("Train split size between 0-1 (will be .2 if left blank): "))
                                    if train_split <= 0 or train_split >= 1:
                                        train_split = .2
                                    self.active_dataset = self.dataset_creator.create_train_test(data_sel,train_split)
                                case _:
                                    print("Invalid selection, try again")
                            loop = False
                    case "5":
                        print(
f"""
1)Train
2)Test
3)Train and test
4)Predict
"""
                        )
                        match(input("Selection: ")):
                            case "1":
                                if "y_data" in self.active_dataset:
                                    self.model_facade.train_model(self.active_dataset["X_data"],self.active_dataset["y_data"])
                                else:
                                    print("Your selected dataset is not for training")
                            case "2":
                                if "y_data" in self.active_dataset:
                                    test_outp_name = input("Name of test results file: ")
                                    if test_outp_name == "":
                                        test_outp_name=self.selected_m_name+"_test_results.txt"
                                    self.model_facade.test_model(self.active_dataset["X_data"],self.active_dataset["y_data"],test_outp_name)
                                else:
                                    print("Your selected dataset is not for testing")
                            case "3":
                                if "y_test" in self.active_dataset:
                                    self.model_facade.train_model(self.active_dataset["X_train"],self.active_dataset["y_train"])
                                    test_outp_name = input("Name of test results file: ")
                                    if test_outp_name == "":
                                        test_outp_name = self.selected_m_name + "_test_results.txt"
                                    self.model_facade.test_model(self.active_dataset["X_test"], self.active_dataset["y_test"],
                                                         test_outp_name)
                                else:
                                    print("Your selected dataset is not for training and testing")
                            case "4":
                                if "X_data" in self.active_dataset:
                                    print("predicted labels1:")
                                    print(self.model_facade.predict_model(self.active_dataset["X_data"]))
                                else:
                                    print("Your selected dataset is not for predicting")
                    case "6":
                        print("Enter a name to send the dataset under, or leave blank to use default name")
                        selection = input("Saved dataset name: ")
                        if selection == "":
                            selection = self.selected_m_name+"_dataset"
                        Pickler.dump("/data/"+selection,self.active_dataset)
                    case _:
                        print("Invalid selection")
            except ValueError:
                print("Invalid input. Please try again")
            except IndexError:
                print("Invalid input. Please dont exceed the presented indices")


if __name__ == "__main__":
    model_facade = ModelFacade()
    cli = CLI()
    cli.cli()