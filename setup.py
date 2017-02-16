# To run, from command prompt navigate to this folder and type "python setup.py build"

from cx_Freeze import setup, Executable
import os

includes_f = ['MonsterCalc.py','calc.py','syntaxhighlighter.py','myfuncs.py','MonsterCalc.png','Monster.png',
              r"C:\Users\acarro12\AppData\Local\Continuum\Anaconda3\pkgs\qt-5.6.2-vc14_0\Library\bin\libEGL.dll"]
include_packs = ['sys','PyQt5','binascii','calc','syntaxhighlighter','myfuncs']
exclude_packs = ['matplotlib','numpy','pandas','scipy','statsmodels','notebook','lxml']

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ['os'], excludes = exclude_packs,includes=include_packs,
                    include_files=includes_f)

base = 'Win32GUI'

executables = [
    Executable("MonsterCalc.py", base=base, targetName = 'MonsterCalc.exe')
]

setup(name='MonsterCalc',
      version = '1.0',
      description = 'Super calculator',
      options = dict(build_exe = buildOptions),
      executables = executables)
