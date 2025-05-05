import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Parámetros
L = 1.0
Nx = Ny = 20
dx = dy = L / (Nx - 1)
max_iter = 200

# Inicialización
T_current = np.zeros((Ny, Nx))
T_next = np.zeros_like(T_current)

# Dirichlet: y=0 (abajo) y y=1 (arriba)
T_current[0, :] = 20
T_current[-1, :] = 50

# Guardar iteraciones
T_iter = np.zeros((max_iter, Ny, Nx))

for k in range(max_iter):
    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            T_next[j, i] = 0.25 * (
                T_current[j+1, i] + T_current[j-1, i] +
                T_current[j, i+1] + T_current[j, i-1]
            )

    # Neumann en x = 0 → T[-1] = T[1]
    for j in range(1, Ny - 1):
        T_next[j, 0] = 0.25 * (
            T_current[j+1, 0] + T_current[j-1, 0] +
            2 * T_current[j, 1]
        )

    # Neumann en x = 1 → T[N+1] = T[N-1]
    for j in range(1, Ny - 1):
        T_next[j, -1] = 0.25 * (
            T_current[j+1, -1] + T_current[j-1, -1] +
            2 * T_current[j, -2]
        )

    # Reaplicar Dirichlet
    T_next[0, :] = 20
    T_next[-1, :] = 50

    T_current = T_next.copy()
    T_iter[k] = T_current.copy()

# Animación
fig, ax = plt.subplots(figsize=(6, 5))
cax = ax.imshow(T_iter[0], origin='lower', cmap='hot', extent=[0, 1, 0, 1], vmin=0, vmax=50)
cbar = fig.colorbar(cax, ax=ax)
cbar.set_label('Temperatura')
title = ax.set_title("Iteración 0")

def update(frame):
    cax.set_data(T_iter[frame])
    title.set_text(f"Iteración {frame}")
    return cax, title

anim = FuncAnimation(fig, update, frames=max_iter, interval=100)
anim.save("estacionaria_malla20_neumann.gif", writer=PillowWriter(fps=10))
