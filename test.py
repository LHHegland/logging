''' Test log class. '''
from lib.classes.log import Log, ExceptionMessageFormatted, variable_value_message
log = Log(__file__)

try: # Code to execute, at least until an exception occurs.
    log.info('Trying Actions…')
        
    # Module code to execute.
    print('🖐 Sample message to user\'s console only.')

    log.debug('Sample debugging message to log only.')

    log.info('Sample informational message to log only.')

    # List variable name and value.
    sample_variable = 5 * 6
    log.info(variable_value_message.get('sample_variable', sample_variable))

    # List dict or class variable names and values.
    log.info(variable_value_message.get('log._exec_info', log._exec_info))

    log.warning('Sample warning message.')

    log.error('Sample error message.')

    log.info('🟩 …Completed Actions.')
except: # Code to handle unspecified exceptions.
    msg = ExceptionMessageFormatted()
    msg.title = 'UNEXPECTED ERROR'
    msg.details = 'An unexpected error has occurred.'
    msg.suggestions = 'Please check your inputs and try again. Or, contact the developer.'
    log.critical(msg.get())
finally: # Code to always execute, even if an exception occurs.
    log.terminate()