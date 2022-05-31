# ReadFish command for flongle flow cell type
```bash
sudo /home/user/miniconda3/envs/readfish/bin/readfish targets --device MN37483 --experiment-name "RF Drosophila adaptive sampling" --toml Drosophila_chr_selection.toml --log-file dm_rf_2.log --channels 1 126
```
# ReadFish command for SpotOn flow cell type
```bash
sudo /home/user/miniconda3/envs/readfish/bin/readfish targets --device MN37483 --experiment-name "RF falciparum adaptive sampling" --toml falciparum_chr_selection.toml --log-file pf_rf.log
```
# Guppy Basecall Server
```bash
/opt/ont/guppy/bin/guppy_basecall_server --log_path /var/log/guppy --config dna_r9.4.1_450bps_hac.cfg --num_callers 1 --cpu_threads_per_caller 62 --port /tmp/.guppy/5555 --ipc_threads 3 --device cuda:0:90%
```
