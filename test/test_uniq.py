import unittest
from shell import eval
import os

class TestUNIQ(unittest.TestCase):
    # Tests that should pass
    def test_uniq(self):
        result = []
        eval('uniq /comp0010/test/test_files/file5.txt', result)
        result = result[0].splitlines(True)
        expected = os.popen('uniq /comp0010/test/test_files/file5.txt').readlines()
        self.assertEqual(result, expected)
    
    def test_uniq_count(self):
        result = []
        eval('uniq -c /comp0010/test/test_files/file5.txt', result)
        result = result[0].splitlines(True)
        expected = os.popen('uniq -c /comp0010/test/test_files/file5.txt').readlines()
        self.assertEqual(result, expected)

    def test_uniq_ignore_case(self):
        result = []
        eval('uniq -i /comp0010/test/test_files/file5.txt', result)
        result = result[0].splitlines(True)
        expected = os.popen('uniq -i /comp0010/test/test_files/file5.txt').readlines()
        self.assertEqual(result, expected)
    
    def test_uniq_unique(self):
        result = []
        eval('uniq -u /comp0010/test/test_files/file5.txt', result)
        result = result[0].splitlines(True)
        expected = os.popen('uniq -u /comp0010/test/test_files/file5.txt').readlines()
        self.assertEqual(result, expected)

    def test_uniq_duplicate(self):
        result = []
        eval('uniq -d /comp0010/test/test_files/file5.txt', result)
        result = result[0].splitlines(True)
        expected = os.popen('uniq -d /comp0010/test/test_files/file5.txt').readlines()
        self.assertEqual(result, expected)

    # Tests that throw an error  
    def test_uniq_no_args(self):
        result = []
        self.assertRaises(Exception, eval, 'uniq', result)

    # Safe vs Unsafe cd
    def test_unsafe_uniq_invalid_file(self):
        result = []
        eval('_uniq /comp0010/blah.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['uniq: /comp0010/blah.txt: No such file or directory'])

    def test_unsafe_uniq_uniqe_duplicated(self):
        result = []
        eval('_uniq -ud /comp0010/test/test_files/file5.txt', result)
        result = result[0].splitlines(True)
        self.assertEqual(list({r.strip() for r in result}),
                         ['uniq: invalid option -- ud'])

if __name__ == '__main__':
    unittest.main()

