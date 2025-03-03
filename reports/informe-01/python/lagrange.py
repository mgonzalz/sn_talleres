# Funcion para calcular los coeficientes de Lagrange L_i(x).
def lagrange_basis(x, x_data, i):
    n = len(x_data)
    L_i = 1
    for j in range(n):
        if j != i:
            L_i *= (x - x_data[j]) / (x_data[i] - x_data[j])
    return L_i

# Funcion para calcular el polinomio de interpolación de Lagrange.
def polinomio_lagrange(x, x_data, y_data):
    n = len(x_data)
    resultado = 0
    for i in range(n):
        resultado += y_data[i] * lagrange_basis(x, x_data, i)
    return resultado
