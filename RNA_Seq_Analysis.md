#### Trim Raw Sequencing Reads to remove Adapter Sequences and Low Quality Reads
```bash
bbduk.sh Xmx20g in=sample_1.fastq.gz in2=sample_2.fastq.gz ref=/home/antpc/miniconda/envs/bbtools/bbtools/lib/resources/adapters.fa out=sample_trim_1.fastq.gz out2=sample_trim_2.fastq.gz ktrim=r k=23 mink=11 hdist=1 tpe tbo threads=8 qtrim=rl minlength=40 trimq=15 maq=25 ftl=15 forcetrimright2=10 overwrite=true
```
#### Remove rRNA Reads from Trimmed FastQ files
```bash
ribodetector_cpu -t 8 -i sample_trim_1.fastq.gz sample_trim_2.fastq.gz -l 150 -e norrna --chunk_size 5000 -o sample_final_1.fastq.gz sample_final_2.fastq.gz -r sample_rRNA_1.fastq.gz sample_rRNA_2.fastq.gz
```
#### Indexing Reference Genome using STAR
```bash
STAR --runThreadN 30 --runMode genomeGenerate --genomeDir GenomeDir/star_index --genomeFastaFiles GenomeDir/GCF_003013715.1_ASM301371v2_genomic.fna --sjdbGTFfile GenomeDir/GCF_003013715.1_ASM301371v2_genomic.gtf --sjdbOverhang 149 # sjdbOverhang will be equal to mean read length -1
```
#### Mapping to the Reference Genome using STAR
```bash
STAR --genomeDir GenomeDir/star_index --readFilesIn sample_final_1.fastq.gz sample_final_2.fastq.gz --runThreadN 12 --quantMode GeneCounts --outSAMtype BAM Unsorted --outFileNamePrefix sample --twopassMode Basic --outSAMstrandField intronMotif --readFilesCommand zcat
samtools sort -@ 6 sample8Aligned.out.bam -o SRR14119418.Aligned.sortedByCoord.out.bam
```
#### Remove Optical and PCR Duplicated
```bash
gatk MarkDuplicates --java-options -Xmx80G -I sample.Aligned.sortedByCoord.out.bam -O sample_final.bam -M sample_md.txt --REMOVE_DUPLICATES true --TMP_DIR $PWD
samtools index -@ 6 sample_final.bam
```
#### Checking for strandedness
```bash
awk 'FNR == 3 {print}' *ReadsPerGene.out.tab > no_feature.txt
awk '{ for (i=1; i<=NF; i++) s[i]+=$i } END { for (i=1; i<=NF; i++) printf "%s ", s[i] }' no_feature.txt > sum.txt
awk '{if ($3/$4 < 0.4) print "forward"; else if ($4/$3 < 0.4) print "reverse"; else print "unstranded" }' sums.txt > strand.txt
```
#### Getting the Counts
```bash

```
