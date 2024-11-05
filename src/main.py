from sklearn.ensemble import RandomForestClassifier
import pickler
import model.model as model
from src.model.model_factory import LoadModelFactory, NewModelFactory

"""sc = RandomForestClassifier(n_estimators=1000, random_state=0)
rawd = pickler.Pickler.read_dump("data/processed_data.dump")
m = model.Model(sc)
data = m.model_data(rawd)
m.train(data["X_train"],data["y_train"])
m.test_model(data["X_test"],data["y_test"],"exResults1.txt")
rawd = pickler.Pickler.read_dump("data/processed_data.dump")
m = NewModelFactory.create_model("logistic_regression")
data = m.model_data(rawd)
m.model_data(rawd)
m.train(data["X_train"],data["y_train"])
m.test_model(data["X_test"],data["y_test"],"exResults5.txt")
"""
rawd = pickler.Pickler.read_dump("data/processed_data.dump")
#m = ModelFactory.create_model("logistic_regression")
m = NewModelFactory.create_model("svc")
data = m.model_data(rawd)
m.model_data(rawd)
m.train(data["X_train"],data["y_train"])
m.test_model(data["X_test"],data["y_test"],"one.txt")