##### This markdown file for running FLYE Assembler for Single Isolate (In this case C.auris)
```bash
module load codes/flye-2.9
flye --nano-raw C_auris_combined.fastq.gz --genome-size 12.5m -o C_auris_flye_assembly -t 16 -i 4
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
