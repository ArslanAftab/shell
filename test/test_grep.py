import unittest
from shell import eval
import re
import os
from collections import deque


class TestGREP(unittest.TestCase):
    def test_grep_single_location(self):
        result = []
        eval('grep eval /comp0010/src/shell.py', result)
        expected = set(
            os.popen('grep eval /comp0010/src/shell.py').readlines())
        self.assertEqual(set(result), expected)

    def test_grep_no_location(self):
        result = []
        self.assertRaises(Exception, eval, 'grep eval', result)

    def test_unsafe_grep_no_location(self):
        result = []
        eval('_grep eval', result)
        self.assertEqual(list({r.strip() for r in result}), [
                         'usage: grep [-R] [-m num] [pattern] [file ...]'])

    def test_grep_multiple_locations(self):
        result = []
        eval('grep and /comp0010/src/shell.py /comp0010/src/executors/grep.py', result)
        expected = set(
            os.popen('grep and /comp0010/src/shell.py /comp0010/src/executors/grep.py').readlines())
        self.assertEqual(set(result), expected)

    def test_grep_missing_location(self):
        result = []
        self.assertRaises(Exception, eval, 'grep text missing.txt', result)

    def test_unsafe_grep_missing_location(self):
        result = []
        eval('_grep text missing.txt', result)
        self.assertEqual(list({r.strip() for r in result}), [
                         'grep: missing.txt: No such file or directory'])

    def test_grep_R(self):
        result = []
        eval('grep -R eval /comp0010/src', result)
        # -I flag is included to suppress binary files
        expected = set(os.popen('grep -RI eval /comp0010/src').readlines())
        self.assertEqual(set(result), expected)

    def test_grep_no_R_directory(self):
        result = []
        self.assertRaises(Exception, eval, 'grep eval /comp0010/src', result)

    def test_unsafe_grep_no_R_directory(self):
        result = []
        eval('_grep eval /comp0010/src', result)
        self.assertEqual(list({r.strip() for r in result}), [
                         'grep: /comp0010/src: Is a directory'])

    def test_grep_R_missing(self):
        result = []
        self.assertRaises(Exception, eval, 'grep -R text missing.txt', result)

    def test_unsafe_grep_R_missing(self):
        result = []
        eval('_grep -R text missing.txt', result)
        self.assertEqual(list({r.strip() for r in result}), [
                         'grep: missing.txt: No such file or directory'])

    def test_grep_m(self):
        result = []
        eval('grep -m 3 eval /comp0010/src/shell.py', result)
        expected = set(
            os.popen('grep -m 3 eval /comp0010/src/shell.py').readlines())
        self.assertEqual(set(result), expected)

    def test_grep_R_m(self):
        result = []
        eval('grep -R -m 3 eval /comp0010/src', result)
        # -I flag is included to suppress binary files
        expected = set(
            os.popen('grep -RI -m 3 eval /comp0010/src').readlines())
        self.assertEqual(set(result), expected)

    def test_grep_regular_expression(self):
        result = []
        eval('grep \'ev..\' /comp0010/src/shell.py', result)
        expected = set(
            os.popen('grep ev.. /comp0010/src/shell.py').readlines())
        self.assertEqual(set(result), expected)


if __name__ == '__main__':
    unittest.main()
