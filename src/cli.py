import os

from src.model.model_facade import ModelFacade
from src.util import Util
"""
class CLI:
    def __init__(self, model_facade):
        self.model_facade = model_facade
        self.create_train_test = None

    def main(self):
        while True:#add fault tolerance
            print("Press 1 to create a model")
            print("Press 2 to print model registries")
            print("Press 3 to register model registries")
            print("Press 4 to load a model")
            print("Press 5 to save a model")
            print("Press 6 to train a model")#not working
            print("Press 7 to test a model")
            print("Press 8 to predict a model")
            print("Press 9 to create a train test split")

            choice = input("Enter your choice: ")
            if choice == '1':
                model_type = input("Enter the model type (e.g., 'decision_tree'): ")
                model = self.model_facade.create_model(model_type)
                print("Model created")
            elif choice == '2':
                registries = self.model_facade.list_model_registry()

                for registry in registries:
                    print(registry)
            elif choice == '3': #fix: does not add a new type of model
                model_name = input("Enter the model name (e.g., 'decision_tree'): ")
                model_class = input("Enter the model class (e.g., 'DecisionTreeClassifier'): ")
                registry = self.model_facade.register_model(model_name, model_class)
                registries = self.model_facade.list_model_registry()

                for registry in registries:
                    print(registry)
            elif choice == '4':#FIX: list the avalible models
                model_name = input("Enter the model name (e.g., 'decision_tree'): ")
                model = self.model_facade.load_model(model_name)
                print("Model loaded")
            elif choice == '5':
                model_name = input("Enter the model name (e.g., 'decision_tree'): ")
                model = self.model_facade.save_model(model_name)
                print("Model Saved")
            elif choice == '6':
                d = self.create_train_test
                model = self.model_facade.train_model(d["X_train"], d["y_train"])
                print("Model trained")
            elif choice == '7':
                d = self.create_train_test
                file_name = input("Enter the file name: ")
                model = self.model_facade.test_model(d["X_test"], d["y_test"], file_name)

                file_path = f"src/saves/test_results/{file_name}"
                try:
                    with open(file_path, 'r') as file:
                        print(file.read())
                except FileNotFoundError:
                    print(f"File {file_path} not found.")
            elif choice == '8':
                d = self.create_train_test
                model = self.model_facade.predict_model(d["X_test"], d["y_test"])
                print("Model predicted")
            elif choice == '9':
                creator_type = input("Enter the creator type (e.g., 'scratch'): ")
                file_name = input("Enter the file name: ")
                self.create_train_test = self.model_facade.create_train_test(creator_type, file_name)
                print("Train test split created")
            elif choice == 'q':
                break"""
class CLI:
    def __init__(self):
        self.model_facade = ModelFacade()
        self.selected_m_name = "None"
        self.util = Util()

    def cli(self):
        while(True):
            try:
                print("1)Create new model 2)Load model from storage 3)Save current model 4)Get dataset 5)Use model")
                print("q) to quit")
                print("Model selected: " + self.selected_m_name)
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
                        continue
                    case "2":
                        directory = self.util.get_project_dir() +  "/saves/models"
                        print(directory)
                        # List only files in the directory
                        i = 0
                        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
                        for file in files:
                            print(str(i) + ") "+file)
                            i += 1
                        model_sel = input("Model selection: ")
                        self.model_facade.load_model(files[int(model_sel)])
                        self.selected_m_name = files[int(model_sel)] + "_" +str(type(self.model_facade.model.classifier))
                        continue
                    case "3":
                        if self.selected_m_name == "None":
                            print("Please select a model to be able to save it")
                        else:
                            print("Enter a name to send the model under, or leave blank to use default name")
                            selection = input("Saved model name: ")
                            if(selection == ""):
                                selection = self.selected_m_name
                            self.model_facade.save_model(selection)
                        continue
                    case "4":
                        dataset_source = input("Enter the dataset source: 1)preprocessed dump of data 2)raw csv")
                        datset_type = input("Select dataset type: 1)train 2)test 3)predict")
                        match
                        continue
                    case "5":
                        continue
                    case "6":
                        continue
                    case _:
                        print("Invalid selection")
                        continue
            except ValueError:
                print("Invalid input. Please try again")
            except IndexError:
                print("Invalid input. Please dont exceed the presented indices")


if __name__ == "__main__":
    model_facade = ModelFacade()
    cli = CLI()
    cli.cli()