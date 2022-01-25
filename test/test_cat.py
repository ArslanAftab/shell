import unittest
from shell import eval


class TestCAT(unittest.TestCase):
    def test_cat_single_file(self):
        result = []
        eval('cat test/test_files/file5.txt', result)
        expected = [
            'apple\napple\nApple\nlemon\norange\norange\nlemon \napple\norange\napple\napple\n']
        self.assertEqual(result, expected)

    def test_cat_multiple_files(self):
        result = []
        eval('cat test/test_files/file1.txt test/test_files/file3.txt test/test_files/file5.txt', result)
        expected = [
            'hello\\n\nline\nsecond\nthird \nfourth\nlast line\napple\napple\nApple\nlemon\norange\norange\nlemon \napple\norange\napple\napple\n']
        self.assertEqual(result, expected)

    def test_cat_n_flag_single_file(self):
        result = []
        eval('cat -n test/test_files/file6.txt', result)
        expected = [
            '       1  AAA\n       2  BBB\n       3  AAA\n       4  aaa\n']
        self.assertEqual(result, expected)

    def test_cat_b_flag_single_file(self):
        result = []
        eval('cat -b test/test_files/file6.txt', result)
        expected = [
            '       1  AAA\n       2  BBB\n       3  AAA\n       4  aaa\n']
        self.assertEqual(result, expected)

    def test_cat_e_flag_single_file(self):
        result = []
        eval('cat -e test/test_files/file6.txt', result)
        expected = ['AAA$\nBBB$\nAAA$\naaa\n']
        self.assertEqual(result, expected)

    def test_cat_ne_flag_single_file(self):
        result = []
        eval('cat -n -e test/test_files/file6.txt', result)
        expected = [
            '       1  AAA$\n       2  BBB$\n       3  AAA$\n       4  aaa\n']
        self.assertEqual(result, expected)

    def test_cat_b_flag_multiple_flags(self):
        result = []
        eval('cat -b test/test_files/file1.txt test/test_files/file6.txt', result)
        expected = [
            '       1  hello\\n\n       2  AAA\n       3  BBB\n       4  AAA\n       5  aaa\n']
        self.assertEqual(result, expected)

    def test_cat_n_flag_multiple_flags(self):
        result = []
        eval('cat -n test/test_files/file1.txt test/test_files/file6.txt', result)
        expected = [
            '       1  hello\\n\n       2  AAA\n       3  BBB\n       4  AAA\n       5  aaa\n']
        self.assertEqual(result, expected)

    def test_cat_e_flag_multiple_flags(self):
        result = []
        eval('cat -e test/test_files/file1.txt test/test_files/file6.txt', result)
        expected = ['hello\\n$\nAAA$\nBBB$\nAAA$\naaa\n']
        self.assertEqual(result, expected)

    def test_safe_cat_invalid_file(self):
        result = []
        self.assertRaises(
            Exception, eval, 'cat: test_files/file7.txt: No such file or directory', result)

    def test_unsafe_cat_invalid_file(self):
        result = []
        eval('_cat test_files/file7.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cat: test_files/file7.txt: No such file or directory'])


if __name__ == '__main__':
    unittest.main()
