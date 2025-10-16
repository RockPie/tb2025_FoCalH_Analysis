import os, json, array, ROOT
import argparse

def main():
    parser = argparse.ArgumentParser(description='Example ROOT file reader')
    parser.add_argument('-i', '--input', required=True, help='Input ROOT file')
    parser.add_argument('-e', '--events', type=int, default=-1, help='Number of events to read')
    args = parser.parse_args()

    input_file = args.input
    if not os.path.isfile(input_file):
        print(f"Error: File {input_file} does not exist.")
        return
    
    root_file = ROOT.TFile.Open(input_file)
    if not root_file or root_file.IsZombie():
        print(f"Error: Could not open file {input_file}.")
        return
    
    root_tree = root_file.Get("data_tree")
    if not root_tree:
        print("Error: Tree 'data_tree' not found in the ROOT file.")
        return
    
    event_number = root_tree.GetEntries()
    print(f"Number of events in the tree: {event_number}")

    event_to_read = args.events if args.events > 0 else event_number

    for _event_index in range(event_to_read):
        root_tree.GetEntry(_event_index)
        event_data = {
            "event_id": root_tree.event_id,
            "value": root_tree.value
        }
        print(json.dumps(event_data, indent=4))

    root_file.Close()