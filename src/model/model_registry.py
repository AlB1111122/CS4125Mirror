from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

class ModelRegistry:
    def __init__(self):
        self._registry = {
            'logistic_regression': LogisticRegression(),
            'decision_tree': DecisionTreeClassifier(),
            'random_forest': RandomForestClassifier(),
            'gradient_boosting': GradientBoostingClassifier(),
            'svc': SVC(probability=True),
        }

    def get_model(self,model_type: str):
        if model_type not in self._registry:
            raise ValueError(f"Unsupported model type: {model_type}")
        return self._registry[model_type]

    def register_model(self, model_name: str, model_class):
        self._registry[model_name] = model_class
