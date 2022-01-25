'Class and associated variables for executing cut commands'
import os
from typing import List
from collections import defaultdict
import globals.file_ops as file_ops
import globals.errors as e


class CUTExecutor():
    'Class for executing cut commands'

    error = e.CUT_OPTION_ERROR
    # Booleans represent whether the flag can take a number argument
    valid_flags = {'b': True, 'c': True}

    def __init__(self, options, args: list, unsafe: bool):
        self._number_list = []
        self._number_dict = defaultdict(list)
        self._args = args
        self.unsafe = unsafe
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        number_list_in_arguments = False
        # Number(s) representing the indexes to be displayed must be present either as a number
        # entered with an option, or as a number list in arguments.
        if not self._check_number_in_option():
            if not self._check_valid_number_list(out):
                return False
            number_list_in_arguments = True

        for index, arg in enumerate(self._args):
            if index == 0 and number_list_in_arguments:
                continue
            # Each argument must be a valid filepath
            if not os.path.isfile(arg):
                e.output_error(self.unsafe, e.MISSING.format('cut', arg), out)
                return False
        return True

    def _check_single_flag_used(self, out) -> bool:
        '''Checks that only one flag of -b or -c is present.'''
        if len(self.entered_letters) == 0:
            e.output_error(self.unsafe, e.CUT_SPECIFY_ERROR, out)
            return False
        if "b" in self.entered_letters and "c" in self.entered_letters:
            e.output_error(self.unsafe, e.CUT_ONE_TYPE_ERROR, out)
            return False
        return True

    def _check_number_in_option(self) -> bool:
        '''Checks that a number is entered after a flag'''
        for flag_dict in self.options:
            if flag_dict['number']:
                return True
        return False

    def _get_number_in_option(self) -> int:
        '''Returns the number entered after a flag'''
        flag_dict = self.options[0]
        return int(flag_dict['number'])

    def _check_valid_number_list(self, out) -> bool:
        '''Checks whether a valid number list has been entered. A valid number list is
        a list of numbers or ranges separated by commas only.'''
        # Assume the first argument is a number list
        number_string = self._args[0]
        if not self._check_valid_number_string_characters(number_string, out):
            return False
        number_list = number_string.split(",")
        if not self._check_valid_number_list_ranges(number_list, out):
            return False
        return True

    def _check_valid_number_list_ranges(self, number_list: list, out) -> bool:
        '''Checks that all numbers in the number list are valid ranges'''
        for number in number_list:
            if number == "":
                e.output_error(self.unsafe, e.CUT_NUMBERED_ERROR, out)
                return False
            if "-" in number:
                if number.count("-") > 1:
                    e.output_error(self.unsafe, e.CUT_INVALID_RANGE, out)
                    return False
                dash_index = number.index("-")
                if dash_index not in [0, len(number) - 1]:
                    number1 = int(number[:dash_index])
                    number2 = int(number[dash_index+1:])
                    if number1 > number2:
                        e.output_error(
                            self.unsafe, e.CUT_DECREASING_RANGE_ERROR, out)
                        return False
        return True

    def _check_valid_number_string_characters(self, number_list: list, out) -> bool:
        '''Checks that all characters in the number_list are only digits, commas or dashes'''
        for char in number_list:
            if not char.isdigit() and char not in ["-", ","]:
                e.output_error(
                    self.unsafe, e.CUT_INVALID_POS_ERROR.format(char), out)
                return False
        return True

    def _set_number_dict(self, number_string: list) -> None:
        '''Sets the number dictionary with the numbers and ranges entered as an argument.
        The dictionary has 4 keys for different types of numbers and ranges: "number" (e.g. 3),
        "start_range" (e.g. -2), "end_range" (e.g. 5-), and "range" (e.g. 1-4).'''
        for number in number_string.split(","):
            if "-" not in number:
                self._number_dict['number'].append(int(number))
            elif number[0] == "-":
                self._number_dict['start_range'].append(int(number[1:]))
            elif number[-1] == "-":
                self._number_dict['end_range'].append(int(number[:-1]))
            else:
                dash_index = number.index("-")
                number1 = int(number[:dash_index])
                number2 = int(number[dash_index+1:])
                self._number_dict['range'].append((number1, number2))

    def _check_zero_in_number_dict(self, out) -> bool:
        '''Checks if zero is present in the number dictionary. Since positions must start
        from 1, it will produce an error if 0 is present.'''
        for number in self._number_dict['number'] + self._number_dict['start_range'] \
                + self._number_dict['range'] + self._number_dict['end_range']:
            if number == 0:
                e.output_error(
                    self.unsafe, e.CUT_NUMBERED_ERROR, out)
                return True
        return False

    def _create_string_list(self) -> List[str]:
        '''Generates a string by reading text in files as a list with the get_file_line_list
        method from file_ops.'''
        string_list = []
        for file_name in self._args:
            string_list += file_ops.get_file_line_list(file_name, False)
        return string_list

    def _create_index_list(self, string_length) -> List[int]:
        '''Creates the list of index positions that will be displayed.'''
        index_list = []
        for number in self._number_dict['number']:
            index_list.append(number-1)
        for number in self._number_dict['start_range']:
            index_list.extend((i-1) for i in range(1, number+1))
        for number1, number2 in self._number_dict['range']:
            index_list.extend((i-1) for i in range(number1, number2+1))
        for number in self._number_dict['end_range']:
            index_list.extend((i-1) for i in range(number, string_length))
        index_list = list(set(index_list))
        index_list.sort()
        return index_list

    def _create_string(self, string_list: list) -> str:
        '''Generates string of required index positions'''
        string = ""
        for line in string_list:
            index_list = self._create_index_list(len(line))
            sub_string = ""
            for index in index_list:
                if index > len(line)-1:
                    break
                sub_string += line[index]
            if len(sub_string) == 0 or sub_string[-1] != "\n":
                sub_string += "\n"
            string += sub_string
        return string

    def execute(self, out) -> None:
        'Check arguments and execute command'
        if not self._check_single_flag_used(out):
            return
        if self._check_number_in_option():
            self._number_dict['number'].append(self._get_number_in_option())
        else:
            number_string = self._args.pop(0)
            self._set_number_dict(number_string)
        if self._check_zero_in_number_dict(out):
            return
        if len(self._args) == 0:
            string_list = [input()]
        else:
            string_list = self._create_string_list()
        string = self._create_string(string_list)
        out.append(string)
