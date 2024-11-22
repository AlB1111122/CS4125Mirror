import argparse
from src.model import model_factory


def main():
    parser = argparse.ArgumentParser(description='CLI for EmailClassifier')
    parser.add_argument('--dataset', type=str, help='Name of the dataset to use')
    parser.add_argument('--model', type=str, help='Name of the model to use')
    
    args = parser.parse_args()

    m = model_factory.NewModelFactory.create_model(args.model)
    d = m.dataset_creator.create_train_test(args.dataset)
    m.train(d["X_train"], d["y_train"])
    m.test_model(d["X_train"], d["y_train"],"test")

if __name__ == "__main__":
    main()