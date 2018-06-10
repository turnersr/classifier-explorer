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


# Issues

```Image does not have 8-bits components```

## Library not loaded
```dyld: Library not loaded: /opt/local/lib/libgcc/libgomp.1.dylib
  Referenced from: OverFeat/bin/macos/overfeatcmd
  Reason: image not found
sh: line 1: 17388 Done                    convert samples/bee.jpg -resize 231x231^ ppm:-
     17389 Abort trap: 6           | OverFeat/bin/macos/overfeatcmd OverFeat/data/default/net_weight_0 6 0 19 ```
     
     ```$ otool -L bin/macos/overfeatcmd
bin/macos/overfeatcmd:
	/System/Library/Frameworks/Accelerate.framework/Versions/A/Accelerate (compatibility version 1.0.0, current version 4.0.0)
	/opt/local/lib/libgcc/libstdc++.6.dylib (compatibility version 7.0.0, current version 7.18.0)
	/opt/local/lib/libgcc/libgomp.1.dylib (compatibility version 2.0.0, current version 2.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1197.1.1)
	/opt/local/lib/libgcc/libgcc_s.1.dylib (compatibility version 1.0.0, current version 1.0.0)```
  
  ```$ install_name_tool -change /opt/local/lib/libgcc/libgomp.1.dylib /usr/local/Cellar/gcc/8.1.0/lib/gcc/8/libgomp.1.dylib bin/macos/overfeatcmd```
  
  ```$ install_name_tool -change /opt/local/lib/libgcc/libstdc++.6.dylib /usr/local/Cellar/gcc/8.1.0/lib/gcc/8/libstdc++.6.dylib bin/macos/overfeatcmd``
     
     
