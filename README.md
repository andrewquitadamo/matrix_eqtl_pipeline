* `remove_vcf_header.py`
	- Removes `##` header lines from VCF files; Keeps `#` header
	- Takes one argument  
		- `-v/--vcf-file` : name of VCF file to remove header from  
	- Has two optional arguments  
		- `-o/--output-file` : Custom name of output file if the `.noh` extension isn't desired  
		- `-s/--stdout` : Prints output to stdout ie console/terminal, can be redirected or piped  

* `vcf_overlap.py`
	- Overlaps the samples from the VCF file and the gene expression file
	- MatrixEQTL requires the VCF file and gene expression file to have the same samples and in the same order
	- Takes two arguments  
		- `-v/--vcf-file` : A VCF file with the header information removed (output of `remove_vcf_header.py`)  
		- `-g/--gene-expression-file` : A gene expression matrix; Each column is a sample, each row is a gene  
	- Takes one optional argument  
		- `-e/--extension` : Custom file extension to be used if `.out` isn't desired  
	- vcf_overlap.py doesn't have a stdout option as it outputs two files

* `filter_snps.py`
	- Minor allele frequency filtering
	- Takes one argument  
		- `-v/--vcf-file` : A VCF file with the header information removed; N.B. To get accurate MAF filtering for your sample, use this step after overlapping  
	- Takes two optional argument  
		- `-o/--output-file` : Custom name of output file if `.maf_filtered` isn't desire  
		- `-s/--stdout` : Prints output to stdout, so it can be redirected or piped  

* `parse.py`
	- Parses a ## headerless VCF file to get summed genotypes; ex `0|0:` becomes `0`, `0|1:` becomes `1`, `1|1:` becomes `2` 
	- Takes one argument  
		- `-v/--vcf-file` : A VCF file with the header information removed  
	- Takes two optional arguments  
		- `-o/--output-file` : Custom name of output file if `.matrix` isn't desired  
		- `-s/--stdout` : Prints output to stdout  

* `position.py`
	- Creates two position files, one in the form required for MatrixEQTL, and one that contains `id`, `chr`, `start`, `stop`, and `type`
	- Takes one argument  
		- `-v/--vcf-file` : A VCF file with the header information removed  
	- Takes two optional arguments  
		- `-o/--output-file` : Custom filename for the genotype positions  
		- `-m/--meqtl-file` : Custom filename for the MatrixEQTL formatted positions  

* `pc_covariates.py`
	- Calculates Principle Components using Scikit-Learn's IncrementalPCA method
	- Takes one argument  
		- `-v/--vcf-file` : A VCF file that has been parsed with `parse.py`  
	- Takes three optional arguments  
		- `-o/--output-file` : Custom filename for the PC covariates, default is `filename.pcs`  
		- `-n/--number-pcs` : Number of PCs to include; default=1  
		- `-s/--stdout` : Prints output to stdout  

* `run_iqn.py`
	- Python wrapper for `general_iqn_py.R`
	- Performs inverse quantile normalization on a gene expression matrix
	- Inverse quantile normalization casts each row (gene expression values from one gene for each sample) onto the standard normal distribution by rank
	- Takes one argument  
		- `-i/--input-file` : A gene expression matrix file; N.B. for the Inverse Quantile Normalization to get the correct results for an eQTL analysis use this step after overlapping  
	- Takes two optional arguments  
		- `-o/--output-file` : Custom filename for the inverse quantile normalized expression matrix, default is `filename.qnorm`  
		- `-s/--stdout` : Prints output to stdout  

* `run_peer.py`
	- Python wrapper for `peer_function.R`
	- Runs PEER on gene expression matrix to calculate PEER factors which can be used as covariates
	- Takes two arguments  
		- `-i/--input-file` : The gene expression matrix filename; N.B. run on the inverse quantile normalized gene expression matrix  
		- `-n/--number-factors` : The number of PEER factors to calculate  
	- Takes one optional argument  
		- `-o/--output-file` : Custom filename for the PEER factors, default is `filename.peer_factors_n` where `n` is the number of factors  

* `combine_covariates.py`
	- Combines genotype PC covariates, gene expression PEER factors and any additional PCs like population and gender
	- Takes two arguments  
		- `-p/--snp-pc-file` :  
		- `-f/--peer-factor-file` :  
	- Takes three optional arguments  
		- `-o/--output-file` : Custom filename for the combined covariates, default is `combined_covariates`  
		- `-a/--additional-covariates` : Filename for any additional covariates to include in the combined covariates file  
		- `-s/--stdout` : Prints output to stdout  

* `run_matrix_eqtl.py`
	- Wrapper for running MatrixEQTL 
	- Takes four arguments  
		- `-g/--genotype-matrix` : Genotype matrix of summed genotypes  
		- `-p/--genotype-positions` : Genotype positions in MatrixEQTL format  
		- `-e/--gene-expression-matrix` : Gene expression matrix  
		- `-g/--gene-positions` : Gene positions in MatrixEQTL format  
	- Takes four additional arguments  
		- `-c/--covariates` : Covariate filename, no default  
		- `-o/--output-file` : Custom filename for the MatrixEQTL output, default is `MatrixEqtlOutput`  
		- `-v/--p-value` : P-value cutoff, default is 0.05  
		- `-q/--qq-plot` : Custom filename for the qq-plot PDF file, default is `MatrixEqtlQQPlot.pdf`  

* `modify_matrix_eqtl.R`
	- Script to create a version of MatrixEQTL Engine that behaves better with Python and rpy2
	- Takes two optional arguments  
		- `-o/--output-file`  
		- `-s/--stdout`  

---------------------------------------------------

* `general_iqn_py.R`
	- Inverse quantile normalization function
	- Takes one argument : Filename of the gene expression matrix to normalize
	- Returns the inverse quantile normalized genen expression matrix

* `peer_function.R`
	- R function to run PEER
	- Takes two arguments :   
		- Filename of gene expression matrix  
		- Number of PEER factors to calculate  
	- Returns the PEER factor matrix 

* `mxeqtl.R`
	- R functions to run MatrixEQTL
	- The main function (mxeqtl) takes six  arguments  
		- `snp_file` : Filename of genotype matrix  
		- `snp_location` : Filename of the genotype positions  
		- `expr_file` : Filename of the gene expression matrix  
		- `expr_location` : Filename of the gene positions  
		- `cis_output_file` : Filename of the output file  
		- `cis_pval` : P-value cutoff  
	- Takes 11 optional arguments  
		- `covariates` : Filename of the covariates, default is no covariate file
		- `trans_pval` :  P-value cutoff for trans associations, default is 0  
		- `trans_output_file` : Filename of the output file for trans association, default is no trans- output filename  
		- `model` : Model type to use. Default is `linear`  
		- `MAF` : MAF cutoff for filtering; Default is 0 and no MAF filtering  
		- `cis_dist` : Maximum distance between genotype and gene  
		- `qq` : Filename of the qq-plot, default is no qq-plot file
		- `missing` : The value of missing data, default is `NA`
		- `sep` : The separating character of the genotype and gene expression matrices, default is "\t"
		- `header` : Binary flag if matrices have a header with IDs, default is `TRUE`
		- `rownames` : Binary flag if matrices have rowname IDs, default is `TRUE`
