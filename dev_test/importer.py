import os
import sys
global REPO
REPO = os.path.dirname(__file__)
def add_path(_path):
    sys.path.append(REPO+os.sep+_path.replace('/',os.sep))

