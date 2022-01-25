import unittest
from shell import eval


class TestTAIL(unittest.TestCase):
    def test_tail(self):
        result = []
        eval('tail /comp0010/test/test_files/file3.txt', result)
        expected = [
            'line\nsecond\nthird \nfourth\nlast line\n']
        self.assertEqual(result, expected)

    def test_tail_long_file(self):
        result = []
        eval('tail /comp0010/test/test_files/long_file.txt', result)
        expected = [
            '17\n18\n19\n20\n21\n22\n23\n24\n25\nend of file\n']
        self.assertEqual(result, expected)

    def test_tail_multiple_arguments(self):
        result = []
        eval('tail /comp0010/test/test_files/file2.txt /comp0010/test/test_files/file3.txt /comp0010/test/test_files/long_file.txt', result)
        expected = ['==> /comp0010/test/test_files/file2.txt <==\nworld\n==> /comp0010/test/test_files/file3.txt <==\nline\nsecond\nthird \nfourth\nlast line\n==> /comp0010/test/test_files/long_file.txt <==\n17\n18\n19\n20\n21\n22\n23\n24\n25\nend of file\n']
        self.assertEqual(result, expected)

    def test_tail_q(self):
        result = []
        eval('tail -q /comp0010/test/test_files/file2.txt /comp0010/test/test_files/file3.txt /comp0010/test/test_files/long_file.txt', result)
        expected = [
            'world\nline\nsecond\nthird \nfourth\nlast line\n17\n18\n19\n20\n21\n22\n23\n24\n25\nend of file\n']
        self.assertEqual(result, expected)

    def test_tail_n0(self):
        result = []
        eval('tail -n 0 /comp0010/test/test_files/file1.txt', result)
        expected = ['']
        self.assertEqual(result, expected)

    def test_tail_n5(self):
        result = []
        eval('tail -n 5 /comp0010/test/test_files/long_file.txt', result)
        expected = [
            '22\n23\n24\n25\nend of file\n']
        self.assertEqual(result, expected)

    def test_tail_n_greater_than_file_length(self):
        result = []
        eval('tail -n 15 /comp0010/test/test_files/file5.txt', result)
        expected = [
            'apple\napple\nApple\nlemon\norange\norange\nlemon \napple\norange\napple\napple\n'
        ]
        self.assertEqual(result, expected)

    def test_tail_q_one_file(self):
        result = []
        eval('tail -q /comp0010/test/test_files/file3.txt', result)
        expected = [
            'line\nsecond\nthird \nfourth\nlast line\n']
        self.assertEqual(result, expected)

    def test_tail_n_q_multiple_arguments(self):
        result = []
        eval('tail -n 5 -q /comp0010/test/test_files/file2.txt /comp0010/test/test_files/file5.txt /comp0010/test/test_files/file6.txt', result)
        expected = [
            'world\nlemon \napple\norange\napple\napple\nAAA\nBBB\nAAA\naaa\n']
        self.assertEqual(result, expected)

    def test_tail_invalid_lines(self):
        result = []
        self.assertRaises(
            Exception, eval, 'tail: invalid number of lines: /comp0010/test/test_files/file1.txt', result)

    def test_tail_invalid_file(self):
        result = []
        self.assertRaises(
            Exception, eval, 'tail: /comp0010/test_files/file7.txt: No such file or directory', result)

    def test_unsafe_tail_invalid_file(self):
        result = []
        eval('_tail /comp0010/test_files/file7.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['tail: /comp0010/test_files/file7.txt: No such file or directory'])


if __name__ == '__main__':
    unittest.main()
