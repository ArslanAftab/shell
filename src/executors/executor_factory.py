from executors.cut import CUTExecutor
from executors.find import FINDExecutor
from executors.ls import LSExecutor
from executors.echo import ECHOExecutor
from executors.pwd import PWDExecutor
from executors.cd import CDExecutor
from executors.grep import GREPExecutor
from executors.cat import CATExecutor
from executors.head import HEADExecutor
from executors.sort import SORTExecutor
from executors.tail import TAILExecutor
from executors.uniq import UNIQExecutor


class ExecutorFactory():

    def __init__(self, function_dict: dict):
        self._args = function_dict['argument_list']
        self.function = function_dict['function']
        self._options = function_dict['options']
        self.unsafe = False
        self._commands_dict = {'pwd': PWDExecutor,
                               'echo': ECHOExecutor,
                               'ls': LSExecutor,
                               'cd': CDExecutor,
                               'grep': GREPExecutor,
                               'cat': CATExecutor,
                               'head': HEADExecutor,
                               'tail': TAILExecutor,
                               'sort': SORTExecutor,
                               'uniq': UNIQExecutor,
                               'cut': CUTExecutor,
                               'find': FINDExecutor}

    @staticmethod
    def get_entered_letters(function, options):
        'Get letters entered in options'
        if function == 'echo':
            return []
        # Options may have been entered seperately or as a block
        if len(options) == 1:
            return list(options[0]['letter'])
        return [flag_pair['letter'] for flag_pair in options]

    def get_command_executor(self, parsed_options):
        if self.function[0] == '_':
            self.unsafe = True
            self.function = self.function[1:]

        if self.function in self._commands_dict:
            return self._commands_dict[self.function](parsed_options, self._args, self.unsafe)
        else:
            return None
