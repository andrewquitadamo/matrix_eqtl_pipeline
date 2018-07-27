import unittest
from unittest import mock
import sys
from run_peer import get_args

class RunPeerTests(unittest.TestCase):

    @mock.patch('os.path.isfile')
    def test_input_and_output_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-i', 'gene_expression_filename', '-o', 'output_filename','-n','5']
        self.assertEqual(get_args(),('gene_expression_filename','5','output_filename'))

    @mock.patch('os.path.isfile')
    def test_only_input_filename(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-i', 'gene_expression_filename','-n','5']
        self.assertEqual(get_args(), ('gene_expression_filename','5','gene_expression_filename.peer_factors_5'))

    def test_nonexistant_file(self):
        sys.argv[1:] = ['-i', 'nonexistant_file']
        with self.assertRaises(SystemExit):
            get_args()

if __name__ == '__main__':
    unittest.main()
