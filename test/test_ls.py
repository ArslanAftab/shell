import unittest
from shell import eval
import re
import os
from collections import deque


class TestLS(unittest.TestCase):
    def test_ls(self):
        result = []
        eval('ls', result)
        expected = set(os.popen('ls').readlines())
        self.assertEqual(set(result), expected)

    def test_ls_a(self):
        result = []
        eval('ls -a', result)
        expected = set(os.popen('ls -a').readlines())
        self.assertEqual(set(result), expected)

    '''
    def test_ls_l(self):
        result = []
        eval('ls -l system_test', result)
        self.assertEqual(
            result, ['20404   Tue Dec 14 15:30:46 2021          ', 'tests.py\n'])
    '''
    '''
    def test_ls_l_a(self):
        result = []
        eval('ls -al system_test', result)
        self.assertEqual(
            result, ['20404   Tue Dec 14 15:30:46 2021          ', 'tests.py\n', '.\n', '..\n'])
    '''

    def test_ls_dir(self):
        result = []
        eval('ls /comp0010/src', result)
        expected = set(os.popen('ls /comp0010/src').readlines())
        self.assertEqual(set(result), expected)

    def test_ls_missing_dir(self):
        result = []
        self.assertRaises(Exception, eval, 'ls missing', result)

    def test_unsafe_ls_missing_dir(self):
        result = []
        eval('_ls missing-dir', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['ls: missing-dir: No such file or directory'])

    def test_ls_multiple_dir(self):
        result = []
        eval('ls /comp0010/src/executors /comp0010/src/globals', result)
        expected = set(
            os.popen('ls /comp0010/src/executors /comp0010/src/globals').readlines())
        self.assertEqual(set(result), expected)


if __name__ == '__main__':
    unittest.main()
