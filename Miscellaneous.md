```bash
sed '/^#/d' YLB4_germline_called_filtered_passed_indels.vcf | awk 'BEGIN{FS="\t";OFS="\t"}{split($10,a,":"); print $1,$2,$4,$5,a[1]}' | awk 'BEGIN{FS="\t";OFS="\t"}{
if($5=="0/1") {print $1,$2,$3,$4"\t"$3"/"$4}
else if($5=="1/1") {print $1,$2,$3,$4"\t"$4"/"$4}
else if($5=="1/2") {split($4,a,","); print $1,$2,$3,$4"\t"a[1]"/"a[2]}
}' > YLB4_final_indels.txt
```
#### DINUMT RUN

```bash
while read p; do awk -F "\t" '{print $6" "$7}' ${p}_insert_size_metrics.txt | sed -n '8p' >> insert_size_metrics; done < list
while read p; do awk '{print $1*5}' ${p}_autocov.txt >> max_cov; done < list
awk 'BEGIN{FS=" ";OFS=" "}{print $1,$2,($1+3*$2), 2*(($1+3*$2))}' insert_size_metrics > temp
paste -d " " list max_cov temp > numt_info
while read p q r s t u; do echo "dinumt.pl --mask_filename=/nfs_master/nirmal/GenomeIndiaProject/CBR/bamfiles/refNumts.38.bed --input_filename=${p}_marked_duplicates.bam --reference=/nfs_master/nirmal/NUMT_testing/GRCh38_full_analysis_set_plus_decoy_hla.fa --output_filename=${p}_dinumt.vcf --prefix=$p --len_cluster_include=`printf '%.*f\n' 0 $t`  --len_cluster_link=`printf '%.*f\n' 0 $u` --max_read_cov=`printf '%.*f\n' 0 $q` --output_support --support_filename=${p}_numt_support.sam --ucsc"; done < "numt_info" | parallel -j 16
```
#### Filtering the DINUMT VCF
```bash
grep -v "#" sample_dinumt.vcf | grep "MLEN" | grep "PASS" | awk 'BEGIN{FS="\t";OFS="\t"}{split($8,a,";"); print $1,$2,a[3],a[7],a[5],a[6]}' | sed 's/MSTART=//g;s/MEND=//g;s/END=//g;s/MLEN=//g' | awk 'BEGIN{FS="\t";OFS="\t"}{if(($5-$4) > $6) print $1,$2,$3,$4,$5,"-"; else print $1,$2,$3,$4,$5,"+"}' > sample_final.txt
grep -v "#" sample_dinumt.vcf | grep "MLEN" | grep "PASS" | awk 'BEGIN{FS="\t";OFS="\t"}{split($8,a,";"); print $1,$2,a[3],a[7],a[5],a[6]}' | sed 's/MSTART=//g;s/MEND=//g;s/END=//g;s/MLEN=//g' | awk 'BEGIN{FS="\t";OFS="\t"}{if(($5-$4) > $6) print $1,$2,$3+$6,$4,$5,"-",$6; else print $1,$2,$3+$6,$4,$5,"+",$6}' | awk 'BEGIN{FS="\t";OFS="\t"}{if($6=="-") print $1,$2,$3,$4,$5,$6,$7,$5+$7,16570+$6+$7; else print $1,$2,$3,$4,$5,$6,$7,$4,$5}' > sample_final.txt
```
#### Concatenating Coverage Data
```bash
while read p; do echo $p `cat ${p}_autocov.txt` `cat ${p}_mitocov.txt`; done < list | awk 'BEGIN{FS=" ";OFS="\t"}{print $1,$2,$3}' > sample_coverage.txt
```
