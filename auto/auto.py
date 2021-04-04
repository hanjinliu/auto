import os
import glob
import time
import threading
import re
from .util import now, CasedFunction

try:
    from .controller import Controller
    USE_TK = True
except Exception:
    from .altcontroller import Controller
    USE_TK = False
    

class AutoAnalyzer:
    def __init__(self, path, recursive=False, include=None, exclude=None, 
                 dt=1, t_end=10*60*60, n_files=100):
        """
        Parameters
        ----------
        path : str
            Path to the directory that will contain files for analysis.
        recursive : bool, optional
            If recursively search for files, by default False
        include : str, optional [^1]
            Only files whose name matches this regular expression will be analyzed.
        exclude : str, optional [^1]
            All the files whose name matches this regular expression will be ignored.
        dt : float, optional
            All the files will be scanned every `dt` seconds, by default 1 seconds.
        t_end : float, optional
            After `t_end` seconds this program will stop, by default 10 hours.
        n_files : int, optional [^2]
            After `n_files` files are analyzed this program will stop, by default
            100 files.
        
        [^1]: These paramters are very important when input files and output files have
        the same extension (e.g. load a tif file, apply median filter, and save it as 
        tif file) because the newly saved file will be analyzed again.
        [^2]: This parameter is also important in case `include` and `exclude` are set
        inappropriately. n_files will be a `stopper` on this accident.
        """        
        
        self.path = path
        
        # prepare pattern matching function
        if include is None and exclude is None:
            matches = lambda s: True
        elif include is None and exclude is not None:
            reg_ex = re.compile(exclude)
            matches = lambda s: not reg_ex.match(s)
        elif include is not None and exclude is None:
            reg_in = re.compile(include)
            matches = lambda s: reg_in.match(s)
        else:
            reg_in = re.compile(include)
            reg_ex = re.compile(exclude)
            matches = lambda s: reg_in.match(s) and not reg_ex.match(s)
        
        # prepare searching function
        if recursive:
            glob_path = os.path.join(self.path, "**", "*")
            scan = lambda: (f for f in glob.glob(glob_path, recursive=True) 
                            if matches(os.path.basename(f)) and
                               os.path.isfile(f))
        else:
            glob_path = os.path.join(self.path, "*")
            scan = lambda: (f for f in glob.glob(glob_path) 
                            if matches(os.path.basename(f)) and
                               os.path.isfile(f))
        
        self.scan = scan
        self.dt = dt
        self.t_end = t_end
        self.n_files = n_files
        self.init()
        
    def __repr__(self):
        return "AutoAnalyzer at " + self.path
    
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
        
        if not USE_TK:
            self.run_without_tk(funcs)
            return None
        
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
    
    def run_without_tk(self,  funcs):
        """
        For Jython and some exceptions.
        """        
        self.init()
        self.loop = True
        self.function_dict = CasedFunction(funcs)
        self.controller = Controller(None)
        self._run_loop()
        
        return None
    
    def _run_loop(self):
        self._add_log("{} | start scanning.".format(now()))
        t0 = time.time()
        
        while self.loop:
            for f in self.scan():
                (f not in self.hist) and self._run(f)
            
                if time.time() - t0 > self.t_end:
                    print("Analysis time exceeded {} sec.".format(self.t_end))
                    print("For longer analysis, set t_end to larger value (10 hr by default).")
                    self.loop = False
                    break
                    
                if len(self.hist) > self.n_files:
                    print("Number of analyzed files exceeded {}".format(self.n_files))
                    print("For larger number, set n_files to larger value (100 by default).")
                    self.loop = False
                    break
            
            time.sleep(self.dt)    
        
        return None    
    
    def _add_log(self, content):
        self.log.append(content)
        self.controller.print_txt(self.log[-1])
        return None
    
    def _run(self, fp):
        _, ext = os.path.splitext(fp)
        func = self.function_dict[ext[1:]]
        if func is not None:
            self._add_log("{} | loaded: {}".format(now(), fp))
            self.hist.append(fp)
            try:
                self.last_ans = func(fp)    
            except Exception as e:
                err_cls = e.__class__.__name__
                self._add_log("{} | {}: {}".format(now(), err_cls, e))
            else:
                self._add_log("{} | finish: {}".format(now(), fp))
            
        return None

