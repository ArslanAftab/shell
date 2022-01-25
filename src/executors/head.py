'Class and associated variables for executing head commands'
from executors.head_tail import HEADTAILExecutor
import globals.errors as e


class HEADExecutor(HEADTAILExecutor):
    'Child class of HEADTAILExecutor for executing head commands'
    error = e.HEAD_OPTION_ERROR

    def check_arguments(self, out):
        'Check arguments are valid'
        return HEADTAILExecutor.check_arguments(self, 'head', out)

    def execute(self, out):
        'Check arguments and execute command'
        HEADTAILExecutor.execute(self, out, 'head')
