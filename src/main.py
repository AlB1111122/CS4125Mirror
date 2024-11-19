from preprocess import DatasetCreator

#m = model_factory.NewModelFactory.create_model("logistic_regression")
dc = DatasetCreator.CSVDatasetCreator()
print(dc.create_train_test("shortAppGallery.csv"))