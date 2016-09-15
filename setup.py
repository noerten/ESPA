import sys
from cx_Freeze import setup, Executable
## you should copy C:\Python27\Lib\site-packages\PyQt4\plugins\sqldrivers to main folder

includes = ["sys", "matplotlib.backends",  "matplotlib.backends.backend_qt4agg",
            "matplotlib.figure", "pylab", "numpy","PyQt4.QtCore","PyQt4.QtGui",
            "PyQt4.QtSql", "matplotlib.backends.backend_tkagg", "atexit",
            "shelve", "dbhash"]
excludes = ['collections.abc', '_gtkagg', '_tkagg', '_agg2', '_cairo',
            '_cocoaagg', '_fltkagg', '_gtk', '_gtkcairo']
packages = []
path = []
base = None
#if sys.platform == 'win32':
#    base = 'Win32GUI'
options = {
    'build_exe': {
        "includes": includes,
        "excludes": excludes,
        "packages": packages,
        "path": path
    }
}

executables = [
    Executable('ESPA.py', base=base)
]

setup(name='ESPA',
      version='0.2',
      description='ESPA',
      options=options,
      executables=executables
      )
