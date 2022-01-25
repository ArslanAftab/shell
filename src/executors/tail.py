'Class and associated variables for executing tail commands'
from executors.head_tail import HEADTAILExecutor
import globals.errors as e


class TAILExecutor(HEADTAILExecutor):
    'Child class of HEADTAILExecutor for executing tail commands'
    error = e.TAIL_OPTION_ERROR

    def check_arguments(self, out):
        'Check arguments are valid'
        return HEADTAILExecutor.check_arguments(self, 'tail', out)

    def execute(self, out):
        'Check arguments and execute command'
        HEADTAILExecutor.execute(self, out, 'tail')
