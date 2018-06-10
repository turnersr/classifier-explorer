# cnn_pipeline
This repo is a set of tools for working with the [OverFeat CNN](https://github.com/sermanet/OverFeat) and scikit-learn to accomplish machine learning tasks. 

This project as initially grew out of a project for predicting housing prices using Google Street view data, but the data-mangling and old code has been removed. It can be referred to in the git history.

# Usage
The main application is based on the scenario where one has a classification problem and would like to use the [OverFeat CNN](https://github.com/sermanet/OverFeat) as a feature extraction tool. 

The image data is assumed to be in different directories for each class. This example we are going to classify digits:

``` bash
class_0 class_1 class_2 class_3 class_4 class_5 class_6 class_7 class_8 class_9
```

We now run OverFeat over all the data.

./gather_overfeat_feature path_to_data_classes 

This command will create a new file with the file extension .overfeat. 

```
ls path_to_data_classes/class_0 
```

```./sklearn_predict configuration_file``` will run through all models specified in the configure file and save off various metrics.
