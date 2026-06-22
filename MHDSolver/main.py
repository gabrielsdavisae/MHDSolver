import os

# Function Import
from configurator import run_configurator
from mesh_generator import generate_mesh
from cycler import run_simulation_cycler

def main():
    print("=== STARTING MHD SOLVER PIPELINE ===")
    
    # Run Configuration (Generates config.json, materials.json, etc.)
    run_configurator()
    
    # Check if config exist
    if os.path.exists("config.json"):
        generate_mesh()
        print("\n_-_-_-_-_-_ Control Volume Established _-_-_-_-_-_")
    else:
        print("Error: config.json missing! Aborting mesh generation.")
        return

    # Run solver loop
    if os.path.exists("Mesh.npy"):
        print("\nInitiating simulation cycles...")
        run_simulation_cycler()
    else:
        print("Error: Mesh.npy missing! Aborting simulation cycles.")
        return
    
    print("\n=== MHD SOLVER PIPELINE COMPLETE ===")

if __name__ == "__main__":
    main()