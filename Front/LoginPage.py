import GUI_Constructor as GC
from GUI_Constructor import *
import Webrequests as WR
from Webrequests import *
import webbrowser
import re

def KB_Username(event):
    # Username must be between 8 and 32 characters long
    length = len(E_Username.get())
    if length < 7:
        L_Valid_Username.config({'text':7 - length, 'fg':'red'})
    elif length > 31:
        L_Valid_Username.config({'text':31 - length, 'fg':'red'})
    else:
        L_Valid_Username.config({'text':'Valid Username', 'fg':'green'})

def KB_Password(event):
    # Password must be between 8 and 32 characters long
    password = E_Password.get()
    char = event.keysym
    
    if len(char) == 1:
        password += char
    elif char == 'BackSpace':
        password = password[:-1]
        
    length = len(password)
    
    if length < 8:
        L_Valid_Password.config({'text':f'Too Short, +{8 - length}', 'fg':'red'})
    elif length > 32:
        L_Valid_Password.config({'text':f'Too Long, {32 - length}', 'fg':'red'})
        
    else:
        password_required_values = ['!']
        missing_requirements = []
        flag = False
        for requirement in password_required_values:
            if requirement not in password:
                missing_requirements.append(requirement)
                flag = True
        if flag:
            L_Valid_Password.config({'text':f'Length Valid but missing {missing_requirements}', 'fg':'red'})
        else:
            L_Valid_Password.config({'text':'Valid Password', 'fg':'green'})


def KB_Email(event):
    # Email must fulfil regex
    regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    if re.fullmatch(regex, E_Email.get()):
        L_Valid_Email.config({'text':'Valid Email', 'fg':'green'})
    
root = GC.gen_root()
window = GC.Window(root, 'Page Title', '600x500', True)

L_Username = GC.Label(window, {'text':'Username:'}, {'column':0, 'row':0, 'columnspan':1})
E_Username = GC.Entry_Box(window, {}, {'column':1, 'row':0, 'columnspan':2}, KB_Username)
L_Valid_Username = GC.Label(window, {}, {'column':3, 'row':0})

L_Password = GC.Label(window, {'text':'Password:'}, {'column':0, 'row':1, 'columnspan':1})
E_Password = GC.Entry_Box(window, {'show':'*'}, {'column':1, 'row':1, 'columnspan':2}, KB_Password)
L_Valid_Password = GC.Label(window, {}, {'column':3, 'row':1})

L_Email = GC.Label(window, {'text':'Email:'}, {'column':0, 'row':2, 'columnspan':1})
E_Email = GC.Entry_Box(window, {}, {'column':1, 'row':2, 'columnspan':2}, KB_Email)
L_Valid_Email = GC.Label(window, {}, {'column':3, 'row':2})

B_Submit = GC.Button(window, {'command':None, 'text':'Submit'}, {'column':1, 'row':3})
B_Close = GC.Button(window, {'command':exit, 'text':'Close'}, {'column':2, 'row':3})





##~~ MENUBAR ~~##

def open_help_website():
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUjcmljayBhc3RsZXkgbmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXA%3D')

menubar = GC.Menu(window)
help_menu = GC.Menu(menubar)
menubar.add_child(help_menu, 'Help')
help_menu.add_command({'label':'Website', 'command':open_help_website})
help_menu.add_command({'label':'Nothing'})

root.mainloop()