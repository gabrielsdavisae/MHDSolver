import numpy as np
import os
import copy

#Function Import
from property_evaluator import prop_eval
from deriver import calculate_all_derivatives
from evaluator import evaluate_cell_physics

def run_simulation_cycler():
    print("\n=== INITIALIZING SIMULATION CYCLER ===")
    
    # Load Mesh
    mesh_path = "Mesh.npy"
    if not os.path.exists(mesh_path):
        print(f"Error: {mesh_path} not found. Please run Mesh_Generator first.")
        return 
        
    control_volume = np.load(mesh_path, allow_pickle=True)
    Nz, Nx, Ny = control_volume.shape
    z_max_index = Nz - 1
    
    # Simulation Stepper
    dx, dy, dz = 0.001, 0.001, 0.005
    dt = 0.001
    total_steps = 15000
    convergence_threshold = 1e-7
    
    # Time Stepper
    for time_step in range(total_steps):
        
        prev_time_volume = np.copy(control_volume)
        
        # Boundary Conditions
        sum_v_inlet = 0.0
        sum_v_outlet = 0.0
        fluid_node_count = 0

        total_uz_sum = 0.0
        total_fluid_nodes_count = 0
        

        # Z Stepper
        for z in range(Nz):   
            pseudoslice = control_volume[z, :, :]
            prev_time_slice = prev_time_volume[z, :, :]
            
            if z == 0:
                back_reference_slice = control_volume[z_max_index, :, :]
                front_reference_slice = control_volume[z + 1, :, :]
            elif z == z_max_index:
                back_reference_slice = control_volume[z - 1, :, :]
                front_reference_slice = control_volume[0, :, :]
            else:
                back_reference_slice = control_volume[z - 1, :, :]
                front_reference_slice = control_volume[z + 1, :, :]
            
            prop_eval(pseudoslice)
            
            # XY Stepper
            for i in range(1, Nx - 1):
                for j in range(1, Ny - 1):
                    cell = pseudoslice[i, j]
                    
                    if cell["type"] == "fluid":
                        derivs = calculate_all_derivatives(
                            pseudoslice, front_reference_slice, back_reference_slice, prev_time_slice,
                            i, j, dx, dy, dz, dt
                        )
                        cell.update(derivs)
                        residuals = evaluate_cell_physics(cell)
                        cell.update(residuals)
                        
                        rho = max(1e-3, cell["density"])
                        cell["u_x"] += dt * (cell["momentum_x"] / rho)
                        cell["u_y"] += dt * (cell["momentum_y"] / rho)
                        cell["u_z"] += dt * (cell["momentum_z"] / rho)
                        total_uz_sum += cell["u_z"]
                        total_fluid_nodes_count += 1

                        if z == 0:
                            sum_v_inlet += cell["u_z"]
                            fluid_node_count += 1
                        elif z == z_max_index:
                            sum_v_outlet += cell["u_z"]
        # Convergence Terms
        avg_v_inlet = sum_v_inlet / max(1, fluid_node_count)
        avg_v_outlet = sum_v_outlet / max(1, fluid_node_count)
        velocity_delta = abs(avg_v_inlet - avg_v_outlet)
        
        # Live Terms
        live_bulk_uz = total_uz_sum / max(1, total_fluid_nodes_count)
        
        # Dynamic update
        print(
            f"Step {time_step:<5} | "
            f"Bulk u_z: {live_bulk_uz:12.6e} m/s | "
            f"Delta (In-Out): {velocity_delta:12.6e}", 
            end="\r"
        )
        
        # Breaker
        if time_step > 1000 and velocity_delta < convergence_threshold:
            print(f"\n[CONVERGENCE] Terminal velocity reached at time step {time_step}!")
            break

    # Diagnostics
    print("\n" + "="*50)
    print("         MHD CHANNEL STATE DIAGNOSTICS          ")
    print("="*50)
    
    # Accumulator metrics
    total_fluid_nodes = 0
    total_wall_nodes = 0
    
    sum_ux, sum_uy, sum_uz = 0.0, 0.0, 0.0
    sum_temp_fluid = 0.0
    sum_temp_wall = 0.0
    
    for z in range(Nz):
        for i in range(Nx):
            for j in range(Ny):
                cell = control_volume[z, i, j]
                
                if cell["type"] == "fluid":
                    total_fluid_nodes += 1
                    sum_ux += cell["u_x"]
                    sum_uy += cell["u_y"]
                    sum_uz += cell["u_z"]
                    sum_temp_fluid += cell["temperature"]
                elif cell["type"] == "wall":
                    total_wall_nodes += 1
                    sum_temp_wall += cell["temperature"]

    # Final Averages
    avg_ux = sum_ux / max(1, total_fluid_nodes)
    avg_uy = sum_uy / max(1, total_fluid_nodes)
    avg_uz = sum_uz / max(1, total_fluid_nodes)
    avg_temp_fluid = sum_temp_fluid / max(1, total_fluid_nodes)
    avg_temp_wall = sum_temp_wall / max(1, total_wall_nodes)

    print(f"  Grid Profile Summary:  Fluid Nodes [{total_fluid_nodes}] | Wall Nodes [{total_wall_nodes}]")
    print(f"  Average Core Velocity Component Vector Fields:")
    print(f"    - u_x (Crossflow Component) : {avg_ux:12.6e} m/s")
    print(f"    - u_y (Buoyancy Component)  : {avg_uy:12.6e} m/s")
    print(f"    - u_z (Axial Core Flow)     : {avg_uz:12.6e} m/s")
    print(f"  Thermodynamic Profile Status:")
    print(f"    - Average Bulk Fluid Temperature : {avg_temp_fluid:10.2f} K")
    print(f"    - Average Containment Wall Temp  : {avg_temp_wall:10.2f} K")
    print("="*50)

    # Saver
    np.save("Mesh_Updated.npy", control_volume, allow_pickle=True)
    print("=== SIMULATION RUN COMPLETE. RESULTS EXPORTED. ===\n")

if __name__ == "__main__":
    run_simulation_cycler()