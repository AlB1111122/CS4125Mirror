from src.model import model_factory
from src.model.model_facade import ModelFacade
from src.preprocess.dataset_creator import *
"""from src.model import model_facade
from ""

mf = model_facade.ModelFacade("""


"""
m = model_factory.NewModelFactory.create_model("decision_tree")
p = pickler.Pickler()
d = p.read_dump("data/processed_data.dump")
de = DataExtractor()
data = {}
data["X_train"], data["y_train"] = de.extract_data(d,"en",10)
#d = m.dataset_creator.create_train_test("AppGallery.csv")
#p.dump("data/train_test",d)
m.train(data["X_train"], data["y_train"])
m.test_model(data["X_train"], data["y_train"],"test")
dsc = LoadProcessedDatasetCreator()
m = model_factory.NewModelFactory.create_model("decision_tree")
d = dsc.create_train_test("processed_data.dump")
m.train(d["X_train"], d["y_train"])
m.test_model(d["X_test"], d["y_test"],"test")

m = model_factory.NewModelFactory.create_model("decision_tree")
sdc = ScratchDatasetCreator()
d = sdc.create_train_test("shortAppGallery.csv")
m.train(d["X_train"], d["y_train"])
m.test_model(d["X_test"], d["y_test"],"test")"""
#mf = ModelFacade()
#mf.
dsc = LoadProcessedDatasetCreator()
d = dsc.create_dataset("processed_data.dump","test")
m = model_factory.LoadModelFactory.create_model("test.pkl")
print(d)
print(m.classifier.predict(d["X_test"]))

print(m.predict(d["X_test"]))
#print(m.classifier.predict(single_instance))