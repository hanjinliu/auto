import tkinter

DARK = "#2C2B29"
GREEN = "#3FFC0C"

class Controller:
    def __init__(self, funclist):
        self.root = tkinter.Tk()
        self.root.configure(bg=DARK)
        self.root.title("Controller")
        self.root.geometry("400x300")
        
        if not isinstance(funclist, list):
            funclist = [funclist]
        
        for i, f in enumerate(funclist):
            self.Button = tkinter.Button(text=f.__name__, bg=DARK, fg=GREEN, font=("Consolas",))
            self.Button.bind("<Button-{}>".format(i+1), f)
            self.Button.pack()

        self.frame = tkinter.Frame(bg=DARK)
        self.frame.pack()

        self.txt_wid = tkinter.Text(self.frame, wrap=tkinter.NONE, bg=DARK, fg=GREEN, font=("Consolas", 10))
        
        
        self.scrollbarx = tkinter.Scrollbar(self.frame, orient=tkinter.HORIZONTAL, command=self.txt_wid.xview)
        self.scrollbarx.pack(side=tkinter.BOTTOM, fill="x")
        self.scrollbary = tkinter.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.txt_wid.yview)
        self.scrollbary.pack(side=tkinter.RIGHT, fill="y")
        
        self.txt_wid["xscrollcommand"] = self.scrollbarx.set
        self.txt_wid["yscrollcommand"] = self.scrollbary.set
        self.txt_wid.pack()
        

    def start(self):
        self.root.mainloop()
        
    def stop(self):
        self.root.destroy()
    
    def print_txt(self, txt):
        self.txt_wid.insert("end", txt + "\n")