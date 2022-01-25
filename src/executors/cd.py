'Class and associated variables for executing cd commands'
import os
import globals.errors as e


class CDExecutor():
    'Class for executing cd commands'
    error = e.CD_OPTION_ERROR
    # cd doesn't take any flags
    valid_flags = {}

    def __init__(self, options, args: list, unsafe: bool):
        self._args = args
        self.unsafe = unsafe
        self._arg = None  # to avoid doing self._args[0]
        self._path = None
        self._rootcuts = ["", "~", "/"]
        # cd doesn't use either of these
        self.options = options
        self.entered_letters = []

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        if len(self._args) > 1:
            e.output_error(self.unsafe, e.CD_ARGUMENT_ERROR, out)
            return False
        # Prevent it being null
        self._arg = '' if not self._args else self._args[0] 
        return True

    @staticmethod
    def _check_directory(dir: str) -> bool:
        'Checks if directory exists'
        return os.path.isdir(dir)

    def execute(self, out) -> None:
        'Check arguments and execute command'
        self._path = os.getcwd()
        # Treat rootcuts the same
        if self._arg in self._rootcuts:
            os.chdir(os.path.expanduser('~'))
        elif self._arg == "..":
            os.chdir('..')
        else:
            dir = os.path.join(self._path, self._arg)
            if self._check_directory(dir):
                os.chdir(dir)
            else:
                e.output_error(self.unsafe, e.MISSING.format(
                    "cd", self._arg), out)
