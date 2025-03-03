# Modelos a resolver.
modelos = {
    "Modelo Exponencial": modelo_exponencial,
    "Modelo Lineal-Exponencial": modelo_lineal_exponencial,
    "Modelo Cuadrático-Exponencial": modelo_cuadratico_exponencial
}

# Parametros iniciales para cada modelo.
parametros_iniciales = {
    "Modelo Exponencial": [10, 5, 0.5],
    "Modelo Lineal-Exponencial": [1, 5, 0.5],
    "Modelo Cuadrático-Exponencial": [1, 5, 0.5]
}


# Diccionario para almacenar los parámetros ajustados.
parametros_ajustados = {}

# Ajuste de los modelos.
for nombre, modelo in modelos.items():
    params_opt, _ = curve_fit(modelo, x_nonzero, y_nonzero, p0=parametros_iniciales[nombre])  # Ajuste con valores iniciales
    parametros_ajustados[nombre] = params_opt
