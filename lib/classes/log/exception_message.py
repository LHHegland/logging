''' Formatted message related classes for more useful exception messages (e.g. warning, error, and critical).

PURPOSE: Organize a variety of nested and subclass modules for
commonly-used formatted message objects for more useful exception
messages (e.g. warning, error, and critical).
'''
import logging # https://docs.python.org/3/library/logging.html
log = logging.getLogger().getChild('lib.classes.log.exception_message')

from dataclasses import dataclass # https://docs.python.org/3/library/dataclasses.html


@dataclass
class ExceptionMessageFormatted:
    ''' General formatted message class for exceptions.

    See: https://docs.python.org/3/library/exceptions.html
         https://docs.python.org/3/tutorial/errors.html
    '''
    title: str = ''
    details: str = ''
    suggestions: str = ''



    def get(self) -> str:
        ''' Return formatted string for more useful warning, error, or critical message. '''
        message = f'{(self.title).upper()}\n'

        if self.details != '':
            # Why is this issue being raised? What are the requirements? What are the consequences?
            message += f'DETAILS:\n{self.details}\n\n'

        if self.suggestions != '':
            # How might the user resolve this issue? What steps might the user take?
            message += f'SUGGESTIONS:\n{self.suggestions}\n\n'

        message += f'TRACING INFORMATION APPEARS BELOW:'
        
        return message