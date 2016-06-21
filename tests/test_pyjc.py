"""
"""

import os
import sys


sys.path.append(os.path.abspath(".."))
import module.pyjc as pyjc


if __name__ == '__main__':

    try:
        java_class = pyjc.JavaClass('non_exist.class', debug = True)
    except Exception as e:
        print e
    print '-' * 40

    try:
        java_class = pyjc.JavaClass('non_class.class', debug = True)
    except Exception as e:
        print e
    print '-' * 40
    
    java_class = pyjc.JavaClass('HelloWorld.class', debug = True)

