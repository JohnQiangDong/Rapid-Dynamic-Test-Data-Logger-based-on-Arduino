# In this section I am importing all the libraries I will need
import numpy as np
import matplotlib.pyplot as plt


# In this section I am setting the domain of solution and the discretised grid

# Space step
h = 1.25  # mm
# Time step
t = 0.1  # s
# Size of the cross-sectional area of the steak
Lx = 25  # mm
Ly = 25  # mm
Heating_time = 30  # s

# Length of each side of the the cross-sectional area of the steak (Number of Nodes each side)
Nx = int(Lx / h) + 1
Ny = int(Ly / h) + 1

# Length of time
Nt = int(Heating_time / t)

# Store Temperature at each point
T = np.zeros((Nx, Ny, Nt))
print(T.shape)

# In this section I am defining arrays I would need (if neeeded)

# T is initialized above for storing the temperature of the steak at each point


# In this section I am setting the boundary conditions/initial values

# Thermal diffusivity (Beef)
a = 0.12  # mm^2/s

# Temperature initialization
# Bottom of the ribeye steak heated near the pan is 100 degrees
# Rest of the ribeye steak is as same as the temperature of the refrigerator where it stored
T[:, :, :] = 5
T[:, 0, :] = 100

# In this section I am implementing the numerical method
r = a * t / h ** 2
print(r)  # check whether the method is convergent

# Calculate the temperature at each time
for k in range(0, Nt - 1):
    # generate matrix to solve the PDE
    # Equations: M * X = A
    M = np.zeros(((Nx - 2) * (Ny - 2), (Nx - 2) * (Ny - 2)))
    A = np.zeros((Nx - 2) * (Ny - 2))

    for i in range(0, (Nx - 2) * (Ny - 2)):
        M[i, i] = 4 * r + 1
        if i % (Ny - 2) != 0:
            M[i - 1, i] = -r
        else:
            A[i] += r * T[0, i % (Ny - 2) + 1, k]

        if (i - (Nx - 2)) >= 0:
            M[i - (Nx - 2), i] = -r
        else:
            A[i] += r * T[int(i / (Nx - 2)) + 1, 0, k]

        if i % (Ny - 2) != Ny - 3:
            M[i + 1, i] = -r
        else:
            A[i] += r * T[-1, i % (Ny - 2) + 1, k]

        if i + (Nx - 2) < (Nx - 2) * (Ny - 2):
            M[i + (Nx - 2), i] = -r
        else:
            A[i] += r * T[int(i / (Nx - 2)) + 1, -1, k]
    # Generate A
    count = 0
    for j in range(1, Nx-1):
        for i in range(1, Ny-1):
            A[count] += T[i, j, k]
            count += 1
    # Solve X
    Result = np.linalg.solve(M, A)

    # Store Calculated results in to Temperature
    count = 0
    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            T[i, j, k + 1] = Result[count]
            count += 1


# In this section I am showing the results

x = np.arange(0, Nx)
y = np.arange(0, Ny)
Xg, Yg = np.meshgrid(x, y)

# Contour Field Plot
cntr1 = plt.contourf(Xg, Yg, T[:, :, 10], levels=10)
plt.title('Heating for 1s')
plt.colorbar(cntr1)
plt.show()
cntr1 = plt.contourf(Xg, Yg, T[:, :, 150], levels=10)
plt.title('Heating for 15s')
plt.colorbar(cntr1)
plt.show()
cntr1 = plt.contourf(Xg, Yg, T[:, :, -1], levels=10)
plt.title('Heating for 30s')
plt.colorbar(cntr1)
plt.show()

# Contour Plot
cntr1 = plt.contour(Xg, Yg, T[:, :, 10], levels=10)
plt.title('Heating for 1s')
plt.colorbar(cntr1)
plt.show()
cntr1 = plt.contour(Xg, Yg, T[:, :, 150], levels=10)
plt.title('Heating for 15s')
plt.colorbar(cntr1)
plt.show()
cntr1 = plt.contour(Xg, Yg, T[:, :, -1], levels=10)
plt.title('Heating for 30s')
plt.colorbar(cntr1)
plt.show()

# 3D Plot
x = np.arange(0,Nx)
y = np.arange(Ny,0,-1)
Xg,Yg = np.meshgrid(x,y)
ax = plt.axes(projection = "3d")
surf = ax.plot_surface(Xg,Yg,T[:,:,10])
plt.title('Heating for 1s')
plt.show()
ax = plt.axes(projection = "3d")
surf = ax.plot_surface(Xg,Yg,T[:,:,150])
plt.title('Heating for 15s')
plt.show()
ax = plt.axes(projection = "3d")
surf = ax.plot_surface(Xg,Yg,T[:,:,-1])
plt.title('Heating for 30s')
plt.show()


# Contour Field Plot Animation
plt.ion()
for k in range(0, Nt - 1, 10):
    cntr1 = plt.contourf(Xg, Yg, T[:, :, k], levels=100)
    plt.title(str(k))
    plt.colorbar(cntr1)
    plt.show()
    plt.pause(0.2)
    plt.clf()
plt.close()


# In this section I am celebrating
print('CW done: I deserve a good mark')
