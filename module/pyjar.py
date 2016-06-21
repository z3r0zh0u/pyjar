"""
Jar File Analyzer
"""

import os
import sys
import struct
import logging


Logger = None


def init_logging(logname, logfile, debug):
    """init logging"""

    global Logger

    Logger = logging.getLogger(logname)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            
    if debug:
        Logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        Logger.addHandler(fh)
    else:
        Logger.setLevel(logging.WARN)
        ch.setLevel(logging.WARN)         
    
    ch.setFormatter(formatter)
    Logger.addHandler(ch)

    if debug:
        log_debug('[******** Debug Mode ********]')


def log_debug(message):
    """log debug message"""

    global Logger

    if Logger is not None:
        Logger.debug(message)


def log_warn(message):
    """log warning message"""

    global Logger

    if Logger is not None:
        Logger.debug(message)


def log_error(message):
    """log error message"""

    global Logger

    if Logger is not None:
        Logger.debug(message)


class JarFile:

    def __init__(self, filename, debug=False, logfile='pyjar_debug.txt'):
        """init JarFile class"""

        logname = os.path.basename(filename)
        init_logging(logname, logfile, debug)

        log_debug('File: ' + filename)
        
        if os.path.isfile(filename) == False:
            raise Exception('File Not Exist: ' + filename)

        self.data = open(filename, 'rb').read()

        