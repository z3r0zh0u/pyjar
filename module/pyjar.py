"""
Jar File Analyzer
"""

import os
import sys
import pyjc
import struct
import zipfile
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
        if logfile:
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
        Logger.warn(message)


def log_error(message):
    """log error message"""

    global Logger

    if Logger is not None:
        Logger.error(message)


class JarFile:

    def __init__(self, filename, debug=False, logfile=None):
        """init JarFile class"""

        logname = os.path.basename(filename)
        init_logging(logname, logfile, debug)
        
        log_debug('File: ' + filename)
        
        if os.path.isfile(filename) == False:
            raise Exception('File Not Exist: ' + filename)

        self.files = list()
        self.class_files = list()
        self.non_class_files = list()
        self.entry_point = None

        self.filename = filename
        self.files = self.__jar_decompress()
        
        for fileitem in self.files:
            if fileitem['name'].endswith('.class') == True:
                tmpfile = '_' + fileitem['name']
                open(tmpfile, 'wb').write(fileitem['data'])
                fileitem['class'] = pyjc.JavaClass(tmpfile, debug=debug, logfile=logfile)
                os.remove(tmpfile)
                self.class_files.append(fileitem)
            elif fileitem['name'] == 'MANIFEST.MF':
                manifest = fileitem['data'].split('\r\n')
                for item in manifest:
                    if item.startswith('Main-Class') == True:
                        self.entry_point = item.strip().split(':')[-1].strip()
            else:
                self.non_class_files.append(fileitem)
        

    def __jar_decompress(self):
        """decompress files in the jar archive"""

        filelist = list()
        with zipfile.ZipFile(self.filename) as zf:
            for name in zf.namelist():
                log_debug('Decompress File: ' + os.path.basename(name))
                fileitem = dict()
                fileitem['name'] = os.path.basename(name)
                fileitem['path'] = name
                fileitem['data'] = zf.read(name)
                filelist.append(fileitem)

        return filelist