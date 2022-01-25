'Class and associated variables for executing find commands'
import os
import globals.errors as e
from glob import glob


class FINDExecutor():
    'Class for executing find commands'

    error = e.FIND_USAGE_ERROR
    # Booleans represent whether the flag can take a number argument
    valid_flags = {}

    def __init__(self, options, args: list, unsafe: bool):
        self._args = args
        self.unsafe = unsafe
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []
        self._path = os.getcwd()
        self._prepend = ''

    def check_globbing(self, argument):
        'Search all globs, recursively in subdirs too'
        if argument[0] == "'":
            # Strip quote
            argument = argument[1:-1]

        # Allows searching of subdirs
        temp_path = f'**{os.sep}{argument}'
        if self._path != os.getcwd():
            #I.e. user specified subdir to find in
            temp_path = f'{self._path}{os.sep}' + temp_path

        globbed_argument = glob(temp_path, recursive=True)
        return globbed_argument

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        if self.handle_name(out):
            if self._args == []:
                e.output_error(self.unsafe, self.error, out)
                return False
            if not os.path.isdir(self._path):
                e.output_error(
                    self.unsafe, e.MISSING.format('find', self._path), out)
                return False
        else:
            # i.e. handlename failed.
            return False
        return True

    def handle_name(self, out) -> bool:
        # -name was picked up as an arg
        if self.options == []:
            if '-name' not in self._args:
                # i.e. find dir name.txt, without [-name]
                e.output_error(self.unsafe, self.error, out)
                return False
            self._args.remove('-name')
            self._path = self._args[0]
            self._args.pop(0)
        # -name was picked up as an flag
        else:
            for option_dict in self.options:
                if option_dict['letter'] != 'name':
                    # i.e. find -badflag name.txt
                    e.output_error(self.unsafe, self.error, out)
                    return False
            # not given a dir, results are './...'
            self._prepend = f'.{os.sep}'
        return True

    def execute(self, out) -> None:
        'Check arguments and execute command'
        # too many files given to find
        if len(self._args) > 2:
            e.output_error(self.unsafe, self.error, out)
        else:
            list_globs = self.check_globbing(self._args[0])
            for arg in list_globs:
                out.append(f'{self._prepend}{arg}\n')
