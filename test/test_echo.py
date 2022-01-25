import unittest
from shell import eval
import re
import os
from collections import deque


class TestECHO(unittest.TestCase):
    def test_echo(self):
        result = []
        eval('echo hello', result)
        self.assertEqual(list({r.strip() for r in result}), ['hello'])

    def test_echo_multiple_arguments(self):
        result = []
        eval('echo hello world', result)
        self.assertEqual(list({r.strip() for r in result}), ['hello world'])

    def test_echo_options(self):
        result = []
        eval('echo -a', result)
        self.assertEqual(list({r.strip() for r in result}), ['-a'])

    def test_echo_options_args(self):
        result = []
        eval('echo -a hello', result)
        self.assertEqual(list({r.strip() for r in result}), ['-a hello'])

    def test_echo_quoted(self):
        result = []
        eval('echo "hello world"', result)
        self.assertEqual(list({r.strip() for r in result}), ['hello world'])

    def test_echo_quoted_unclosed(self):
        result = []
        eval('echo \'hello world', result)
        self.assertEqual(list({r.strip() for r in result}), ['hello world'])

    def test_echo_disabled_double_quotes(self):
        result = []
        eval('echo \'\"\"\'', result)
        self.assertEqual(list({r.strip() for r in result}), ['\"\"'])


if __name__ == '__main__':
    unittest.main()
