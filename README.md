# kml_optimizer

## Overview

A python script written to compress a KML file. The code is set up to reduce the size of a KML file, while minimizing the loss of polygon shape quality in the file. This is really helpful to people such as GIS and BI Analysts facing KML file size constraints with their mapping and analytic tools. The script comes with three compression settings to help handle the different circumstances that often come up.

## Features
Runs on Linux, Mac and Windows machines.
The script is set up to automatically install all unmet prerequisite packages using pip.
This script will generated an optimized KML file in the optimized_data subdirectory.
The script comes with High, Medium, and Low sensitivity settings.
The script reduced the file size of the sample KML file from 3MB down to 2.5MB on the high setting
without sacrificing quality. A size reduction of 16.67%
Tested on Python 2.7 and 3.5

## How to Use
1. Make sure you have python 2 or 3 installed with pip on your machine
2. Clone the git repository
```R
git clone https://github.com/JECSand/kml_optimizer.git
```
3. cd into the kml_optimizer directory
4. Place the KML file you wish to optimize into the kml_data subdirectory
* Make sure it is formatted similarly as the sample one that came with the repo.
* I am working on it being easier with the formatting. Coming in a future update.
5. Run the script in a terminal/command prompt command with the following format:
```R
python kml_optimizer.py "kml_file" "sensitivity"
```
* "kml_file":
    * The name of the file in the kml_data directory you wish to optimized.
    * For the time being be mindful of the formatting of the files your bring in.
* "sensitivity":
    * The sensitivity setting of the process. The higher the setting, the more coordinate pairs will get cut.
    * Options are: Low, Medium, and High
6. Once the Process is complete, the optimized file will be found in the optimized_files subdirectory.

## Example
```R
python kml_optimizer.py "England local council overlay.kml" "high"
```

## Example Results
* On the highest setting the sample file's size was reduced by over 16% with no visible loss of quality.
* The before and after screen-shots shown below are essentially identical.

### Before Optimization: 3MB File Size
[![Screenshot_from_2017-10-21_03-22-22.png](https://s1.postimg.org/8jhs6y5m5b/Screenshot_from_2017-10-21_03-22-22.png)](https://postimg.org/image/53fgeuvz2z/)

### After Optimization: 2.5MB Files Size
[![Screenshot_from_2017-10-21_03-22-39.png](https://s1.postimg.org/6ouq6ny1vj/Screenshot_from_2017-10-21_03-22-39.png)](https://postimg.org/image/601gmnaiuz/)
