import os
import sys
sys.path.insert(0, os.path.abspath('../src/python'))

project = 'FRUCache'
author = 'Aaron Buhr'
release = '1.0'

extensions = ['myst_parser']
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

html_theme = 'alabaster'
html_static_path = ['_static']