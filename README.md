# Example Analysis Python Project for the FoCal TB 2025

## Data preparation

The test beam data is stored in the EOS system at CERN. 

#### Raw data files

The raw data files are in the directory `/eos/experiment/alice/focal/tb2025_Oct_SPS/FoCalH/data/beam`

You can copy the data files with the `scp` command. For example, to copy a single file:

```
scp <user_name>@lxplus.cern.ch:/eos/experiment/alice/focal/tb2025_Oct_SPS/FoCalH/data/beam/Run0142.ch2g <target_directory>
```

Here `<user_name>` is your CERN username and `<target_directory>` is the directory on your local machine where you want to store the file.

#### Root data files

The root data files are in the directory `/eos/experiment/alice/focal/tb2025_Oct_SPS/FoCalH/root/beam`

You can copy the root files with the `scp` command. For example, to copy a single file:

```
scp <user_name>@lxplus.cern.ch:/eos/experiment/alice/focal/tb2025_Oct_SPS/FoCalH/root/beam/Run0142.root <target_directory>
```

Here `<user_name>` is your CERN username and `<target_directory>` is the directory on your local machine where you want to store the file.

## Root file structure

The root files contain a tree named `data_tree`. The branches of the tree are:
- `timestamps_0`: Timestamps of each event on **VLDB+ Board #0**
- `timestamps_1`: Timestamps of each event on **VLDB+ Board #1**
- `val0_list_0`: ADC values of each event on **VLDB+ Board #0**
- `val0_list_1`: ADC values of each event on **VLDB+ Board #1**
- `val1_list_0`: ToT values of each event on **VLDB+ Board #0**
- `val1_list_1`: ToT values of each event on **VLDB+ Board #1**
- `val2_list_0`: ToA values of each event on **VLDB+ Board #0**
- `val2_list_1`: ToA values of each event on **VLDB+ Board #1**
- `tc_list_0`: Tc flag values of each event on **VLDB+ Board #0**
- `tc_list_1`: Tc flag values of each event on **VLDB+ Board #1**
- `tp_list_0`: Tp flag values of each event on **VLDB+ Board #0**
- `tp_list_1`: Tp flag values of each event on **VLDB+ Board #1**
- `crc32_list_0`: CRC32 values of each event on **VLDB+ Board #0**
- `crc32_list_1`: CRC32 values of each event on **VLDB+ Board #1**
- `last_heartbeat_0`: Last heartbeat values of each event on **VLDB+ Board #0** (not implemented)
- `last_heartbeat_1`: Last heartbeat values of each event on **VLDB+ Board #1** (not implemented)