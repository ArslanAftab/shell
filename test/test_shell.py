import unittest
from shell import eval
from collections import deque
import os
from parsy import ParseError


class TestShell(unittest.TestCase):
    def test_shell_single_flag_invalid_number(self):
        result = []
        self.assertRaises(Exception, eval, 'ls -l3', result)

    def test_shell_unsafe_single_flag_invalid_number(self):
        result = []
        eval('_ls -l3', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['ls: illegal option -- l\nusage: ls [-la] [directory ...]'])

    def test_shell_flag_block(self):
        result = []
        eval('grep -Rm3 eval /comp0010/src/shell.py', result)
        expected = set(
            os.popen('grep -Rm3 eval /comp0010/src/shell.py').readlines())
        self.assertEqual(set(result), expected)

    def test_shell_flag_block_invalid_number(self):
        result = []
        self.assertRaises(Exception, eval, 'ls -la3', result)

    def test_shell_unsafe_flag_block_invalid_number(self):
        result = []
        eval('_ls -la3', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['ls: illegal option -- la\nusage: ls [-la] [directory ...]'])

    def test_shell_piped_list(self):
        result = []
        eval('ls /comp0010/ | grep src', result)
        expected = set(os.popen('ls /comp0010/ | grep src').readlines())
        self.assertEqual(set(result), expected)

    def test_shell_backticks(self):
        result = []
        eval('echo a`echo a`a', result)
        self.assertEqual(result, ['aaa\n'])

    def test_shell_input_redirection(self):
        result = []
        eval('grep eval < /comp0010/src/shell.py', result)
        expected = set(
            os.popen('grep eval < /comp0010/src/shell.py').readlines())
        self.assertEqual(set(result), expected)

    def test_shell_nonexistant_command(self):
        result = []
        self.assertRaises(ParseError, eval, 'non', result)

    def test_shell_unsafe_invalid_letter(self):
        result = []
        eval('_ls -b', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['ls: illegal option -- b\nusage: ls [-la] [directory ...]'])


if __name__ == "__main__":
    unittest.main()
