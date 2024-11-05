from src.model.model import Model
from src.pickler import Pickler

class ModelLoader:
    @staticmethod
    def create_model_from_dump(dump_name: str) -> Model:
        model = Pickler.read_dump("models/" + dump_name)
        return Model(model)