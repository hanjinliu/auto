import os
from datetime import datetime

def now():
    """
    Get current time in formatted string.
    """    
    return datetime.now().strftime(r"%Y/%m/%d %H:%M:%S")

def rename(path, newname):
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
    