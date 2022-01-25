'Class and associated variables for executing grep commands'
import os
import globals.errors as e
import globals.file_ops as fo


class GREPExecutor():
    'Class for executing grep commands'

    error = e.GREP_OPTION_ERROR
    # Booleans represent whether the flag can take a number argument
    valid_flags = {'R': False, 'm': True}

    def __init__(self, options, args: list, unsafe: bool):
        self.unsafe = unsafe
        self._args: list = args
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        # Grep must be given a search value and at least one location
        if len(self._args) < 2:
            e.output_error(self.unsafe, e.GREP_USAGE_ERROR, out)
            return False

        for arg in self._args[1:]:
            # Directories can only be given as locations if the -R flag is present
            if 'R' not in self.entered_letters and os.path.isdir(arg):
                e.output_error(
                    self.unsafe, e.IS_DIRECTORY.format('grep', arg), out)
                return False

            # All locations must be real
            if 'R' in self.entered_letters:
                if not os.path.isfile(arg) and not os.path.isdir(arg):
                    e.output_error(
                        self.unsafe, e.MISSING.format('grep', arg), out)
                    return False
        return True

    def _output(self, out, matches: list) -> None:
        'Add the output text to the shell output deque'
        if 'm' in self.entered_letters:
            for flag_dict in self.options:
                if 'm' in flag_dict['letter']:
                    max_matches = int(flag_dict['number'])
            matches = matches[:max_matches]
        out.extend(matches)

    def execute(self, out) -> None:
        'Execute the command'
        content = self._args[0]
        locations = self._args[1:]
        matches = []

        for location in locations:
            if os.path.isdir(location):
                matches += fo.search_directory(content, location)
            elif os.path.isfile(location):
                # If multiple locations are given, the search_file() function appends the file name
                matches += fo.search_file(content,
                                          location, len(locations) > 1)
            else:
                e.output_error(self.unsafe, e.MISSING.format(
                    'grep', location), out)

        self._output(out, matches)
