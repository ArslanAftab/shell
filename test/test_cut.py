import unittest
from shell import eval


class TestCUT(unittest.TestCase):
    def t(self):
        result = []
        eval('cut /comp0010/test/test_files/', result)
        expected = [
        ]
        self.assertEqual(result, expected)

    def test_cut_single(self):
        result = []
        eval('cut -b 3 /comp0010/test/test_files/file5.txt', result)
        expected = ['p\np\np\nm\na\na\nm\np\na\np\np\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_multiple_numbers(self):
        result = []
        eval('cut -c 1,2,3 /comp0010/test/test_files/file3.txt', result)
        expected = ['lin\nsec\nthi\nfou\nlas\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_range(self):
        result = []
        eval('cut -c 1-4 /comp0010/test/test_files/file5.txt', result)
        expected = ['appl\nappl\nAppl\nlemo\noran\noran\nlemo\nappl\noran\nappl\nappl\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_start_range(self):
        result = []
        eval('cut -c -4 /comp0010/test/test_files/file5.txt', result)
        expected = ['appl\nappl\nAppl\nlemo\noran\noran\nlemo\nappl\noran\nappl\nappl\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_end_range(self):
        result = []
        eval('cut -b 3- /comp0010/test/test_files/file5.txt', result)
        expected = ['ple\nple\nple\nmon\nange\nange\nmon \nple\nange\nple\nple\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_multiple_end_range(self):
        result = []
        eval('cut -b 5-,2- /comp0010/test/test_files/file5.txt', result)
        expected = ['pple\npple\npple\nemon\nrange\nrange\nemon \npple\nrange\npple\npple\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_multiple_ranges(self):
        result = []
        eval('cut -c 1-2,4-5 /comp0010/test/test_files/file5.txt', result)
        expected = ['aple\naple\nAple\nleon\norng\norng\nleon\naple\norng\naple\naple\n'
                    ]
        self.assertEqual(result, expected)

    def test_cat_large_number_as_position(self):
        result = []
        eval('cut -c 15 /comp0010/test/test_files/file3.txt', result)
        expected = ['\n\n\n\n\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_multiple_files(self):
        result = []
        eval('cut -c -3 /comp0010/test/test_files/file3.txt /comp0010/test/test_files/file5.txt /comp0010/test/test_files/file6.txt', result)
        expected = ['lin\nsec\nthi\nfou\nlas\napp\napp\nApp\nlem\nora\nora\nlem\napp\nora\napp\napp\nAAA\nBBB\nAAA\naaa\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_multiple_mixed_number_list(self):
        result = []
        eval('cut -b 1-2,4,5- /comp0010/test/test_files/file3.txt /comp0010/test/test_files/file5.txt /comp0010/test/test_files/file6.txt', result)
        expected = ['lie\nseond\nthrd \nforth\nlat line\naple\naple\nAple\nleon\nornge\nornge\nleon \naple\nornge\naple\naple\nAA\nBB\nAA\naa\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_overlapped_range(self):
        result = []
        eval('cut -b 2-4,3-5 /comp0010/test/test_files/file3.txt /comp0010/test/test_files/file5.txt /comp0010/test/test_files/file6.txt', result)
        expected = ['ine\necon\nhird\nourt\nast \npple\npple\npple\nemon\nrang\nrang\nemon\npple\nrang\npple\npple\nAA\nBB\nAA\naa\n'
                    ]
        self.assertEqual(result, expected)

    def test_cut_invalid_file(self):
        result = []
        self.assertRaises(
            Exception, eval, 'cut: /comp0010/test/test_files/file7.txt: No such file or directory', result)

    def test_unsafe_cut_invalid_file(self):
        result = []
        eval('_cut -b 3 /comp0010/test/test_files/file7.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: /comp0010/test/test_files/file7.txt: No such file or directory'])

    def test_unsafe_cut_decreasing_range_error(self):
        result = []
        eval('_cut -c 5-2 /comp0010/test/test_files/file3.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: invalid decreasing range'])

    def test_cut_invalid_position(self):
        result = []
        self.assertRaises(
            Exception, eval, 'cut: invalid byte/character position /', result)

    def test_unsafe_cut_invalid_position(self):
        result = []
        eval('_cut -b /comp0010/test/test_files/file3.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: invalid byte/character position /'])

    def test_unsafe_cut_double_commas(self):
        result = []
        eval('_cut -b 1,2,,3 /comp0010/test/test_files/file5.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: byte/character positions are numbered from 1'])

    def test_unsafe_cut_double_dash_range(self):
        result = []
        eval('_cut -b 1--3 /comp0010/test/test_files/file6.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: invalid byte or character range'])

    def test_unsafe_cut_both_flags_used(self):
        result = []
        eval('_cut -b -c 3 /comp0010/test/test_files/file3.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: only one type of list may be specified'])

    def test_unsafe_cut_no_flag_used(self):
        result = []
        eval('_cut 3 /comp0010/test/test_files/file3.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: you must specify a list of bytes, characters, or fields'])

    def test_unsafe_cut_0_position(self):
        result = []
        eval('_cut -b 0 /comp0010/test/test_files/file3.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: byte/character positions are numbered from 1'])

    def test_unsafe_cut_0_end_range(self):
        result = []
        eval('_cut -b 0- /comp0010/test/test_files/file3.txt', result)
        self.assertEqual(list({r.strip() for r in result}),
                         ['cut: byte/character positions are numbered from 1'])


if __name__ == '__main__':
    unittest.main()
