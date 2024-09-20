import pandas as pd
import unidecode  # For removing accents

# Load the Excel file
file_path = 'Linkdn.xlsx'
df = pd.read_excel(file_path)

df = df.dropna(subset=['description'])

# Load the mapping CSV file
mapping_file_path = 'MapeoCategoria.csv'
mapping_df = pd.read_csv(mapping_file_path)

# Create a dictionary from the mapping CSV file
mapping_dict = dict(zip(mapping_df['workType'], mapping_df['areaName']))

# Function to map workType to areaName
def map_area_name(work_type):
    # Find the best match in the mapping dictionary
    for key in mapping_dict:
        if key in str(work_type).lower():
            return mapping_dict[key]
    return 'Varios'

# Load the mapping contractType CSV file
mapping_contract_file_path = 'MapeoContractTypeLinkdn.csv'
mapping_contract_df = pd.read_csv(mapping_contract_file_path)
print(mapping_contract_df.head())

# Create a dictionary from the mapping CSV file
mapping_contract_dict = dict(zip(mapping_contract_df['contractType'], mapping_contract_df['tipoTrabajo']))

# Function to map workType to areaName
def map_tipo_trabajo(work_type):
    # Find the best match in the mapping dictionary
    for key in mapping_contract_dict:
        if key in str(work_type):
            return mapping_contract_dict[key]
    return 'Varios'

# Load the mapping experience CSV file
mapping_experience_file_path = 'MapeoExperienceLinkdn.csv'
mapping_experience_df = pd.read_csv(mapping_experience_file_path)
print(mapping_experience_df.head())

# Create a dictionary from the mapping CSV file
mapping_experience_dict = dict(zip(mapping_experience_df['experienceLevel'], mapping_experience_df['experiencia']))

# Function to map contractType to tipoTrabajo
def map_experiencia(experience_type):
    # Find the best match in the mapping dictionary
    for key in mapping_experience_dict:
        if key in str(experience_type):
            return mapping_experience_dict[key]
    return None

# Function to clean description column
def clean_description(desc):
    if isinstance(desc, str):  # Check if desc is a string
        desc = desc.replace(',', '.')
        desc = desc.replace('\n', ' ')
    return desc

# Apply cleaning function to description column
df['descripcion'] = df['description'].apply(clean_description)

# Function to split location into ciudad, provincia, and pais
def split_location(loc):
    if isinstance(loc, str):
        parts = loc.split(', ')
        if len(parts) == 3:
            return pd.Series(parts, index=['ciudad', 'provincia', 'pais'])
        elif len(parts) == 2:
            return pd.Series([None, parts[0], parts[1]], index=['ciudad', 'provincia', 'pais'])
        elif len(parts) == 1:
            return pd.Series([None, None, parts[0]], index=['ciudad', 'provincia', 'pais'])
    return pd.Series([None, None, None], index=['ciudad', 'provincia', 'pais'])

# Apply split_location function to location column
df[['ciudad', 'provincia', 'pais']] = df['location'].apply(split_location)

# Function to normalize text
def normalize_text(text):
    if isinstance(text, str):  # Check if text is a string
        text = unidecode.unidecode(text)  # Remove accents
        text = ''.join(e for e in text if e.isalnum() or e.isspace())  # Remove special characters
        text = text.lower()  # Convert to lowercase
    return text

# Apply normalization to relevant columns
df['companyName'] = df['companyName'].apply(normalize_text)
df['descripcion'] = df['descripcion'].apply(normalize_text)
df['title'] = df['title'].apply(normalize_text)
#df['sector'] = df['sector'].apply(normalize_text)
df['workType'] = df['workType'].apply(normalize_text)

# Apply the mapping function to the workType column
df['areaName'] = df['workType'].apply(map_area_name)
# Apply the mapping function to the contractType column
df['tipoTrabajo'] = df['contractType'].apply(map_tipo_trabajo)
# Apply the mapping function to the Experience column
df['experiencia'] = df['experienceLevel'].apply(map_experiencia)

df = df.drop(columns=['description', 'workType', 'contractType', 'experienceLevel', 'sector', 'applyType', 'companyId',
                      'companyUrl', 'jobUrl', 'location'])

# Definir el valor de la nueva columna
origen = 'linkdin'

# Insertar la columna 'origen' en la segunda posición (índice 1)
df.insert(1, 'origen', origen)
# Insertar la columna 'origen' en la segunda posición (índice 1)
df.insert(0, 'id', origen)

# Crear la columna 'id' con un secuencial y la palabra 'linkdin'
df['id'] = [f'{i+1}linkdin' for i in range(len(df))]
df = df.rename(columns={'companyName': 'empresa', 'title': 'titulo'})

# Define keyword lists for each category
remote_keywords = ['virtual', 'remoto', 'remote', 'remota']
hybrid_keywords = ['hibrido', 'semipresencial', 'hybrid']
in_person_keywords = ['presencial','movilizacion', 'in person']

# Function to determine the modalidadTrabajo based on descripcion
def determine_modalidad(descripcion):
    if any(keyword in descripcion.lower() for keyword in remote_keywords):
        return 'Remoto'
    elif any(keyword in descripcion.lower() for keyword in hybrid_keywords):
        return 'Híbrido'
    elif any(keyword in descripcion.lower() for keyword in in_person_keywords):
        return 'Presencial'
    else:
        return 'Presencial'

# Apply the function to create the modalidadTrabajo column
df['modalidadTrabajo'] = df['descripcion'].apply(determine_modalidad)

print(df.head())

# Save the modified DataFrame to a new Excel file
output_file_path = 'LinkdinV3.csv'
df.to_csv(output_file_path, index=False)

print("Data processing complete. The modified file is saved as 'LinkdinV3.xlsx'.")
