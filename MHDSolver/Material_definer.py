import numpy as np
import json
import os
import argparse

def add_new_material_from_csv(csv_path, material_name):
    # Load data sheet
    data = np.genfromtxt(csv_path, delimiter=',', names=True, deletechars='', autostrip=True)
    
    T_data = data['Temperature']

    roughness_mm = float(data['Surface_Roughness'][0])

    fitted_material_entry = {
        "name": material_name,
        "absolute_roughness_mm": roughness_mm
    }

    # JSON Map
    properties_to_fit = {
        "thermal_conductivity_poly": "Thermal_Conductivity",
        "electrical_conductivity_poly": "Electrical_Conductivity",
        "density_poly": "Density",
        "specific_heat_poly": "Specific_Heat"
    }

    # Generate polynomial
    for json_key, csv_column_name in properties_to_fit.items():
        current_property_data = data[csv_column_name]
        
        # Fit polynomial
        coeffs = np.polyfit(T_data, current_property_data, deg=3)
        
        # Pack coefficients cleanly
        fitted_material_entry[json_key] = {
            "c3": float(coeffs[0]),
            "c2": float(coeffs[1]),
            "c1": float(coeffs[2]),
            "c0": float(coeffs[3])
        }
        
    # Append JSON
    json_filename = "materials.json"
    
    if os.path.exists(json_filename) and os.path.getsize(json_filename) > 0:
        with open(json_filename, 'r') as f:
            database = json.load(f)
    else:
        database = {}

    db_key = material_name.lower().replace(" ", "_")
    database[db_key] = fitted_material_entry
    
    with open(json_filename, 'w') as f:
        json.dump(database, f, indent=4)
        
    print(f"Successfully processed all 4 property curves for solid material: {material_name}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Universal MHD Simulation Material Ingestion Tool."
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the target material CSV file")
    parser.add_argument("-n", "--name", required=True, help="The display name for the material database entry")
    
    args = parser.parse_args()
    
    print(f"\n[Ingestion Engine] Initializing solid material curve fit pipeline...")
    print(f"Target File: {args.file}")
    print(f"Database Profile Name: {args.name}\n")
    
    # Function Call
    add_new_material_from_csv(csv_path=args.file, material_name=args.name)