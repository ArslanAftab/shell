'Class and associated variables for pasring user input'
from parsy import regex, string, seq

spaces = regex(r'\s*')


class Parser:
    'Class for parsing user input'

    @staticmethod
    def initial_parse(text: str):
        'Parse the initial user input'
        bracket = regex(r'(>>|>|<){1}') << spaces.optional()

        safe_functions_list = ['cd', 'ls', 'echo',
                               'pwd', 'cat', 'head',
                               'tail', 'grep', 'sort',
                               'uniq', 'cut', 'find']

        unsafe_functions_list = ['_' + func for func in safe_functions_list]

        safe_function = regex(
            r'|'.join(safe_functions_list)) << spaces.optional()

        unsafe_function = regex(
            r'|'.join(unsafe_functions_list)) << spaces.optional()

        function = unsafe_function | safe_function

        options = regex(
            r'(-([a-zA-Z]{2,}\s*\d*(-\d*)?))|(-[a-zA-Z]\s*\d*(?!(-\d*|(,\d+)+))\s*)*') << spaces.optional()

        single_argument = regex(r'[^\n|;><]*')

        redirection = seq(
            bracket=bracket, location=single_argument) << spaces.optional()

        command = seq(function=function, options=options.optional(),
                      argument_list=single_argument.optional(),
                      redirection=redirection.many())

        pipe_list = command.sep_by(spaces + string('|') + spaces, min=2)

        item = pipe_list.tag('piped_list') | command.tag('single_command')

        entry = item.sep_by(spaces + string(';') + spaces)

        return entry.parse(text)

    @staticmethod
    def arguments_parse(text: str):
        'Reparse arguments to check proper formatting'
        if text is None:
            return []

        # Argument format following language bnf
        single_quoted = regex(r'\'[^\n\']*\'')
        back_quoted = regex('`[^\n`]*`')
        double_quoted = string('"') >> regex(
            r'((`[^\n`]*`)|([^\n"`]))*') << string('"')

        quoted_argument = single_quoted | back_quoted | double_quoted
        single_argument = regex(r'[^\n\s;|<>"\'`]+')
        argument = quoted_argument | single_argument
        argument_list = argument.sep_by(spaces) << spaces.optional()

        # Catch errors and return None to show unparsibility rather than raising ParseError
        try:
            parse = argument_list.parse(text)
            return parse
        # Can't be sure of the exception that parsy will throw
        except:
            return None

    @staticmethod
    def options_parse(text: str):
        'Reparse options to check proper formatting'
        if text is None:
            return []

        single_number = regex(r'[0-9]+') << spaces.optional()
        number_range = regex(r'[0-9]+-[0-9]+') << spaces.optional()

        number = number_range | single_number

        flag_block = seq(letter=string('-') >> regex(r'[a-zA-Z]{2,}') << spaces.optional(),
                         number=number.optional())

        single_flag = seq(letter=string('-') >> regex(
            r'[a-zA-Z]') << spaces.optional(), number=number.optional())

        flag_list = single_flag.sep_by(spaces)

        new_options = flag_block | flag_list

        # Catch errors and return None to show unparsibility rather than raising ParseError
        try:
            parse = new_options.parse(text)
            return parse
        # Can't be sure of the exception that parsy will throw
        except:
            return None
