import tkinter as tk
from tkinter import messagebox

def gen_root():
    return tk.Tk()

class Window():
    
    def __init__(self, root:object, title:str, geometry:str, resizable:bool):
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(resizable, resizable)

class Window_Item():
    
    def __init__(self, placement_args:dict, keybind_func = None):
        if keybind_func: self.item.bind('<KeyPress>', keybind_func)
        self.item.grid(placement_args)

    def config(self, args:dict) -> object:
        self.item.config(args)
        return self.item
    
    def get(self) -> str|bool:
        return self.item.get()
    
    def clear(self) -> object:
        self.item.delete(0, tk.END)
        return self.item

class Button(Window_Item):
    
    def __init__(self, master:Window, item_args:dict, placement_args:dict, keybind_func=None):
        self.item = tk.Button(master.root, item_args)  
        super().__init__(placement_args, keybind_func)

    #Overrides the class get
    def get(self, *args, **kwargs):
        raise AttributeError("Button has no get function")

class Text_Box(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args:dict, keybind_func=None):
        self.item = tk.Text(master.root, item_args)
        super().__init__(placement_args, keybind_func)

class Entry_Box(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args:dict, keybind_func=None):
        self.item = tk.Entry(master.root, item_args)
        super().__init__(placement_args, keybind_func)

class Check_Box(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args: dict, keybind_func=None):
        self.item = tk.Checkbutton(master.root, item_args)
        super().__init__(placement_args, keybind_func)

class Label(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args: dict, keybind_func=None):
        self.item = tk.Label(master.root, item_args)
        super().__init__(placement_args, keybind_func)


class Error_Message():
    def __init__(self, title:str, message:str):
        self.message = messagebox.showerror(title, message)

class Menu():
    
    _cls_top_level_master = None
    
    def __init__(self, master:object, tearoff:bool|int = 0):
        self.root = tk.Menu(master=master.root, tearoff=tearoff)
        
        if Menu._cls_top_level_master == None:
            Menu._cls_top_level_master = master.root
            master.root.config(menu = self.root)

    def add_child(self, child:object, label:str|None = None):
        submenu = self.root.add_cascade(menu = child.root, label = label)
        return submenu

    def add_command(self, menu_args:dict):
        command = self.root.add_command(menu_args)
        return command

    def add_seperator(self):
        separator = self.root.add_separator()
        return separator