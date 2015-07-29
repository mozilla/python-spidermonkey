import os
import sys

def pytest_configure():
    sys.path.insert(0, os.path.abspath(os.curdir))
