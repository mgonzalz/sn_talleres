import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Parámetros
L = 1.0
Nx = Ny = 20
dx = dy = L / (Nx - 1)
max_iter = 300

# Inicialización
T_current = np.zeros((Ny, Nx))
T_next = np.zeros_like(T_current)
T_current[0, :] = 20     # y = 0 (abajo)
T_current[-1, :] = 50    # y = 1 (arriba)

# Lista para guardar fotogramas
frames = []

# Preparar figura
fig, ax = plt.subplots(figsize=(6, 5))
c = ax.imshow(T_current, origin='lower', extent=[0, 1, 0, 1],
              cmap='hot', vmin=20, vmax=50)
fig.colorbar(c, ax=ax, label='Temperatura')
title = ax.set_title("Iteración 0")

# Función de actualización
def update(frame):
    global T_current, T_next
    for j in range(1, Ny - 1):
        for i in range(Nx):
            if i == 0:
                T_next[j, i] = 0.25 * (
                    T_current[j + 1, i] + T_current[j - 1, i] + 2 * T_current[j, i + 1]
                )
            elif i == Nx - 1:
                T_next[j, i] = 0.25 * (
                    T_current[j + 1, i] + T_current[j - 1, i] + 2 * T_current[j, i - 1]
                )
            else:
                T_next[j, i] = 0.25 * (
                    T_current[j + 1, i] + T_current[j - 1, i] +
                    T_current[j, i + 1] + T_current[j, i - 1]
                )

    # Reimponer Dirichlet en y
    T_next[0, :] = 20
    T_next[-1, :] = 50

    T_current = T_next.copy()
    c.set_data(T_current)
    title.set_text(f"Iteración {frame}")
    return [c, title]

# Crear animación
ani = FuncAnimation(fig, update, frames=max_iter, interval=30, blit=False)

# Guardar como GIF a mayor velocidad
ani.save("estacionaria_neumann_dirichlet.gif", writer=PillowWriter(fps=20))
