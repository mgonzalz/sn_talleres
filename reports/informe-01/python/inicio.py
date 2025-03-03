# Funcion para leer los datos desde un archivo txt.
def leer_datos(archivo):
    datos = np.loadtxt(archivo)
    x = datos[:, 0]
    y = datos[:, 1]
    return x, y

# Graficacion de los datos originales.
plt.figure(figsize=(8, 6))
plt.scatter(x_data, y_data, color='black', marker='x', alpha=0.8)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Datos Originales")
plt.grid(True)
plt.savefig("../figures/informe-01/datos.png")
plt.show()
