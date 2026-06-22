import json
import math
import numpy as np

def prop_eval(pseudoslice):
    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
    with open("materials.json", "r") as json_file:
        materials_data = json.load(json_file)
    with open("fluids.json", "r") as json_file:
        fluids_data = json.load(json_file)

    active_fluid = fluids_data[config_data["fluid"]]
    V_f_coeffs  = active_fluid["viscosity_poly"]
    E_f_coeffs  = active_fluid["electrical_conductivity_poly"]
    Th_f_coeffs = active_fluid["thermal_conductivity_poly"]
    p_f_coeffs  = active_fluid["density_poly"]

    active_material = materials_data[config_data["material"]]
    Th_m_coeffs = active_material["thermal_conductivity_poly"]
    p_m_coeffs  = active_material["density_poly"]

    Nx, Ny = pseudoslice.shape
    for i in range(Nx):
        for j in range(Ny):
            cell = pseudoslice[i, j]
            T = cell["temperature"]

            if cell["type"] == "wall":
                cell["thermal_conductivity"] = (T**3)*(Th_m_coeffs["c3"]) + (T**2)*(Th_m_coeffs["c2"]) + (T)*(Th_m_coeffs["c1"]) + (Th_m_coeffs["c0"])
                cell["density"] = (T**3)*(p_m_coeffs["c3"]) + (T**2)*(p_m_coeffs["c2"]) + (T)*(p_m_coeffs["c1"]) + (p_m_coeffs["c0"])
                cell["viscosity"] = 0.0
                cell["electrical_conductivity"] = 0.0

            elif cell["type"] == "fluid":
                cell["viscosity"] = (T**3)*(V_f_coeffs["c3"]) + (T**2)*(V_f_coeffs["c2"]) + (T)*(V_f_coeffs["c1"]) + (V_f_coeffs["c0"])
                cell["electrical_conductivity"] = (T**3)*(E_f_coeffs["c3"]) + (T**2)*(E_f_coeffs["c2"]) + (T)*(E_f_coeffs["c1"]) + (E_f_coeffs["c0"])
                cell["thermal_conductivity"] = (T**3)*(Th_f_coeffs["c3"]) + (T**2)*(Th_f_coeffs["c2"]) + (T)*(Th_f_coeffs["c1"]) + (Th_f_coeffs["c0"])
                cell["density"] = (T**3)*(p_f_coeffs["c3"]) + (T**2)*(p_f_coeffs["c2"]) + (T)*(p_f_coeffs["c1"]) + (p_f_coeffs["c0"])