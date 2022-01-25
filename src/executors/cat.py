'Class and associated variables for executing cat commands'
import os
from typing import List
import globals.file_ops as file_ops
import globals.errors as e


class CATExecutor():
    'Class for executing cat commands'

    error = e.CAT_OPTION_ERROR
    # Booleans represent whether the flag can take a number argument
    valid_flags = {'b': False, 'e': False, 'n': False}

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
                    self.unsafe, e.MISSING.format('cat', arg), out)
                return False
        return True

    def _create_string_list(self) -> List[str]:
        '''Generates a string by reading text in files as a list with the get_file_line_list
        method from file_ops.'''
        string_list = []
        for file_name in self._args:
            string_list += file_ops.get_file_line_list(file_name, False)
        return string_list

    def _create_string(self, string_list: list) -> str:
        '''Generates string by reading and joining strings stored in a list'''
        line_number = 1
        for index, line in enumerate(string_list):
            # Line numbers will be added if the -n flag is present, or if the -b flag is present
            # and the line is non-empty. -b flag overrules if both flags are present
            if "n" in self.entered_letters and "b" not in self.entered_letters \
                    or "b" in self.entered_letters and not (line.isspace() or len(line) == 0):
                string_list[index] = self._add_line_number(line, line_number)
                line_number += 1

            # End of line character $ will be added if -e flag is present
            if "e" in self.entered_letters and index != len(string_list) - 1:
                string_list[index] = self._add_end_of_line(string_list[index])
        return ''.join(string_list)

    @staticmethod
    def _add_end_of_line(string) -> str:
        'Adds end of field character $ to the end of a string'
        return f"{string[:-1]}$\n"

    @staticmethod
    def _add_line_number(string, line_number) -> str:
        'Adds a formatted line number to the start of a string'
        return f"       {line_number}  {string}"

    def execute(self, out) -> None:
        'Check arguments and execute command'
        if len(self._args) == 0:
            string_list = [input()+"\n"]
        else:
            string_list = self._create_string_list()
        string = self._create_string(string_list)
        out.append(string)
