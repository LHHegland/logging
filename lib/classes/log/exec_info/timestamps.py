''' Timestamps related classes for log execution information class.

PURPOSE: Organize a variety of nested and subclass modules for
commonly-used log execution timpestamp information objects.
'''
import logging # https://docs.python.org/3/library/logging.html
log = logging.getLogger().getChild('lib.classes.log.exec_info.timpestamps')

from dataclasses import dataclass # https://docs.python.org/3/library/dataclasses.html

import datetime # https://docs.python.org/3/library/datetime.html



@dataclass
class _Timestamps:
    ''' UTC timestamps for module execution log information. '''
    start: datetime = None # UTC timestamp for the start of the module execution.
    end: datetime = None # UTC timestamp for the end of the module execution.

    def __post_init__(self):
         # Set the start time to the current UTC time.
         self.start = datetime.datetime.now(datetime.UTC)



    def _get_elapsed(self) -> str:
        ''' Get text message for elapsed time between start and end times. '''
        included_seconds = 0
        elapsed_seconds = (self.end - self.start).total_seconds()

        whole_minutes = int(elapsed_seconds // 60)
        included_seconds += 60 * whole_minutes

        whole_seconds = int(elapsed_seconds - included_seconds)
        included_seconds += whole_seconds

        whole_milliseconds = int((elapsed_seconds - included_seconds) * 1000)
        included_seconds += whole_milliseconds / 1000

        whole_microseconds = int((elapsed_seconds - included_seconds) * 1000000)

        return f'{whole_minutes:d}m {whole_seconds:d}s {whole_milliseconds:d}ms {whole_microseconds:d}μs'