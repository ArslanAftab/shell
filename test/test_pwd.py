import unittest
from shell import eval
import re
import os
from collections import deque


class TestPWD(unittest.TestCase):
    def test_pwd(self):
        result = []
        eval('pwd', result)
        expected = set(os.popen('pwd').readlines())
        self.assertEqual(set(result), expected)

    def test_pwd_args(self):
        result = []
        self.assertRaises(Exception, eval, 'pwd a', result)

    def test_unsafe_pwd_args(self):
        result = []
        eval('_pwd a', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['pwd: too many arguments'])


if __name__ == '__main__':
    unittest.main()
