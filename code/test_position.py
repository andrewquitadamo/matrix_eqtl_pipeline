import unittest
from unittest import mock
import sys
from position import get_args
from position import parse_info
from position import position
from position import parse

class PositionTests(unittest.TestCase):
    @mock.patch('os.path.isfile')
    def test_input_filename(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename']
        self.assertEqual(get_args(), ('vcf_filename', 'vcf_filename.positions', 'vcf_filename.meqtl_positions'))

    @mock.patch('os.path.isfile')
    def test_input_and_output_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename', '-o', 'output_filename', '-m', 'meqtl_output_filename']
        self.assertEqual(get_args(),('vcf_filename','output_filename', 'meqtl_output_filename'))

    @mock.patch('os.path.isfile')
    def test_input_and_meqtl_output_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename', '-m', 'meqtl_output_filename']
        self.assertEqual(get_args(),('vcf_filename','vcf_filename.positions', 'meqtl_output_filename'))

    @mock.patch('os.path.isfile')
    def test_input_and_pos_output_args(self, mock_os_is_file):
        mock_os_is_file.return_value = True
        sys.argv[1:] = ['-v', 'vcf_filename', '-o', 'output_filename']
        self.assertEqual(get_args(),('vcf_filename','output_filename', 'vcf_filename.meqtl_positions'))

    def test_nonexistant_file(self):
        sys.argv[1:] = ['-v', 'nonexistant_file']
        with self.assertRaises(SystemExit):
            get_args()

    def test_parse_info_indel(self):
        info = 'AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152;EAS_AF=0.3363;AMR_AF=0.3602;AFR_AF=0.4909;EUR_AF=0.4056;SAS_AF=0.4949;AA=|||unknown(NO_COVERAGE);VT=INDEL'        
        pos = '10177'
        self.assertEqual(parse_info(info, pos), ('INDEL', '10177'))

    def test_parse_info_sv(self):
        info = 'TSD=null;SVTYPE=ALU;MEINFO=AluYa4_5,1,223,-;SVLEN=222;CS=ALU_umary'
        pos = '645710'
        self.assertEqual(parse_info(info, pos), ('ALU', '645932'))

    def test_parse_info_sv_end(self):
        info = 'SVTYPE=DUP;SVLEN=181574;IMPRECISE;CIEND=-150,150;CIPOS=-150,150;END=850204;CS=DUP_delly GT:FT:CN:GL:CNL:AVGPOST'
        pos = '668630'
        self.assertEqual(parse_info(info, pos), ('DUP', '850204'))

    def test_parse_info_snp(self):
        info = 'AC=480;AF=0.0958466;AN=5008;NS=2504;DP=26761;EAS_AF=0.005;AMR_AF=0.1138;AFR_AF=0.0144;EUR_AF=0.1859;SAS_AF=0.1943;AA=a|||;VT=SNP'
        pos = '14464'
        self.assertEqual(parse_info(info, pos), ('SNP', '14464'))

    def test_position_indel(self):
        info = 'AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152;EAS_AF=0.3363;AMR_AF=0.3602;AFR_AF=0.4909;EUR_AF=0.4056;SAS_AF=0.4949;AA=|||unknown(NO_COVERAGE);VT=INDEL'        
        pos = '10177'
        self.assertEqual(position(info, pos), ('10177', '10177', 'INDEL'))

    def test_position_sv(self):
        info = 'TSD=null;SVTYPE=ALU;MEINFO=AluYa4_5,1,223,-;SVLEN=222;CS=ALU_umary'
        pos = '645710'
        self.assertEqual(position(info, pos), ('645932', '645821', 'ALU'))

    def test_position_sv_end(self):
        info = 'SVTYPE=DUP;SVLEN=181574;IMPRECISE;CIEND=-150,150;CIPOS=-150,150;END=850204;CS=DUP_delly GT:FT:CN:GL:CNL:AVGPOST'
        pos = '668630'
        self.assertEqual(position(info, pos), ('850204', '759417', 'DUP'))

    def test_position_info_snp(self):
        info = 'AC=480;AF=0.0958466;AN=5008;NS=2504;DP=26761;EAS_AF=0.005;AMR_AF=0.1138;AFR_AF=0.0144;EUR_AF=0.1859;SAS_AF=0.1943;AA=a|||;VT=SNP'
        pos = '14464'
        self.assertEqual(position(info, pos), ('14464','14464','SNP'))

    def test_parse_indel(self):
        line = '1 10177 rs367896724 A AC 100 PASS  AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152;EAS_AF=0.3363;AMR_AF=0.3602;AFR_AF=0.4909;EUR_AF=0.4056;SAS_AF=0.4949;AA=|||unknown(NO_COVERAGE);VT=INDEL GT 1|0 0|1 0|1'
        self.assertEqual(parse(line), ('rs367896724','1','10177','10177','INDEL','10177'))

    def test_parse_sv(self):
        line = '1 645710 ALU_umary_ALU_2 A <INS:ME:ALU> . . TSD=null;SVTYPE=ALU;MEINFO=AluYa4_5,1,223,-;SVLEN=222;CS=ALU_umary GT:GL:AVGPOST 0|0:-0.0,-0.0,-0.0:0.993 0|0:-0.0,-0.0,-0.0:0.9905 0|0:-0.0,-0.0,-0.0:0.9914'
        self.assertEqual(parse(line),('ALU_umary_ALU_2', '1', '645710', '645932','ALU','645821'))

if __name__ == '__main__':
    unittest.main()
