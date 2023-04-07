#### Running Blast Command Locally

##### Making a Custom Database
```bash
makeblastdb -in custom_seq.fasta -parse_seqids -blastdb_version 5 -title "custom_db" -dbtype nucl
```
```bash
blastn -db /nfs_master/nirmal/database/custom_blast/seq.fasta -query C_auris_barcode01.contigs.fasta -out C_auris_barcode01_blast_out.tsv -num_threads 16 -max_target_seqs 1 -max_hsps 1 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"
```
