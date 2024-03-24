import sys
from cx_Freeze import setup, Executable

# List of modules to exclude
exclude_modules = [
    "tkinter", 'pydoc', 'email', 'html', "concurrent",  "multiprocessing",  "test", "xml", "xmlrpc", "csv", "unittest", 
                "PyQt5.QtDBus",
                "PyQt5.QtNetwork",
                "PyQt5.QtOpenGL",
                "PyQt5.QtPrintSupport",
                "PyQt5.QtQml",
                "PyQt5.QtQuick",
                "PyQt5.QtSql",
                "PyQt5.QtTest",
                "PyQt5.QtWebChannel",
                "PyQt5.QtWebEngine",
                "PyQt5.QtWebEngineCore",
                "PyQt5.QtWebEngineWidgets",
                "PyQt5.QtWebSockets",
                "PyQt5.QtXml",
                "PyQt5.QtXmlPatterns",
                "PyQt5.Qml"
                
]

include_modules = ["PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets", "configparser", "os", "sys", "osgeo.ogr"]


# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "excludes": exclude_modules, "includes": include_modules
}



base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" if you don't want the console window to appear

setup(
    name="ADAS Delivery Utility",
    version="1.0",
    description="ADAS delivery Utility",
    options={"build_exe": build_exe_options},
    executables=[Executable("adas_project/main.py", base=base)],
    license= "LICENSE"
)
