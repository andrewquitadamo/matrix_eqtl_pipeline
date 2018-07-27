import unittest
from unittest import mock
import sys
from parse import get_args
from parse import add_genotypes
from parse import parse

class FilterTests(unittest.TestCase):
    
    @mock.patch('os.path.isfile')
    def test_input_and_output_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename', '-o', 'output_filename']
        self.assertEqual(get_args(),('vcf_filename','output_filename'))

    @mock.patch('os.path.isfile')
    def test_input_only_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename']
        self.assertEqual(get_args(),('vcf_filename','vcf_filename.matrix'))

    def test_nonexistant_file(self):
        sys.argv[1:] = ['-v', 'nonexistant_file']
        with self.assertRaises(SystemExit):
            get_args()
    
    def test_add_genotypes(self):
        id = "test1"
        genos = ['0|0', '0|0:1', '1|1', '0|1', '1|0']
        self.assertEqual(add_genotypes(id, genos),"test1\t0\t0\t2\t1\t1")

    def test_parse_header(self):
        header = "#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00105"
        self.assertEqual(parse(header),"snpid\tHG00096\tHG00097\tHG00099\tHG00100\tHG00101\tHG00102\tHG00105")

    def test_parse_genotype(self):
        line = "1 10177 rs367896724 A AC 100 PASS AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152 GT 1|0 0|1 0|1 1|0 0|0 1|0 1|0"
        self.assertEqual(parse(line), 'rs367896724\t1\t1\t1\t1\t0\t1\t1')

    def test_parse_x_chr(self):
        line = "X 10177 rs367896724 A AC 100 PASS AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152 GT 1|0 0|1 0|1 1|0 0|0 1|0 1|0"
        self.assertIsNone(parse(line))

if __name__ == '__main__':
    unittest.main()
