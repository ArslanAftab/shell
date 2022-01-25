'Class and associated variables for executing sort commands'
import os
from typing import List
import globals.file_ops as file_ops
import globals.errors as e


class SORTExecutor():
    'Class for executing sort commands'

    error = e.SORT_OPTION_ERROR
    # Booleans represent whether the flag can take a number argument
    valid_flags = {'r': False}

    def __init__(self, options, args: list, unsafe: bool):
        self._args = args
        self.unsafe = unsafe
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        for arg in self._args:
            # Each argument must be a valid filepath
            if not os.path.isfile(arg):
                e.output_error(
                    self.unsafe, e.SORT_CANNOT_READ_ERROR.format(arg), out)
                return False
        return True

    def _create_string_list(self) -> List[str]:
        '''Generates a string by reading text in files as a list with the get_file_line_list
        method from file_ops.'''
        string_list = []
        for file_name in self._args:
            string_list += file_ops.get_file_line_list(file_name, False)
        return string_list

    def _create_sorted_string(self, string_list: list) -> str:
        '''Generates a sorted string by sorting the list, and then joining the strings together'''
        string_list.sort()
        # Reverse the order if -r flag is present
        if "r" in self.entered_letters:
            string_list.reverse()
        return ''.join(string_list)

    def execute(self, out) -> None:
        'Check arguments and execute command'
        if len(self._args) == 0:
            string_list = [input()]
        else:
            string_list = self._create_string_list()
        string = self._create_sorted_string(string_list)
        out.append(string)
