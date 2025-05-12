# Parámetros físicos.
alpha = 0.01
L = 1.0

# Discretización espacial.
Nx = Ny = 20 # Mallado cuadrado.
dx = L / (Nx - 1) # Espaciado entre nodos.

# Discretización temporal.
dt = 0.01 # Paso de tiempo.
T_max = 5 # Tiempo total de simulación.
Nt = int(T_max / dt) # Número de pasos de tiempo.



# Malla espacial.
x = np.linspace(0, L, Nx) # Vector de Nx puntos espaciados uniformemente entre 0 y L.
y = np.linspace(0, L, Ny) # Vector de Ny puntos espaciados uniformemente entre 0 y L.
X, Y = np.meshgrid(x, y) # Creación de la malla 2D: Matriz N^2.

# Condición inicial.
T = -50 * np.cos(np.pi * X / 2) * np.cos(np.pi * Y / 2) # Matriz en instante t=0.



# Construcción de la matriz A mediante Sparse: Esquema de 5 puntos.
def build_sparse_matrix_A(Nx, Ny, alpha, dt, dx):
    N = Nx * Ny # Número total de nodos: N^2.
    A = lil_matrix((N, N)) # Matriz dispersa vacía: Cada fila se representa como una lista de columnas con valores distintos de cero.
    lam = alpha * dt / dx**2 # Número de Fourier: lambda.
    for j in range(Ny):
        for i in range(Nx):
            idx = j * Nx + i # De 2D a 1D.
            if j == 0 or j == Ny - 1:  # Dirichlet en y=0 y y=L. Valor fijo.
                A[idx, idx] = 1
                continue
            A[idx, idx] = 1 + 4 * lam # Coeficiente de la diagonal principal.
            if i == 0: # Neumann x=0.
                A[idx, idx + 1] = -2 * lam # Reflexión simétrica.
            elif i == Nx - 1:  # Neumann x=L.
                A[idx, idx - 1] = -2 * lam # Reflexión simétrica.
            else:
                A[idx, idx - 1] = -lam # Izquierda.
                A[idx, idx + 1] = -lam # Derecha.
            A[idx, idx - Nx] = -lam # Arriba.
            A[idx, idx + Nx] = -lam # Abajo.
    return csc_matrix(A) # Convertir a formato CSR para eficiencia en la solución.

A_sparse = build_sparse_matrix_A(Nx, Ny, alpha, dt, dx)



# Simulación y captura de frames.
frames = []
for n in range(Nt): # Iterar sobre el tiempo.
    T_flat = T.flatten() # Convertir a 1D para la matriz dispersa.
    T_flat[:Nx] = 20         # y = 0.
    T_flat[-Nx:] = 50        # y = 1.
    T_new = spsolve(A_sparse, T_flat) # A*x=b.
    T = T_new.reshape((Ny, Nx)) # Volver a 2D.
    if n % 5 == 0:           # Guardar cada 5 pasos (~100 frames totales).
        frames.append(T.copy())

# Crear animación.
fig, ax = plt.subplots(figsize=(6, 5))
cax = ax.imshow(frames[0], origin='lower', cmap='hot', extent=[0, 1, 0, 1], interpolation='bilinear')
cbar = fig.colorbar(cax, ax=ax)
cbar.set_label('Temperatura')
title = ax.set_title("t = 0.00 s")
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid(False)
plt.show()



# Animación de la simulación.
def update(frame_idx):
    cax.set_data(frames[frame_idx])
    t_val = frame_idx * 5 * dt
    title.set_text(f"t = {t_val:.2f} s")
    return cax, title

anim = FuncAnimation(fig, update, frames=len(frames), interval=100)
