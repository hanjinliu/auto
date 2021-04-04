import os
import glob
import time
from datetime import datetime
import threading
try:
    from .controller import Controller
except Exception:
    from .altcontroller import Controller


def now():
    """
    Get current time in formatted string.
    """    
    return datetime.now().strftime(r"%Y/%m/%d %H:%M:%S")

def none_func(*args, **kwargs):
    return None

class CasedFunction:
    def __init__(self, d, default_key="*"):
        """
        Parameters
        ----------
        d : dict or callable
            Make 'key -> callable' dictionary
        """
        self.default_key = default_key
        
        if isinstance(d, dict):
            self.funcs = d
        else:
            raise TypeError
        
        if default_key not in self.funcs.keys():
            self.funcs[default_key] = none_func

        # check if callable
        for k, f in self.funcs.items():
            if not isinstance(k, str):
                raise TypeError("non-string object in key: {}".format(k))
            if not callable(f):
                raise TypeError("non-callable object contained: {}".format(f))
    
    def __getitem__(self, key):
        if key not in self.funcs.keys():
            key = self.default_key
        return self.funcs[key]


class AutoAnalyzer:
    def __init__(self, path, recursive=False, filename="*", dt=10, t_end=10800):
        """
        Parameters
        ----------
        path : str
            Path to the directory that will contain files for analysis.
        recursive : bool, optional
            If recursively search for files, by default False
        filename : str, optional
            Filename to analyze. You can also use wildcard "*" (e.g. if `filename` 
            is "*-nM-Protein.*" then both "10-nM-Protein.tif" and "50-nM-Protein.png"
            will match but "DNA.txt" will not).
            This paramter is very important when input files and output files have the 
            same extension (e.g. load a tif file, apply median filter, and save it as 
            tif file) because the newly saved file will be analyzed again.
            By default "*".
        dt : float, optional
            All the files will be scanned every `dt` seconds, by default 10.
        t_end : float, optional
            After `t_end` seconds this program will stop, by default 10800.
        """        
        
        self.path = path
        
        if recursive:
            glob_path = os.path.join(self.path, "**", filename)
            scan = lambda: glob.glob(glob_path, recursive=self.recursive)
        else:
            glob_path = os.path.join(self.path, filename)
            scan = lambda: glob.glob(glob_path)
        self.scan = scan
        self.recursive = recursive
        self.dt = dt
        self.t_end = t_end
        self.init()
    
    def init(self):
        """
        Initialize the inner state of the analyzer.
        """        
        self.hist = [] # already analyzed file paths
        self.last_ans = None
        self.log = []
        self.loop = False
        self.function_dict = None # ext -> function
        self.controller = None
        return None
        
    def run(self, funcs):
        """
        Start auto-analysis.

        Parameters
        ----------
        funcs : dict(str->callable)
            To specify what function will be called for each extension. For
            example, `funcs={"tif": tif_func, "txt": txt_func}` means that
            for path=".../XX.tif", `tif_func(path)` will be called and for 
            path=".../YY.txt", `txt_func(path)` will be called.
        """        
        
        th_run = threading.Thread(target=self._run_loop)
        
        def stop(arg):
            self.loop = False
            self.controller.stop()
            th_run.join()
            
        self.init()
        self.loop = True
        self.function_dict = CasedFunction(funcs)
        self.controller = Controller(stop)
        
        
        th_run.start()
        self.controller.start()
        
        return None
    
    def run2(self,  funcs):
        self.init()
        self.loop = True
        self.function_dict = CasedFunction(funcs)
        self.controller = Controller(None)
        self._run_loop()
        
        return None
    
    def _run_loop(self):
        self.add_log("{} | start scanning.".format(now()))
        t0 = time.time()
        while self.loop and time.time() - t0 < self.t_end:
            for f in self.scan():
                (f not in self.hist) and self._run(f)
            time.sleep(self.dt)
        
        return None
    
    
    def add_log(self, content):
        self.log.append(content)
        self.controller.print_txt(self.log[-1])
        return None
    
    def _run(self, fp):
        self.add_log("{} | start: {}".format(now(), fp))
        
        _, ext = os.path.splitext(fp)
        func = self.function_dict[ext[1:]]
        func is not none_func and self.hist.append(fp)
        self.last_ans = func(fp)
        
        self.add_log("{} | finish: {}".format(now(), fp))
        return None

