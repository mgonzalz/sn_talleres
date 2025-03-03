# Funcion para ajustar un polinomio de mediante mínimos cuadrados.
def polynomial_regression(x, y, degree):
    X = np.vander(x, degree + 1, increasing=True)  # Matriz de Vandermonde.
    coeffs = np.linalg.inv(X.T @ X) @ X.T @ y  # Resolver ecuación normal.
    return coeffs

# Funcion para evaluar un polinomio en los puntos dado un conjunto de coeficientes.
def evaluate_polynomial(coeffs, x_vals):
    y_vals = np.zeros_like(x_vals)
    for i, coef in enumerate(coeffs):
        y_vals += coef * (x_vals ** i)  # Evaluación manual del polinomio.
    return y_vals
