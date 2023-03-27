##### This markdown file for running FLYE Assembler for Single Isolate (In this case C.auris)
```bash
module load codes/flye-2.9
flye --nano-raw C_auris_combined.fastq.gz --genome-size 12.5m -o C_auris_flye_assembly -t 16 -i 4
```
```bash
medaka_consensus -i C_auris_combined.fastq.gz -d draft.fasta -o C_auris_medaka_polish -t 32 -m r1041_e82_260bps_sup_g632
```
