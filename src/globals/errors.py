'Global variable and functions for use in error handling'
MISSING = '{}: {}: No such file or directory\n'
INVALID_LINES = '{}: invalid number of lines: "{}"\n'
REQUIRED_ARGUMENT = '{}: option requires an argument -- "{}"\n'
INVALID_ARGUMENT = '{}: Invalid argument\n'
IS_DIRECTORY = '{}: {}: Is a directory\n'

CD_ARGUMENT_ERROR = 'cd: too many arguements\n'
PWD_ARGUMENT_ERROR = 'pwd: too many arguments\n'

GREP_USAGE_ERROR = 'usage: grep [-R] [-m num] [pattern] [file ...]\n'
FIND_USAGE_ERROR = 'usage: find [path] [-name] [file ...]\n'

CUT_OPTION_ERROR = 'cut: bad option: {}\n'
CAT_OPTION_ERROR = 'cat: bad option: {}\n'
CD_OPTION_ERROR = 'cd: bad option: {}\n'
GREP_OPTION_ERROR = 'grep: illegal option -- {}\nusage: grep [-R] [-m num] [pattern] [file ...]\n'
HEAD_OPTION_ERROR = 'head: illegal option -- {}\nusage: head [-cn]... [FILE]...\n'
TAIL_OPTION_ERROR = 'tail: illegal option -- {}\nusage: tail [-cn]... [FILE]...\n'
LS_OPTION_ERROR = 'ls: illegal option -- {}\nusage: ls [-la] [directory ...]\n'
PWD_OPTION_ERROR = 'pwd: bad option: {}\n'
SORT_OPTION_ERROR = 'sort: invalid option -- {}\n'
UNIQ_OPTION_ERROR = 'uniq: invalid option -- {}\n'
SORT_CANNOT_READ_ERROR = 'sort: cannot read: {}: No such file or directory\n'
HEAD_TAIL_LINES_ERROR = '{}: invalid number of lines: {}\n'
CUT_DECREASING_RANGE_ERROR = 'cut: invalid decreasing range\n'
CUT_INVALID_POS_ERROR = 'cut: invalid byte/character position {}\n'
CUT_SPECIFY_ERROR = 'cut: you must specify a list of bytes, characters, or fields\n'
CUT_ONE_TYPE_ERROR = 'cut: only one type of list may be specified\n'
CUT_NUMBERED_ERROR = 'cut: byte/character positions are numbered from 1\n'
CUT_INVALID_RANGE = 'cut: invalid byte or character range\n'


def output_error(unsafe: bool, message: str, stream) -> None:
    'Change handling method based on whether invoking executor was safe or unsafe'
    if unsafe:
        stream.append(message)
    else:
        raise Exception(message)
