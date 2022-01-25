import unittest
from shell import eval
import os


class TestCD(unittest.TestCase):
    # Tests that should pass
    def test_cd_root(self):
        result = []
        eval('cd; pwd', result)
        os.chdir(os.path.expanduser('~'))
        self.assertEqual(list({r.strip() for r in result}), [os.getcwd()])

    def test_cd_existing_dir(self):
        result = []
        eval('cd /comp0010/src; pwd', result)
        os.chdir('/comp0010/src')
        self.assertEqual(list({r.strip() for r in result}), [os.getcwd()])

    def test_cd_parent_dir(self):
        result = []
        eval('cd /comp0010/src; cd ..; pwd', result)
        os.chdir('/comp0010/src')
        os.chdir('..')
        self.assertEqual(list({r.strip() for r in result}), [os.getcwd()])

    def test_cd_parent_dir2(self):
        result = []
        eval('cd ..; pwd', result)
        os.chdir('..')
        self.assertEqual(list({r.strip() for r in result}), [os.getcwd()])

    # Tests that throw an error

    def test_cd_too_many_args(self):
        result = []
        self.assertRaises(Exception, eval, 'cd usr arg arg ', result)

    def test_cd_invalid_flag(self):
        result = []
        self.assertRaises(Exception, eval, 'cd -a ', result)

    # Safe vs Unsafe cd

    def test_cd_non_existing_dir(self):
        result = []
        self.assertRaises(Exception, eval, 'cd missing', result)

    def test_safe_cd_too_many_args(self):
        result = []
        eval('_cd arg arg arg', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cd: too many arguements'])


if __name__ == '__main__':
    unittest.main()
