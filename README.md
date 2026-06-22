## About the Project

This repository contains a suite of Python scripts designed to calculate the final velocity of a Magnetohydrodynamic (MHD) propulsor. 

The simulation models performance by analyzing the interplay between several key variables:

* **Electromagnetic Inputs:** Applied voltage and magnetic field strength
* **Fluid & Environmental Properties:** Working fluid type and temperature
* **Geometric & Structural Factors:** Channel shape/dimensions and material selection

## How It Works

The repository currently consists of three core scripts that handle the data preprocessing and the simulation execution:

### 1. Preprocessing & Material Definitions
* **`fluid_definer.py`**: Imports thermal property charts for new fluids and generates thermal polynomials to calculate dynamic physical properties during the simulation.
* **`material_definer.py`**: Functions similarly to the fluid definer, allowing the import of custom material properties and creating the necessary polynomial curves for the solver.

### 2. Core Simulation
* **`main.py`**: The central execution script. It manages the entire solution process, binds user-defined inputs to the governing solver, and handles the simulation loop.

## Usage Examples

Currently, this project is entirely command-line based. While implementing a Graphical User Interface (GUI) is a future development goal, all interactions are currently conducted via the terminal.

### Fluid Definer
```bash
python fluid_definer.py -f 35PSU_Saltwater.csv -n "Saltwater 35PSU"
```
  This starts the fluid definer script, and tells it to look for a filename
  "35PSU_Saltwater.csv" and to internally save it as "Saltwater 35PSU" in
  the file fluids.JSON.

  Material_definer.py
  ===================
  ```bash
python Material_definer.py -f PVC.csv -n "PVC"
```
  This starts the material definer script, and tells it to look for a filename "PVC.csv" and     to internally save it as "PVC in  file materials.JSON

  Main.py
  =======
  ```bash
  python Main.py
  ```
  This begins the solver program. The steps are straight forward, but nonetheless an example     is shown below:

```bash
=== STARTING MHD SOLVER PIPELINE ===

=== CONFIGURATION SELECTION ===
[1] Use existing config.json profile
[2] Configure a brand new physical case study
Select an option (1 or 2):

user input > 2
```
  This allows us to modify the existing config file, you can change all properties, or not       call specific ones you'd like to remain the same.

```bash
--- MHD PARAMETER PARAMETER OPTIONS ---
usage: Enter options exactly like command flags. Example: -g round -b 1.2 -t 300

MHD Simulation Quick Configurator

optional arguments:
  -h, --help            show this help message and exit
  -m MATERIAL, --material MATERIAL
                        Material profile name
  -f FLUID, --fluid FLUID
                        Fluid profile name
  -g {square,round}, --geometry {square,round}
                        Propulsor profile type (square/round)
  -v VOLTAGE, --voltage VOLTAGE
                        Supplied voltage (V)
  -b MAGNETIC, --magnetic MAGNETIC
                        Magnetic field strength B_y (T)
  -l LENGTH, --length LENGTH
                        Pipe length (m)
  -r RESOLUTION, --resolution RESOLUTION
                        Resolution factor (Rf)
  -d DIAMETER_WIDTH, --diameter_width DIAMETER_WIDTH
                        Diameter (m)
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature(C)
---------------------------------------
Enter your configuration flags below:
user input > -m PVC -f saltwater_35psu -g round -v 12 -b 1 -l 3 -r 4 -d 0.05 -t 26
```
This above says the following, I want the material of the propulsor to be PVC, the working fluid/propellent/conducting fluid to be saltwater 35PSU,
I want the pipe to have a round rofile, I want the voltage source to be 12 volts, the magnetic field to be 1 Telsa, I want the length of the propulsor
to be 3 meters, with a cell resolution of 4 (This multiplies the total number of cells, bigger numbers increase accurately and dramatically increase
computation time) I want the diameter of the pipe to be 0.05 meters, and the initial temperature is 26 degrees Celsius.
```bash
config.json successfully generated and updated!
Generating 3D Mesh Volume...
# # # # # # # # # # # # # # # # # #
# # # # # # # . . . . # # # # # # #
# # # # # . . . . . . . . # # # # #
# # # # . . . . . . . . . . # # # #
# # # . . . . . . . . . . . . # # #
# # . . . . . . . . . . . . . . # #
# # . . . . . . . . . . . . . . # #
# . . . . . . . . . . . . . . . . #
# . . . . . . . . . . . . . . . . #
# . . . . . . . . . . . . . . . . #
# . . . . . . . . . . . . . . . . #
# # . . . . . . . . . . . . . . # #
# # . . . . . . . . . . . . . . # #
# # # . . . . . . . . . . . . # # #
# # # # . . . . . . . . . . # # # #
# # # # # . . . . . . . . # # # # #
# # # # # # # . . . . # # # # # # #
# # # # # # # # # # # # # # # # # #
```
This shows the user the profile of the propsulor the solver will use to analyze the system. The # indicates a wall cell, and the . indicates a fluid cell.
```bash
Successfully extruded control_area into control_volume!
3D Shape: (933, 18, 18)
Control volume saved successfully!

_-_-_-_-_-_ Control Volume Established _-_-_-_-_-_

Initiating simulation cycles...

=== INITIALIZING SIMULATION CYCLER ===
Step 1     | Bulk u_z: 1.278866e-03 m/s | Delta (In-Out): 9.019194e-08
```
  This is a live-view of the time-step the solver is on, as well as the bulk velocity inside     the pipe, in the direction down the pipe/parallel within the
  pipe (z), as well as the difference in velocity between the inlet and the outlet velocity,     at steady state operation (Maximum velocity) the electromagnetic
  forces are balanced by the viscous/frictional/shear forces within the fluid and against the    walls. All additional energy added to the system is simply to
  counter-act the energy lost.

  This has a long solution time, for the sake of this document I reduced the resolution factor   to 0.25 by >2 , >-r 0.25, since the resolution factor above was
  4, this new profile has 1/16th the cells, and is far less accurate. (It only has one fluid     cell)
```bash
Enter your configuration flags below:
> -r 0.25

config.json successfully generated and updated!
Generating 3D Mesh Volume...
# # #
# . #
# # #
Successfully extruded control_area into control_volume!
3D Shape: (59, 3, 3)
Control volume saved successfully!

_-_-_-_-_-_ Control Volume Established _-_-_-_-_-_

Initiating simulation cycles...
Step 2475  | Bulk u_z: 1.808972e-01 m/s | Delta (In-Out): 9.996418e-08
[CONVERGENCE] Terminal velocity reached at time step 2475!

==================================================
         MHD CHANNEL STATE DIAGNOSTICS
==================================================
  Grid Profile Summary:  Fluid Nodes [59] | Wall Nodes [472]
  Average Core Velocity Component Vector Fields:
    - u_x (Crossflow Component) : 0.000000e+00 m/s
    - u_y (Buoyancy Component)  : 0.000000e+00 m/s
    - u_z (Axial Core Flow)     : 1.808972e-01 m/s
  Thermodynamic Profile Status:
    - Average Bulk Fluid Temperature :      26.00 K
    - Average Containment Wall Temp  :      26.00 K
==================================================
=== SIMULATION RUN COMPLETE. RESULTS EXPORTED. ===


=== MHD SOLVER PIPELINE COMPLETE ===
Press any key to continue . . .
```
  So our result for us settings (at r=0.25) predicts a velocity of 0.181 m/s, or 0.4 mph. A      result like this is expected for such a poor resolution.
  In actual systems, the most advanced MHD propulsors acheive a maximum velocity of ~4.7 m/s     or ~10.5 mph.

## What if I do want to add a new material/fluid?
  There is a excel file, and two example `.csv` files for saltwater and pvc in the directory.    Simply modify these files with appropriate values and pass them through the appropriate        definer.
  Note: There are additional properties like "material roughness" or "specfific heat" these      are properties that aren't currently used but are intended to be adopted in a future version.
