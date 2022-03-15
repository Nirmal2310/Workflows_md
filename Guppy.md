# Guppy Basecalling Markdown
This file contains the installion and working of tools provided by guppy.

**Installation**
```bash
wget https://mirror.oxfordnanoportal.com/software/analysis/ont-guppy-6.0.6-1.el7.x86_64.rpm
su # Enter superuser mode
yum install epel-release
yum install ont-guppy-6.0.6-1.el7.x86_64.rpm
```
Guppy will be installed at **/opt/ont/guppy/**

**Basecalling Script**
```bash
guppy_basecaller -c /opt/ont/guppy/data/basecalling_model.cfg -i </path/to/the/input/fast5/files> --cpu_threads_per_caller <> -s </path/for/the/output/fastq/files> --recursive --compress_fastq --num_callers <> --device cuda:0,1:90% --trim_adapters
```
```bash
c = basecalling model config file for our flowcell/kit combination
i = path of the directory containing fast5 files
cpu_threads_per_caller = number of working threads. GPU basecalling allows only one CPU support thread per GPU caller.
num_callers = number of parallel basecallers or maximum number of CPU threads.
chunks_per_runner (parameter in config file) = Maximum number of chunks which can be submitted to a single neural network runner before computation. Increasing this will increase GPU basecalling performance. fast -> 160, hac -> 256, sup -> 208
gpu_runners_per_device = Number of neural network runners to create per CUDA device. Increasing this may improve GPU performance but will increase GPU memory use. fast -> 8, hac -> 4, sup -> 12 
recursive = run basecalling for multiple fast5 files
compress_fastq = output fastq files will be gzipped
device = specifying GPU devices (0,1 are the GPUs installed in the system and guppy will use 90% of both the GPUs)
trim_adpaters = Trim adpater sequences from the output fastq files
```
> If your system has GPUs make sure to use them for basecalling as basecalling using only CPU is very very slow and make sure you have cuda installed.
> Visit the following [link](https://gist.github.com/sirselim/2ebe2807112fae93809aa18f096dbb94) for more information about how to optimize guppy basecaller based on the computing power. 
