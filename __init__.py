#!/usr/bin/env python3
#

import platform

class SystemNotSupported(Exception): pass

if platform.system() == "Windows":
    from winmakeshortcut import *
else:
    raise SystemNotSupported("Sorry, Windows only at the moment.")

### examples ###
def demo1():
    # make a desktop shortcut that runs this file in a command line window
    make_lnk(
        target = find_python(), # get the version of python currently being used
        location = get_desktop() + r"\awesomeprogram.lnk", # put the shortcut on the desktop
        arguments = __file__, # start this current file from the shortcut
        )

def demo3():
    # make a desktop shortcut to /r/learnpython
    make_lnk(
        target = "https://old.reddit.com/r/learnpython/new/",
        location = get_desktop() + r"\Get Python Help.url", # put the shortcut on the desktop
        )

democlimenu = """\
welcome to the shortcut creator
1) make desktop shortcut to this program in cli
2) start gui
3) make desktop shortcut to /r/learnpython
4) exit
"""
def demomain():
    if len(sys.argv) > 1:
        resp = sys.argv[1]
    else:
        print(democlimenu)
        resp = input("What do you want to do? > ")
    match resp:
        case "1":
            demo1()
        case "3":
            demo3()
        case "4":
            return

if __name__ == "__main__":
    demomain()
