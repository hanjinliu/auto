# for Jython

class Controller:
    
    def __init__(self, arg):
        pass
    
    def start(self):
        self.exitflag = False
    
    def stop(self):
        self.exitflag = True
    
    def print_txt(self, txt):
        print(txt)