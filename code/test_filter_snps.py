import unittest
from unittest import mock
import sys
from filter_snps import filter
from filter_snps import get_args

class FilterTests(unittest.TestCase):
    
    def test_filter_hash(self):
        self.assertEqual(filter('#Test Line'), '#Test Line')

    def test_no_minor_allele(self):
        line = '1 10177 rs367896724 A AC 100 PASS AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152 GT 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0'        
        self.assertIsNone(filter(line))

    def test_minor_allele_above_cutoff(self):
        line = '1 10177 rs367896724 A AC 100 PASS AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152 GT 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|1'        
        self.assertEqual(filter(line), line)

    def test_minor_allele_below_cutoff(self):
        line = '1 10177 rs367896724 A AC 100 PASS AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152 GT 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|0 0|1 0|0 0|0 0|0'        
        self.assertIsNone(filter(line))

    @mock.patch('os.path.isfile')
    def test_input_and_output_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename', '-o', 'output_filename']
        self.assertEqual(get_args(),('vcf_filename','output_filename'))

    @mock.patch('os.path.isfile')
    def test_only_input_filename(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename']
        self.assertEqual(get_args(), ('vcf_filename', 'vcf_filename.maf_filtered'))

    def test_nonexistant_file(self):
        sys.argv[1:] = ['-v', 'nonexistant_file']
        with self.assertRaises(SystemExit):
            get_args()

if __name__ == '__main__':
    unittest.main()
