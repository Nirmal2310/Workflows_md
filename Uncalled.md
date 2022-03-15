# This markdown file contains scripts for installing and running UNCALLED

**Installation**
```bash
module load compilers/gcc-9.3
git clone --recursive https://github.com/skovaka/UNCALLED.git
cd UNCALLED
python3 setup.py install --user
```
**Fast5 mapping**
```bash
uncalled index -o <output_index_prefix> reference.fasta # can be multifasta file
uncalled map -t <> <output_index_prefix> fast5_list.txt > uncalled_out.paf
```
**UNCALLED PAF FILE DESCRIPTION**
- Column 1: Query sequence name
- Column 2: Query sequence length
- Column 3: Query start (0-based)
- Column 4: Query end (0-based)
- Column 5: Relative strand ( +, - or *)
- Column 6: Target sequence name
- Column 7: Target sequence length
- Column 8: Target start
- Column 9: Target end
- Column 10: Number of residues match
- Column 11: Alignment block length
- Column 12: Mapping quality

> Both realtime and fast5 mapping outputs contains following custom attributes in each PAF entry:

- mt: map time (Time in milliseconds it took to map the read)
- ch: channel (MinIon channel that the read came from)
- st: start sample (Global sequencing start time of the read)

**Accuracy Statistics**

To check the accuracy of UNCALLED mapping, we will first map the basecalled reads with the reference fasta file using minimap2.
```bash
minimap2 -x map-ont -t <> reference.fasta combined.fastq > minimap2_true.paf
uncalled pafstats -r minimap2_true.paf uncalled_out.paf > stats.txt
```
- TP:true positive - percent infile reads that overlap reference read locations 
- FP:fasle positive - percent infile reads that do not overlap reference read locations
- TN:true negative - percent of reads which were not aligned in reference or infile
- FN:false negative - percent of reads which were aligned in the reference but not in the infile
- NA:not aligned/not applicable

> **Masking**: For eukaryotic genome references with many repeats and low complexity regions it is recommended to apply masking in order to get optimum accuracy.

```bash
module load compilers/gcc-9.3
UNCALLED/masking/mask_internal.sh <target_reference.fasta> 10 30 <output_prefix> # Recommended parameters
k-mer length: 10
iterations: 30
```
```bash
bowtie-build <target_reference.fasta> <bowtie_index_prefix>
UNCALLED/masking/mask_external.sh <bowtie_index_prefix> <output_prefix>mask30.fa 50 5 16 <out_prefix>
minimum repeat length: 50
minimum repeat copy number: 5
number of threads: 16
```
Use this double masked reference fasta file for mapping eukaryotic reads.

**UNCALLED Real-time**
```bash
uncalled <reference_index_prefix> --port 8000 -t <> --enrich -c 3 > uncalled_out.paf
enrich = This mode will keep reads that map to the reference provided.
-c/--max-chunks = number of chunks to attempt mapping before giving up on a read (3 is optimum for enrichment and 10 is optimum for depletion).
--chunk-size = size of chunks in seconds
--port = MinION device port
```
```bash
uncalled <reference_index_prefix> --port 8000 -t <> --deplete -c 10 > uncalled_out.paf
deplete = This mode will eject reads that map to the provided reference fasta file.
--even = by specifying this parameter UNCALLED will eject reads from even channels.
--odd = will only eject reads from odd channels.
```
Real-time output paf file will also contain the following attributes:
- ej: ejected (Time that the eject signal was sent, in milliseconds since last chunk was received.)
- kp: kept (Time that UNCALLED decided to keep the read, in milliseconds since last chunk was received.) 
- en: ended (Time that UNCALLED determined the read ended, in milliseconds since last chunk was received.)
- mx: mux scan (Time that the read would have been ejected, had it not have occured within a mux scan.) 
- wt: wait time (Time in milliseconds that the read was queued but was not actively being mapped, either due to thread delays or waiting for new chunks.)

