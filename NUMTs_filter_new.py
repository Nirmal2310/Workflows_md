import argparse
import pandas as pd
import sys

def main(numt_file, sam_file, min_reads, max_length):
    sample_name = numt_file.replace("_final.txt","")
    print(sample_name)
    df_sam = pd.read_csv(sam_file, names=['QNAME','FLAG','RNAME','POS','MAPQ','CIGAR','RNEXT','PNEXT','TLEN','SEQ','QUAL','SA','XA','MC','MD','PG','NM','AS','XS'], sep = "\t", engine = 'python', comment="@")
    df_sam = df_sam[(df_sam["MAPQ"].astype(int) > 0) & ((df_sam['RNAME'] == "chrM") | (df_sam['RNEXT'] == "chrM"))]
    df_sam = df_sam[~df_sam.RNAME.isin(['chrM'])]
    numt_df = pd.read_csv(numt_file, names=['CHR', 'START', 'END', 'REF', 'MSTART', 'MEND', 'MLENGTH'], sep = "\t", engine = 'python')
    numt_df = numt_df[(numt_df['CHR'] != "chrUn_KI270753v1")]
    len = round(float(max_length)/2)
    numt_df['Cluster_Start'] = numt_df['START'].astype(int) - len
    numt_df['Cluster_End'] = numt_df['END'].astype(int) + len
    final_df = pd.DataFrame(columns=['CHR', 'START', 'END', 'MSTART', 'MEND', 'MLENGTH', 'Cluster_Start', 'Cluster_End'])
    for i in range(0,numt_df.shape[0]):
        seq=numt_df.iloc[i,0]
        start=numt_df.iloc[i,7]
        end=numt_df.iloc[i,8]
        s = 0
        filtered_sam = df_sam[(df_sam['RNAME'].astype(str) == seq)]
        for j in range(0, filtered_sam.shape[0]):
            if(start <= filtered_sam.iloc[j,3].astype(int) <= end):
                s=s+1
        if(s >= int(min_reads)):
            print(s)
            final_df = pd.concat([final_df, pd.DataFrame([numt_df.iloc[i]])], ignore_index=True)
    final_df.to_csv(sample_name + "_min_" + min_reads + "_reads" + "_filtered.tsv",sep="\t", index=False, encoding='utf-8', header=False)

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is a script for filtering the VCF file obtained from dinumt.It takes the dinumt VCF file, the support sam file, mininum reads to support the NUMT and maximum distance to cluster the NUMTs.")

    # VCF file argument
    parser.add_argument('-n', '--numt', type=str, required=True, help='Path to the VCF file.')

    # SAM file argument
    parser.add_argument('-s', '--sam', type=str, required=True, help='Path to the Discordant SAM file.')

    # User input 1 argument
    parser.add_argument('-m', '--min_reads', type=str, required=True, help='Minimum Number of Reads Supporting the Cluster.')

    # User input 2 argument
    parser.add_argument('-l', '--max_length', type=str, required=True, help='Maximum Distance to Group NUMTs. (mean insert size + 3*sd))')

    args = parser.parse_args()
    
    main(args.numt, args.sam, args.min_reads, args.max_length)
