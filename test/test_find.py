import unittest
from shell import eval
import os


class TestFIND(unittest.TestCase):
    # Tests that should pass
    def test_find(self):
        result = []
        eval("find -name 'requirements.txt'", result)
        expected = set(os.popen("find -name 'requirements.txt'").readlines())
        self.assertEqual(set(result), expected)
    
    def test_find_no_backticks(self):
        result = []
        eval("find -name requirements.txt", result)
        expected = set(os.popen("find -name 'requirements.txt'").readlines())
        self.assertEqual(set(result), expected)
    
    
    def test_find_dir(self):
        result = []
        eval("find /comp0010/test/test_files -name '*.txt'", result)
        expected = set(os.popen("find /comp0010/test/test_files -name '*.txt'").readlines())
        self.assertEqual(set(result), expected)
    
    def test_find_globbing(self):
        result = []
        eval("find -name '*.txt'", result)
        expected = set(os.popen("find -name '*.txt'").readlines())
        self.assertEqual(set(result), expected)

    # Tests that throw an error  
    def test_find_too_many_args(self):
        result = []
        self.assertRaises(Exception, eval, "find -name /comp0010 '*.txt' 'anotherfile.txt'", result)    

    # Safe vs Unsafe cd
    def test_unsafe_find_no_args(self):
        result = []
        eval("_find", result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['usage: find [path] [-name] [file ...]'])
    
    def test_unsafe_find_no_args2(self):
        result = []
        eval("_find -name", result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['usage: find [path] [-name] [file ...]'])
    
    def test_unsafe_find_bad_option_with_dir(self):
        result = []
        eval("_find /comp0010/test/test_files '*.txt'", result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['usage: find [path] [-name] [file ...]'])

    def test_unsafe_find_bad_option(self):
        result = []
        eval("_find -badoption '*.txt'", result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['usage: find [path] [-name] [file ...]'])
    
    def test_unsafe_find_missing_dir(self):
        result = []
        eval("_find /comp0010/missing -name '*.txt'", result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['find: /comp0010/missing: No such file or directory'])

if __name__ == '__main__':
    unittest.main()

