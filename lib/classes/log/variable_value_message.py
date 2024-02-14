''' Formatted label-value message related classes for more quick and easy informational and debugging messages.

PURPOSE: Organize a variety of nested and subclass modules for
commonly-used formatted messages for variable names and values
related object classes for quicker and easier informational and
debugging messages.
'''
import logging # https://docs.python.org/3/library/logging.html
log = logging.getLogger().getChild('lib.classes.log.variable_value_message')

import pprint # https://docs.python.org/3/library/pprint.html
pp = pprint.PrettyPrinter(indent=4, width=160, compact=False,sort_dicts=False)

from typing import Any # https://docs.python.org/3/library/typing.html

def get(name: str, value: Any) -> str:
    ''' Format variable name and value for print or logging, especially for info and debug messages. '''
    if isinstance(value, (bool, bytes, int, float, str, list, tuple, type(None))):
        return f'🔎VarVal🔍 {name} ({type(value)}): {value}'
    else:
        return f'🔎VarVal🔍 {name} ({type(value)}):\n{pp.pformat(value)}'