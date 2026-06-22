# Fluid_definer.py
import numpy as np
import json
import os
import argparse

def add_new_fluid_from_csv(csv_path, fluid_name, gascheck):
    # Load data sheet
    data = np.genfromtxt(csv_path, delimiter=',', names=True, deletechars='', autostrip=True)
    
    T_data = data['Temperature']

    if gascheck:
        R_gas = float(data['R_Gas_Constant'][0])
    else:
        R_gas = 0.0

    fitted_fluid_entry = {
        "name": fluid_name,
        "gas_constant_R": R_gas,
        "gas_check": bool(gascheck)
    }

    properties_to_fit = {
        "viscosity_poly": "Viscosity",
        "density_poly": "Density",
        "electrical_conductivity_poly": "Electrical_Conductivity",
        "thermal_conductivity_poly": "Thermal_Conductivity",
        "cp_poly": "Specific_Heat_CP",
        "cv_poly": "Specific_Heat_CV"
    }

    # Generate Polynomial
    for json_key, csv_column_name in properties_to_fit.items():
        current_property_data = data[csv_column_name]
        coeffs = np.polyfit(T_data, current_property_data, deg=3)
        fitted_fluid_entry[json_key] = {
            "c3": float(coeffs[0]),
            "c2": float(coeffs[1]),
            "c1": float(coeffs[2]),
            "c0": float(coeffs[3])
        }
        
    # JSON Map
    json_filename = "fluids.json"
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as f:
            database = json.load(f)
    else:
        database = {}

    db_key = fluid_name.lower().replace(" ", "_")
    database[db_key] = fitted_fluid_entry
    
    with open(json_filename, 'w') as f:
        json.dump(database, f, indent=4)
        
    print(f"Successfully processed all 6 property curves for {fluid_name}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Universal MHD Simulation Fluid Ingestion Tool. Fits polynomial curves to a CSV data sheet."
    )
    parser.add_argument(
        "-f", "--file", 
        required=True, 
        help="Path to the target data CSV file (e.g., saltwater_35psu.csv)"
    )
    parser.add_argument(
        "-n", "--name", 
        required=True, 
        help="The display name for the fluid database entry (e.g., 'Saltwater 35PSU')"
    )
    parser.add_argument(
        "--gas", 
        action="store_true", 
        help="Include this flag if the fluid is a compressible gas. Omit for liquids."
    )
    
    args = parser.parse_args()
    
    print(f"\n[Ingestion Engine] Initializing curve fit pipeline...")
    print(f"Target File: {args.file}")
    print(f"Database Profile Name: {args.name}")
    print(f"Compressible Gas Mode: {args.gas}\n")
    
    # Function Call
    add_new_fluid_from_csv(csv_path=args.file, fluid_name=args.name, gascheck=args.gas)