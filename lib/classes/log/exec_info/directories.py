''' Directories related classes for log execution information class.

PURPOSE: Organize a variety of nested and subclass modules for
commonly-used log execution directory information objects.
'''
import logging # https://docs.python.org/3/library/logging.html
log = logging.getLogger().getChild('lib.classes.log.exec_info.directories')

from dataclasses import dataclass # https://docs.python.org/3/library/dataclasses.html



@dataclass
class _Directories:
    ''' Directories for log file. '''
    initial: str = None # Initial application log directory; i.e. \\logs.
    final: str = None # Optional: Final (project) log directory based
                      # on validated user input that is generated during runtime.