import tkinter

class Controller:
    def __init__(self, funclist):
        self.root = tkinter.Tk()
        self.root.title("Controller")
        self.root.geometry("400x300")
        
        
        if not isinstance(funclist, list):
            funclist = [funclist]
        
        for i, f in enumerate(funclist):
            self.Button = tkinter.Button(text=f.__name__)
            self.Button.bind("<Button-{}>".format(i+1), f)
            self.Button.pack()

        
        self.txt_wid = tkinter.Text(self.root, wrap=tkinter.NONE)
        self.txt_wid.pack()

    def start(self):
        self.root.mainloop()
        
    def stop(self):
        self.root.destroy()
    
    def print_txt(self, txt):
        self.txt_wid.insert("end", txt + "\n")