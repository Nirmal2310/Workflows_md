#### Running Blast Command Locally

##### Making a Custom Database
```bash
makeblastdb -in custom_seq.fasta -parse_seqids -blastdb_version 5 -title custom_db -dbtype nucl -out custom_seq
```
```bash
blastn -db /nfs_master/nirmal/database/custom_blast/seq.fasta -query C_auris_barcode01.contigs.fasta -out C_auris_barcode01_blast_out.tsv -num_threads 16 -max_target_seqs 1 -max_hsps 1 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"
```
```bash
blastn -db /nfs_master/nirmal/database/custom_blast/custom_seq -query C_auris_barcode01.contigs.fasta -out C_auris_barcode01_blast_out.tsv -num_threads 16 -outfmt "6 std staxids stitle" -perc_identity 80 -qcov_hsp_perc 100
```
#### Blast Standard Output ( -outfmt "6 std")
```bash
1  qseqid      query or source (gene) sequence id
2  sseqid      subject or target (reference genome) sequence id
3  pident      percentage of identical positions
4  length      alignment length (sequence overlap)
5  mismatch    number of mismatches
6  gapopen     number of gap openings
7  qstart      start of alignment in query
8  qend        end of alignment in query
9  sstart      start of alignment in subject
10  send        end of alignment in subject
11  evalue      expect value
12  bitscore    bit score
```
