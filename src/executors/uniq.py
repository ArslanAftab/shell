'Class and associated variables for executing uniq commands'
import os
import globals.file_ops as file_ops
import globals.errors as e


class UNIQExecutor():
    'Class for executing uniq commands'
    error = e.UNIQ_OPTION_ERROR
    valid_flags = {'c': False, 'd': False, 'u': False, 'i': False}

    def __init__(self, options, args: list, unsafe: bool):
        self._args = args
        self.unsafe = unsafe
        self.options = options if isinstance(options, list) else [options]
        self.entered_letters = []

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        for arg in self._args:
            if not os.path.isfile(arg):
                e.output_error(self.unsafe, e.MISSING.format('uniq', arg), out)
                return False
            # User cannot see both unique and distinct...
            if 'u' in self.entered_letters and 'd' in self.entered_letters:
                e.output_error(self.unsafe, self.error.format(''.join(
                    self.entered_letters)), out)
                return False
        return True

    def _string_counter(self, string_list: list) -> list:
        'Return a list of tuples, grouping lines and showing their count'
        string_list += '\n'
        previous = ''
        lines = []
        count = 1
        for line in string_list:
            # Reduced branching using custom comparison
            if self._cmp(line, previous):
                count += 1
            else:
                # When the line changes, we can store previous block
                lines.append((previous, count))
                count = 1
                previous = line
        lines.pop(0)
        return lines

    def _cmp(self, string1: str, string2: str) -> bool:
        'Used for case sensitivity'
        if 'i' not in self.entered_letters:
            return string1 == string2
        else:
            return string1.casefold() == string2.casefold()

    def _unpack_results(self, counted_lines: list) -> list:
        counted_lines = [line for line in counted_lines if line != ""]

        # Remove/Format counts into each line
        for index, (line, count) in enumerate(counted_lines):
            if 'c' in self.entered_letters:
                counted_lines[index] = self._add_line_number(line, count)
            else:
                counted_lines[index] = line
        return counted_lines

    def _filter_lines(self, lines: list) -> list:
        if 'd' in self.entered_letters and not 'u' in self.entered_letters:
            for index, (line, count) in enumerate(lines):
                if count <= 1:
                    # Replace uniques with '', i.e. hide them
                    lines[index] = ""
            return lines
        elif 'u' in self.entered_letters and not 'd' in self.entered_letters:
            for index, (line, count) in enumerate(lines):
                if count > 1:
                    # Replace duplicates with '', i.e. hide them
                    lines[index] = ""
            return lines
        return lines

    def _create_string(self) -> str:
        'Generates string by reading text in files'
        string_list = []
        for file_name in self._args:
            string_list += file_ops.get_file_line_list(file_name)

        # Group lines and count
        counted_lines = self._string_counter(string_list)

        # Filter by flag
        counted_lines = self._filter_lines(counted_lines)

        # Unpack according to count flag
        lines = self._unpack_results(counted_lines)

        return ''.join(lines)

    def _add_line_number(self, string, line_number):
        return f"      {line_number} {string}"

    def execute(self, out) -> None:
        'Check arguments and execute command'
        if len(self._args) == 0:
            e.output_error(self.unsafe, e.MISSING.format('uniq', ''), out)
        else:
            string = self._create_string()
        out.append(string)
