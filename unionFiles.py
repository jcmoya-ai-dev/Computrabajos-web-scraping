import pandas as pd

# Cargar los tres archivos CSV
df1 = pd.read_csv('computrabajoAllV2.2.csv')
df2 = pd.read_csv('multitrabajosV2.1.csv')
df3 = pd.read_csv('LinkdinV3.csv')

# Unir los tres DataFrames, asegurando que las columnas no coincidentes se llenen con 'NoInfo'
df_combined = pd.concat([df1, df2, df3], ignore_index=True, join='outer')

# Exportar el DataFrame unido a un nuevo archivo CSV
df_combined.to_csv('TrabajosEcuadorV2.csv', index=False)

print("Los archivos CSV se han unido correctamente y exportado a 'TrabajosEcuadorV2.csv'.")
