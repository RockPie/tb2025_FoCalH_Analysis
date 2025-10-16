# Example Analysis Python Project for the FoCal TB 2025

## Prerequisites

- Python 3.8 or higher
- ROOT with PyROOT bindings (https://root.cern/install/)

To test if ROOT is correctly installed, you can run the following command in command line:

``` bash
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
```

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

## Read root data file

The library `lib/lib/lib_tb2025_data_reader.py` provides some functions to easily read the root data files.

#### Run the example script

You can run the example script `script/101_example_reader.py` to see how to read the root data file and generate the ADC/ToT/ToA waveforms for some example channels.

```bash
python script/101_example_reader.py -i <path_to_root_data_file>
```

#### Read root file

```python
import lib.lib_tb2025_data_reader as tb2025

root_data_file_path = "<path_to_root_file>"
root_data_file      = ROOT.TFile.Open(root_data_file_path)
root_data_tree      = root_data_file.Get("data_tree")
root_data_frame     = tb2025.read_tb2025_data(root_data_tree)
```

#### Get a specific ADC value

!!! Important
    The channel indexing in the function `get_adc_value`, `get_tot_value`, and `get_toa_value` is different from the raw data branch indexing.

For example, to get the ADC value of `VLDB+ Board #0`, `Channel 20`, `Machine Gun 5`, at `Event 33`:
```python
vldb_index          = 0
channel_index       = 20
machine_gun_index   = 5
event_index         = 33
root_data_tree.GetEntry(event_index)
adc_value = tb2025.get_adc_value(root_data_frame, vldb_index, channel_index, machine_gun_index)
```

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