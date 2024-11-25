# User Guide
The user interacts with the email classifier through a command line interface.
The cli is mostly selecting numbers that correspond to options but, at some points a user will be asked to give names to files and the like.
When the user starts the CLI they are presented with the options: 
```
1)Create new model  
2)Load model from storage   
3)Save current model   
4)Get dataset   
5)Use model  
6)Save current dataset   
q)To quit  
```
1. Create new model: this option allows a user to create a new, untrained model from the list of supported model types.
2. Load model from storage: allows a user to use a model that was previously created and trained, and stored for future use. The models are loaded from the /saves/models directory.
3. Save current model: save the model you are currently working with so its training can be leveraged for future use.
4. Get dataset: allows a user to create a new dataset for training from a csv file, or load a previously processed and saved dataset. They can select a csv file that has already been entered into the system or give it a new one by passing in an absolute path to the file. The user can make a dataset stable for 1 usage at a time (training, testing, or predicting, called single usage, it can be used multipule times, its just not suitable for the ```3)Train and test``` in the model usage ) or training and testing together.
5. Use model: the user is prompted ```1)Train 2)Test 3)Train and test 4)Predict``` which uses the selected model, and dataset to perform the selected action.
    + when predicting, the model will print the labels it predicts for each data element it is given from the datset
    + when training a results .txt file will be created in the test_results directory,
6. Save current dataset: as it takes a long time to translate the data so a user may want to save a dataset to load it later, they will be asked to name the file


