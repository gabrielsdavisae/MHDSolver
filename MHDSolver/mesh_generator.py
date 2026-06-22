import json
import math
import copy
import os
import numpy as np

def generate_mesh():
    print("Generating 3D Mesh Volume...")

    JSON_FILENAME_1 = "config.json"
    JSON_FILENAME_2 = "fluids.json"

    # Import Parameters
    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
    with open("fluids.json", "r") as json_file:
        fluids_data = json.load(json_file)
    
    g = config_data["geometry"]
    b = config_data["magnetic"]
    l = config_data["length"]
    r_config = config_data["resolution"]
    d = config_data["diameter_width"]
    T = config_data["temperature"]

    # Extract fluid properties based on temperature
    Visc = (fluids_data[config_data["fluid"]])["viscosity_poly"]
    Econduct = (fluids_data[config_data["fluid"]])["electrical_conductivity_poly"]
    electrical_conductivity = (T**3)*(Econduct["c3"]) + (T**2)*(Econduct["c2"]) + (T)*(Econduct["c1"]) + (Econduct["c0"])
    viscosity = (T**3)*(Visc["c3"]) + (T**2)*(Visc["c2"]) + (T)*(Visc["c1"]) + (Visc["c0"])

    # Hartman diameter
    minimum_delta = (1 / (b * r_config)) * ((viscosity / electrical_conductivity)**0.5)

    def create_default_cell(p1=0, p2=0, T_initial=T, P_initial=0.0):
        """
        Generates a comprehensive data storage dictionary for a single mesh node.
        Includes primitive properties, fluid fields, space/time gradients, and residuals.
        """
        return {
            # Type Identification & Spatial Coords
            "type": "fluid",          # or "wall"
            "position_1": p1,
            "position_2": p2,

            # Thermofluid Properties
            "u_x": 0.0,
            "u_y": 0.0,
            "u_z": 0.0,
            "pressure": P_initial,
            "temperature": T_initial,
            "W_total": 0.0,

            # Dynamic Properties
            "density": 0.0,
            "viscosity": 0.0,
            "electrical_conductivity": 0.0,
            "thermal_conductivity": 0.0,
            "magnetic_field_y": 1.2,  # By
            "electric_field_x": 100.0, # Ex

            # Gradient Terms
        
        
            # First-Order Spatial & Temporal Gradients
            "du_x_x": 0.0, "du_x_y": 0.0, "du_x_z": 0.0, "du_x_t": 0.0,
            "du_y_x": 0.0, "du_y_y": 0.0, "du_y_z": 0.0, "du_y_t": 0.0,
            "du_z_x": 0.0, "du_z_y": 0.0, "du_z_z": 0.0, "du_z_t": 0.0,
        
            "dW_total_x": 0.0, "dW_total_y": 0.0, "dW_total_z": 0.0, "dW_total_t": 0.0,
        
            # Static Pressure Driving Gradients
            "dP_dx": 0.0, "dP_dy": 0.0, "dP_dz": 0.0,

            # Second-Order Pure Laplacians
            "du_x_xx": 0.0, "du_x_yy": 0.0, "du_x_zz": 0.0,
            "du_y_xx": 0.0, "du_y_yy": 0.0, "du_y_zz": 0.0,
            "du_z_xx": 0.0, "du_z_yy": 0.0, "du_z_zz": 0.0,
        
            "dT_xx": 0.0, "dT_yy": 0.0, "dT_zz": 0.0,

            # Second-Order Cross Derivatives
            "du_x_xy": 0.0, "du_x_xz": 0.0, "du_x_yz": 0.0,
            "du_x_yx": 0.0, "du_x_zx": 0.0, "du_x_zy": 0.0,
        
            "du_y_xy": 0.0, "du_y_xz": 0.0, "du_y_yz": 0.0,
            "du_y_yx": 0.0, "du_y_zx": 0.0, "du_y_zy": 0.0,
        
            "du_z_xy": 0.0, "du_z_xz": 0.0, "du_z_yz": 0.0,
            "du_z_yx": 0.0, "du_z_zx": 0.0, "du_z_zy": 0.0,

            # System Conservation Terms
            "continuity": 0.0,
            "momentum_x": 0.0,
            "momentum_y": 0.0,
            "momentum_z": 0.0,
            "energy":     0.0
        }

    # Unified Sizing
    Nz = math.ceil(l / minimum_delta)
    Nxy = math.ceil(d / minimum_delta) + 2
    control_area = np.empty([Nxy, Nxy], dtype=object)

    # Standard Initialization Loop for all profiles
    for i in range(Nxy):
        for j in range(Nxy):
            control_area[i, j] = create_default_cell(p1=i, p2=j)

    # Generating Wall Cells
    if g == "square":
        for i in range(Nxy):
            for j in range(Nxy):
                if i == 0 or i == Nxy-1 or j == 0 or j == Nxy-1:
                    control_area[i, j]["type"] = "wall"

    elif g == "round":
        grid_center = (Nxy - 1) / 2.0
        grid_radius = (d / 2.0) / minimum_delta
    
        for i in range(Nxy):
            for j in range(Nxy):
                distance_from_center = math.sqrt((i - grid_center)**2 + (j - grid_center)**2)
                if distance_from_center >= grid_radius or i == 0 or i == Nxy - 1 or j == 0 or j == Nxy - 1:
                    control_area[i, j]["type"] = "wall"

    # Visual Validation Map
    for row in control_area:
        line_chars = []
        for cell in row:
            if cell["type"] == "wall":
                line_chars.append("#")
            else:
                line_chars.append(".")
        print(" ".join(line_chars))

    # Generate control volume
    control_volume = np.empty([Nz, Nxy, Nxy], dtype=object)

    # Extrude Profile down Volume
    for z in range(Nz):
        for i in range(Nxy):
            for j in range(Nxy):
                control_volume[z, i, j] = copy.deepcopy(control_area[i, j])

    print(f"Successfully extruded control_area into control_volume!")
    print(f"3D Shape: {control_volume.shape}")
    np.save("mesh.npy", control_volume, allow_pickle=True)
    print("Control volume saved successfully!")