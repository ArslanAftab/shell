'Class and associated variables for executing echo commands'


class ECHOExecutor():
    'Class for executing echo commands'
    error = ''
    valid_flags = {}

    def __init__(self, options, args: list, unsafe: bool):
        self._args: list = args
        self.unsafe = unsafe
        self.options = options
        self.entered_letters = []

    def check_arguments(self, out) -> bool:
        'Check arguments are valid'
        # out is unused however must be present for the method to be anonymously called
        # Can never be given bad arguements
        return True

    def execute(self, out) -> None:
        'Execute command'
        # out is unused however must be present for the method to be anonymously called
        string_list = []
        if self._args != ['']:
            # Formats arguments following the specification, removing " ' where necessary
            for args_string in self._args:
                if len(args_string) > 0 and args_string[0] == "\"" or args_string[0] == "\'":
                    if len(args_string.replace("\"", "").replace("\'", "")) == 0:
                        if args_string[0] == '\'' and args_string[-1] == '\'':
                            args_string = args_string.replace('\'', '')
                    else:
                        args_string = args_string.replace(
                            "\"", "").replace("\'", "")
                    string_list += [args_string]
                else:
                    args_string = args_string.replace(
                        "\"", "").replace("\'", "")
                    string_list += args_string.split()
        # Since echo has no flags, they are treated as arguments
        out.append(self.options + ' '.join(string_list) + '\n')
