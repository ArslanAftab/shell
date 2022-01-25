'Class and associated variables for executing head/tail commands'
import os
import globals.errors as e
import globals.file_ops as file_ops


class HEADTAILExecutor():
    'Class for executing Head/Tail commands'

    # Booleans represent whether the flag can take a number argument
    valid_flags = {'n': True, 'q': False}

    def __init__(self, options, args: list, unsafe: bool):
        self.unsafe = unsafe
        self._args = args
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []

    def check_arguments(self, command, out) -> bool:
        'Check arguments are valid'
        for arg in self._args:
            # Each argument must be a valid filepath
            if not os.path.isfile(arg):
                e.output_error(
                    self.unsafe, e.MISSING.format(command, arg), out)
                return False
        return True

    def _create_string(self, command, num_of_lines) -> str:
        'Generates string by reading text in files as a list, and then joining to form a string'
        string = ""
        # Do not need to build a string for 0 lines
        if num_of_lines == 0:
            return string
        for file_name in self._args:
            # A title string is required if the -q flag is not present
            # and if there is more than one file to be read
            if "q" not in self.entered_letters and len(self._args) > 1:
                string += f"==> {file_name} <==\n"
            string_list = file_ops.get_file_line_list(
                file_name, command == "tail")[:num_of_lines]
            if command == "tail":
                string_list.reverse()
            # Ensure final line ends with a newline character
            if string_list[-1][-1] != "\n":
                string_list[-1] += "\n"
            string += ''.join(string_list)

        return string

    def _check_num_of_lines(self, command, out) -> int:
        '''Checks the number entered beside the -n flag if present, outputting an error
        and returning -1 if there is no number. Returns a default value of 10
        if the flag is not present.'''
        for flag_dict in self.options:
            if flag_dict['letter'] == 'n':
                if not flag_dict['number']:
                    e.output_error(
                        self.unsafe, e.HEAD_TAIL_LINES_ERROR.format(command, self._args[0]), out)
                    return -1
                num_of_lines = int(flag_dict['number'])
                return num_of_lines
        return 10

    def execute(self, out, command) -> None:
        'Execute the command'
        if len(self._args) == 0:
            string = input() + "\n"
        else:
            num_of_lines = self._check_num_of_lines(command, out)
            if num_of_lines == -1:
                return
            string = self._create_string(command, num_of_lines)

        out.append(string)
