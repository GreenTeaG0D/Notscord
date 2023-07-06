import tkinter as tk
import GUI_Constructor as GC
from GUI_Constructor import *

root = tk.Tk()

window = GC.Window(root, 'Page Title', '600x500', True)

E_Username = GC.Entry_Box(window, {}, {'row':0, 'column':0}, None)
E_Password = GC.Entry_Box(window, {'show':'*'}, {'row':0, 'column':1}, None)
B_Submit = GC.Button(window, {'command':None, 'text':'Submit'}, {'row':0, 'column':2}, None)
B_Submit = GC.Button(window, {'command':exit(1), 'text':'Close'}, {'row':1, 'column':2}, None)