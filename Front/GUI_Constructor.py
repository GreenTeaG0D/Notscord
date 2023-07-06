import tkinter as tk

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

    def config(self, args:dict):
        self.item.config(args)
        return self.item
    
    def get(self, start:str|float|None = None, end:str|float|None = None):
        return self.item.get(start, end)

class Button(Window_Item):
    
    def __init__(self, master:Window, item_args:dict, placement_args:dict, keybind_func=None):
        super().__init__(placement_args, keybind_func)
        self.item = tk.Button(master.root, self.item_args)  

    #Overrides the class get
    def get(self, *args, **kwargs):
        raise AttributeError("Button has no get function")

class Text_Box(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args:dict, keybind_func=None):
        self.item = tk.Text(master.root, item_args)
        super().__init__(placement_args, keybind_func)

class Entry_Box(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args:dict, keybind_func=None):
        self.item = tk.Entry(master.root, self.item_args)
        super().__init__(item_args, placement_args, keybind_func)

class Check_Box(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args: dict, keybind_func=None):
        self.item = tk.Checkbutton(master.root, item_args)
        super().__init__(placement_args, keybind_func)

class Label(Window_Item):
    def __init__(self, master:Window, item_args:dict, placement_args: dict, keybind_func=None):
        self.item = tk.Label(master.root, item_args)
        super().__init__(placement_args, keybind_func)


class Menu():
    def __init__(self, master:object, tearoff:bool|int = 0):
        self.menu = tk.Menu(master=master, tearoff=tearoff)
        if master == tk.Tk:
            master.config(menu = self.menu)

    def add_child(self, child:object, label:str):
        submenu = self.menu.add_cascade(menu = child, label = label)
        return submenu

    def add_command(self, menu_args:dict|None = None):
        command = self.menu.add_command(menu_args)
        return command

    def add_seperator(self):
        separator = self.menu.add_separator()
        return separator