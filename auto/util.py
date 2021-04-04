import os
from datetime import datetime

def now():
    """
    Get current time in formatted string.
    """    
    return datetime.now().strftime(r"%Y/%m/%d %H:%M:%S")

def rename(path, newname):
    """
    Totally rename file.
    """    
    dname = os.path.dirname(path)
    return os.path.join(dname, newname)

def add_prefix(path, prefix="E-"):
    """
    Add prefix to the filename.
    add_prefix(".../XX.tif", "Pre") returns ".../PreXX.tif"
    """    
    fname = os.path.basename(path)
    dname = os.path.dirname(path)
    return os.path.join(dname, prefix + fname)

def add_suffix(path, suffix="-0"):
    """
    Add suffix to the filename.
    add_suffix(".../XX.tif", "Suf") returns ".../XXSuf.tif"
    """    
    fname, ext = os.path.splitext(os.path.basename(path))
    dname = os.path.dirname(path)
    return os.path.join(dname, fname + suffix + ext)

def add_directory(path, newdir="Results"):
    """
    Add a directory to the path. If that directory does not exist,
    then new directory will be made.
    add_directory(".../XX.tif", "NewDir") returns ".../NewDir/XXS.tif"
    """    
    fname = os.path.basename(path)
    dname = os.path.dirname(path)
    new_dname = os.path.join(dname, newdir)
    if not os.path.exists(new_dname):
        os.makedirs(new_dname, exist_ok=False)
    return os.path.join(new_dname, fname)

def change_ext(path, new_ext="txt"):
    """
    Change extension.
    change_ext(".../XX.tif", "csv") returns ".../XX.csv"
    """
    name, ext = os.path.splitext(path)
    if not new_ext.startswith("."):
        new_ext = "." + new_ext
    return name + new_ext


class CasedFunction:
    def __init__(self, d):
        """
        Parameters
        ----------
        d : dict or callable
            Make 'key -> callable' dictionary
        """
        
        if isinstance(d, dict):
            self.funcs = d
        else:
            raise TypeError

        # check if callable
        for k, f in self.funcs.items():
            if not isinstance(k, str):
                raise TypeError("non-string object in key: {}".format(k))
            if not callable(f):
                raise TypeError("non-callable object contained: {}".format(f))
    
    def __getitem__(self, key):
        return self.funcs.get(key, None)
    