# To run, from command prompt navigate to this folder and type "python setup.py build"

from cx_Freeze import setup, Executable
import os

includes_f = ['MonsterCalc.py', 'calc.py', 'keywords.py', 'syntaxhighlighter.py','myfuncs.py', 'resistors.py', 
              'toolButtons.py', 'MonsterCalc.png','Monster.png','Functions.png', 'release_notes.txt', 'demo.txt']
include_packs = ['sys','pyside2','binascii','calc','syntaxhighlighter','myfuncs']
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
      version = '1.9',
      description = 'Super calculator',
      options = dict(build_exe = buildOptions),
      executables = executables)
