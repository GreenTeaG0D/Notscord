import tkinter as tk
import GUI_Constructor as GC
from GUI_Constructor import *
import webbrowser


def pull_entries():
    Username = E_Username.get()
    Password = E_Password.get()
    print(Username, Password)


root = tk.Tk()
window = GC.Window(root, 'Page Title', '600x500', True)
E_Username = GC.Entry_Box(window, {}, {'column':0, 'row':0, 'columnspan':2})
E_Password = GC.Entry_Box(window, {'show':'*'}, {'column':0, 'row':1, 'columnspan':2})
B_Submit = GC.Button(window, {'command':pull_entries, 'text':'Submit'}, {'column':0, 'row':2})
B_Submit = GC.Button(window, {'command':exit, 'text':'Close'}, {'column':1, 'row':2})

def open_help_website():
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUjcmljayBhc3RsZXkgbmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXA%3D')

menubar = GC.Menu(window)
help_menu = GC.Menu(menubar)
menubar.add_child(help_menu, 'Help')
help_menu.add_command({'label':'Website', 'command':open_help_website})
help_menu.add_seperator()

# root.config(menu = menubar.root)
root.mainloop()