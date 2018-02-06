import os
import sys
path = os.path.split(__file__)[0]
path = os.path.split(path)[0]
sys.path.insert(0, path)
import pyscene
