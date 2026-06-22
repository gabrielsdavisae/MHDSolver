import argparse
import json
import os
import shlex

def run_configurator():
    print("\n=== CONFIGURATION SELECTION ===")
    
    # Config Check
    config_exists = os.path.exists("config.json")
    
    if config_exists:
        print("[1] Use existing config.json profile")
        print("[2] Configure a brand new physical case study")
        choice = input("Select an option (1 or 2): ").strip()
    else:
        print("No existing configuration found. Initializing setup...")
        choice = "2"

    if choice == "1":
        print("Using existing config.json profile. Proceeding to grid layout...")
        return

    elif choice == "2":
        parser = argparse.ArgumentParser(
            description="MHD Simulation Quick Configurator",
            usage="Enter options exactly like command flags. Example: -g round -b 1.2 -t 300"
        )
        # Material / Fluid Arguments
        parser.add_argument("-m", "--material", help="Material profile name")
        parser.add_argument("-f", "--fluid", help="Fluid profile name")
    
        # Simulation Parameters
        parser.add_argument("-g", "--geometry", choices=["square", "round"], help="Propulsor profile type (square/round)")
        parser.add_argument("-v", "--voltage", type=float, help="Supplied voltage (V)")
        parser.add_argument("-b", "--magnetic", type=float, help="Magnetic field strength B_y (T)")
        parser.add_argument("-l", "--length", type=float, help="Pipe length (m)")
        parser.add_argument("-r", "--resolution", type=float, help="Resolution factor (Rf)")
        parser.add_argument("-d", "--diameter_width", type=float, help="Diameter (m)")
        parser.add_argument("-t", "--temperature", type=float, help="Temperature(C)")

        # Helper Guide
        print("\n--- MHD PARAMETER PARAMETER OPTIONS ---")
        parser.print_help()
        print("---------------------------------------")
        
        # Error Loop
        while True:
            raw_input = input("\nEnter your configuration flags below:\n> ").strip()
            
            try:
                parsed_list = shlex.split(raw_input)
                args = parser.parse_args(parsed_list)
                break
            except SystemExit:
                print("Invalid format or missing arguments. Review the options above and try again.")

        args_dict = vars(args)
        provided_args = {k: v for k, v in args_dict.items() if v is not None}

        if os.path.exists("config.json"):
            with open("config.json", "r") as json_file:
                current_config = json.load(json_file)
        else:
            current_config = {}

        # Update
        current_config.update(provided_args)

        # Save
        with open("config.json", "w") as json_file:
            json.dump(current_config, json_file, indent=4)
            
        print("\nconfig.json successfully generated and updated!")
        
    else:
        print("Invalid selection. Defaulting to existing config.json profile.")