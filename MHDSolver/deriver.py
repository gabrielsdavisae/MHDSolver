import math

def calculate_all_derivatives(pseudoslice, front_slice, back_slice, prev_time_slice, i, j, dx, dy, dz, dt):
    cell = pseudoslice[i, j]
    
    # Wall Boundary Condition (No slip / Stationary boundaries)
    if cell["type"] == "wall":
        empty_derivatives = {}
        for comp in ["u_x", "u_y", "u_z"]:
            for d in ["_x", "_y", "_z", "_xx", "_yy", "_zz", "_xy", "_xz", "_yz", "_yx", "_zx", "_zy", "_t"]:
                empty_derivatives[f"d{comp}{d}"] = 0.0
        return empty_derivatives

    # Define Cell Pointers
    cell_right = pseudoslice[i + 1, j]
    cell_left  = pseudoslice[i - 1, j]
    cell_above = pseudoslice[i, j + 1]
    cell_below = pseudoslice[i, j - 1]
    cell_front = front_slice[i, j]
    cell_back  = back_slice[i, j]
    cell_past  = prev_time_slice[i, j] 

    # Dictionary Term
    results = {}

    # Direction Loop
    for comp in ["u_x", "u_y", "u_z"]:
        
        du_dx = (cell_right[comp] - cell_left[comp]) / (2.0 * dx)
        du_dy = (cell_above[comp] - cell_below[comp]) / (2.0 * dy)
        du_dz = (cell_front[comp] - cell_back[comp])  / (2.0 * dz)

        du_dt = (cell[comp] - cell_past[comp]) / dt

        du_dxx = (cell_right[comp] - 2.0 * cell[comp] + cell_left[comp]) / (dx ** 2)
        du_dyy = (cell_above[comp] - 2.0 * cell[comp] + cell_below[comp]) / (dy ** 2)
        du_dzz = (cell_front[comp] - 2.0 * cell[comp] + cell_back[comp])  / (dz ** 2)

        du_dxy = (pseudoslice[i+1, j+1][comp] - pseudoslice[i-1, j+1][comp] - pseudoslice[i+1, j-1][comp] + pseudoslice[i-1, j-1][comp]) / (4.0 * dx * dy)
        du_dxz = (front_slice[i+1, j][comp]   - front_slice[i-1, j][comp]   - back_slice[i+1, j][comp]   + back_slice[i-1, j][comp])   / (4.0 * dx * dz)
        du_dyz = (front_slice[i, j+1][comp]   - front_slice[i, j-1][comp]   - back_slice[i, j+1][comp]   + back_slice[i, j-1][comp])   / (4.0 * dy * dz)

        results[f"d{comp}_x"]   = du_dx
        results[f"d{comp}_y"]   = du_dy
        results[f"d{comp}_z"]   = du_dz
        results[f"d{comp}_t"]   = du_dt
        results[f"d{comp}_xx"]  = du_dxx
        results[f"d{comp}_yy"]  = du_dyy
        results[f"d{comp}_zz"]  = du_dzz
        
        results[f"d{comp}_xy"]  = du_dxy
        results[f"d{comp}_yx"]  = du_dxy
        
        results[f"d{comp}_xz"]  = du_dxz
        results[f"d{comp}_zx"]  = du_dxz
        
        results[f"d{comp}_yz"]  = du_dyz
        results[f"d{comp}_zy"]  = du_dyz

    return results