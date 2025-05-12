# Parámetros inicialización.
L = 1.0 # Longitud del dominio.
Nx = Ny = 20  # Mallado cuadrado.
dx = L / (Nx - 1) # Espaciado entre nodos.
N = Nx * Ny # Número total de nodos.

# Condiciones de contorno.
T_abajo = 20 # Temperatura en y=0.
T_arriba = 50 # Temperatura en y=L.
b = np.zeros(N) # Vector b para el sistema Ax=b.



# Construcción de la matriz A en formato CSR.
data = [] # Datos no nulos de la matriz.
indices = [] # Índices de las columnas correspondientes a los datos.
indptr = [0] # Puntero para la posición de inicio de cada fila.

for j in range(Ny):
    for i in range(Nx): # Recorrer cada nodo de la malla.
        idx = j * Nx + i # De 2D a 1D.
        row_data = [] # Datos de la fila actual.
        row_indices = [] # Índices de la fila actual.

        if j == 0: # Dirichlet en y=0.
            row_data.append(1)
            row_indices.append(idx)
            b[idx] = T_abajo # Cambiar signo para el sistema Ax=b.

        elif j == Ny - 1: # Dirichlet en y=L.
            row_data.append(1)
            row_indices.append(idx)
            b[idx] = T_arriba

        else:
            # Diagonal central.
            row_data.append(-4)
            row_indices.append(idx)

            if i == 0: # Neumann en x=0.
                row_data.append(2)
                row_indices.append(idx + 1)
            elif i == Nx - 1: # Neumann en x=L.
                row_data.append(2)
                row_indices.append(idx - 1)
            else: # Interior del dominio.
                row_data += [1, 1]
                row_indices += [idx - 1, idx + 1]

            # Arriba y abajo.
            row_data += [1, 1]
            row_indices += [idx - Nx, idx + Nx]

        # Añadir a CSR.
        data.extend(row_data)
        indices.extend(row_indices)
        indptr.append(len(data))



# Método de Gauss-Seidel para resolver Ax=b.
def gauss_seidel_csr(data, indices, indptr, b, tol=1e-5, max_iter=10000):
    # Inicializar variables.
    N = len(b)
    x = np.zeros_like(b)

    for _ in range(max_iter):
        x_old = x.copy() # Guardar la solución anterior para la convergencia.
        for i in range(N):
            row_start = indptr[i] # Inicio de la fila i.
            row_end = indptr[i + 1] # Fin de la fila i.
            sum_ = 0
            diag = 0
            for k in range(row_start, row_end): # Recorrer la fila i.
                col = indices[k] # Columna correspondiente al dato.
                val = data[k] # Valor del dato.
                if col == i: # Diagonal principal.
                    diag = val
                else: # Sumar los productos de la fila.
                    sum_ += val * x[col]
            x[i] = (b[i] - sum_) / diag # Actualizar la solución.
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            break
    return x



T_flat = gauss_seidel_csr(data, indices, indptr, b)
T = T_flat.reshape((Ny, Nx)) # Volver a 2D.

plt.imshow(T, origin='lower', cmap='hot', extent=[0, 1, 0, 1], interpolation='bilinear')
plt.colorbar(label='Temperatura')
plt.title("Solución estacionaria")
plt.show()
