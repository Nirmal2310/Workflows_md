#### Compression of BAM File to CRAM
```bash
samtools view -@ 8 -T reference.fasta -C -o sample.cram sample.bam
```
#### Compression and Decompression of Illumina Fastq File using SPRING
```bash
spring -c -i file_1.fastq.gz file_2.fastq.gz -o file.spring -t 16 -g  # (Compression)
spring -d -i file.spring -o file_1.fastq.gz file_2.fastq.gz -g -t 16 (Decompression)
```
#### Compression and Decompression of Nanopore Fastq File using NanoSpring
```bash
NanoSpring -c -t 16 -i file.fastq.gz -o file.NanoSpring # Compression
NanoSpring -d -t 16 -i file.NanoSpring -o file.fastq.gz # Decompression
```
#### Compression and Decompression of Nanopore Signal Data (Fast5)
```bash
h5repack -f UD=32020,5,0,0,2,1,1 input.fast5 output.fast5 #(compression)
h5repack -f GZIP=1 input.fast5 output.fast5 #(decompression)
```
