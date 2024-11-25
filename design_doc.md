 # Design Doc

## Overview

This app is an email classifier that automatically categorizes incoming emails into various categories that we have outlined  
in our datasets from the labs.

We're using multiple different machine learning classifiers like `logistic regression` and `gradient boosting` to classify  
our emails.

Abstract Base Classes were used to prevent instantiation of base classes and interfaces for good code health.

## Breakdown

### Factory Pattern

#### Justification

A Factory pattern allows us to get models from new sources and treat all of them in the same manner as we're loading them,  
which allows for easier scalability as we can easily add and remove sources for our models.

The overall design goal for this model is to make the app more scalable, configurable and flexible as it allows the user  
to directly interact with the model-making process of the app.

Since both factories use the same methods, we can pass them into the same method as they have the same functionality.

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

class ModelRegistry:
    """Class to allow the use of different AI models under a unified framework  """
    def __init__(self):
        self._registry = {
            'logistic_regression': LogisticRegression(),
            'decision_tree': DecisionTreeClassifier(),
            'random_forest': RandomForestClassifier(),
            'gradient_boosting': GradientBoostingClassifier(),
            'svc': SVC(probability=True),
            'naive_bayes': GaussianNB(),
            'mlp': MLPClassifier(),
        }

    def get_model(self,model_type: str):
        """Return a model, if it exists"""
        if model_type not in self._registry:
            raise ValueError(f"Unsupported model type: {model_type}")
        return self._registry[model_type]

    def register_model(self, model_name: str, model_class):
        """Allows adding extra models to the registry"""
        self._registry[model_name] = model_class

    def list_registries(self):
        """Return s a list of names of the models"""
        return self._registry.keys()
```

The advantage here is that we can change the source of the model we are creating, such as swapping model_registry with creating a model from a dump.
We can also use our concrete classes interchangeably as they all use the AbstractModelFactory Contract.

This allows new model sources to be added to the system without modifying the existing code, which satisfies the Open-Closed SOLID principle.  
This also encapsulates and abstracts the object creation process through polymorphism, as the clients don't need to know the specifics of creating a model.

![Factory Pattern](./images/Factory_Diagram.png)

### Decorator Pattern

#### Justification

We decided to use a Decorator pattern for the dataset creator class as it clearly marks the methods as having had preprocessing work done to them.
The logic is reused between methods.  
Additionally the ``autoprocessed`` decorator clearly shows a separation of concerns as it applies all the preprocessing steps and the methods themselves shape the data. 
The dynamic argument handling in the preprocessor allows future classes that need more or fewer arguments will not require modifications of the existing classes.  
This allows for concise and readable methods in our classes.

It was best to apply this pattern towards the methods within our class, which in our case is ``autoprocessed(func)``. As  
this is our main decorator method. It could also be used outside of methods to help improve extensibility in the future.

````python
def autoprocessed(func):
    def wrapper(instance, *args, **kwargs):
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
````

![Decorator Pattern](./images/Decorator_Diagram.png)

### Singleton

#### Justification

The Singleton Util class provides a method to allow all other classes within our app to access the project directory, as  
that's required by most if not all of our classes within our implementation.

It allows us to have a unified method, in the sense that it behaves in the exact way in every invocation across all the classes  
that require the project directory. In addition, this mitigates the issue of python's context-dependent path resolution.  
As in the directory where the application is run from would likely break the paths of existing files.

````python
  # allows us to do tmp = Util();
def __new__(cls):
    if cls.__instance is None:
      cls.__instance = super(Util, cls).__new__(cls)
    return cls.__instance
````
This ensures there is only ever one copy of ``Util``.
The purpose of this pattern is to allow maintainability within our app.

![Singleton](./images/Singleton.png)

### Facade

#### Justification

It encapsulates and consolidates interactions with the model and the model factories to remove the need for manual configuration and allow easy use of the model in the command line interface.  
This provides a simple API for users to interact with. Our Factory Pattern also enables modularity, as the facade abstracts away the internal logic of these interactions.  
If something needs to be changed or added, the Facade or the client that uses it does not need to change.

Additionally, new functions can be added to the model facade without needing to edit the subsystem classes.

To do achieve this pattern we turned our Factory Pattern into a series of subsystem classes that link to the main Facade class.

````python
class ModelFacade:
    """Class to control all teh complex processes of the model"""
    def __init__(self):
        self.model_registry = ModelRegistry()
        self.model = None

    def create_model(self, model_type: str):
        """Create a specified module"""
        self.model = model_factory.NewModelFactory.create_model(model_type)
        return self.model
    
    def load_model(self, model_name: str):
        """Load a specified module from file"""
        self.model = model_factory.LoadModelFactory.create_model(model_name)
        return self.model
    
    def register_model(self, model_name: str, model_class: str):
        """register the model to the model registry"""
        return self.model_registry.register_model(model_name, model_class)
    
    def list_model_registry(self):
        """Get the list of modules from the model registry"""
        return self.model_registry.list_registries()
    
    def save_model(self, model_name: str):
        """Save teh trained module to disk"""
        return self.model.save_model(model_name)
    
    def train_model(self, X_train, y_train):
        """Train the model with teh specified data"""
        return self.model.train(X_train, y_train)
    
    def test_model(self, X_test, y_test, file_name: str):
        """Test the model with the specified data"""
        return self.model.test_model(X_test, y_test, file_name)
    
    def predict_model(self, X_test):
        """Use a trained module to predict classification of new data"""
        return self.model.predict(X_test)

````

The primary goal of this Facade pattern was to help us achieve flexibility and scalability within our app, as when our  
app requires more functionality this pattern is able to handle new additions to our app.

![Facade](./images/Facade_Diagram.png)

### Strategy

#### Justification

A key part of this application is presenting the user with flexible tools in our CLI, and we implemented the Strategy pattern in our CLI.  
This allows users at runtime to select from a variety of machine-learning models to train, test, and predict with.  
Additionally, the user can choose from multiple types of data sources and the dataset creator's algorithm can also be changed at runtime.

Our Strategy pattern is inside the CLI, where we have encapsulated the creating of datasets and selection of the model.

````python
# As you can see in this code snippet, it doesn't matter whether LoadProcessedDatasetCreator or ScratchDatasetCreator is selected.
# The logic afterward isn't changed, and we can swap between them at runtime.
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
            continue
    if dataset_source == "":
        throw_error(IndexError)
    print("Pick the file you want to load from: 1)Enter full path to new file 2)Pick from known data")
    match input("Selection: "):
        case "1":
            data_sel = input("Enter absolute path to file: ")
            filen = os.path.basename(data_sel)
            try:
                shutil.copy(data_sel, self.util.get_project_dir() + dataset_source)
                data_sel = filen
            except shutil.SameFileError:
                print("File already exists")
                loop = False
                continue
        case "2":
            print(dataset_source)
            data_sel = self.select_from_dir(dataset_source)
        case _:
            print("Invalid selection, try again")
            loop = False
            continue

````

Throughout the runtime of the app, the user can change the machine-learning algorithm used to classify or train the data.

The main goal of this pattern was to make our app more flexible, as it allows us to have a mechanism to encapsulate and interchange  
algorithms at runtime.

![Strategy](./images/Strategy_Diagram.png)

### Sequence Diagram

The below diagram outlines the flow of events as a user interacts with our app. We primarily make things go through the CLI  
as it's the main way that the user interacts with the app.

![Sequence of events](./images/Sequence_Diagram.png)

