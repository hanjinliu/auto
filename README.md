# Automation of Experimental Data Analysis

## Example in ImageJ

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