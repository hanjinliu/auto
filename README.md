# Automation of Experimental Data Analysis

## Automation in ImageJ

```python
imp = IJ.openImage("C:/.../Image-1.tif");
IJ.run(imp, "Median...", "radius=2");
IJ.saveAs(imp, "Tiff", "C:/.../Med_Image-1.tif");
```

```python
import sys
sys.path.append(r"...\auto")
from auto import AutoAnalyzer, add_prefix

def func(path):
    imp = IJ.openImage(path)
    IJ.run(imp, "Median...", "radius=2")
    IJ.saveAs(imp, "Tiff", add_prefix(path))

aa = AutoAnalyzer(filename="Image*.tif")
aa.run({"tif": func})

```