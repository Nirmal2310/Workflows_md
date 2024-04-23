## This MarkDown File Contains the steps to build Organism Package Database using NCBI for Candida auris B11220.

#### Step 1: Getting Necessary Files
```bash
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/013/715/GCF_003013715.1_ASM301371v2/GCF_003013715.1_ASM301371v2_genomic.gtf.gz -O C_auris_B11220.gtf.gz
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/013/715/GCF_003013715.1_ASM301371v2/GCF_003013715.1_ASM301371v2_gene_ontology.gaf.gz -O C_auris_B11220.gaf.gz
gunzip C_auris_B11220.gaf.gz C_auris_B11220.gtf.gz
```
#### Step 2: Preparing Files for Creating the Database
```bash
awk 'BEGIN{FS="\t";OFS="\t"}{if($3=="gene") print $1,$9}' C_auris_B11220.gtf | awk 'BEGIN{FS="\t";OFS="\t"}{split($2,a,";"); for(i=1;i<=length(a);i++) if(a[i]~/GeneID/) print a[i],$1}' | sed 's/db_xref "//g;s/"//g;s/GeneID://g' > chr_names.txt
awk 'BEGIN{FS="\t";OFS="\t"}{if($3=="CDS") print $9}' C_auris_B11220.gtf | awk 'BEGIN{FS="\t";OFS="\t"}{split($1,a,";"); for(i=1;i<=length(a);i++) if(a[i]~/GeneID/) gid=a[i]; else if(a[i]~/gene_id/) gsym=a[i]; else if(a[i]~/product/) prod=a[i]; print gid,gsym,prod}' | sort | uniq  | sed 's/db_xref "GeneID://g;s/gene_id "//g;s/ product "//g;s/"//g' |  awk 'BEGIN{FS="\t";OFS="\t"}{print $1,$2,"\""$3"\""}' > gene_symbols.txt
awk '{if(NR>9) print $0}' C_auris_B11220.gaf | awk 'BEGIN{FS="\t";OFS="\t"}{print $2,$5,$7}' | sort | uniq > GO_terms.txt
```
#### Step 3: Creating the Organism Database Using the Above Files
```R
chr_data <- read.table(file="GenomeDir/chr_names.txt")
colnames(chr_data) <- c("GID", "CHROMOSOME")

gene_symbol_data <- read.table(file="GenomeDir/gene_symbols.txt")
colnames(gene_symbol_data) <- c("GID", "SYMBOL", "GENENAME")

gene_ontology_data <- read.table(file="GenomeDir/GO_terms.txt")
colnames(gene_ontology_data) <- c("GID", "GO", "EVIDENCE")

makeOrgPackage(gene_info=gene_symbol_data, chromosome=chr_data, go=gene_ontology_data, version="0.1",
maintainer="Nirmal Singh Mahar <bez207518@iitd.ac.in>",
author="Nirmal Singh Mahar <bez207518@iitd.ac.in>",
outputDir = ".",
tax_id="498019",
genus="Candida",
species="auris",
goTable="go")
```
