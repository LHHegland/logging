''' Log-related Classes

PURPOSE: Organize a variety of nested and subclass modules for
commonly-used log objects (e.g. fmtval, fmtmsg).
and methods (e.g. info, debug, warning, error, critical).

USAGE:
 - if in top-level environment module (i.e. users' main
   entrypoint; if __name__ == '__main__'):
     1. include code below immediately after module's docstring
        (see PEP 257 – Docstring Conventions at https://peps.python.org/pep-0257/ ):
            from lib.classes.log import Log
            # Can move logfile from \\logs to project log directory after validating user input; see #2.
            log = Log(__file__)

     2. include code below at end of "finally" block in module's
        try-except-finally block
        (see https://docs.python.org/3/tutorial/errors.html#defining-clean-up-actions ):
            # Close, then move log file, if desired, to final log directory;
            # e.g. project directory either input as execution argument by
            # user or generated during runtime.
            # If empty, None, or '', log remains in original directory.
            log.terminate('D:\\path\\to\\log\\')

 - if in importable module (e.g. class or utility module), include code below
   immediately after module docstring:
        import logging
        log = logging.getLogger().getChild('fully_qualified_module_import_path') # e.g. lib.classes.log


EXAMPLE MODULE #1:
    """ Example top-level environment module for Log class use. """
    from lib.classes.log import Log
    log = Log(__file__) # Log to 'logs\\' directory, relative to module file.
                       # Creates, if missing.
    
    [ … other imports and definitions … ]

    if __name__ == '__main__':
        try: # Code to execute, at least until an exception occurs
            log.info('Trying Actions…')
            
            # … module code to execute, at least until an exception occurs …
            
            # … user messages as needed …
            print('🖐 Message to user.')
            log.debug('Message.')
            log.info('Message')
            log.info(fmtval('my_varname', my_var)) # list variable names and values for debugging
            log.warning('Message.')
            log.error('Message.')
            log.critical('Message.')
            
            log.info('🟩 …Completed Actions.')
        # … optional code to handle specified exceptions …
        except Exception: # Code to handle unspecified exceptions
            log.exception('🟥 FATAL ERROR: UNEXPECTED EXCEPTION OCCURRED!')
        finally: # Code to always execute, even if an exception occurs
            log.terminate() # Close, then leave log file in 'logs\\' directory, relative to module file.


EXAMPLE MODULE #2:
    """ Example importable module (e.g. class or utility module) for Log class use. """
    # NOTE: log initialized in top-level environment module importing this
    # class or utility module will connect to log initialized below, labeling
    # this modules' log entries with specified fully_qualified_module_import_path
    import logging
    log = logging.getLogger().getChild('fully_qualified_module_import_path') # e.g. lib.classes.log
    
    [ … other imports and definitions … ]

    # … module code to execute, at least until an exception occurs …


REFERENCES:
  - Python → Documentation
      - HOWTO: Logging
          - Basic Logging Tutorial -- https://docs.python.org/3/howto/logging.html
          - Advanced Logging Tutorial -- https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial
          - Logging Cookbook -- https://docs.python.org/3/howto/logging-cookbook.html
      - The Python Standard Library
          - logging
              - Logging -- https://docs.python.org/3/library/logging.html
              - .config — configuration -- https://docs.python.org/3/library/logging.config.html
              - .handlers — handlers -- https://docs.python.org/3/library/logging.handlers.html
'''
import logging # https://docs.python.org/3/library/logging.html
log = logging.getLogger().getChild('lib.classes.log')

from dataclasses import dataclass, field # https://docs.python.org/3/library/dataclasses.html

import datetime # https://docs.python.org/3/library/datetime.html
import os # https://docs.python.org/3/library/os.html
import shutil

from lib.classes.log.exec_info import _ExecInfo

from lib.classes.log.exception_message import ExceptionMessageFormatted
import lib.classes.log.variable_value_message


@dataclass
class Log:
    ''' General log class. '''
    _module_filepathname: str
    _exec_info: _ExecInfo = field(default_factory=_ExecInfo)
    _log: logging.Logger = None



    def __post_init__(self):
        ''' Clean-up dataclass initialization. '''
        self._exec_info.set_info(self._module_filepathname)
        # Check if initial logs directory exists, create if not.
        logs_dirpathname = os.path.join(self._exec_info._directories.initial, 'logs')
        if not os.path.exists(logs_dirpathname):
            os.mkdir(logs_dirpathname)
            self.initialize()
            msg = ExceptionMessageFormatted()
            msg.title = 'LOGS DIRECTORY CREATED'
            msg.details = (
                'Module uses logging and needs a log directory.\n'
               f'A directory for logs did not exist in {self._exec_info._directories.initial}.\n'
               f'Therefore, the logger created {logs_dirpathname}.'
            )
            self.warning(msg.get())
        else:
            self.initialize()



    def initialize(self) -> None:
        ''' Initialize logging to logs\\module_name_timestamp.log. '''
        self.setup(self._exec_info._get_filepathname())
        self.info(self._get_header())



    def _get_header(self) -> str:
        ''' Return log header. '''
        return (
             'BEGIN LOGGING...\n'
            f'START: {self._exec_info._timestamps.start.isoformat()}\n'
            f'USER: {self._exec_info._user}\n'
            f'OPERATING SYSTEM: {self._exec_info._system}\n'
            f'PYTHON VERSION:: {self._exec_info._python_version}\n'
            f'ROOT: {self._exec_info._get_module_filepathname()}\n'
            f'ARGUMENTS: {self._exec_info._arguments}\n'
            f'LOG: {self._exec_info._get_filepathname()}\n'
             '========== STARTING =========='
        )



    def debug(self, message) -> None:
        ''' Log debug message.'''
        self._log.debug(message)

    def info(self, message) -> None:
        ''' Log info message.'''
        self._log.info(message)

    def warning(self, message) -> None:
        ''' Log warning message.'''
        self._log.warning(message)

    def error(self, message) -> None:
        ''' Log error message.'''
        self._log.error(message)

    def critical(self, message) -> None:
        ''' Log critical message.'''
        self._log.critical(message)



    def terminate(self, dirpathname: str | None = None) -> None:
        ''' Set end execution end time, add log footer, copy to final log directory, if provided.

        INPUT:
        - dirpathname (str) = final log directory path and name; e.g. dirpathname\\module_name_timestamp.log)
        '''
        self._exec_info._timestamps.end = datetime.datetime.now(datetime.UTC)
        logfile_pathname = self._exec_info._get_filepathname()
        self._exec_info._directories.final = dirpathname
        self.info(self._get_footer())
        if dirpathname is not None:
            shutil.copy(logfile_pathname, dirpathname)



    def _get_footer(self) -> str:
        ''' Return log footer. '''
        footer = (
             '========== ENDING ==========\n'
        )

        if self._exec_info._directories.final is None:
            footer += '*** Final log directory not specified. ***\n'
        else:
            footer += 'Log copied to specified directory.\n'
            
        footer += (
            '\n'
            f'LOG: {self._exec_info._get_filepathname()}\n'
             '\n'
            f'  END: {self._exec_info._timestamps.end.isoformat()}\n'
            f'- START: {self._exec_info._timestamps.start.isoformat()}\n'
            f'= ELAPSED: {self._exec_info._timestamps._get_elapsed()}'
        )

        return footer


    def setup(self, filepathname: str | None = None) -> None:
        ''' Store or display helpful log record messages for testing and debugging.

        INPUT:
        - filepathname (str)(optional) = path and name of log file, if omitted stream to stderr
                                         (e.g. D:\\path\\name.log)
        '''



        # ---------- FILTERS ----------
        # Define filter functions
        def filter_fyi(record: logging.LogRecord) -> bool:
            ''' Filter to accept log records with level less than warning level, otherwise ignore.

            OUTPUT:
            - (bool) = true to accept, false to ignore
            '''
            return record.levelno < 30 # logging.WARNING value



        def filter_alert(record: logging.LogRecord) -> bool:
            ''' Filter to accept log records with level greater than or equal to warning level, otherwise ignore.

            OUTPUT:
            - (bool) = true to accept, false to ignore
            '''
            # Because child handlers do not check message level, do it here:
            # See https://www.electricmonk.nl/log/2017/08/06/understanding-pythons-logging-module/
            return record.levelno >= 30 # logging.WARNING value



        def filter_add_cntxt(record: logging.LogRecord) -> bool:
            ''' Filter to add contextual color character flag (cntxt_flag) to LogRecord (e.g. ⚪, ⬛, 🟧, 🟥, 🟥🟥)

            OUTPUT:
            - (bool) = true to accept all records
            '''
            match record.levelname:
                case 'DEBUG':
                    record.cntxt_flag = '⚪'
                case 'INFO':
                    record.cntxt_flag = '⬛'
                case 'WARNING':
                    record.cntxt_flag = '🟧'
                case 'ERROR':
                    record.cntxt_flag = '🟥'
                case 'CRITICAL':
                    record.cntxt_flag = '🟥🟥'
                case _:
                    record.cntxt_flag = ''
            
            return True # accept all records



        # ---------- LOGGING LEVEL ----------
        # Create logger instance for all log record messages.
        # See https://docs.python.org/3/howto/logging.html#logging-flow
        #     https://docs.python.org/3/howto/logging.html#loggers
        self._log = logging.getLogger() # Create logger instance.
        self._log.setLevel(logging.DEBUG) # Set logger level ≥ debug level.
        # No logger filter needed.



        # ---------- FORMATTERS ----------
        # Create date format for all formatters.
        # See https://docs.python.org/3/library/time.html#time.strftime
        datefmt = '%Y-%m-%d %H:%M:%S %z'
        
        # Create different log record formats for various handler formatters.
        # See https://docs.python.org/3/library/logging.html#logrecord-attributes
        # For stderr, omit contextual color flag.
        fmt_stderr_fyi = (
            '%(message)s \n'
            '%(asctime)s - %(name)s - %(levelname)s'
        )
        fmt_stderr_alert = (
            '\n'
            '%(message)s \n'
            '%(asctime)s - %(name)s - %(levelname)s \n'
            '%(threadName)s → %(processName)s \n'
            '%(pathname)s \n'
            '→ %(module)s → %(funcName)s @ %(lineno)d \n'
            'EXCEPTION INFO: %(exc_info)s \n'
        )
        # For file, include contextual color flag.
        fmt_file_fyi = (
            '\n'
            '%(cntxt_flag)s %(message)s \n'
            '%(asctime)s - %(name)s - %(levelname)s \n'
        )
        fmt_file_alert = (
            '\n'
            '%(cntxt_flag)s %(message)s \n'
            '%(asctime)s - %(name)s - %(levelname)s \n'
            '%(threadName)s → %(processName)s \n'
            '%(pathname)s \n'
            '→ %(module)s → %(funcName)s @ %(lineno)d \n'
            'EXCEPTION INFO: %(exc_info)s \n'
        )

        # Create formatters for handlers.
        # See https://docs.python.org/3/howto/logging.html#formatters
        formatter_stderr_fyi = logging.Formatter(fmt_stderr_fyi, datefmt)
        formatter_stderr_alert = logging.Formatter(fmt_stderr_alert, datefmt)
        
        formatter_file_fyi = logging.Formatter(fmt_file_fyi, datefmt)
        formatter_file_alert = logging.Formatter(fmt_file_alert, datefmt)



        # ---------- HANDLERS ----------
        if filepathname == None: # Log all messages to stderr only.
            # Create logger handler to stderr for fyi messages (e.g. debug and info).
            # See https://docs.python.org/3/library/logging.handlers.html
            # See https://docs.python.org/3/library/logging.html#filter-objects
            handler_stderr_fyi = logging.StreamHandler() # Create handler.
            handler_stderr_fyi.setLevel(logging.DEBUG) # Set handler level ≥ debug level.
            handler_stderr_fyi.addFilter(filter_fyi) # Add handler filter: < warning level (i.e. only debug and info).
            handler_stderr_fyi.setFormatter(formatter_stderr_fyi) # Set handler formatter.
            self._log.addHandler(handler_stderr_fyi) # Add handler to logger instance.
            
        else: # Log all messages to logfile, plus alerts to stderr.
            # Create logger handler to logfile for fyi messages (e.g. debug and info).
            # See https://docs.python.org/3/library/logging.handlers.html
            # See https://docs.python.org/3/library/logging.html#filter-objects
            handler_file_fyi = logging.FileHandler(filepathname, mode='a', encoding='utf-8') # Create handler.
            handler_file_fyi.setLevel(logging.DEBUG) # Set handler level.
            handler_file_fyi.addFilter(filter_fyi) # Add handler filter: allow only fyi messages (e.g. debug and info).
            handler_file_fyi.addFilter(filter_add_cntxt) # Add handler filter: add contextual color flag.
            handler_file_fyi.setFormatter(formatter_file_fyi) # Set handler formatter.
            self._log.addHandler(handler_file_fyi) # Add handler to logger instance.
        
            # Create logger handler to logfile for alert messages (e.g. warning, error, and critical).
            # See https://docs.python.org/3/library/logging.handlers.html
            # See https://docs.python.org/3/library/logging.html#filter-objects
            handler_file_alert = logging.FileHandler(filepathname, mode='a', encoding='utf-8') # Create handler.
            handler_file_alert.setLevel(logging.WARNING) # Set handler level.
            handler_file_alert.addFilter(filter_alert) # Add handler filter: allow only alert messages (e.g. warning, error, and critical).
            handler_file_alert.addFilter(filter_add_cntxt) # Add handler filter: add contextual color flag.
            handler_file_alert.setFormatter(formatter_file_alert) # Set handler formatter.
            self._log.addHandler(handler_file_alert) # Add handler to logger instance.
        
        # Create logger handler to stderr for alert messages (e.g. warning, error, and critical).
        # See https://docs.python.org/3/library/logging.handlers.html
        # See https://docs.python.org/3/library/logging.html#filter-objects
        handler_stderr_alert = logging.StreamHandler() # Create handler.
        handler_stderr_alert.setLevel(logging.WARNING) # Set handler level ≥ warning level.
        handler_stderr_alert.addFilter(filter_alert) # Add handler filter: allow only alert messages (e.g. warning, error, and critical).
        handler_stderr_alert.setFormatter(formatter_stderr_alert) # Set handler formatter.
        self._log.addHandler(handler_stderr_alert) # Add handler to logger instance.