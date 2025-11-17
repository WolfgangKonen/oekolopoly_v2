import sys
import os
from cx_Freeze import setup, Executable

# File for creating standalone executable for oekolopoly 2.0
# invoke: python setup.py build

files_to_include = ['assets', 'trained_agents',
                    'bin', 'Spielanleitung.pdf',
                    ]

packages_to_include = ['oekolopoly']

executable = Executable(
    script="oekolopoly_gui.py",
    base="gui",
    icon="oekolopoly/my_oekolopoly_gui/assets/python_icon.ico"
)

setup(
    name="Oekolopoly_v2",
    version="1.0",
    description="Oekolopoly",
    author="Me",
    options={'build_exe': {'include_files': files_to_include, 'packages': packages_to_include}},
    executables=[executable]
)
