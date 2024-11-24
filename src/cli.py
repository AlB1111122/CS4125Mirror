from src.model.model_facade import ModelFacade


class CLI:
    def __init__(self, model_facade):
        self.model_facade = model_facade
        self.create_train_test = None

    def main(self):
        while True:
            print("Press 1 to create a model")
            print("Press 2 to print model registries")
            print("Press 3 to register model registries")
            print("Press 4 to load a model")
            print("Press 5 to save a model")
            print("Press 6 to train a model")
            print("Press 7 to test a model")
            print("Press 8 to predict a model")
            print("Press 9 to create a train test split")

            print("Press q to quit")

            choice = input("Enter your choice: ")
            if choice == '1':
                model_type = input("Enter the model type (e.g., 'decision_tree'): ")
                model = self.model_facade.create_model(model_type)
                print("Model created")
            elif choice == '2':
                registries = self.model_facade.list_model_registry()

                for registry in registries:
                    print(registry)
            elif choice == '3':
                model_name = input("Enter the model name (e.g., 'decision_tree'): ")
                model_class = input("Enter the model class (e.g., 'DecisionTreeClassifier'): ")
                registry = self.model_facade.register_model(model_name, model_class)
                registries = self.model_facade.list_model_registry()

                for registry in registries:
                    print(registry)
            elif choice == '4':
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
                break


if __name__ == "__main__":
    model_facade = ModelFacade()
    cli = CLI(model_facade)
    cli.main()