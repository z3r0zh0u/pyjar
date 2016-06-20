"""
Test file for pyjar
"""

import os
import sys


sys.path.append(os.path.abspath(".."))
import pyjar.pyjar as pyjar


if __name__ == '__main__':

    try:
        java_class = pyjar.JavaClass('non_exist.class', debug = True)
    except Exception as e:
        print e
    print '-' * 40

    try:
        java_class = pyjar.JavaClass('non_class.class', debug = True)
    except Exception as e:
        print e
    print '-' * 40
    
    java_class = pyjar.JavaClass('HelloWorld.class', debug = True)

