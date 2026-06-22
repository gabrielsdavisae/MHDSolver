def evaluate_cell_physics(cell):
    # Extract cell properties
    rho   = cell["density"]
    mu    = cell["viscosity"]
    sigma = cell["electrical_conductivity"]
    k_T   = cell["thermal_conductivity"]
    P     = cell["pressure"]
    W_tot = cell["W_total"]

    ux, uy, uz = cell["u_x"], cell["u_y"], cell["u_z"]
    By = cell.get("magnetic_field_y", 1.2)
    Ex = cell.get("electric_field_x", 100.0)
    
    # Spatial First Derivatives
    du_x_x, du_y_y, du_z_z = cell["du_x_x"], cell["du_y_y"], cell["du_z_z"]
    div_u = du_x_x + du_y_y + du_z_z

    # Continuity Equatiion

    residual_continuity = rho * div_u

    # Momentum Equation

        # X-direction
    lhs_x = rho * (cell["du_x_t"] + ux*du_x_x + uy*cell["du_x_y"] + uz*cell["du_x_z"])
    viscous_dim_x = cell["du_x_xx"] + cell["du_x_yy"] + cell["du_x_zz"] 
    rhs_x = -cell["dP_dx"] + mu * viscous_dim_x - sigma * ux * (By**2)
    residual_momentum_x = rhs_x - lhs_x 

        # Y-direction
    lhs_y = rho * (cell["du_y_t"] + ux*cell["du_y_x"] + uy*du_y_y + uz*cell["du_y_z"])
    viscous_dim_y = cell["du_y_xx"] + cell["du_y_yy"] + cell["du_y_zz"]
    rhs_y = -cell["dP_dy"] + mu * viscous_dim_y
    residual_momentum_y = rhs_y - lhs_y

        # Z-Direction
    lhs_z = rho * (cell["du_z_t"] + ux*cell["du_z_x"] + uy*cell["du_z_y"] + uz*du_z_z)
    viscous_dim_z = cell["du_z_xx"] + cell["du_z_yy"] + cell["du_z_zz"]
    rhs_z = -cell["dP_dz"] + mu * viscous_dim_z + sigma * By * (Ex - uz * By)
    residual_momentum_z = rhs_z - lhs_z 

    # Energy Equation
    energy_advection = ux * cell["dW_total_x"] + uy * cell["dW_total_y"] + uz * cell["dW_total_z"]
    LHS_energy = cell["dW_total_t"] + (W_tot * div_u) + energy_advection

    thermal_conduction = k_T * (cell["dT_xx"] + cell["dT_yy"] + cell["dT_zz"])
    pressure_work      = -(P * div_u)
    
    squared_gradients = (2.0 * (du_x_x**2 + du_y_y**2 + du_z_z**2) + 
                         (cell["du_y_x"] + cell["du_x_y"])**2 + 
                         (cell["du_z_y"] + cell["du_y_z"])**2 + 
                         (cell["du_x_z"] + cell["du_z_x"])**2)
                         
    viscous_dissipation = mu * squared_gradients
    
    joule_heating = sigma * ((Ex - uz * By)**2)

    RHS_energy = thermal_conduction + pressure_work + viscous_dissipation + joule_heating
    residual_energy = RHS_energy - LHS_energy

    return {
        "continuity": residual_continuity,
        "momentum_x": residual_momentum_x,
        "momentum_y": residual_momentum_y,
        "momentum_z": residual_momentum_z,
        "energy":     residual_energy
    }