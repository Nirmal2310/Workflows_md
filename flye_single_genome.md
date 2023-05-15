##### This markdown file for running FLYE Assembler for Single Isolate (In this case C.auris)
###### Error Correction of Nanopore Reads using Illumina Sequencing Data
```bash
zcat sample_combined.fastq.gz | awk 'NR%4==1||NR%4==2' | tr "@" ">" > sample_combined.fasta
mkdir temp
gunzip -c sample_?.fastq.gz | awk "NR % 4 == 2" | sort -T ./temp | tr NT TN | ropebwt2 -LR | tr NT TN | fmlrc-convert sample_msbwt.npy
fmlrc -p 16 sample_msbwt.npy sample_combined.fasta sample_combined_corrected.fasta
canu -trim -p sample_corrected -d sample_corrected_trimming genomeSize=12000000 -corrected -nanopore sample_combine_corrected.fasta useGrid=false
reformat.sh in=sample_corrected.trimmedReads.fasta.gz out=sample_corrected.trimmedReads_5K.fasta.gz minLength=5000
conda activate flye
flye --nano-corr sample_corrected.trimmedReads_5K.fasta.gz --genome-size 12000000 -o C_auris_sample_flye_assembly -t 16 -i 4 --no-alt-contigs
```
###### MEDAKA POLISHING (Using Long Read Sequencing Data)
```bash
medaka_consensus -i C_auris_combined.fastq.gz -d draft.fasta -o C_auris_medaka_polish -t 32 -m r1041_e82_260bps_sup_g632
```
###### POLYPOLISH POLISHING (Using Short Read Sequencing Data)
```bash
bwa index consensus.fasta
bwa mem -t 16 -a draft.fasta reads_1.fastq.gz > alignments_1.sam
bwa mem -t 16 -a draft.fasta reads_2.fastq.gz > alignments_2.sam
polypolish_insert_filter.py --in1 alignments_1.sam --in2 alignments_2.sam --out1 filtered_1.sam --out2 filtered_2.sam
polypolish draft.fasta filtered_1.sam filtered_2.sam > polished.fasta
```
###### POLKA POLISHING (Using Short Read Sequencing Data)
```bash
polca.sh -a polished.fasta -r 'polishing _reads1.fastq polishing_reads2.fastq' -t 16 -m 160G
```
###### CLAIR3 Variant Calling (For Haploid Organism, in this case Candida auris)
```bash
cd barcode01
docker run -v $PWD:$PWD --cpus 16 -w $PWD --rm hkubal/clair3:v1.0.0 run_clair3.sh --bam_fn="$PWD/barcode04_sorted.bam" --ref_fn="$PWD/C_auris_reference_GCF003013715.fasta" --threads="16"  --platform="ont" --model_path="$PWD/r1041_e82_260bps_sup_g632" --output="$PWD/C_auris_barcode04_clair3_variant_calling" --ctg_name="NC_072812.1,NC_072813.1,NC_072814.1,NC_072815.1,NC_072816.1,NC_072817.1,NC_072818.1" --no_phasing_for_fa --include_all_ctgs --haploid_precise --gvcf
# Please Note that the model files, bam file and the reference file should be in the same folder. Also please make a index file of the reference before running clair3
```
##### JOINT VARIANT CALLING (FOR PHYLOGENETIC TREE)
```bash
gatk GenotypeGVCFs -R C_auris_reference_GCF003013715.fasta -V C_auris_barcode01_variants.vcf.gz -V C_auris_barcode02_variants.vcf.gz ... -O C_auris_joint_variants.vcf.gz
gatk SelectVariants -V C_auris_joint_variants.vcf.gz -select-type SNP -O C_auris_joint_variants_snps.vcf.gz
```
##### CONVERTING TO PHYLIP FORMAT
```bash
vcf2phylip.py -i C_auris_joint_variants_snps.vcf.gz -o C_auris_joint_variants.phy
```
##### MAKING PHYLOGENETIC TREE USING RaXML
```bash
raxmlHPC -s C_auris_joint_variants.phy -m GTRGAMMA -n C_auris_joint_variants.tree
```
