## This Markdown File contains the steps to annotate Candida auris Genome. It comprised of following steps:
1. Prediction of Protein Coding Genes (BRAKER)
2. Prediction of tRNA genes (tRNAScan)
3. Prediction of rRNA genes (RNAmmer)
4. Identification of PFAM Domains (HMMER3 + PFAM/TIGRFAM Database)
5. Functional Annotation of Genes: BlastKoala
6. Gene Name Assignment: Using the output of HMMER, SwissProt and Kegg Products.

### Step 1: Prediction of Protein Coding Genes:
BRAKER provides multiple modes for the PCG predictions but it works best when both RNA-Seq Data and Protein Data is available.

A) Installation:
Create a new conda environment and install the dependencies of Braker
```bash
conda create -n braker -y && conda activate braker
conda install -c bioconda perl=5.34.0 -y
conda install -c conda-forge gcc -y
cpan App::cpanminus
cpanm install File::Spec::Functions
cpanm install Hash::Merge
cpanm install List::Util
cpanm install MCE::Mutex
cpanm install Module::Load::Conditional
cpanm install Parallel::ForkManager
cpanm install POSIX
cpanm install Scalar::Util::Numeric
cpanm install YAML
cpanm install Math::Utils
cpanm install File::HomeDir
cpanm install threads
cpanm install YAML::XS
cpanm install Data::Dumper
cpanm install Thread::Queue
```
Download GeneMark-ES/ET/EP from [here.](http://exon.gatech.edu/GeneMark/license_download.cgi) Now change the path of perl:
```bash
perl change_path_in_perl_scripts.pl "/home/nirmal/new-cluster/miniconda/envs/braker/bin/perl"
perl check_install.bash # To check the successful installation of GeneMark-ES
```
Downlod and Install GeneMark-ETP:
```bash
git clone https://github.com/gatech-genemark/GeneMark-ETP.git
conda install -c bioconda bedtools -y
conda install -c bioconda sra-tools -y
conda install -c bioconda hisat2 -y
conda install -c bioconda samtools -y
conda install -c bioconda stringtie -y
conda install -c bioconda gffread -y
conda install -c bioconda diamond -y
conda install -c bioconda bamtools -y
```
Download and Install Augustus:
```bash
git clone https://github.com/Gaius-Augustus/Augustus.git
cd Augustus
conda install -c conda-forge lp_solve -y
conda install -c conda-forge suitesparse -y
conda install -c anaconda gsl -y
make augustus
```
Edit common.mk file in the Augustus directory
```bash
# Definitions common to all Makefiles
# This file is included from other Makefiles in the augustus project.
AUGVERSION = 3.4.0

# set ZIPINPUT to false if you do not require input gzipped input genome files,
# get compilation errors about the boost iostreams library or
# the required libraries libboost-iostreams-dev and lib1g-dev are not available
ZIPINPUT = true

# set COMPGENEPRED to false if you do not require the comparative gene prediction mode (CGP) or
# the required libraries
# libgsl-dev, libboost-all-dev, libsuitesparse-dev, liblpsolve55-dev, libmysql++-dev and libsqlite3-dev
# are not available
#COMPGENEPRED = true

MYSQL = false

# set these paths to the correct locations if you have installed the corresponding packages in non-default locations:
INCLUDE_PATH_ZLIB        := -I/home/nirmal/new-cluster/miniconda/envs/braker/include
LIBRARY_PATH_ZLIB        := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_BOOST       := -I/home/nirmal/new-cluster/miniconda/envs/braker/include
LIBRARY_PATH_BOOST       := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_LPSOLVE     := -I/home/nirmal/new-cluster/miniconda/envs/braker/include/lpsolve
LIBRARY_PATH_LPSOLVE     := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_SUITESPARSE := -I/home/nirmal/new-cluster/miniconda/envs/braker/include
LIBRARY_PATH_SUITESPARSE := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_GSL         := -I/home/nirmal/new-cluster/miniconda/envs/braker/include
LIBRARY_PATH_GSL         := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_MYSQL       := -I/home/nirmal/new-cluster/miniconda/envs/braker/include/mysql      # the path to mysql++ may have to be adjusted
LIBRARY_PATH_MYSQL       := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_SQLITE      := -I/home/nirmal/new-cluster/miniconda/envs/braker/include
LIBRARY_PATH_SQLITE      := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_BAMTOOLS    := -I/home/nirmal/new-cluster/miniconda/envs/braker/include/bamtools
LIBRARY_PATH_BAMTOOLS    := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_HTSLIB      := -I/home/nirmal/new-cluster/miniconda/envs/braker/include/htslib
LIBRARY_PATH_HTSLIB      := -L/home/nirmal/new-cluster/miniconda/envs/braker/lib -Wl,-rpath,/home/nirmal/new-cluster/miniconda/envs/braker/lib
INCLUDE_PATH_SEQLIB      := -I /usr/include/SeqLib -I/usr/include/htslib -I/usr/include/jsoncpp
LIBRARY_PATH_SEQLIB      := -L/usr/lib/x86_64-linux-gnu -Wl,-rpath,/usr/lib/x86_64-linux-gnu

# alternatively add paths with header files to INCLS and paths with library files to LDFLAGS

ifeq ($(shell uname -s), Darwin)
        # path for default homebrew installation of lp_solve
        INCLUDE_PATH_LPSOLVE = -I/usr/local/opt/lp_solve/include
        # path for default homebrew installation of mysql and mysql++
        INCLUDE_PATH_MYSQL = -I/usr/local/opt/mysql/include/mysql -I/usr/local/opt/mysql++/include/mysql
        # path for default homebrew installation of bamtools
        INCLUDE_PATH_BAMTOOLS = -I/usr/local/opt/bamtools/include/bamtools
        # path for default homebrew installation of htslib
        INCLUDE_PATH_HTSLIB = -I/usr/local/opt/htslib/include/htslib
endif
```
#### Note: The include path and library path is dependent on where your miniconda/anaconda is installed. Please edit it accordingly.