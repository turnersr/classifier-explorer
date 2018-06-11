# Classifier Explorer
This repo is a set of tools for assessing the performance of a wide range of classifiers and their parameters in parallel using scikit-learn.

# Usage
If you have a classification problem and a need to test a variety of classifiers and their parameters in parallel without much setup, then this is the tool.

```python3 scikit-learn_predict configuration_file.yaml``` is the main function and configure_file.yaml specifies all models and parameter ranges to use. It will evaluate models in parallel. This program will save all trained models as well as the results of 10 different classification metrics. An example configuration file is given in model.yaml .


# Quick start

assuming your observations are datasets/X.npy and targets saved in datasets/y.np, then
```
python3 scikit-learn_predict model.yaml
```

will work and save the trained models in ```model_files/``` and the classification performance data in ```model_metrics```

```python3 model_evaluation/classification_report.py model_metrics/``` will give an overview of performance. 

     
# Historical Notes
This initially grew out of a project for predicting housing prices using Google Street view data and [OverFeat CNN](https://github.com/sermanet/OverFeat), but the data-mangling and old code has been removed. It can be referred to in the git history. The initial motivation for this library can be found at https://nsauder.github.io/streetscope/. The project also used to be called cnn_pipeline but the name changed, too.
