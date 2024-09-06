import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameters
Lx = 180
Ly = 200
Lz = 10       # Size of the cubic domain (mm)
Nx = 20       # Number of grid points along x
Ny = 20       # Number of grid points along y
Nz = 10       # Number of grid points along z
alpha = 0.2  # Thermal diffusivity (mm^2/s)
T_initial = -20.0  # Initial temperature 
T_room = 25.0  # Room temperature

# Discretization
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
dz = Lz / (Nz - 1)
dt = 1 # Time step

# Initialize the grid
T = np.ones((Nx, Ny, Nz)) * T_room
T[:, :, :] = T_initial  # Set the entire cube to the initial temperature
T[:, 0, :] = T_room  # Set the bottom boundary to room temperature
T[:, -1, :] = T_room  # Set the top boundary to room temperature
T[0, :, :] = T_room  # Set the left boundary to room temperature
T[-1, :, :] = T_room  # Set the right boundary to room temperature
T[:, :, 0] = T_room  # Set the front boundary to room temperature
T[:, :, -1] = T_room  # Set the back boundary to room temperature

# Time stepping (explicit finite difference)
num_steps = 65

# T_plot saves the calculated crossed-sectional data in x-z plane
T_plot = np.zeros((Nx, Ny, num_steps))

for step in range(num_steps):
    print(step)
    Tn = T.copy()  # Copy the current temperature field
    T_plot[:,:,step] = T[:,:,5].copy()
    print(T[:,:,5])
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            for k in range(1, Nz-1):
                T[i, j, k] = Tn[i, j, k] + 0.1 * alpha * dt * (
                    (Tn[i+1, j, k] - 2*Tn[i, j, k] + Tn[i-1, j, k]) / dx**2 +
                    (Tn[i, j+1, k] - 2*Tn[i, j, k] + Tn[i, j-1, k]) / dy**2 +
                    (Tn[i, j, k+1] - 2*Tn[i, j, k] + Tn[i, j, k-1]) / dz**2
                )

# Visualization
# Contour Field Plot Animation
x = np.linspace(0, Lx, Nx-2)
y = np.linspace(0, Ly, Ny-2)
Xg, Yg = np.meshgrid(x, y)


cntr1 = plt.contourf(Xg, Yg, T_plot[1:-1,1:-1,-1], levels=10)
plt.title('Cross-sectional Temperature after 60s (Ti = -20)')
plt.colorbar(cntr1)
plt.show()

#Animation
'''
kw = {
    'vmin': T_plot.min(),
    'vmax': T_plot.max(),
    'levels': np.linspace(T_plot[1:-1, 1:-1, -1].min(), T_plot[1:-1,1:-1,-1].max(), 100),
}

#plt.ion()
for k in range(0, num_steps - 1, 5):
    cntr1 = plt.contourf(Xg, Yg, T_plot[1:-1, 1:-1, k], **kw)
    plt.title(str(k))
    plt.colorbar(cntr1)
    plt.show()
    #plt.pause(1)
    #plt.clf()
#plt.close()
'''


# Save data into Excel
data_columns = T_plot[:,:,-1]

# Create an empty DataFrame
df = pd.DataFrame()

# Specify the Excel file path
excel_file_path = 'Heat tranfer simulator/PVC_output.xlsx'

# Loop through the data and add columns to the DataFrame
for i, data_col in enumerate(data_columns, start=1):
    column_name = f'x{i}'
    df[column_name] = data_col

# Write the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)

print(f'Data saved to {excel_file_path}')