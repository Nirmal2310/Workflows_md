```bash
sed '/^#/d' YLB4_germline_called_filtered_passed_indels.vcf | awk 'BEGIN{FS="\t";OFS="\t"}{split($10,a,":"); print $1,$2,$4,$5,a[1]}' | awk 'BEGIN{FS="\t";OFS="\t"}{
if($5=="0/1") {print $1,$2,$3,$4"\t"$3"/"$4}
else if($5=="1/1") {print $1,$2,$3,$4"\t"$4"/"$4}
else if($5=="1/2") {split($4,a,","); print $1,$2,$3,$4"\t"a[1]"/"a[2]}
}' > YLB4_final_indels.txt
```
#### DINUMT RUN

```bash
while read p; do awk -F "\t" '{print $6" "$7}' ${p}_insert_size_metrics.txt | sed -n '8p'; done < list > insert_size_metrics
while read p; do awk '{print $1*5}' ${p}_autocov.txt; done < list > max_cov
awk 'BEGIN{FS=" ";OFS=" "}{print $1,$2,($1+3*$2), 2*(($1+3*$2))}' insert_size_metrics > temp
paste -d " " list max_cov temp > numt_info
while read p q r s t u; do echo "dinumt.pl --mask_filename=/nfs_master/nirmal/GenomeIndiaProject/CBR/bamfiles/refNumts.38.bed --input_filename=${p}_marked_duplicates.bam --reference=/nfs_master/nirmal/NUMT_testing/GRCh38_full_analysis_set_plus_decoy_hla.fa --output_filename=${p}_dinumt.vcf --prefix=$p --len_cluster_include=`printf '%.*f\n' 0 $t`  --len_cluster_link=`printf '%.*f\n' 0 $u` --max_read_cov=`printf '%.*f\n' 0 $q` --ucsc"; done < "numt_info" | parallel -j 16
```
#### Filtering the DINUMT VCF
```bash
grep -v "#" sample_dinumt.vcf | grep "MLEN" | grep "PASS" | awk 'BEGIN{FS="\t";OFS="\t"}{split($8,a,";"); print $1,$2,a[7],a[5],a[6]}' | sed 's/MSTART=//g;s/MEND=//g;s/END=//g;s/MLEN=//g' | awk 'BEGIN{FS="\t";OFS="\t"}{if(($4-$3) > $5) print $1,$2-1,$2,$3,$4,"-",$5; else print $1,$2-1,$2,$3,$4,"+",$5}' > sample_final.txt
```
#### Concatenating Coverage Data
```bash
while read p; do echo $p `cat ${p}_autocov.txt` `cat ${p}_mitocov.txt`; done < list | awk 'BEGIN{FS=" ";OFS="\t"}{print $1,$2,$3}' > sample_coverage.txt
```
#### MToolBox From BAM File
```bash
samtools view -h sample_sorted.bam chrM | samtools sort -n | samtools fastq -@ 8 - -1 sample.R1.fastq.gz -2 sample.R2.fastq.gz -0 /dev/null -s /dev/null -n
ls sample*fastq.gz | sed 's/ /\n/g' > sample.lst
bash mtoolbox_config.sh -i sample
MToolBox.sh -i sample.conf -m "-t 16" -a "-t 16" && rm -r sample*fastq.gz
```
#### Extracting Metadata using BioSample ID
```bash
cat biosample_id.txt | join-into-groups-of 10 | xargs -n 1 sh -c 'epost -db biosample -id "$0" -format acc | elink -target sra | efetch -db sra -format runinfo -mode xml | xtract -pattern Row -def "NA" -element Run spots bases spots_with_mates avgLength size_MB download_path Experiment LibraryStrategy LibrarySelection LibrarySource LibraryLayout InsertSize InsertDev Platform Model SRAStudy BioProject ProjectID Sample BioSample SampleType TaxID ScientificName SampleName CenterName Submission Consent >> metadata.txt'
# biosample_id.txt file has the required BIOSAMPLE IDs
```
#### Removing Files with Zero NUMT Calls
```bash
for x in "$(wc -l *min*5* | awk -F " " '{if($1==0) print $2}')"; do rm -r $x; done
```
#### Generating 10000 random 9-mers genome coordinates
```bash
bedtools random -l 9 -n 100000 -seed 1234 -g chr_size.txt
# l is the length of the region
# n is the total number of coordinates to be produced
# seed is for producing reproducible result
# g is the file containing size of the chromosomes
```

#### Autokill a process after a specific time
```bash
# I am running Icarust simulator for 48 hours and I am using timeout command to kill the command after 48 hours
timeout --foreground -k 48h 48h cargo run --release -- -s /DATA2/config_str.toml -v
```
#### Get the Download Link from the Accession Number using FFQ
```bash
while read id; do ffq --ftp $id | grep -Eo '"url": "[^"]*"' | grep -o '"[^"]*"$'; done < "accession_list" > ftp_link

sed -i 's/"//g;s/^/wget -c /g' ftp_link

cat ftp_link | parallel -j 2 {}
```
#### Get the Phred Score from Fastq File using bioawk (Bioawk is installed using conda)
```bash
zcat sample.fastq.gz |  bioawk -c fastx '{print meanqual($qual)}' > qual.txt
```
```r
tmp <- read.table(file="qual.txt", header = FALSE)

colnames(tmp) <- "Phred"

tmp <- tmp %>%
  mutate(Bin = cut(Phred, breaks = c(seq(1,max(Phred),1),max(Phred)), include.lowest = TRUE, right = TRUE, labels = as.character(c(seq(1,max(Phred),1))))) %>%
  select(-Phred) %>%
  group_by(Bin) %>% summarise(Counts = n())

tmp %>% ggplot(aes(Bin,Counts)) +
  geom_bar(stat = "identity", fill = "#00005E") +
  theme_classic() +
  xlab("Phred Score") +
  ylab("Frequency") +
  theme(
    axis.title.x = element_text(size = 14, face = "bold", colour = "black"),
    axis.title.y = element_text(size = 14, face = "bold", colour = "black"),
    strip.text.x = element_text(size = 14, face = "bold", colour = "black"),
    axis.text.y= element_text(size=14, face = "bold", colour = "black"),
    axis.text.x= element_text(size=14, face = "bold", colour = "black"),
    legend.title= element_text(colour="black",size=14, face = "bold"),
    legend.text= element_text(colour="black", size=14, face = "bold"),
    axis.line = element_line(colour = "black", linewidth = 0.5, linetype = "solid" ),
    strip.background = element_blank(),
    legend.position = "right"
  )
```
