import numpy as np
import matplotlib.pyplot as plt

# Parámetros
L = 1.0
Nx = Ny = 20
dx = dy = L / (Nx - 1)
max_iter = 500

# Inicialización
T_current = np.zeros((Ny, Nx))
T_next = np.zeros_like(T_current)

# Condiciones de contorno: Dirichlet en y, Neumann en x
T_current[0, :] = 20    # y = 0
T_current[-1, :] = 50   # y = 1

# Método iterativo (Jacobi)
for _ in range(max_iter):
    for j in range(1, Ny - 1):
        for i in range(Nx):
            if i == 0:  # Neumann en x = 0
                T_next[j, i] = 0.25 * (
                    T_current[j + 1, i] + T_current[j - 1, i] + 2 * T_current[j, i + 1]
                )
            elif i == Nx - 1:  # Neumann en x = L
                T_next[j, i] = 0.25 * (
                    T_current[j + 1, i] + T_current[j - 1, i] + 2 * T_current[j, i - 1]
                )
            else:  # Interior
                T_next[j, i] = 0.25 * (
                    T_current[j + 1, i] + T_current[j - 1, i] +
                    T_current[j, i + 1] + T_current[j, i - 1]
                )
    # Reimponer Dirichlet
    T_next[0, :] = 20
    T_next[-1, :] = 50
    T_current = T_next.copy()

# Visualización con degradado más suave
plt.figure(figsize=(6, 5))
plt.imshow(T_current, origin='lower', extent=[0, 1, 0, 1],
           cmap='inferno', vmin=20, vmax=50)  # Cambia aquí el colormap si quieres otro
plt.colorbar(label='Temperatura')
plt.title("Distribución Estacionaria (20×20)\nNeumann en x, Dirichlet en y")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(False)
plt.tight_layout()
plt.show()

# Imprimir valores finales (opcional)
print("\nDistribución de temperatura (20×20):\n")
for j in reversed(range(Ny)):
    fila = f"y={j*dy:.2f}  "
    for i in range(Nx):
        fila += f"{T_current[j, i]:6.2f} "
    print(fila)
