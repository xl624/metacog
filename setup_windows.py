from cx_Freeze import setup, Executable
import os

includefiles = ['times-new-roman.ttf','bag.py','button.py','inputbox.py','colors.py','instances.pkl','instances_prac.pkl','.\Data']
# ,r"C:\\Users\\lxykh\\AppData\\Local\\Programs\\Python\\Python36\\DLLs\\tcl86t.dll", \
                 # r"C:\\Users\\lxykh\AppData\\Local\\Programs\\Python\\Python36\\DLLs\\tk86t.dll"
includes = []
excludes = []
packages = []

#additional_mods = ['numpy.core._methods', 'numpy.lib.format']
setup(
    name = "metacognition",
    version = "0.1",
    description = "",
    options = {'build_exe':{'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable("main.py", base="Win32Gui")])