# Funcion potencial.
def power_law(x, a0, a1):
    return a0 * x**a1

# Filtrar datos para evitar problemas con log(0)
valid_indices =  x_data > 0
x_nonzero = x_data[valid_indices]
y_nonzero = y_data[valid_indices]

# Transformacion logaritmica.
log_x_nonzero = np.log(x_nonzero)
log_y_nonzero = np.log(y_nonzero)

# Ajustar una regresion lineal en la escala log-log
coeffs = polynomial_regression(log_x_nonzero, log_y_nonzero, degree=1)

# Extracción de coeficientes
a1_manual = coeffs[1]  # Pendiente
log_a0_manual = coeffs[0]  # Intercepto en la escala log-log
a0_manual = np.exp(log_a0_manual)  # Volver a la escala original
'''
