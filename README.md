# Automation of Experimental Data Analysis

Although many automatic analysis tools are available now, we still at least need to run analysis manually. This module provides tools for automatic detection of newly generated files  and sending each file to the function(s) you want to run.

## Basic Usage

```python
# Import analyzer
from auto import AutoAnalyzer

# Define functions
def txt_func(x):
    "What you want to do with the txt file in the path `x`."

def csv_func(x):
    "What you want to do with the csv file in the path `x`."

# Define an analyzer
aa = AutoAnalyzer(r"...\your_directory")

# Bind functions to corresponding extensions
aa.run({"txt": txt_func, "csv": csv_func})
```

## Example Usage in ImageJ

In Fiji, you can record analysis procedure in a Python script (Plugins > Macros > Record...).

Here's a sample script recorded by opening an image, applying median filter (Process > Filters > Median...) and saving in the same directory.

```python
imp = IJ.openImage("C:/.../Image-1.tif");
IJ.run(imp, "Median...", "radius=5");
IJ.saveAs(imp, "Tiff", "C:/.../Med_Image-1.tif");
```
From this record you can automate analysis.

```python
import sys
sys.path.append(r"...\auto") # path to this module
from auto import AutoAnalyzer, add_prefix
from ij import IJ

# This function 
def run_median_filter(path):
    # Open an image
    imp = IJ.openImage(path)
    # Run median filter
    IJ.run(imp, "Median...", "radius=5")
    # Add prefix 'Med-' and save it.
    IJ.saveAs(imp, "Tiff", add_prefix(path, "Med-"))

# Newly generated tif files must be excluded to avoid duplicated 
# analysis. Here we pass regular expression "Med-.*" to exclude
# files whose names start with "Med-".
aa = AutoAnalyzer(r"...\your_directory", exclude="Med-.*")

# Run median filter only for tif files.
aa.run({"tif": run_median_filter})
```

To stop analyzer you need to push "kill" button to interrupt.

## Example Usage in CPython

CPython provides much abundant libraries than Jython, such as `pandas`, `scikit-learn`, `matplotlib` etc., so that you can do more sophisticated analysis and draw beautiful figures. Here in this module, `Tkinter` based GUI is also available with the same script.

```python
from auto import AutoAnalyzer, add_suffix, change_ext
import pandas as pd
import matplotlib.pyplot as plt

def save_hist(path):
    # Prepare a figure
    fig = plt.figure()
    # Read a csv file
    df = pd.read_csv(path, header=None)
    # Draw a histogram
    plt.hist(df[0], bins=25, density=True)
    # Write labels
    plt.xlabel("F.I. (a.u.)")
    plt.ylabel("freq")
    # Save the figure
    fig.savefig(change_ext(path, "png"))

aa = AutoAnalyzer(r"...\your_directory")
aa.run({"csv": save_hist}) # GUI is called.
```

## Details of AutoAnalyzer

```python
AutoAnalyzer(self, path, recursive=False, include=None, exclude=None, dt=1, t_end=10*60*60, n_files=100)
```

*arguments*
- `path` : str
  Path to the directory that will contain files for analysis.

*keyward arguments*
- `recursive` : bool, optional
  If recursively search for files, by default False
- `include` : str, optional
  Only files whose name matches this regular expression will be analyzed.
- `exclude` : str, optional
  All the files whose name matches this regular expression will be ignored.
- `dt` : float, optional
  All the files will be scanned every `dt` seconds, by default 1 seconds.
- `t_end` : float, optional
  After `t_end` seconds this program will stop, by default 10 hours.
- `n_files` : int, optional
  After `n_files` files are analyzed this program will stop, by default 100 files.

## Other Utility Functions

- `add_prefix(path, prefix="E-")`
  e.g.) `add_prefix(".../XX.tif", "Pre")` &rarr; `".../PreXX.tif"`
- `add_suffix(path, suffix="-0")`
  e.g.) `add_suffix(".../XX.tif", "Suf")` &rarr; `".../XXSuf.tif"`
- `add_directory(path, newdir="Results")`
  e.g.) `add_directory(".../XX.tif", "NewDir")` &rarr; `".../NewDir/XXS.tif"`
- `rename(path, newname)`
  e.g.) `rename(".../XX.tif", "YY.tif")` &rarr; `".../YY.tif"`
- `change_ext(path, new_ext="txt")`
  e.g.) `change_ext(".../XX.tif", "csv")` &rarr; `".../XX.csv"`