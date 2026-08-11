A similar project to [pyshortcut](https://github.com/newville/pyshortcuts), but I made it before I knew that one existed.

Main differences: This project has no external dependencies, and this project uses powershell commands internally to do the work instead of win API calls.

# Make Windows shortcuts to your python programs!

## Option 1: <br>
Run the makeshortcut_GUI.pyw file to make the shortcut. NOTE: It helps if you run from the same python venv or executable that you want to use to run the program in the future.

![Blank](./imgs/scrshot.png)

Fill in the fields. Note that you can and should specify a venv to use, if you are using a venv (and you probably should be).


## Option 2: <br>
Include an option inside your program to make the shortcut. For example:
```python
from makeshortcut import make_lnk

resp = input("What do you want to do? > ")
if resp == "shortcut":
    # make a desktop shortcut that runs this file in a command line window
    make_lnk(
        target = find_python(), # get the version of python currently being used
        location = get_desktop() + r"\awesomeprogram.lnk", # put the shortcut on the desktop
        arguments = __file__, # start this current file from the shortcut
        )
```
