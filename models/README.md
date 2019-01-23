### Review the examples in the **eb_12_v07** directories.

In particular, the configuration in **res.js**, which controls the scope.

Note that **res.js** is not simple JSON.


# Usage:

Open a console in the models directory and run one of the following commands as required.<br>

```
python build_config.py
```
_Summary_
1. Read configuration
2. **Create missing directories and files.**
3. Scan the ground truth, reading XML files, and write a "data.csv" file.
4. Select training and evaluation data, and write "train.csv" and "eval.csv" files.

Edit the file "res.js" to control what scalings and tilings are produced.
<br>
<br>


```
python build_data.py
```
_Summary_
1. Read configuration
2. Read "train.csv" and "eval.csv" files.
3. Build scalings and tilings.

Review the results in **LabelImg**.
<br>
<br>


```
python build_records.py
```
_Summary_
1. Read configuration
2. Build TensorFlow records for "eval" and "train"
<br>
<br>

