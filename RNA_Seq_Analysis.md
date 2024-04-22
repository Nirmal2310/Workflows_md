#### Trim Raw Sequencing Reads to remove Adapter Sequences and Low Quality Reads
```bash
bbduk.sh -Xmx20g in=sample_1.fastq.gz in2=sample_2.fastq.gz ref=/home/antpc/miniconda/envs/bbtools/bbtools/lib/resources/adapters.fa out=sample_trim_1.fastq.gz out2=sample_trim_2.fastq.gz ktrim=r k=23 mink=11 hdist=1 tpe tbo threads=8 qtrim=rl minlength=40 trimq=10 maq=20 ftl=10 overwrite=true

#### Please check the read length first. If it is less than 70 bp then the above command will trim 10 bp from the start (left) and 10 bp from end (right) and over all the readlength will become less than 40 and hence will get discarded. So, to avoid that always check the read length before preprocessing.
```
#### Remove rRNA Reads from Trimmed FastQ files
```bash
ribodetector -t 20 -i sample_trim_1.fastq.gz sample_trim_2.fastq.gz -l 150 -m 50 -e norrna --chunk_size 256 -o sample_final_1.fastq.gz sample_final_2.fastq.gz -r sample_rRNA_1.fastq.gz sample_rRNA_2.fastq.gz
```
#### Indexing Reference Genome using STAR
```bash
STAR --runThreadN 30 --runMode genomeGenerate --genomeDir GenomeDir/star_index_50bp --genomeFastaFiles GenomeDir/GCF_003013715.1_ASM301371v2_genomic.fna --sjdbGTFfile GenomeDir/GCF_003013715.1_ASM301371v2_genomic.gtf --sjdbOverhang 49 --genomeSAindexNbases 10 # sjdbOverhang will be equal to mean read length -1
```
#### Mapping to the Reference Genome using STAR
```bash
STAR --genomeDir GenomeDir/star_index --readFilesIn sample_final_1.fastq.gz sample_final_2.fastq.gz --runThreadN 12 --quantMode GeneCounts --outSAMtype BAM Unsorted --outFileNamePrefix sample --twopassMode Basic --outSAMstrandField intronMotif --readFilesCommand zcat
samtools sort -@ 6 sampleAligned.out.bam -o sample.Aligned.sortedByCoord.out.bam
```
#### Remove Optical and PCR Duplicated
```bash
gatk MarkDuplicates --java-options -Xmx80G -I sample.Aligned.sortedByCoord.out.bam -O sample_final.bam -M sample_md.txt --REMOVE_DUPLICATES true --TMP_DIR $PWD
samtools index -@ 6 sample_final.bam
```
#### Checking for strandedness
```bash
awk 'FNR == 3 {print}' sampleReadsPerGene.out.tab | awk '{ for (i=1; i<=NF; i++) s[i]+=$i } END { for (i=1; i<=NF; i++) printf "%s ", s[i] }' | awk '{if ($3/$4 < 0.4) print "forward"; else if ($4/$3 < 0.4) print "reverse"; else print "unstranded" }' > sample_strand.txt
```
#### Getting the Counts
```bash
# Unstranded Data
awk 'BEGIN{FS="\t";OFS="\t"}{print $1,$2}' sampleReadsPerGene.out.tab
# Forward Stranded Data
awk 'BEGIN{FS="\t";OFS="\t"}{print $1,$3}' sampleReadsPerGene.out.tab
# Reverse Stranded Data
awk 'BEGIN{FS="\t";OFS="\t"}{print $1,$4}' sampleReadsPerGene.out.tab
```
#### Getting the Counts After Marking Duplicates
```bash
featureCounts -a GenomeDir/GCF_003013715.1_ASM301371v2_genomic.gtf -o sample_counts.txt -p sample_final.bam -s 0 # Unstranded Data, -p is for paired-end data
featureCounts -a GenomeDir/GCF_003013715.1_ASM301371v2_genomic.gtf -o sample_counts.txt -p sample_final.bam -s 1 # Forward Stranded Data
featureCounts -a GenomeDir/GCF_003013715.1_ASM301371v2_genomic.gtf -o sample_counts.txt -p sample_final.bam -s 2 # reversely Stranded Data
awk 'BEGIN{FS="\t";OFS="\t"}{if(NR>2) print $1,$7}' sample_counts.txt > sample_gene_counts.txt
```
