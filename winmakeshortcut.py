#!/usr/bin/env python3
#

import subprocess
import sys
from pathlib import Path

def powershell_run(cmd):
    proc = subprocess.run(["powershell", cmd], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    return proc.stdout.decode().strip(), proc.stderr.decode().strip()

class FileCreationError(Exception): pass

# https://learn.microsoft.com/en-us/troubleshoot/windows-client/admin-development/create-desktop-shortcut-with-wsh
def make_lnk(target:str|Path, location:str|Path, description:str=None, working_dir:str=None, arguments:str=None, icon_location:str=None, window_style:str|int=None, hot_key:str=None):
    r"""
    Create a Windows shortcut
    Reminder: all windows filepaths in your code should be "raw" strings, with an "r" in front, or have the \ escaped (doubled)
      very good:  data = r"C:\User\Path\image.jpg"
      also works: data = "C:\\User\Path\\image.jpg"
      very bad:   data = "C:\User\Path\image.jpg"

    Parameters
    ----------
    target : str
        The file path to the execuatable or url we should use
        Generally this would be the python executable or venv
        But could also be any file or url
        Example: r"C:\Path\python.exe"
        Example: r"C:\Path\notepad.exe"
        Example: r"C:\Path\catphoto.jpg"
        Example: "https://old.reddit.com/r/learnpython/new/"
    location : str
        Full path where the shortcut will be created. Must end with ``.lnk`` or ``.url``.
    description : str, optional
        Shortcut description text shown in the file properties.
    working_dir : str, optional
        The working directory to assign to the shortcut.
    arguments : str, optional
        The .py file you want to start, plus any other arguments to pass to the target when invoked.
    icon_location : str, optional
        Path to the icon file (or executable containing icons).
        Example: r"C:\Path\app.exe,0"
        Example: r"C:\Path\myicon.ico"
    window_style : int, optional
        Window display mode when launched. Common values:
            * 1 — normal window
            * 3 — maximized
            * 7 — minimized
    hot_key : str, optional
        Keyboard hotkey to associate with the shortcut
        Example: "Ctrl+Alt+F"

    Raises
    ------
    FileCreationError
    """
    if not str(location).endswith((".lnk", ".url")):
        raise FileCreationError("The shortcut pathname must end with .lnk or .url.")
    pscmd = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{location}');"
    pscmd += rf"$s.TargetPath='{target}';"
    if description:
        pscmd += rf"$s.Description='{description}';"
    if working_dir:
        pscmd += rf"$s.WorkingDirectory='{working_dir}';"
    if arguments:
        pscmd += rf"""$s.Arguments='"{arguments}"';"""
    if icon_location:
        pscmd += rf"$s.IconLocation='{icon_location}';"
    if window_style: # 1=normal; 3=maximized; 7=minimized
        pscmd += rf"$s.WindowStyle='{window_style}';"
    if hot_key:
        pscmd += rf"$s.Hotkey ='{hot_key}';"
    pscmd += r"$s.Save()"
    stdout, stderr = powershell_run(pscmd)
    if stderr:
        print(stderr)
        raise FileCreationError("Could not create shortcut file.")

def get_lnk_target(fp:Path):
    pscmd = f'(New-Object -ComObject WScript.Shell).CreateShortcut("{fp}").TargetPath'
    stdout, stderr = powershell_run(pscmd)
    if stderr:
        print(stderr)
        raise FileCreationError("Could not create shortcut file.")
    return stdout

def get_specialfolder(specialname):
    # https://learn.microsoft.com/en-us/dotnet/api/system.environment.specialfolder?view=net-10.0
    cmd = f"[Environment]::GetFolderPath([Environment+SpecialFolder]::{specialname})"
    stdout, stderr = powershell_run(cmd)
    if stderr:
        print("ERROR when looking for special folder", specialname)
    return stdout

def get_sendto():
    # shell:sendto
    # put a shortcut in this folder to add it to your right click menu under the "send to" flyout
    return get_specialfolder("Sendto")
def get_programs():
    # shell:programs (start menu)
    # put a shortcut here to add it to your start menu
    get_specialfolder("Programs")
def get_desktop():
     # shell:desktop (could be custom setting ie cloud)
    return get_specialfolder("Desktop")

def find_python():
    "finds the cli version of the currently running global or venv interpreter"
    target = sys.executable
    if target.endswith('pythonw.exe'):
        target = target.removesuffix('pythonw.exe') + 'python.exe'
    return target
def find_pythonw():
    "finds the windowless version of the currently running global or venv interpreter"
    target = sys.executable
    if target.endswith('python.exe'):
        target = target.removesuffix('python.exe') + 'pythonw.exe'
    return target

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
3) exit
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

if __name__ == "__main__":
    demomain()
