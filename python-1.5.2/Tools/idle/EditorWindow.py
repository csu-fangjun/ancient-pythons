import sys
import os
import string
import re
import imp
from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import idlever
import WindowList

# File menu

#$ event <<open-module>>
#$ win <Alt-m>
#$ unix <Control-x><Control-m>

#$ event <<open-class-browser>>
#$ win <Alt-c>
#$ unix <Control-x><Control-b>

#$ event <<open-path-browser>>

#$ event <<close-window>>
#$ unix <Control-x><Control-0>
#$ unix <Control-x><Key-0>
#$ win <Alt-F4>

# Edit menu

#$ event <<Copy>>
#$ win <Control-c>
#$ unix <Alt-w>

#$ event <<Cut>>
#$ win <Control-x>
#$ unix <Control-w>

#$ event <<Paste>>
#$ win <Control-v>
#$ unix <Control-y>

#$ event <<select-all>>
#$ win <Alt-a>
#$ unix <Alt-a>

# Help menu

#$ event <<help>>
#$ win <F1>
#$ unix <F1>

#$ event <<about-idle>>

# Events without menu entries

#$ event <<remove-selection>>
#$ win <Escape>

#$ event <<center-insert>>
#$ win <Control-l>
#$ unix <Control-l>

#$ event <<do-nothing>>
#$ unix <Control-x>


about_title = "About IDLE"
about_text = """\
IDLE %s

An Integrated DeveLopment Environment for Python

by Guido van Rossum
""" % idlever.IDLE_VERSION

class EditorWindow:

    from Percolator import Percolator
    from ColorDelegator import ColorDelegator
    from UndoDelegator import UndoDelegator
    from IOBinding import IOBinding
    import Bindings
    from Tkinter import Toplevel

    about_title = about_title
    about_text = about_text

    vars = {}

    def __init__(self, flist=None, filename=None, key=None, root=None):
        self.flist = flist
        root = root or flist.root
        self.root = root
        if flist:
            self.vars = flist.vars
        self.menubar = Menu(root)
        self.top = top = self.Toplevel(root, menu=self.menubar)
        self.vbar = vbar = Scrollbar(top, name='vbar')
        self.text = text = Text(top, name='text', padx=5,
                                background="white", wrap="none")

        self.createmenubar()
        self.apply_bindings()

        self.top.protocol("WM_DELETE_WINDOW", self.close)
        self.top.bind("<<close-window>>", self.close_event)
        text.bind("<<center-insert>>", self.center_insert_event)
        text.bind("<<help>>", self.help_dialog)
        text.bind("<<about-idle>>", self.about_dialog)
        text.bind("<<open-module>>", self.open_module)
        text.bind("<<do-nothing>>", lambda event: "break")
        text.bind("<<select-all>>", self.select_all)
        text.bind("<<remove-selection>>", self.remove_selection)
        text.bind("<3>", self.right_menu_event)
        if flist:
            flist.inversedict[self] = key
            if key:
                flist.dict[key] = self
            text.bind("<<open-new-window>>", self.flist.new_callback)
            text.bind("<<close-all-windows>>", self.flist.close_all_callback)
            text.bind("<<open-class-browser>>", self.open_class_browser)
            text.bind("<<open-path-browser>>", self.open_path_browser)

        vbar['command'] = text.yview
        vbar.pack(side=RIGHT, fill=Y)

        text['yscrollcommand'] = vbar.set
        if sys.platform[:3] == 'win':
            text['font'] = ("lucida console", 8)
        text.pack(side=LEFT, fill=BOTH, expand=1)
        text.focus_set()

        self.per = per = self.Percolator(text)
        if self.ispythonsource(filename):
            self.color = color = self.ColorDelegator(); per.insertfilter(color)
            ##print "Initial colorizer"
        else:
            ##print "No initial colorizer"
            self.color = None
        self.undo = undo = self.UndoDelegator(); per.insertfilter(undo)
        self.io = io = self.IOBinding(self)

        undo.set_saved_change_hook(self.saved_change_hook)
        io.set_filename_change_hook(self.filename_change_hook)

        if filename:
            if os.path.exists(filename):
                io.loadfile(filename)
            else:
                io.set_filename(filename)

        self.saved_change_hook()

        self.load_extensions()

        menu = self.menudict.get('windows')
        if menu:
            end = menu.index("end")
            if end is None:
                end = -1
            if end >= 0:
                menu.add_separator()
                end = end + 1
            self.wmenu_end = end
            WindowList.register_callback(self.postwindowsmenu)

    def wakeup(self):
        if self.top.wm_state() == "iconic":
            self.top.wm_deiconify()
        else:
            self.top.tkraise()
        self.text.focus_set()

    menu_specs = [
        ("file", "_File"),
        ("edit", "_Edit"),
        ("windows", "_Windows"),
        ("help", "_Help"),
    ]

    def createmenubar(self):
        mbar = self.menubar
        self.menudict = menudict = {}
        for name, label in self.menu_specs:
            underline, label = prepstr(label)
            menudict[name] = menu = Menu(mbar, name=name)
            mbar.add_cascade(label=label, menu=menu, underline=underline)
        self.fill_menus()

    def postwindowsmenu(self):
        # Only called when Windows menu exists
        # XXX Actually, this Just-In-Time updating interferes
        # XXX badly with the tear-off feature.  It would be better
        # XXX to update all Windows menus whenever the list of windows
        # XXX changes.
        menu = self.menudict['windows']
        end = menu.index("end")
        if end is None:
            end = -1
        if end > self.wmenu_end:
            menu.delete(self.wmenu_end+1, end)
        WindowList.add_windows_to_menu(menu)

    rmenu = None

    def right_menu_event(self, event):
        self.text.tag_remove("sel", "1.0", "end")
        self.text.mark_set("insert", "@%d,%d" % (event.x, event.y))
        if not self.rmenu:
            self.make_rmenu()
        rmenu = self.rmenu
        self.event = event
        iswin = sys.platform[:3] == 'win'
        if iswin:
            self.text.config(cursor="arrow")
        rmenu.tk_popup(event.x_root, event.y_root)
        if iswin:
            self.text.config(cursor="ibeam")

    rmenu_specs = [
        # ("Label", "<<virtual-event>>"), ...
        ("Close", "<<close-window>>"), # Example
    ]

    def make_rmenu(self):
        rmenu = Menu(self.text, tearoff=0)
        for label, eventname in self.rmenu_specs:
            def command(text=self.text, eventname=eventname):
                text.event_generate(eventname)
            rmenu.add_command(label=label, command=command)
        self.rmenu = rmenu

    def about_dialog(self, event=None):
        tkMessageBox.showinfo(self.about_title, self.about_text,
                              master=self.text)

    helpfile = "help.txt"

    def help_dialog(self, event=None):
        helpfile = self.helpfile
        if not os.path.exists(helpfile):
            base = os.path.basename(self.helpfile)
            for dir in sys.path:
                fullname = os.path.join(dir, base)
                if os.path.exists(fullname):
                    helpfile = fullname
                    break
        if self.flist:
            self.flist.open(helpfile)
        else:
            self.io.loadfile(helpfile)

    def select_all(self, event=None):
        self.text.tag_add("sel", "1.0", "end-1c")
        self.text.mark_set("insert", "1.0")
        self.text.see("insert")
        return "break"

    def remove_selection(self, event=None):
        self.text.tag_remove("sel", "1.0", "end")
        self.text.see("insert")

    def open_module(self, event=None):
        # XXX Shouldn't this be in IOBinding or in FileList?
        try:
            name = self.text.get("sel.first", "sel.last")
        except TclError:
            name = ""
        else:
            name = string.strip(name)
        if not name:
            name = tkSimpleDialog.askstring("Module",
                     "Enter the name of a Python module\n"
                     "to search on sys.path and open:",
                     parent=self.text)
            if name:
                name = string.strip(name)
            if not name:
                return
        # XXX Ought to support package syntax
        # XXX Ought to insert current file's directory in front of path
        try:
            (f, file, (suffix, mode, type)) = imp.find_module(name)
        except ImportError, msg:
            tkMessageBox.showerror("Import error", str(msg), parent=self.text)
            return
        if type != imp.PY_SOURCE:
            tkMessageBox.showerror("Unsupported type",
                "%s is not a source module" % name, parent=self.text)
            return
        if f:
            f.close()
        if self.flist:
            self.flist.open(file)
        else:
            self.io.loadfile(file)

    def open_class_browser(self, event=None):
        filename = self.io.filename
        if not filename:
            tkMessageBox.showerror(
                "No filename",
                "This buffer has no associated filename",
                master=self.text)
            return None
        head, tail = os.path.split(filename)
        base, ext = os.path.splitext(tail)
        import pyclbr
        if pyclbr._modules.has_key(base):
            del pyclbr._modules[base]
        save_cursor = self.text["cursor"]
        self.text["cursor"] = "watch"
        self.text.update_idletasks()
        import ClassBrowser
        ClassBrowser.ClassBrowser(self.flist, base, [head])
        self.text["cursor"] = save_cursor
    
    def open_path_browser(self, event=None):
        import PathBrowser
        PathBrowser.PathBrowser(self.flist)

    def gotoline(self, lineno):
        if lineno is not None and lineno > 0:
            self.text.mark_set("insert", "%d.0" % lineno)
            self.text.tag_remove("sel", "1.0", "end")
            self.text.tag_add("sel", "insert", "insert +1l")
            self.center()

    def ispythonsource(self, filename):
        if not filename:
            return 1
        base, ext = os.path.splitext(os.path.basename(filename))
        if os.path.normcase(ext) in (".py", ".pyw"):
            return 1
        try:
            f = open(filename)
            line = f.readline()
            f.close()
        except IOError:
            return 0
        return line[:2] == '#!' and string.find(line, 'python') >= 0

    def close_hook(self):
        if self.flist:
            self.flist.close_edit(self)

    def set_close_hook(self, close_hook):
        self.close_hook = close_hook

    def filename_change_hook(self):
        if self.flist:
            self.flist.filename_changed_edit(self)
        self.saved_change_hook()
        if self.ispythonsource(self.io.filename):
            self.addcolorizer()
        else:
            self.rmcolorizer()

    def addcolorizer(self):
        if self.color:
            return
        ##print "Add colorizer"
        self.per.removefilter(self.undo)
        self.color = self.ColorDelegator()
        self.per.insertfilter(self.color)
        self.per.insertfilter(self.undo)

    def rmcolorizer(self):
        if not self.color:
            return
        ##print "Remove colorizer"
        self.per.removefilter(self.undo)
        self.per.removefilter(self.color)
        self.color = None
        self.per.insertfilter(self.undo)

    def saved_change_hook(self):
        short = self.short_title()
        long = self.long_title()
        if short and long:
            title = short + " - " + long
        elif short:
            title = short
        elif long:
            title = long
        else:
            title = "Untitled"
        icon = short or long or title
        if not self.get_saved():
            title = "*%s*" % title
            icon = "*%s" % icon
        self.top.wm_title(title)
        self.top.wm_iconname(icon)

    def get_saved(self):
        return self.undo.get_saved()

    def set_saved(self, flag):
        self.undo.set_saved(flag)

    def reset_undo(self):
        self.undo.reset_undo()

    def short_title(self):
        filename = self.io.filename
        if filename:
            filename = os.path.basename(filename)
        return filename

    def long_title(self):
        return self.io.filename or ""

    def center_insert_event(self, event):
        self.center()

    def center(self, mark="insert"):
        text = self.text
        top, bot = self.getwindowlines()
        lineno = self.getlineno(mark)
        height = bot - top
        newtop = max(1, lineno - height/2)
        text.yview(float(newtop))

    def getwindowlines(self):
        text = self.text
        top = self.getlineno("@0,0")
        bot = self.getlineno("@0,65535")
        if top == bot and text.winfo_height() == 1:
            # Geometry manager hasn't run yet
            height = int(text['height'])
            bot = top + height - 1
        return top, bot

    def getlineno(self, mark="insert"):
        text = self.text
        return int(float(text.index(mark)))

    def close_event(self, event):
        self.close()

    def maybesave(self):
        if self.io:
            return self.io.maybesave()

    def close(self):
        self.top.wm_deiconify()
        self.top.tkraise()
        reply = self.maybesave()
        if reply != "cancel":
            WindowList.unregister_callback(self.postwindowsmenu)
            if self.close_hook:
                self.close_hook()
            colorizing = 0
            if self.color:
                colorizing = self.color.colorizing
                doh = colorizing and self.top
                self.color.close(doh) # Cancel colorization
            if not colorizing:
                self.top.destroy()
        return reply

    def load_extensions(self):
        self.extensions = {}
        self.load_standard_extensions()

    def load_standard_extensions(self):
        for name in self.get_standard_extension_names():
            try:
                self.load_extension(name)
            except:
                print "Failed to load extension", `name`
                import traceback
                traceback.print_exc()

    def get_standard_extension_names(self):
        import extend
        return extend.standard

    def load_extension(self, name):
        mod = __import__(name)
        cls = getattr(mod, name)
        ins = cls(self)
        self.extensions[name] = ins
        kdnames = ["keydefs"]
        if sys.platform == 'win32':
            kdnames.append("windows_keydefs")
        elif sys.platform == 'mac':
            kdnames.append("mac_keydefs")
        else:
            kdnames.append("unix_keydefs")
        keydefs = {}
        for kdname in kdnames:
            if hasattr(ins, kdname):
                keydefs.update(getattr(ins, kdname))
        if keydefs:
            self.apply_bindings(keydefs)
            for vevent in keydefs.keys():
                methodname = string.replace(vevent, "-", "_")
                while methodname[:1] == '<':
                    methodname = methodname[1:]
                while methodname[-1:] == '>':
                    methodname = methodname[:-1]
                methodname = methodname + "_event"
                if hasattr(ins, methodname):
                    self.text.bind(vevent, getattr(ins, methodname))
        if hasattr(ins, "menudefs"):
            self.fill_menus(ins.menudefs, keydefs)
        return ins

    def apply_bindings(self, keydefs=None):
        if keydefs is None:
            keydefs = self.Bindings.default_keydefs
        text = self.text
        text.keydefs = keydefs
        for event, keylist in keydefs.items():
            if keylist:
                apply(text.event_add, (event,) + tuple(keylist))

    def fill_menus(self, defs=None, keydefs=None):
        # Fill the menus.
        # Menus that are absent or None in self.menudict are ignored.
        if defs is None:
            defs = self.Bindings.menudefs
        if keydefs is None:
            keydefs = self.Bindings.default_keydefs
        menudict = self.menudict
        text = self.text
        for mname, itemlist in defs:
            menu = menudict.get(mname)
            if not menu:
                continue
            for item in itemlist:
                if not item:
                    menu.add_separator()
                else:
                    label, event = item
                    checkbutton = (label[:1] == '!')
                    if checkbutton:
                        label = label[1:]
                    underline, label = prepstr(label)
                    accelerator = get_accelerator(keydefs, event)
                    def command(text=text, event=event):
                        text.event_generate(event)
                    if checkbutton:
                        var = self.getrawvar(event, BooleanVar)
                        menu.add_checkbutton(label=label, underline=underline,
                            command=command, accelerator=accelerator,
                            variable=var)
                    else:
                        menu.add_command(label=label, underline=underline,
                            command=command, accelerator=accelerator)
    
    def getvar(self, name):
        var = self.getrawvar(name)
        if var:
            return var.get()
    
    def setvar(self, name, value, vartype=None):
        var = self.getrawvar(name, vartype)
        if var:
            var.set(value)
    
    def getrawvar(self, name, vartype=None):
        var = self.vars.get(name)
        if not var and vartype:
            self.vars[name] = var = vartype(self.text)
        return var


def prepstr(s):
    # Helper to extract the underscore from a string,
    # e.g. prepstr("Co_py") returns (2, "Copy").
    i = string.find(s, '_')
    if i >= 0:
        s = s[:i] + s[i+1:]
    return i, s


keynames = {
 'bracketleft': '[',
 'bracketright': ']',
 'slash': '/',
}

def get_accelerator(keydefs, event):
    keylist = keydefs.get(event)
    if not keylist:
        return ""
    s = keylist[0]
    s = re.sub(r"-[a-z]\b", lambda m: string.upper(m.group()), s)
    s = re.sub(r"\b\w+\b", lambda m: keynames.get(m.group(), m.group()), s)
    s = re.sub("Key-", "", s)
    s = re.sub("Control-", "Ctrl-", s)
    s = re.sub("-", "+", s)
    s = re.sub("><", " ", s)
    s = re.sub("<", "", s)
    s = re.sub(">", "", s)
    return s


def fixwordbreaks(root):
    # Make sure that Tk's double-click and next/previous word
    # operations use our definition of a word (i.e. an identifier)
    tk = root.tk
    tk.call('tcl_wordBreakAfter', 'a b', 0) # make sure word.tcl is loaded
    tk.call('set', 'tcl_wordchars', '[a-zA-Z0-9_]')
    tk.call('set', 'tcl_nonwordchars', '[^a-zA-Z0-9_]')


def test():
    root = Tk()
    fixwordbreaks(root)
    root.withdraw()
    if sys.argv[1:]:
        filename = sys.argv[1]
    else:
        filename = None
    edit = EditorWindow(root=root, filename=filename)
    edit.set_close_hook(root.quit)
    root.mainloop()
    root.destroy()

if __name__ == '__main__':
    test()
