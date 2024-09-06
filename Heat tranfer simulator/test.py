import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameters
Lx = 150  # Length in x direction (mm)
Ly = 90  # Length in y direction (mm)
Lz = 10   # Length in z direction (mm)
Nx = 150  # Number of grid points along x
Ny = 90   # Number of grid points along y
Nz = 20   # Number of grid points along z
alpha = 0.02  # Thermal diffusivity (mm^2/s) TPU: 0.11 PVC:0.08
T_initial = 70.0  # Initial temperature in the center of the cube (Celsius)
T_room = 20.0     # Room temperature (Celsius)
Time = 122         # Total time duration (s)

# Discretization
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
dz = Lz / (Nz - 1)
dt = 1  # Time step (s)

# Stability check
if alpha * dt / dx**2 >= 0.5 or alpha * dt / dy**2 >= 0.5 or alpha * dt / dz**2 >= 0.5:
    raise ValueError("The time step is too large for stability. Please reduce dt.")

# Initialize the grid
T = np.ones((Nx, Ny, Nz)) * T_initial
T[:, 0, :] = T_room  # Set the bottom boundary to room temperature
T[:, -1, :] = T_room  # Set the top boundary to room temperature
T[0, :, :] = T_room  # Set the left boundary to room temperature
T[-1, :, :] = T_room  # Set the right boundary to room temperature
T[:, :, 0] = T_room  # Set the front boundary to room temperature
T[:, :, -1] = T_room  # Set the back boundary to room temperature

# Time stepping (explicit finite difference)
num_steps = int(Time / dt)

# Data storage for analysis
T_plot = np.zeros((Nx-2, Ny-2, Nz-2, num_steps))
T_Surface = []
T_Core = []
Time_list = []

for step in range(num_steps):
    Tn = T.copy()  # Copy the current temperature field
    T_plot[:, :, :, step] = T[1:-1, 1:-1, 1:-1].copy()
    
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            for k in range(1, Nz-1):
                T[i, j, k] = Tn[i, j, k] + alpha * dt * (
                    (Tn[i+1, j, k] - 2*Tn[i, j, k] + Tn[i-1, j, k]) / dx**2 +
                    (Tn[i, j+1, k] - 2*Tn[i, j, k] + Tn[i, j-1, k]) / dy**2 +
                    (Tn[i, j, k+1] - 2*Tn[i, j, k] + Tn[i, j, k-1]) / dz**2
                )
    
    # Record temperatures for analysis
    T_Surface.append(T[20, 20, 5])
    T_Core.append(T[75, 45, 10])
    Time_list.append(step * dt)
    print(step)

    # Update boundaries to maintain room temperature (Dirichlet boundary conditions)
    T[:, 0, :] = T_room
    T[:, -1, :] = T_room
    T[0, :, :] = T_room
    T[-1, :, :] = T_room
    T[:, :, 0] = T_room
    T[:, :, -1] = T_room

# Plotting temperature profiles
plt.plot(Time_list, T_Surface, label='Surface Temperature')
plt.plot(Time_list, T_Core, label='Core Temperature')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.title('Temperature vs Time')
plt.show()

# Save data in excel
df_temps = pd.DataFrame({
    'Time (s)': Time_list,
    'Surface Temperature (°C)': T_Surface,
    'Core Temperature (°C)': T_Core
})

# Specify the Excel file path for temperatures
excel_file_path_temps = '/Users/john/Documents/GitHub/Rapid-Dynamic-Test-Data-Logger-based-on-Arduino/Heat tranfer simulator/Temperatures_' + str(T_initial) + '_' + str(alpha) + '.xlsx'

# Write the temperatures DataFrame to an Excel file
df_temps.to_excel(excel_file_path_temps, index=False)

print(f'Data saved to{excel_file_path_temps}')