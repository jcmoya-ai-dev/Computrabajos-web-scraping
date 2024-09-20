import pandas as pd

# Cargar el CSV original
df = pd.read_csv('computrabajoAllV2.csv')

# Definir el valor de la nueva columna
origen = 'computrabajo'

# Insertar la columna 'origen' en la segunda posición (índice 1)
df.insert(1, 'origen', origen)

# Exportar el dataframe a un nuevo archivo CSV
df.to_csv('computrabajoAllV2.1.csv', index=False)

print("El archivo CSV se ha modificado y exportado correctamente.")
