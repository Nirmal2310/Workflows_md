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
STAR --runThreadN 30 --runMode genomeGenerate --genomeDir GenomeDir/star_index --genomeFastaFiles --sjdbGTFfile --sjdbOverhang
```
#### Mapping to the Reference Genome using STAR
```bash
STAR --genomeDir GenomeDir/star_index --readFilesIn sample_final_1.fastq.gz sample_final_2.fastq.gz --runThreadN 12 --quantMode GeneCounts --outSAMtype BAM SortedByCoordinate --outFileNamePrefix sample --twopassMode Basic --outSAMstrandField intronMotif --readFilesCommand zcat
```
