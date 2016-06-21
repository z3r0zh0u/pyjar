"""
Test file for pyjar
"""

import os
import sys

sys.path.append(os.path.abspath(".."))
import module.pyjar as pyjar


if __name__ == '__main__':

    logfile = 'debug.txt'

    testjar = pyjar.JarFile('HelloWorld.jar', debug=True, logfile=logfile)