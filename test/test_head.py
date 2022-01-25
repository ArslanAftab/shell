import unittest
from shell import eval


class TestHEAD(unittest.TestCase):
    def test_head(self):
        result = []
        eval('head /comp0010/test/test_files/file3.txt', result)
        expected = [
            'line\nsecond\nthird \nfourth\nlast line\n']
        self.assertEqual(result, expected)

    def test_head_long_file(self):
        result = []
        eval('head /comp0010/test/test_files/long_file.txt', result)
        expected = [
            'start of file\n1\n2\n3\n4\n5\n6\n7\n8\n9\n']
        self.assertEqual(result, expected)

    def test_head_multiple_arguments(self):
        result = []
        eval('head /comp0010/test/test_files/file2.txt /comp0010/test/test_files/file3.txt /comp0010/test/test_files/long_file.txt', result)
        expected = ['==> /comp0010/test/test_files/file2.txt <==\nworld\n==> /comp0010/test/test_files/file3.txt <==\nline\nsecond\nthird \nfourth\nlast line\n==> /comp0010/test/test_files/long_file.txt <==\nstart of file\n1\n2\n3\n4\n5\n6\n7\n8\n9\n']
        self.assertEqual(result, expected)

    def test_head_n0(self):
        result = []
        eval('head -n 0 /comp0010/test/test_files/file1.txt', result)
        expected = ['']
        self.assertEqual(result, expected)

    def test_head_n5(self):
        result = []
        eval('head -n 5 /comp0010/test/test_files/long_file.txt', result)
        expected = [
            'start of file\n1\n2\n3\n4\n']
        self.assertEqual(result, expected)

    def test_head_n_greater_than_file_length(self):
        result = []
        eval('head -n 15 /comp0010/test/test_files/file5.txt', result)
        expected = [
            'apple\napple\nApple\nlemon\norange\norange\nlemon \napple\norange\napple\napple\n'
        ]
        self.assertEqual(result, expected)

    def test_head_q_one_file(self):
        result = []
        eval('head -q /comp0010/test/test_files/file3.txt', result)
        expected = [
            'line\nsecond\nthird \nfourth\nlast line\n']
        self.assertEqual(result, expected)

    def test_head_n_q_multiple_arguments(self):
        result = []
        eval('head -n 5 -q /comp0010/test/test_files/file2.txt /comp0010/test/test_files/file5.txt /comp0010/test/test_files/file6.txt', result)
        expected = [
            'world\napple\napple\nApple\nlemon\norange\nAAA\nBBB\nAAA\naaa\n']
        self.assertEqual(result, expected)

    def test_head_invalid_lines(self):
        result = []
        self.assertRaises(
            Exception, eval, 'head: invalid number of lines: /comp0010/test/test_files/file1.txt', result)

    def test_unsafe_head_invalid_lines(self):
        result = []
        eval('_head -n /comp0010/test/test_files/file1.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['head: invalid number of lines: /comp0010/test/test_files/file1.txt'])

    def test_head_invalid_file(self):
        result = []
        self.assertRaises(
            Exception, eval, 'head: /comp0010/test/test_files/file7.txt: No such file or directory', result)

    def test_unsafe_head_invalid_file(self):
        result = []
        eval('_head /comp0010/test/test_files/file7.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['head: /comp0010/test/test_files/file7.txt: No such file or directory'])


if __name__ == '__main__':
    unittest.main()
