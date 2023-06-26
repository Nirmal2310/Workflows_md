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
