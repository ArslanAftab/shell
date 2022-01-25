import unittest
from shell import eval
import re
from parse import Parser
import os
from collections import deque
from parsy import ParseError


class TestPARSER(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parser_single_command_no_options_no_arguments_no_redirection(self):
        result = self.parser.initial_parse('ls')
        expected = [('single_command', {'function': 'ls', 'options': '',
                    'argument_list': '', 'redirection': []})]
        self.assertEqual(result, expected)

    def test_parser_single_command_options(self):
        result = self.parser.initial_parse('ls -a')
        expected = [('single_command', {'function': 'ls', 'options': '-a',
                    'argument_list': '', 'redirection': []})]
        self.assertEqual(result, expected)

    def test_parser_single_command_arguments(self):
        result = self.parser.initial_parse('ls dir1')
        expected = [('single_command', {'function': 'ls', 'options': '',
                    'argument_list': 'dir1', 'redirection': []})]
        self.assertEqual(result, expected)

    def test_parser_single_command_redirection(self):
        result = self.parser.initial_parse('ls > file1.txt')
        expected = [('single_command', {'function': 'ls', 'options': '',
                    'argument_list': '', 'redirection': [{'bracket': '>', 'location': 'file1.txt'}]})]
        self.assertEqual(result, expected)

    def test_parser_single_command_options_arguments(self):
        result = self.parser.initial_parse('ls -l dir1')
        expected = [('single_command', {'function': 'ls', 'options': '-l ',
                    'argument_list': 'dir1', 'redirection': []})]
        self.assertEqual(result, expected)

    def test_parser_single_command_options_redirection(self):
        result = self.parser.initial_parse('ls -l > file1.txt')
        expected = [('single_command', {'function': 'ls', 'options': '-l ',
                    'argument_list': '', 'redirection': [{'bracket': '>', 'location': 'file1.txt'}]})]
        self.assertEqual(result, expected)

    def test_parsr_single_command_arguments_redirection(self):
        result = self.parser.initial_parse('ls dir1 > file1.txt')
        expected = [('single_command', {'function': 'ls', 'options': '',
                    'argument_list': 'dir1 ', 'redirection': [{'bracket': '>', 'location': 'file1.txt'}]})]
        self.assertEqual(result, expected)

    def test_parser_single_command_options_arguments_redirection(self):
        result = self.parser.initial_parse('ls -l dir1 > file1.txt')
        expected = [('single_command', {'function': 'ls', 'options': '-l ',
                    'argument_list': 'dir1 ', 'redirection': [{'bracket': '>', 'location': 'file1.txt'}]})]
        self.assertEqual(result, expected)

    def test_parser_multiple_commands(self):
        result = self.parser.initial_parse('ls;cat file1.txt')
        expected = [('single_command', {'function': 'ls', 'options': '', 'argument_list': '', 'redirection': []}),
                    ('single_command', {'function': 'cat', 'options': '', 'argument_list': 'file1.txt', 'redirection': []})]
        self.assertEqual(result, expected)

    def test_parser_piped_list(self):
        result = self.parser.initial_parse('ls | grep src')
        expected = [('piped_list', [{'function': 'ls', 'options': '', 'argument_list': '', 'redirection': []}, {
                     'function': 'grep', 'options': '', 'argument_list': 'src', 'redirection': []}])]
        self.assertEqual(result, expected)

    def test_parser_failed_initial_parse(self):
        self.assertRaises(ParseError, self.parser.initial_parse, 'r')

    def test_parser_options_parse_none(self):
        result = self.parser.options_parse(None)
        self.assertEqual(result, [])

    def test_parser_arguments_parse_none(self):
        result = self.parser.arguments_parse(None)
        self.assertEqual(result, [])

    def test_parser_failed_arguments_parse(self):
        result = self.parser.arguments_parse('`')
        self.assertEqual(result, None)

    def test_parser_options_parser_single_flag_no_number(self):
        result = self.parser.options_parse('-l')
        expected = [{'letter': 'l', 'number': None}]
        self.assertEqual(result, expected)

    def test_parser_options_parser_single_flag_number_no_space(self):
        result = self.parser.options_parse('-l4')
        expected = [{'letter': 'l', 'number': '4'}]
        self.assertEqual(result, expected)

    def test_parser_options_parser_single_flag_number_space(self):
        result = self.parser.options_parse('-l 4')
        expected = [{'letter': 'l', 'number': '4'}]
        self.assertEqual(result, expected)

    def test_parser_options_parser_flag_block_no_number(self):
        result = self.parser.options_parse('-la')
        expected = {'letter': 'la', 'number': None}
        self.assertEqual(result, expected)

    def test_parser_options_parser_flag_block_number_no_space(self):
        result = self.parser.options_parse('-la4')
        expected = {'letter': 'la', 'number': '4'}
        self.assertEqual(result, expected)

    def test_parser_options_parser_flag_block_number_space(self):
        result = self.parser.options_parse('-la 4')
        expected = {'letter': 'la', 'number': '4'}
        self.assertEqual(result, expected)

    def test_parser_options_parser_multiple_single_flags(self):
        result = self.parser.options_parse('-l -a')
        expected = [{'letter': 'l', 'number': None},
                    {'letter': 'a', 'number': None}]
        self.assertEqual(result, expected)

    def test_parser_failed_options_parse(self):
        result = self.parser.options_parse('-l4a4')
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
