#!/usr/bin/env python3
#

import sys
from pathlib import Path

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

"""
make a shortcut to your python program!
"""

import winmakeshortcut

CURRENT_PYTHON="Current python"
GLOBAL_PY = "Global py.exe"
e_packing = dict(padx=3, pady=3)
class MetaVar(ttk.LabelFrame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.set, self.get = self.var.set, self.var.get

class BrowseMixin:
    def initbtn(self, browse_func=None):
        self.browse_func = browse_func or filedialog.askopenfilename
        btn = ttk.Button(self, text="..", width=3, command=self.browse)
        btn.pack()
    def browse(self):
        fn = self.browse_func()
        if not fn:
            return # user cancelled
        self.var.set(fn)
        self.ent.xview_moveto(1.0)

class SimpleEntry(MetaVar):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ent = ttk.Entry(self,textvariable=self.var)
        self.ent.pack(side=tk.LEFT, fill=tk.X, expand=True)

class ComboFileEntry(MetaVar, BrowseMixin):
    def __init__(self, parent=None, browse_func=None, options:dict=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.options = options
        self.ent = ttk.Combobox(self,textvariable=self.var, values=options)
        self.ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.initbtn(browse_func)

class FileEntry(SimpleEntry, BrowseMixin):
    def __init__(self, parent=None, browse_func=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.initbtn(browse_func)

# LOCATIONS = "Desktop", "Sendto", "Start Menu"
LOCATIONS = {
    "Desktop":winmakeshortcut.get_desktop,
    "Sendto":winmakeshortcut.get_sendto,
    "Start Menu":winmakeshortcut.get_programs,
}

EXECUTABLES = {
f"{CURRENT_PYTHON} ({'.'.join(map(str,sys.version_info[:2]))})":sys.executable,
}

for ver in winmakeshortcut.findall_py_versions():
    EXECUTABLES[f"{GLOBAL_PY} ({ver})"] = ver

class Main(tk.Frame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.name = SimpleEntry(self, text="Shortcut Name")
        self.name.pack(fill=tk.X, **e_packing)

        self.desc = SimpleEntry(self, text="Shortcut Tooltip (optional)")
        self.desc.pack(fill=tk.X, **e_packing)

        self.location = ComboFileEntry(self, text="Save Location",
            options = list(LOCATIONS),
            browse_func=filedialog.askdirectory)
        self.location.pack(fill=tk.X, **e_packing)

        self.target = ComboFileEntry(self, text="Python Executable", options=list(EXECUTABLES))
        self.target.pack(fill=tk.X, **e_packing)

        self.argument = FileEntry(self, text="Python file")
        if len(sys.argv) > 1:
            self.argument.set(sys.argv[1])
        self.argument.pack(fill=tk.X, **e_packing)

        self.runtype = MetaVar(self, text="Run type")
        self.runtype.var.set("CLI") # set defualt
        rb = tk.Radiobutton(self.runtype, text="CLI (command line window)", variable=self.runtype.var, value="CLI")
        rb.pack(anchor=tk.W)
        rb = tk.Radiobutton(self.runtype, text="GUI window (no command line)", variable=self.runtype.var, value="GUI")
        rb.pack(anchor=tk.W)
        self.runtype.pack(fill=tk.X, **e_packing)

        self.iconfile = FileEntry(self, text="Icon file (optional)")
        self.iconfile.pack(fill=tk.X, **e_packing)

        btn = ttk.Button(self, text="Make shortcut!", command=self.on_gotime)
        btn.pack()

    def on_gotime(self):
        if not (name := self.name.get()):
            return messagebox.showerror("Error", "Name is required")
        if not (loc := self.location.get()):
            return messagebox.showerror("Error", "Location is required")
        if not (tar := self.target.get()):
            return messagebox.showerror("Error", "Executable is required")

        if loc in LOCATIONS:
            loc = LOCATIONS[loc]()
        location = Path(loc) / f"{name}.lnk"

        if tar.startswith(CURRENT_PYTHON):
            tar = EXECUTABLES[tar]
        elif tar.startswith(GLOBAL_PY):
            tar = winmakeshortcut.get_py_executable(tar)
            assert tar.endswith("python.exe")

        if tar.endswith("python.exe") and self.runtype.get() == "GUI":
            tar = tar.removesuffix('python.exe') + 'pythonw.exe'
        elif tar.endswith("pythonw.exe") and self.runtype.get() == "CLI":
            tar = tar.removesuffix('pythonw.exe') + 'python.exe'

        winmakeshortcut.make_lnk(
            target=tar,
            location=location,
            description=self.desc.get() or None,
            working_dir=location.parent,
            arguments=self.argument.get() or None,
        )
        self.exit()

def main():
    root = tk.Tk()
    win = Main(root)
    win.pack(fill=tk.BOTH)
    root.mainloop()

if __name__ == "__main__":
    main()
