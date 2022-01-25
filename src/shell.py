'Shell'
import sys
import os
from collections import deque
from glob import glob
import re
from parse import Parser
from executors.executor_factory import ExecutorFactory
import globals.file_ops as fo
import globals.errors as e


def check_single_flag(cmd, flag_dict, out):
    'Check single flag validity'
    if flag_dict['number'] is not None and cmd.valid_flags[flag_dict['letter']] is False:
        e.output_error(
            cmd.unsafe, cmd.error.format(flag_dict['letter']), out)
        return False
    return True


def check_flag_block(cmd, flag_dict, out):
    'Check flag block validity'
    if flag_dict['number'] is not None and cmd.valid_flags[flag_dict['letter'][-1]] is False:
        e.output_error(
            cmd.unsafe, cmd.error.format(flag_dict['letter']), out)
        return False
    return True


def check_flags(function, cmd, out):
    'Check flag validity'
    # Echo can not throw flag errors so shouldn't check
    # Find does not have a flag implemented, apart from -name test
    if function in ['echo', 'find']:
        return True
    # Defined in shell.py to stop duplication of code in each executor
    for letter in cmd.entered_letters:
        if letter not in cmd.valid_flags:
            e.output_error(
                cmd.unsafe, cmd.error.format(letter), out)
            return False

    # Number checks should be handled differently if a flag block was entered
    for flag_dict in cmd.options:
        if len(flag_dict['letter']) == 1:
            if not check_single_flag(cmd, flag_dict, out):
                return False

        if len(flag_dict['letter']) > 1:
            if not check_flag_block(cmd, flag_dict, out):
                return False

    return True


def get_parsed_options(function_dict):
    'Get what will be given to the executor as options'
    # Echo takes no flags and so treats them like arguments
    # so they should not be reparsed into a dicitonary format
    raw_options = function_dict['options']
    if function_dict['function'] == 'echo':
        return raw_options
    return Parser().options_parse(raw_options)


def execute_command(function_dict, executor_factory, parsed_options, stream):
    'Execute the command'
    cmd = executor_factory.get_command_executor(parsed_options)
    # Output error if executor could not be found
    if cmd is None:
        stream.append(
            f'shell: command not found: {executor_factory.function}\n')
        return

    # Assign entered letter for options validity checks
    cmd.entered_letters = ExecutorFactory.get_entered_letters(
        executor_factory.function, cmd.options)

    # Check validity of given options and arguments
    if check_flags(executor_factory.function, cmd, stream) and cmd.check_arguments(stream):
        redirection = function_dict['redirection']
        output_redirection = [
            redirection_dict for redirection_dict in redirection if redirection_dict['bracket'] in ['>', '>>']]
        # Write execution output to a buffer and write to given file if redirection specified
        if output_redirection != []:
            buffer = []
            cmd.execute(buffer)
            for destination in output_redirection:
                fo.output_to_file(
                    buffer, destination['bracket'], destination['location'])
            del buffer[:]
        else:
            cmd.execute(stream)


def check_globbing(argument_list):
    'Check argument list for globbed arguments and replace them with the globs output'
    globbed_list = []
    for argument in argument_list:
        globbed_argument = glob(argument)
        globbed_list += globbed_argument if globbed_argument else [argument]
    return globbed_list


def check_backticks(argument_list):
    'Check argument list for arguments surrounded by backticks and pre-evaluate them'
    if isinstance(argument_list, str):
        argument_list = [argument_list]
    for i, arg in enumerate(argument_list):
        if '`' in arg:
            pattern = '.*`(.+)`.*'
            substring = re.search(pattern, arg).group(1)
            buffer = []
            eval(substring, buffer)
            argument_list[i] = arg.replace(
                '`'+substring+'`', ''.join(buffer).strip())
    return argument_list


def single_eval(function_dict, stream):
    'Evaluate the single command'
    # Parser should not parse arguments twice if the function is echo
    if function_dict['function'] != 'echo':
        function_dict['argument_list'] = Parser().arguments_parse(
            function_dict['argument_list'])
    # Pre-evaluate any arguments surrounded by backticks
    function_dict['argument_list'] = check_backticks(
        function_dict['argument_list'])
    # Amend arguments if globbed arguments exist
    if function_dict['function'] != 'find':
        function_dict['argument_list'] = check_globbing(
            function_dict['argument_list'])
    # Add content from input redirection as an argument
    redirection = function_dict['redirection']
    for redirection_dict in redirection:
        if redirection_dict['bracket'] == '<':
            function_dict['argument_list'].append(redirection_dict['location'])
    # Get the correct executor object, re-parse options and execute the command
    executor_factory = ExecutorFactory(function_dict)
    parsed_options = get_parsed_options(function_dict)
    # Output error if options cannot be parsed again, indicating incorrect format
    if parsed_options is None:
        e.output_error(executor_factory.unsafe,
                       f'{executor_factory.function}: Invalid options', stream)
    else:
        execute_command(function_dict, executor_factory,
                        parsed_options, stream)


def piped_eval(function_dict_list, stream):
    'Evaluate all commands in a pipe list'
    for i, function_dict in enumerate(function_dict_list[:-1]):
        # Write the output of each function a temporary file
        # and sets the temporary file name as an argument for the next function
        function_dict['redirection'].append(
            {'bracket': '>', 'location': 'pipe_temp_input.txt'})
        single_eval(function_dict, [])
        function_dict_list[i] = function_dict
        function_dict_list[i+1]['argument_list'] = ' '.join(
            (function_dict_list[i+1]['argument_list'] + ' pipe_temp_input.txt').split())
    # Execute the final single_command then delete the temporary file
    single_eval(function_dict_list[-1], stream)
    os.remove('pipe_temp_input.txt')


def eval(cmd_input, stream):
    'Evaluate the parsed input to cmdline'
    parsed_input = Parser().initial_parse(cmd_input)
    for command_tuple in parsed_input:
        if command_tuple[0] == 'single_command':
            single_eval(command_tuple[1], stream)
        elif command_tuple[0] == 'piped_list':
            piped_eval(command_tuple[1], stream)


def main():
    'Main function'
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        eval(sys.argv[2], out)
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque()
            eval(cmdline, out)
            while len(out) > 0:
                print(out.popleft(), end="")


if __name__ == "__main__":
    main()
