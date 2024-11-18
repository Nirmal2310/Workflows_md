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

a) Create a new conda environment and install the dependencies of Braker
```bash
conda create -n braker -y && conda activate braker
conda install -c bioconda perl=5.34.0 -y
conda install -c conda-forge gcc -y
curl -L https://cpanmin.us | perl - App::cpanminus
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
cpanm install Statistics::LineFit
```
b) Download GeneMark-ES/ET/EP from [here.](http://exon.gatech.edu/GeneMark/license_download.cgi) Now change the path of perl:
```bash
perl change_path_in_perl_scripts.pl "/home/nirmal/new-cluster/miniconda/envs/braker/bin/perl"
perl check_install.bash # To check the successful installation of GeneMark-ES
```
c) Downlod and Install GeneMark-ETP:
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
d) Download and Install Augustus:
```bash
git clone https://github.com/Gaius-Augustus/Augustus.git
cd Augustus
conda install -c conda-forge lp_solve -y
conda install -c conda-forge suitesparse -y
conda install -c anaconda gsl -y
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

```bash
make augustus
```


e) Download and Install ProtHint
```bash
 wget https://github.com/gatech-genemark/ProtHint/releases/download/v2.6.0/ProtHint-2.6.0.tar.gz
tar -xvf ProtHint-2.6.0.tar.gz
export PATH="/home/nirmal/tools/ProtHint/bin/:$PATH"
```
f) Download and Install Other Dependencies
```bash
git clone https://github.com/Gaius-Augustus/TSEBRA
conda install -c bioconda cdbtools -y
pip install biopython
```
g) Export All Paths to Bashrc
```bash
export PATH="/home/nirmal/tools/BRAKER-3.0.3/scripts/:$PATH"
export GENEMARK_PATH="/home/nirmal/tools/GeneMark-EX/:$PATH"
export PATH="/home/nirmal/tools/Augustus/bin/:/home/nirmal/tools/Augustus/scripts/:$PATH"
export AUGUSTUS_CONFIG_PATH=/home/nirmal/tools/Augustus/config/
export PATH="/home/nirmal/tools/ProtHint-2.6.0/bin/:$PATH"
export PATH="/home/nirmal/tools/TSEBRA/bin/:$PATH"
```
#### Running BRAKER for Candida auris Genome
```bash
braker.pl --genome=C_auris_IITD_B11221_v1.fasta --rnaseq_sets_dirs=/nfs_master/nirmal/Nanopore/c_auris_methylation/pass/C_auris_annotation_data --rnaseq_sets_ids=SRR11511212,SRR13193644,SRR13193646,SRR18885077 --threads 16 --fungus
# Make Sure the Fastq File is unzipped.
```
### Step 2: Prediction of tRNA genes:
```bash
conda create -n eukaryote_annotation -y && conda activate eukaryote_annotation
conda install -c bioconda trnascan-se -y
tRNAscan-se -o C_auris_tRNA.out -f C_auris_tRNA.ss -m C_auris_tRNA.stats C_auris_genome.fasta
```
### Step 3: Prediction of rRNA genes:
RNAmmer can be downloaded from [here.](https://services.healthtech.dtu.dk/services/RNAmmer-1.2/)
```bash
conda create -n rnammer -y && conda activate rnammer
conda install -c conda-forge perl -y
conda install -c biconda hmmer2 -y
conda install -c bioconda perl-xml-simple -y
mkdir RNAmmer && mv rnammer-1.2.Unix.tar.gz
tar -xvf rnammer-1.2.Unix.tar.gz
export PATH="/home/nirmal/tools/RNAmmer/:$PATH"
```
EDIT THE 35th, 50 and 51st line of rnammer to: 
```bash
my $INSTALL_PATH = "/home/nirmal/tools/RNAmmer";
$HMMSEARCH_BINARY = "/home/nirmal/new-cluster/miniconda/envs/rnammer/bin/hmmsearch2";
$PERL = "/home/nirmal/new-cluster/miniconda/envs/rnammer/bin/perl";
```
```bash
rnammer -S euk -gff C_auris_rRNA.gff -multi -f C_auris_rRNA.fasta -h C_auris_rRNA -m tsu,ssu,lsu C_auris_genome.fasta
```
### Step 4: Identification of Protein Domains:
```bash
conda activate eukaryote_annotation
conda install -c bioconda hmmer -y
hmmsearch --pfamtblout C_auris_pfam_hmmer_out.txt --cpu 16 -o hmmer_out /home/nirmal/bin/Pfam-A.hmm braker.aa
```

