''' Execution information related classes for Log Class.

PURPOSE: Organize a variety of nested and subclass modules for
commonly-used log execution information objects.
'''
import logging # https://docs.python.org/3/library/logging.html
log = logging.getLogger().getChild('lib.classes.log.exec_info')

from dataclasses import dataclass, field # https://docs.python.org/3/library/dataclasses.html

import getpass # https://docs.python.org/3/library/getpass.html
import os # https://docs.python.org/3/library/os.html
import platform # https://docs.python.org/3/library/platform.html
import sys  # https://docs.python.org/3/library/sys.html

from lib.classes.log.exec_info.directories import _Directories
from lib.classes.log.exec_info.timestamps import _Timestamps



@dataclass
class _ExecInfo:
    ''' Module execution information for log file. '''
    _module_basename: str = None
    _arguments: list[str] = field(default_factory=list)
    _directories: _Directories = field(default_factory=_Directories)
    _user: str = field(default_factory=getpass.getuser)
    _system: platform.uname_result = field(default_factory=platform.uname)
    _python_version: str = field(default_factory=platform.python_version)
    _timestamps: _Timestamps = field(default_factory=_Timestamps)



    def set_info(self, _module_filepathname: str):
        ''' Clean-up dataclass initialization. '''
        # Initially, the calling module's __file__ is assigned to _module_basename.
        # Break _module_basename components into directory and basename without extension.
        self._directories.initial = os.path.dirname(_module_filepathname)
        self._module_basename = os.path.splitext(os.path.basename(_module_filepathname))[0]
        self._arguments = sys.argv[1:]



    def _get_filepathname(self) -> str:
        ''' Return log file path and name as module basename plus execution timestamp (yyyymmddhhmmss) with log extension. '''
        if self._directories.final is None:
            dirpath = os.path.join(self._directories.initial, 'logs')
        else:
            dirpath = self._directories.final

        basename_ext = self._module_basename + '_' + self._timestamps.start.strftime('%Y%m%d%H%M%S') + os.extsep + 'log'

        return os.path.join(dirpath, basename_ext)



    def _get_module_filepathname(self) -> str:
        ''' Return module file path and name. '''
        return os.path.join(self._directories.initial, self._module_basename + os.extsep + 'py')