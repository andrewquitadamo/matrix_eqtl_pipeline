* Python3
	* Numpy
	* Scipy
	* Scikit-Learn
	* Pandas
* R (>3.3)
* PEER
* RPy2


STEPS
==================================
*Data*
mkdir data
scp aquitada@hpc.uncc.edu:/users/aquitada/1000-miRNA-test/data/ALL.wgs.mergedSV.v3.20130502.svs.genotypes.vcf data/
scp aquitada@hpc.uncc.edu:/users/aquitada/1000-miRNA-test/data/gene_expression data/
scp aquitada@hpc.uncc.edu:/users/aquitada/1000-miRNA-test/data/gene_positions data/

*Code*
git clone https://github.com/andrewquitadamo/matrix_eqtl_pipeline.git
wget https://raw.githubusercontent.com/shilab/meQTL_functions/master/R/mxeqtl.R -P code/
python3 code/modify_matrix_eqtl.py

*Dependancies*

apt install python-setuptools
apt update
apt install python3-pip
python3 -m pip install scikit-learn
python3 -m pip install scipy
#python3 -m pip install numpy 
python3 -m pip install pandas

sudo add-apt-repository "deb http://cran.rstudio.com/bin/linux/ubuntu $(lsb_release -sc)/"
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
sudo add-apt-repository ppa:marutter/rdev
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install r-base
wget https://github.com/downloads/PMBio/peer/R_peer_source_1.3.tgz
tar -xvzf R_peer_source_1.3.tgz
R CMD INSTALL R_peer_source_1.3.tgz

python3 -m pip install rpy2
