# This markdown file contains the information about RGI pipeline installtion and working script

**Installation**
> Make sure that your system has docker installed and your profile has the priviledge to install softwares using docker
```bash
docker pull finlaymaguire/rgi:latest
```
**Downloading and loading CARD database locally**
```bash
wget https://card.mcmaster.ca/latest/data
tar -xvf data ./card.json
docker run -v $PWD:$PWD --workdir $PWD --rm finlaymaguire/rgi:latest rgi load --card_json ./card.json --local
```
**RGI script**
> Make sure that the input fasta files are present in the working directory as well as the CARD database. 
```bash
docker run -v $PWD:$PWD --workdir $PWD --rm finlaymaguire/rgi:latest rgi main --input_sequence <input fasta file> --output_file <output file prefix> --input_type contig --local --clean
```
**Output.txt** will contain the information regarding the antimicrobial genes present in the fasta file. 
