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