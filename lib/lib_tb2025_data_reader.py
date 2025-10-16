import ROOT
import array

FPGA_CHANNEL_NUMBER = 152
FPGA_VALID_CHANNEL_NUMBER = 144

MACHINE_GUN_MAX = 16

def read_tb2025_data(_root_tree, _machine_gun=MACHINE_GUN_MAX, _channel_number=FPGA_CHANNEL_NUMBER):
    data_frame = {}
    data_frame["timestamps_0"] = array.array('Q', [0] * (_machine_gun))
    data_frame["timestamps_1"] = array.array('Q', [0] * (_machine_gun))
    data_frame["daqh_list_0"] = array.array('I', [0] * (4*_machine_gun))
    data_frame["daqh_list_1"] = array.array('I', [0] * (4*_machine_gun))
    data_frame["tc_list_0"] = array.array('B', [0] * (_machine_gun*_channel_number))
    data_frame["tc_list_1"] = array.array('B', [0] * (_machine_gun*_channel_number))
    data_frame["tp_list_0"] = array.array('B', [0] * (_machine_gun*_channel_number))
    data_frame["tp_list_1"] = array.array('B', [0] * (_machine_gun*_channel_number))
    data_frame["val0_list_0"] = array.array('I', [0] * (_machine_gun*_channel_number))
    data_frame["val0_list_1"] = array.array('I', [0] * (_machine_gun*_channel_number))
    data_frame["val1_list_0"] = array.array('I', [0] * (_machine_gun*_channel_number))
    data_frame["val1_list_1"] = array.array('I', [0] * (_machine_gun*_channel_number))
    data_frame["val2_list_0"] = array.array('I', [0] * (_machine_gun*_channel_number))
    data_frame["val2_list_1"] = array.array('I', [0] * (_machine_gun*_channel_number))
    data_frame["crc32_list_0"] = array.array('I', [0] * (4*_machine_gun))
    data_frame["crc32_list_1"] = array.array('I', [0] * (4*_machine_gun))
    data_frame["last_heartbeat_0"] = array.array('I', [0] * (_machine_gun))
    data_frame["last_heartbeat_1"] = array.array('I', [0] * (_machine_gun))

    _root_tree.SetBranchAddress("timestamps_0", data_frame["timestamps_0"])
    _root_tree.SetBranchAddress("timestamps_1", data_frame["timestamps_1"])
    _root_tree.SetBranchAddress("daqh_list_0", data_frame["daqh_list_0"])
    _root_tree.SetBranchAddress("daqh_list_1", data_frame["daqh_list_1"])
    _root_tree.SetBranchAddress("tc_list_0", data_frame["tc_list_0"])
    _root_tree.SetBranchAddress("tc_list_1", data_frame["tc_list_1"])
    _root_tree.SetBranchAddress("tp_list_0", data_frame["tp_list_0"])
    _root_tree.SetBranchAddress("tp_list_1", data_frame["tp_list_1"])
    _root_tree.SetBranchAddress("val0_list_0", data_frame["val0_list_0"])
    _root_tree.SetBranchAddress("val0_list_1", data_frame["val0_list_1"])
    _root_tree.SetBranchAddress("val1_list_0", data_frame["val1_list_0"])
    _root_tree.SetBranchAddress("val1_list_1", data_frame["val1_list_1"])
    _root_tree.SetBranchAddress("val2_list_0", data_frame["val2_list_0"])
    _root_tree.SetBranchAddress("val2_list_1", data_frame["val2_list_1"])
    _root_tree.SetBranchAddress("crc32_list_0", data_frame["crc32_list_0"])
    _root_tree.SetBranchAddress("crc32_list_1", data_frame["crc32_list_1"])
    _root_tree.SetBranchAddress("last_heartbeat_0", data_frame["last_heartbeat_0"])
    _root_tree.SetBranchAddress("last_heartbeat_1", data_frame["last_heartbeat_1"])

    return data_frame

def all_channel_to_valid_channel(_all_channel_index):
    # for each 38 channels, the 0, 19 channel is not used
    if _all_channel_index < 0 or _all_channel_index >= FPGA_CHANNEL_NUMBER:
        return -1
    if (_all_channel_index % 19) == 0:
        return -1

    return _all_channel_index - (_all_channel_index // 19) - 1

def valid_channel_to_all_channel(_valid_channel_index):
    if _valid_channel_index < 0 or _valid_channel_index >= FPGA_VALID_CHANNEL_NUMBER:
        return -1
    return _valid_channel_index + (_valid_channel_index // 18) + 1

# * Get the adc value of a specific channel for a specific machine gun index
#   - data_frame: The data frame returned by read_tb2025_data
#   - _machine_gun_index: The index of the machine gun (0 to _machine_gun-1)
#   - _channel_index: The index of the channel
def get_channel_adc(data_frame, _vldb_index, _machine_gun_index, _valid_channel_index):
    if _valid_channel_index < 0 or _valid_channel_index >= FPGA_VALID_CHANNEL_NUMBER:
        return -1
    if _vldb_index < 0 or _vldb_index > 1:
        return -1
    all_channel_index = valid_channel_to_all_channel(_valid_channel_index)
    adc_value = data_frame["val0_list_" + str(_vldb_index)][_machine_gun_index * FPGA_CHANNEL_NUMBER + all_channel_index]
    return adc_value

def get_channel_tot(data_frame, _vldb_index, _machine_gun_index, _valid_channel_index):
    if _valid_channel_index < 0 or _valid_channel_index >= FPGA_VALID_CHANNEL_NUMBER:
        return -1
    if _vldb_index < 0 or _vldb_index > 1:
        return -1
    all_channel_index = valid_channel_to_all_channel(_valid_channel_index)
    tot_value = data_frame["val1_list_" + str(_vldb_index)][_machine_gun_index * FPGA_CHANNEL_NUMBER + all_channel_index]
    if tot_value >= 512:
        tot_value = (tot_value - 512) * 8
    return tot_value

def get_channel_toa(data_frame, _vldb_index, _machine_gun_index, _valid_channel_index):
    if _valid_channel_index < 0 or _valid_channel_index >= FPGA_VALID_CHANNEL_NUMBER:
        return -1
    if _vldb_index < 0 or _vldb_index > 1:
        return -1
    all_channel_index = valid_channel_to_all_channel(_valid_channel_index)
    toa_value = data_frame["val2_list_" + str(_vldb_index)][_machine_gun_index * FPGA_CHANNEL_NUMBER + all_channel_index]
    return toa_value
