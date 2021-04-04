# Automation of Experimental Data Analysis

## Example in ImageJ

`Process` > `Filters` > `Median...`

```python
imp = IJ.openImage("C:/.../Image-1.tif");
IJ.run(imp, "Median...", "radius=5");
IJ.saveAs(imp, "Tiff", "C:/.../Med_Image-1.tif");
```

```python
import sys
sys.path.append(r"...\auto")
from auto import AutoAnalyzer, add_prefix
from ij import IJ

def run_median_filter(path):
    imp = IJ.openImage(path)
    IJ.run(imp, "Median...", "radius=5")
    IJ.saveAs(imp, "Tiff", add_prefix(path, "Med-"))

aa = AutoAnalyzer(r"...\your_directory", exclude="Med-.*")
aa.run({"tif": run_median_filter})
```