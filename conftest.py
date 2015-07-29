import os
import sys

def pytest_configure():
    path = os.path.abspath(os.path.basename(__file__))
    sys.path.insert(0, path)
