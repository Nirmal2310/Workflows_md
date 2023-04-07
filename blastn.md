#### Running Blast Command Locally
```bash
blastn -db /nfs_node3/nirmal/database/blast/16S_ribosomal_RNA/16S_ribosomal_RNA -query fasta_header -out out -num_threads 128 -max_target_seqs 1 -max_hsps 1 -outfmt 6 std staxids stitle
```
