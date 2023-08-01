### This repository contains all the commands for Methylation Calling Analysis
#### Converting Bam File to BED file to get the coordinates of Modified regions
##### Tool: modkit
```bash
modkit pileup sample.bam sample.bed -t 16 --cpg --ref reference.fasta # Tabulates base modification calls across genomic positions.
# --cpg: Only output counts at CpG motifs.
modkit summary sample.bam -t 16 > sample_modified_summary.txt # Summarize the mod tags present in a bam and get basic statistics.
```
#### bedMethyl column descriptions

| column | name                  | description                                                                    | type  |
|--------|-----------------------|--------------------------------------------------------------------------------|-------|
| 1      | chrom                 | name of reference sequence from BAM header                                     | str   |
| 2      | start position        | 0-based start position                                                         | int   |
| 3      | end position          | 0-based exclusive end position                                                 | int   |
| 4      | modified base code    | single letter code for modified base                                           | str   |
| 5      | score                 | Equal to N<sub>valid_cov</sub>.                                                | int   |
| 6      | strand                | '+' for positive strand '-' for negative strand, '.' when strands are combined | str   |
| 7      | start position        | included for compatibility                                                     | int   |
| 8      | end position          | included for compatibility                                                     | int   |
| 9      | color                 | included for compatibility, always 255,0,0                                     | str   |
| 10     | N<sub>valid_cov</sub> | See definitions below.                                                         | int   |
| 11     | fraction modified     | N<sub>mod</sub> / N<sub>valid_cov</sub>                                        | float |
| 12     | N<sub>mod</sub>       | See definitions below.                                                         | int   |
| 13     | N<sub>canonical</sub> | See definitions below.                                                         | int   |
| 14     | N<sub>other_mod</sub> | See definitions below.                                                         | int   |
| 15     | N<sub>delete</sub>    | See definitions below.                                                         | int   |
| 16     | N<sub>filtered</sub>  | See definitions below.                                                         | int   |
| 17     | N<sub>diff</sub>      | See definitions below.                                                         | int   |
| 18     | N<sub>nocall</sub>    | See definitions below.                                                         | int   |

#### Definitions:

* N<sub>mod</sub> - Number of calls passing filters that were classified as a residue with a specified base modification.
* N<sub>canonical</sub> - Number of calls passing filters were classified as the canonical base rather than modified. The
exact base must be inferred by the modification code. For example, if the modification code is `m` (5mC) then
the canonical base is cytosine. If the modification code is `a`, the canonical base is adenosine.
* N<sub>other mod</sub> - Number of calls passing filters that were classified as modified, but where the modification is different from the listed base (and the corresponding canonical base is equal). For example, for a given cytosine there may be 3 reads with
`h` calls, 1 with a canonical call, and 2 with `m` calls. In the bedMethyl row for `h` N<sub>other_mod</sub> would be 2. In the
`m` row N<sub>other_mod</sub> would be 3.
* N<sub>valid_cov</sub> - the valid coverage. N<sub>valid_cov</sub> = N<sub>mod</sub> + N<sub>other_mod</sub> + N<sub>canonical</sub>, also used as the `score` in the bedMethyl
* N<sub>diff</sub> - Number of reads with a base other than the canonical base for this modification. For example, in a row
for `h` the canonical base is cytosine, if there are 2 reads with C->A substitutions, N<sub>diff</sub> will be 2.
* N<sub>delete</sub> - Number of reads with a deletion at this reference position
* N<sub>filtered</sub> - Number of calls where the probability of the call was below the threshold. The threshold can be
set on the command line or computed from the data (usually filtering out the lowest 10th percentile of calls).
* N<sub>nocall</sub> - Number of reads aligned to this reference position, with the correct canonical base, but without a base
modification call. This can happen, for example, if the model requires a CpG dinucleotide and the read has a
CG->CH substitution such that no modification call was produced by the basecaller.

#### Filtering BED File:
This command will filter the sites that has atleast 10X sequencing depth and the methylated sites frequency is 50%.
```bash
sed -i 's/ /\t/g' sample.bed
awk 'BEGIN{FS="\t";OFS="\t"}{if($10>=10 && $11 >=0.5}' sample.bed > sample_filtered.bed
```
