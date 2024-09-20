import pandas as pd
import unidecode  # For removing accents

# Load the Excel file
file_path = 'multitrabajosV2.csv'
df = pd.read_csv(file_path)

df = df.dropna(subset=['descripcion'])

# Load the mapping CSV file
mapping_file_path = 'MapeoTipoTrabajoMultitrabajos.csv'
mapping_df = pd.read_csv(mapping_file_path)

# Create a dictionary from the mapping CSV file
mapping_dict = dict(zip(mapping_df['tipoTrabajoPrev'], mapping_df['tipoTrabajo']))

# Function to map tipoTrabajoPrev to tipoTrabajo
def map_tipo_trabajo(work_type):
    # Find the best match in the mapping dictionary
    for key in mapping_dict:
        if key in str(work_type):
            return mapping_dict[key]
    return 'Varios'

# Load the mapping area CSV file
mapping_area_file_path = 'areas.csv'
mapping_area_df = pd.read_csv(mapping_area_file_path)

# Create a dictionary from the mapping CSV file
mapping_area_dict = dict(zip(mapping_area_df['id'].astype(str), mapping_area_df['areaName']))

# Function to map tipoTrabajoPrev to tipoTrabajo
def map_area_name(work_type):
    # Find the best match in the mapping dictionary
    for key in mapping_area_dict:
        if key in str(work_type):
            return mapping_area_dict[key]
    return 'Varios'

# Function to split location into ciudad, provincia, and pais
def split_location(loc):
    if isinstance(loc, str):
        parts = loc.split(', ')
        if len(parts) == 3:
            return pd.Series(parts, index=['ciudad', 'provincia', 'pais'])
        elif len(parts) == 2:
            return pd.Series([parts[0], parts[1], 'Ecuador'], index=['ciudad', 'provincia', 'pais'])
        elif len(parts) == 1:
            return pd.Series([None, parts[0], 'Ecuador'], index=['ciudad', 'provincia', 'pais'])
    return pd.Series([None, None, 'Ecuador'], index=['ciudad', 'provincia', 'pais'])

# Apply split_location function to location column
df[['ciudad', 'provincia', 'pais']] = df['localizacion'].apply(split_location)

# Apply the mapping function to the idArea column
df['areaName'] = df['idArea'].apply(map_area_name)
# Apply the mapping function to the tipotrabajo column
df['tipoTrabajo'] = df['tipoTrabajo'].apply(map_tipo_trabajo)

df = df.drop(columns=['localizacion', 'idArea', 'promedioEmpresa', 'tipoAviso'])

print(df.head())

# Save the modified DataFrame to a new csv file
output_file_path = 'MultitrabajosV2.1.csv'
df.to_csv(output_file_path, index=False)

print("Data processing complete. The modified file is saved as 'MultitrabajosV2.csv'.")
