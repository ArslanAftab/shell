import unittest
from shell import eval
import re
import os
from collections import deque


class TestSORT(unittest.TestCase):
    def test_sort(self):
        result = []
        eval('sort /comp0010/test/test_files/file5.txt', result)
        expected = [
            'Apple\napple\napple\napple\napple\napple\nlemon\nlemon \norange\norange\norange\n']
        self.assertEqual(result, expected)

    def test_sort_multiple_arguments(self):
        result = []
        eval('sort /comp0010/test/test_files/file3.txt /comp0010/test/test_files/file5.txt /comp0010/test/test_files/file6.txt', result)
        expected = [
            'AAA\nAAA\nApple\nBBB\naaa\napple\napple\napple\napple\napple\nfourth\nlast line\nlemon\nlemon \nline\norange\norange\norange\nsecond\nthird \n']
        self.assertEqual(result, expected)

    def test_sort_no_final_newline(self):
        result = []
        eval('sort /comp0010/test/test_files/file4.txt', result)
        expected = ['\nPizza\n']
        self.assertEqual(result, expected)

    def test_sort_reversed(self):
        result = []
        eval('sort -r /comp0010/test/test_files/file3.txt', result)
        expected = ['third \nsecond\nline\nlast line\nfourth\n']
        self.assertEqual(result, expected)

    def test_sort_invalid_file(self):
        result = []
        self.assertRaises(
            Exception, eval, 'sort: cannot read: /comp0010/test_files/file7.txt: No such file or directory', result)

    def test_unsafe_sort_invalid_file(self):
        result = []
        eval('_sort /comp0010/test_files/file7.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['sort: cannot read: /comp0010/test_files/file7.txt: No such file or directory'])


if __name__ == '__main__':
    unittest.main()
