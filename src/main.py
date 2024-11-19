from preprocess import preprocessor
from model import model_factory

p = preprocessor.Preprocessor()
data = p.process("shortAppGallery.csv")

m = model_factory.NewModelFactory.create_model("logistic_regression")
train = m.model_data(data)
m.train(train["X_train"],train["y_train"])
m.test_model(train["X_test"],train["y_test"], "classModelTest.txt")