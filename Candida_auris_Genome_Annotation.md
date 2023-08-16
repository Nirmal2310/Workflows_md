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
#conda install -c conda-forge mysql -y
conda install -c conda-forge lp_solve -y
conda install -c conda-forge suitesparse -y
conda install -c anaconda gsl -y
#conda install -c bioconda seqiolib -y
make augustus

```
