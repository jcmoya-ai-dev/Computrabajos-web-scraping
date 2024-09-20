import pandas as pd
import unidecode  # For removing accents

# Load the Excel file
file_path = 'computrabajoAllV2.1.csv'
df = pd.read_csv(file_path)

df = df.dropna(subset=['descripcion'])

# Load the mapping file
mapping_experiencia_file_path = 'MapeoExperienciaComputrabajo.csv'
mapping_experiencia_df = pd.read_csv(mapping_experiencia_file_path)

# Create a dictionary from the mapping file
mapping_experiencia_dict = dict(zip(mapping_experiencia_df['experienciaAnos'], mapping_experiencia_df['experiencia']))

# Function to map experienciaAnos to experiencia
def map_experiencia(experiencia_anios):
    # Handle cases where experiencia_anios is not in the dictionary
    return mapping_experiencia_dict.get(experiencia_anios, 'Sin Experiencia')

# Apply the mapping function to create a new column 'experiencia'
df['experiencia'] = df['experienciaAnos'].apply(map_experiencia)

# Load the mapping CSV file
mapping_file_path = 'MapeoTipoTrabajoComputrabajos.csv'
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

# Define bin edges and labels
bin_edges = [15, 25, 35, 45, 65,100]
bin_labels = ['15-24', '25-34', '35-44', '45-64', '65+']

# Function to map edadMinima and edadMaxima to their respective age groups
def map_age_groups(age, bin_edges, bin_labels):
    return pd.cut([age], bins=bin_edges, labels=bin_labels, right=False)[0]

# Apply mapping to create new columns
df['grupoEdadMinima'] = df['edadMinima'].apply(lambda x: map_age_groups(x, bin_edges, bin_labels))
df['grupoEdadMaxima'] = df['edadMaxima'].apply(lambda x: map_age_groups(x, bin_edges, bin_labels))

df = df.drop(columns=['experienciaAnos', 'skills', 'tipoContrato', 'descripcionTitulo', 'categoria',
                      'empresaVerificada', 'anuncioRelevante', 'promedioEmpresa'])

# Save the modified DataFrame to a new CSV file
output_file_path = 'computrabajoAllV2.2.csv'
df.to_csv(output_file_path, index=False)

print("Data processing complete. The modified file is saved as 'computrabajoAllV2.2.csv'.")