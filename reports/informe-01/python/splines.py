# Construccion del spline cúbico natural. Devuelve los coeficientes de los polinomios por tramos.
def spline_cubico(x_data, y_data):
    n = len(x_data) - 1  # Numero de intervalos.
    h = np.diff(x_data)  # Tamaño de cada subintervalo.
    b = np.diff(y_data) / h  # Diferencias divididas.

    # Matriz tridiagonal y vector de terminos independientes.
    A = np.zeros((n + 1, n + 1))
    b_vec = np.zeros(n + 1)

    # Condiciones de frontera naturales.
    A[0, 0] = 1
    A[n, n] = 1

    for i in range(1, n):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        b_vec[i] = 3 * (b[i] - b[i - 1])

    # Resolucion del sistema tridiagonal para obtener segunda derivada (c coeficientes)
    c = np.linalg.solve(A, b_vec)

    # Calcular coeficientes a, b, c, d para cada subintervalo
    a = y_data[:-1]
    d = np.diff(c) / (3 * h)
    b = b - h * (2 * c[:-1] + c[1:]) / 3

    return a, b, c[:-1], d, x_data


# Evaluacion del spline cubico en un conjunto de puntos x.
def evaluar_spline(x, x_data, a, b, c, d):
    n = len(x_data) - 1
    y_vals = np.zeros_like(x)
    
    for i in range(n):
        indices = (x >= x_data[i]) & (x <= x_data[i + 1])
        dx = x[indices] - x_data[i]
        y_vals[indices] = a[i] + b[i] * dx + c[i] * dx**2 + d[i] * dx**3

    return y_vals
