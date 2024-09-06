import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

# Parameters
Lx = 200
Ly = 180
Lz = 10       # Size of the cubic domain (mm)
Nx = 150       # Number of grid points along x
Ny = 90       # Number of grid points along y
Nz = 20       # Number of grid points along z
alpha = 0.2  # Thermal diffusivity (mm^2/s) TPU: 0.11 PVC:0.08
T_initial = -20.0 # Initial temperature in the center of the cube (starting from 60 degrees Celsius)
T_room = 25.0  # Room temperature
Time = 10 # Time Duration (s)

# Discretization
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
dz = Lz / (Nz - 1)
dt = 1 # Time step (s)

# Initialize the grid
T = np.ones((Nx, Ny, Nz)) * T_initial
T[:, :, :] = T_initial  # Set the entire cube to the initial temperature
T[:, 0, :] = T_room  # Set the bottom boundary to room temperature
T[:, -1, :] = T_room  # Set the top boundary to room temperature
T[0, :, :] = T_room  # Set the left boundary to room temperature
T[-1, :, :] = T_room  # Set the right boundary to room temperature
T[:, :, 0] = T_room  # Set the front boundary to room temperature
#T[:, :, -1] = T_room  # Set the back boundary to room temperature

# Time stepping (explicit finite difference)
num_steps = int(Time / dt)
print("num_steps: ",num_steps)

# T_plot saves the calculated crossed-sectional data in x-z plane
T_plot = np.zeros((Nx-2, Ny-2, Nz-2, num_steps))
# T_Surface saves the change of the surface temperature between each step
T_Surface = []
# T_Core saves the change of the core temperature between each step
T_Core = []
Time = []

for step in range(num_steps):
    print(step)
    Tn = T.copy()  # Copy the current temperature field
    T_plot[:,:,:,step] = T[1:-1,1:-1,1:-1].copy()
    #print(T[1:-1,1:-1,5])
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            for k in range(1, Nz-1):
                T[i, j, k] = Tn[i, j, k] + 0.1 * alpha * dt * (
                    (Tn[i+1, j, k] - 2*Tn[i, j, k] + Tn[i-1, j, k]) / dx**2 +
                    (Tn[i, j+1, k] - 2*Tn[i, j, k] + Tn[i, j-1, k]) / dy**2 +
                    (Tn[i, j, k+1] - 2*Tn[i, j, k] + Tn[i, j, k-1]) / dz**2
                )
                T_Surface.append(T[20,20,5])
                T_Core.append(T[75,45,10]) 
                Time.append(step*dt)

    # Implement insulated boundary conditions
    # Bottom boundary
    #T[:, -1, :] = T[:, -2, :]
    # Top boundary remains unchanged to allow heat conduction outwards
    # Left boundary
    #T[0, :, :] = T[1, :, :]
    # Right boundary
    #T[-1, :, :] = T[-2, :, :]
    # Front boundary
    #T[:, :, 0] = T[:, :, 1]
    # Back boundary
    T[:, :, -1] = T[:, :, -2]
# Visualization
# Contour Field Plot Animation
x = np.linspace(0, Lx, Nx-2)
y = np.linspace(0, Ly, Ny-2)
Xg, Yg = np.meshgrid(x, y)

'''
cntr1 = plt.contour(Xg, Yg, T_plot[:,:,-1], levels=100)
plt.title('Heating for 20s')
plt.colorbar(cntr1)
plt.show()
'''


#Animation
'''
plt.ion()
for k in range(0, num_steps - 1, 5):
    cntr1 = plt.contourf(Xg, Yg, T_plot[1:-1, 1:-1, k], levels=100,vmin = -40, vmax = -38)
    plt.title(str(k))
    plt.colorbar(cntr1)
    plt.show()
    plt.pause(1)
    plt.clf()
#plt.close()
'''

X, Y, Z = np.meshgrid(np.arange(Nx-2), np.arange(Ny-2), -np.arange(Nz-2))
x = np.linspace(0, Lx, Nx-2)
y = np.linspace(0, Ly, Ny-2)
z = np.linspace(0, Lz, Nz-2)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
kw = {
    'vmin': T_plot.min(),
    'vmax': T_plot.max(),
    'levels': np.linspace(T_plot.min(), T_plot.max(), 10),
}

#plt.ion()


for k in range(0, num_steps, 5):
    # Create a figure with 3D ax
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, projection='3d')

    _ = ax.contourf(
        X[:, :, 0], Y[:, :, 0], T_plot[:, :, 0, k],
        zdir='z', offset=0, **kw
    )
    _ = ax.contourf(
        X[0, :, :], T_plot[0, :, :,k], Z[0, :, :],
        zdir='y', offset=0, **kw
    )
    C = ax.contourf(
        T_plot[:, 5, :,k], Y[:, -1, :], Z[:, -1, :],
        zdir='x', offset=X.max(), **kw
    )

    # Set limits of the plot from coord limits
    xmin, xmax = X.min(), X.max()
    ymin, ymax = Y.min(), Y.max()
    zmin, zmax = Z.min(), Z.max()
    ax.set(xlim=[xmin, xmax], ylim=[ymin, ymax], zlim=[zmin, zmax*2])

    # Plot edges
    edges_kw = dict(color='0.4', linewidth=1, zorder=1e3)
    ax.plot([xmax, xmax], [ymin, ymax], 0, **edges_kw)
    ax.plot([xmin, xmax], [ymin, ymin], 0, **edges_kw)
    ax.plot([xmax, xmax], [ymin, ymin], [zmin, zmax], **edges_kw)

    # Set labels and zticks
    ax.set(
        xlabel='X [mm]',
        ylabel='Y [mm]',
        zlabel='Z [mm]',
        zticks=[0, -5, -10, -15],
    )

    # Set zoom and angle view
    ax.view_init(40, -30, 0)
    ax.set_box_aspect(None, zoom=0.9)

    # Colorbar
    fig.colorbar(C, ax=ax, fraction=0.02, pad=0.1, label='Name [units]')
    
    plt.title(str(k))
    plt.show()
    #plt.pause(1)
    #plt.clf()

'''
for i in range(0,int(num_steps),10):
    print(i," core: ",T_plot[35,35,5,i])
for i in range(0,int(num_steps),10):
    print(i," surface: ",T_plot[4,3,5,i])

#plt.plot(Time,T_Surface)
#plt.show()
#plt.scatter(i*dt,T_Surface[i])
#plt.show()
'''
'''
# Save data into Excel
data_columns = T_plot[:,:,5,-1]

# Create an empty DataFrame
df = pd.DataFrame()

# Specify the Excel file path
excel_file_path = 'Heat tranfer simulator/Result_' + str(T_initial) + '_' + str(alpha) + '.xlsx'

# Loop through the data and add columns to the DataFrame
for i, data_col in enumerate(data_columns, start=1):
    column_name = f'x{i}'
    df[column_name] = data_col

# Write the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)

print(f'Data saved to {excel_file_path}')
'''