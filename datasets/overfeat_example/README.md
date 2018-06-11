# Example Senario - Work in progess. Not ready yet

In this example, we use the [OverFeat CNN](https://github.com/sermanet/OverFeat) as a feature extraction tool and test 100  classifiers in parallel. 

For this example, The image data is assumed to be in different directories for each digit class.

``` bash
$ ls datasets/digit_example/
0	1	2	3	4	5	6	7	8	9
```

We now run OverFeat over all the data.

./gather_overfeat_feature path_to_data_classes 

This command will create a new file with the file extension .overfeat. 

```./sklearn_predict configuration_file``` will run through all models specified in the configure file and save off various metrics.


## Issues with the example

### Library not loaded
```
dyld: Library not loaded: /opt/local/lib/libgcc/libgomp.1.dylib
  Referenced from: OverFeat/bin/macos/overfeatcmd
  Reason: image not found
sh: line 1: 17388 Done                    convert samples/bee.jpg -resize 231x231^ ppm:-
     17389 Abort trap: 6           | OverFeat/bin/macos/overfeatcmd OverFeat/data/default/net_weight_0 6 0 19 
```
     
```
$ otool -L bin/macos/overfeatcmd
bin/macos/overfeatcmd:
    /System/Library/Frameworks/Accelerate.framework/Versions/A/Accelerate (compatibility version 1.0.0, current version 4.0.0)
    /opt/local/lib/libgcc/libstdc++.6.dylib (compatibility version 7.0.0, current version 7.18.0)
    /opt/local/lib/libgcc/libgomp.1.dylib (compatibility version 2.0.0, current version 2.0.0)
    /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1197.1.1)
    /opt/local/lib/libgcc/libgcc_s.1.dylib (compatibility version 1.0.0, current version 1.0.0)
```

Fix the reference to the GCC libraries:

```
  $ install_name_tool -change /opt/local/lib/libgcc/libgomp.1.dylib /usr/local/Cellar/gcc/8.1.0/lib/gcc/8/libgomp.1.dylib bin/macos/overfeatcmd
```
  
```
  $ install_name_tool -change /opt/local/lib/libgcc/libstdc++.6.dylib /usr/local/Cellar/gcc/8.1.0/lib/gcc/8/libstdc++.6.dylib bin/macos/overfeatcmd
```