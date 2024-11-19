from src.model import model_factory

m = model_factory.NewModelFactory.create_model("logistic_regression")
d = m.dataset_creator.create_train_test("shortAppGallery.csv")
m.train(d["X_train"], d["y_train"])
m.test_model(d["X_train"], d["y_train"],"test")
