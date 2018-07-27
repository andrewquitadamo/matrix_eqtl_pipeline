import unittest
from unittest import mock
import sys
from remove_vcf_header import get_args

class RunPeerTests(unittest.TestCase):

    @mock.patch('os.path.isfile')
    def test_input_and_output_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-i', 'vcf_filename', '-o', 'output_filename',]
        self.assertEqual(get_args(),('vcf_filename','output_filename'))

    @mock.patch('os.path.isfile')
    @mock.patch('__builtin__.open')
    def test_only_input_filename(self, mock_os_is_file, mock_open):
        mock_os_is_file.return_value = True
        mock_open.return_value = 'vcf_filename.noh'
        sys.argv[1:] = ['-i', 'vcf_filename',]
        self.assertEqual(get_args(), ('vcf_filename','vcf_filename.noh'))

    def test_nonexistant_file(self):
        sys.argv[1:] = ['-i', 'nonexistant_file']
        with self.assertRaises(SystemExit):
            get_args()

if __name__ == '__main__':
    unittest.main()
