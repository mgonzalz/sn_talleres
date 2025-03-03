def modelo_exponencial(x, a0, a1, a2):
    return a0 - a1 * np.exp(-a2 * x)

def jacobian_exp(x, a0, a1, a2):
    df_da0 = x
    df_da1 = -np.exp(-a2 * x)
    df_da2 = a1 * x * np.exp(-a2 * x)
    return np.column_stack((df_da0, df_da1, df_da2))


def modelo_lineal_exponencial(x, a0, a1, a2):
    return a0 * x - a1 * np.exp(-a2 * x)

def jacobian_lineal_exp(x, a0, a1, a2):
    df_da0 = x
    df_da1 = -np.exp(-a2 * x)
    df_da2 = a1 * x * np.exp(-a2 * x)
    return np.column_stack((df_da0, df_da1, df_da2))


def modelo_cuadratico_exponencial(x, a0, a1, a2):
    return a0 * x**2 - a1 * np.exp(-a2 * x)

def jacobian_cuadratico_exp(x, a0, a1, a2):
    df_da0 = x**2
    df_da1 = -np.exp(-a2 * x)
    df_da2 = a1 * x * np.exp(-a2 * x)
    return np.column_stack((df_da0, df_da1, df_da2))


def gauss_newton(x_data, y_data, modelo, jacobiano, a_init, tol=1e-6, max_iter=100):
    a_current = np.array(a_init, dtype=float)  # Inicialización de parámetros.
    iter_count = 0

    while iter_count < max_iter:
        iter_count += 1

        # Evaluación el modelo en los valores actuales de los parámetros.
        y_pred = modelo(x_data, *a_current)
        residuals = y_data - y_pred

        # Cálculo del Jacobiano
        Z = jacobiano(x_data, *a_current)

        # (Z^T Z) Δa = Z^T D mediante mínimos cuadrados.
        delta_a, _, _, _ = np.linalg.lstsq(Z.T @ Z, Z.T @ residuals, rcond=None)
        a_current += delta_a

        # Criterio de convergencia.
        error = np.linalg.norm(delta_a) / np.linalg.norm(a_current)
        if error < tol:
            break

    return a_current, iter_count

