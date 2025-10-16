import os, sys, ROOT, time
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import lib.lib_tb2025_data_reader as tb2025

def main():
    parser = argparse.ArgumentParser(description='Example ROOT file reader')
    parser.add_argument('-i', '--input', required=False, help='Input ROOT file', default=os.path.join(os.path.dirname(__file__), '../data/beamtests/Run0143.root'))
    parser.add_argument('-o', '--output', required=False, help='Output ROOT file', default='')
    parser.add_argument('-e', '--events', type=int, default=-1, help='Number of events to read')
    args = parser.parse_args()

    script_name = os.path.basename(__file__)
    print(f"Running script: {script_name}")

    input_file = args.input
    if not os.path.isfile(input_file):
        print(f"Error: File {input_file} does not exist.")
        return
    
    input_file = ROOT.TFile.Open(input_file)
    if not input_file or input_file.IsZombie():
        print(f"Error: Could not open file {input_file}.")
        return
    
    # create output file
    output_file = args.output
    if not output_file:
        # create in default output file folder dump/<script_name>/
        output_dir = os.path.join("dump", script_name)
        os.makedirs(output_dir, exist_ok=True)
        # assign output file name the same as input file name but with .root extension
        input_base_name = os.path.basename(args.input)
        output_file = os.path.join(output_dir, input_base_name)
    output_file = ROOT.TFile.Open(output_file, "RECREATE")
    if not output_file or output_file.IsZombie():
        print(f"Error: Could not create output file {output_file}.")
        return
    
    root_tree = input_file.Get("data_tree")
    if not root_tree:
        print("Error: Tree 'data_tree' not found in the ROOT file.")
        return
    
    data_frame = tb2025.read_tb2025_data(root_tree, _machine_gun=16)
    
    event_number = root_tree.GetEntries()
    print(f"Number of events in the tree: {event_number}")

    event_to_read = args.events if args.events > 0 else event_number

    example_vldb_to_display = [0, 1] # show all vldb
    # ! Here is the valid channel index, excluding the COMMON_MODE (CM) and CALIBRATION (Calib) channels
    # ! So only 72 channels are valid for each H2GCROC
    example_channel_to_display = [0, 1, 2, 3, 18, 19, 20, 21, 37, 38, 39, 40]
    list_adc_waveforms = []
    for _vldb_index in example_vldb_to_display:
        for _chn in example_channel_to_display:
            th2d_adc = ROOT.TH2F(f"vldb {_vldb_index}, _adc_ch{_chn}", f"ADC Waveform Channel {_chn} in VLDB {_vldb_index};Time Bin;ADC", tb2025.MACHINE_GUN_MAX, 0, tb2025.MACHINE_GUN_MAX, 256, 0, 1024)
            th2d_adc.SetStats(0)
            list_adc_waveforms.append(th2d_adc)
    list_tot_waveforms = []
    for _vldb_index in example_vldb_to_display:
        for _chn in example_channel_to_display:
            th2d_tot = ROOT.TH2F(f"vldb {_vldb_index}, _tot_ch{_chn}", f"ToT Waveform Channel {_chn} in VLDB {_vldb_index};Time Bin;ToT", tb2025.MACHINE_GUN_MAX, 0, tb2025.MACHINE_GUN_MAX, 256, 0, 4096)
            th2d_tot.SetStats(0)
            list_tot_waveforms.append(th2d_tot)
    list_toa_waveforms = []
    for _vldb_index in example_vldb_to_display:
        for _chn in example_channel_to_display:
            th2d_toa = ROOT.TH2F(f"vldb {_vldb_index}, _toa_ch{_chn}", f"ToA Waveform Channel {_chn} in VLDB {_vldb_index};Time Bin;ToA", tb2025.MACHINE_GUN_MAX, 0, tb2025.MACHINE_GUN_MAX, 256, 0, 1024)
            th2d_toa.SetStats(0)
            list_toa_waveforms.append(th2d_toa)

    start_time = time.time()
    print(f"Reading {event_to_read} events...")

    for _event_index in range(event_to_read):
        root_tree.GetEntry(_event_index)
        print(f"Event {_event_index}, timestamps_0: {data_frame['timestamps_0'][0]}, timestamps_1: {data_frame['timestamps_1'][0]}")
        for _vldb_index in example_vldb_to_display:
            for _chn_index in example_channel_to_display:
                for _machine_gun_index in range(tb2025.MACHINE_GUN_MAX):
                    list_adc_waveforms[example_vldb_to_display.index(_vldb_index) * len(example_channel_to_display) + example_channel_to_display.index(_chn_index)].Fill(_machine_gun_index, tb2025.get_channel_adc(data_frame, _vldb_index, _machine_gun_index, _chn_index))
                    list_tot_waveforms[example_vldb_to_display.index(_vldb_index) * len(example_channel_to_display) + example_channel_to_display.index(_chn_index)].Fill(_machine_gun_index, tb2025.get_channel_tot(data_frame, _vldb_index, _machine_gun_index, _chn_index))
                    list_toa_waveforms[example_vldb_to_display.index(_vldb_index) * len(example_channel_to_display) + example_channel_to_display.index(_chn_index)].Fill(_machine_gun_index, tb2025.get_channel_toa(data_frame, _vldb_index, _machine_gun_index, _chn_index))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Finished reading {event_to_read} events in {elapsed_time:.2f} seconds.")

    output_file.cd()
    for th2d in list_adc_waveforms:
        th2d.Write()
    for th2d in list_tot_waveforms:
        th2d.Write()
    for th2d in list_toa_waveforms:
        th2d.Write()
    output_file.Close()

    input_file.Close()

if __name__ == "__main__":
    main()