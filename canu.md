## CANU is used for assembling Long Reads (mainly PacBio and Nanopore). Here I am doing all the three steps i.e. correct, trim, assemble, manually.
### 1. Trimming
```bash
canu -correct -p DM_BL -d DM_BL_CANU genomeSize=130m -nanopore DM_BL_hac.fastq useGrid=false

p=process name
d=directory name
genomeSize=approx genome size to calculate the depth
useGrid=false (to run canu locally). Through this canu automatically utilize all the available resources and distribute them accordingly among all the steps 
```
