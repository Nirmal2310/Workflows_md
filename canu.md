## CANU is used for assembling Long Reads (mainly PacBio and Nanopore). Here I am doing all the three steps i.e. correct, trim, assemble, manually.
### 1. Correction
```bash
canu -correct -p C_auris_barcode01 -d C_auris_barcode01_correction genomeSize=13m -nanopore barcode01_combined.fastq.gz useGrid=false

p=process name
d=directory name
genomeSize=approx genome size to calculate the depth
useGrid=false (to run canu locally). Through this canu automatically utilize all the available resources and distribute them accordingly among all the steps 
```
### 2. Trimming
```bash
canu -trim -p C_auris_barcode01 -d C_auris_barcode01_trimming genomeSize=13m -corrected -nanopore C_auris_barcode01_correction/C_auris_barcode01.correctedReads.fasta.gz useGrid=false
```
### 3. Assembling
```bash
canu -p C_auris_barcode01 -d C_auris_barcode01_assembly genomeSize=13m correctedErrorRate=0.200 -trimmed -corrected -nanopore C_auris_barcode01_trimming/C_auris_barcode01.trimmedReads.fasta.gz useGrid=false
```
