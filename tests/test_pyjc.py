"""
Test file for pyjc
"""

import os
import sys


sys.path.append(os.path.abspath(".."))
import module.pyjc as pyjc


if __name__ == '__main__':

    logfile = 'pyjc_debug.txt'

    try:
        java_class = pyjc.JavaClass('non_exist.class', debug = True)
    except Exception as e:
        print e
    print '-' * 40

    try:
        java_class = pyjc.JavaClass('non_class.class', debug = True, logfile = logfile)
    except Exception as e:
        print e
    print '-' * 40
    
    java_class = pyjc.JavaClass('HelloWorld.class', debug = True, logfile = logfile)

