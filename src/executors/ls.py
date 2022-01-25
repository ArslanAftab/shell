'Class and associated variables for executing ls commands'
import os
from os import listdir
import time
import globals.errors as e


class LSExecutor():
    'Class for executing ls commands'

    error = e.LS_OPTION_ERROR
    # Booleans represent whether the flag can take a number argument
    valid_flags = {'l': False, 'a': False}

    def __init__(self, options, args: list, unsafe: bool):
        self._args = args
        self.unsafe = unsafe
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        # Only real directories can be given as arguments
        for arg in self._args:
            if not os.path.isdir(arg):
                e.output_error(
                    self.unsafe, e.MISSING.format('ls', arg), out)
                return False
        return True

    def _output(self, directory: str, out) -> None:
        'Add the output text to the shell output deque'
        for item in listdir(directory):
            # -a flag must be present to allow hidden files to be shown
            if 'a' not in self.entered_letters and item.startswith('.'):
                continue

            # If the -l flag is present, extra info is also shown for each item
            if 'l' in self.entered_letters:
                modification_time = time.ctime(
                    os.path.getmtime(f'{directory}/{item}'))
                byte_size = os.path.getsize(f'{directory}/{item}')
                out.append(f'{byte_size}   {modification_time}          ')
            out.append(f'{item}\n')

        # Even in the root directory, . and .. are present in output if -a is present
        if 'a' in self.entered_letters:
            out.append('.\n')
            out.append('..\n')

    def execute(self, out) -> None:
        'Check arguments and execute command'
        # If no location is given, the cwd is used
        if self._args == []:
            self._output(os.getcwd(), out)
        else:
            # If multiple directories were given, the name is also outputted
            for directory in self._args:
                if len(self._args) > 1:
                    out.append(f'{directory}:\n')
                self._output(directory, out)
                out.append('\n')
            # Remove the final \n character
            out.pop()
