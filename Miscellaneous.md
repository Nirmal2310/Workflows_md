```bash
sed '/^#/d' YLB4_germline_called_filtered_passed_indels.vcf | awk 'BEGIN{FS="\t";OFS="\t"}{split($10,a,":"); print $1,$2,$4,$5,a[1]}' | awk 'BEGIN{FS="\t";OFS="\t"}{
if($5=="0/1") {print $1,$2,$3,$4"\t"$3"/"$4}
else if($5=="1/1") {print $1,$2,$3,$4"\t"$4"/"$4}
else if($5=="1/2") {split($4,a,","); print $1,$2,$3,$4"\t"a[1]"/"a[2]}
}' > YLB4_final_indels.txt
```
#### DINUMT RUN

```bash
while read p; do awk -F "\t" '{print $6" "$7}' ${p}_insert_size_metrices.txt | sed -n '8p' >> insert_size_metrics; done < list
```
