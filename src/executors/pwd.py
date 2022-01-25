'Class and associated variables for executing pwd commands'
import os
import globals.errors as e


class PWDExecutor():
    'Class for executing pwd commands'

    error = e.PWD_OPTION_ERROR
    valid_flags = {}

    def __init__(self, options, args: bool, unsafe: bool):
        self._args = args
        self.unsafe = unsafe
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []

    def check_arguments(self, out):
        'Check arguments are valid'
        # pwd must take no arguments
        if len(self._args) != 0:
            e.output_error(self.unsafe, e.PWD_ARGUMENT_ERROR, out)
            return False
        return True

    @staticmethod
    def execute(out):
        'Execute command'
        out.append(f'{os.getcwd()}\n')
