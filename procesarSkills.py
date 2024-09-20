import pandas as pd
import re

# Cargar los archivos CSV
data = pd.read_csv('TrabajosEcuadorV2.csv')  # El archivo con la columna "descripcion"
synonym_mapping = pd.read_csv('Sorted_Synonym_Mapping.csv')  # Mapeo de sinónimos
hard_skills = pd.read_csv('Sorted_Hard_Skills.csv')  # Hard skills
soft_skills = pd.read_csv('Sorted_Soft_Skills.csv')  # Soft skills

# 1. Normalizar el texto y hacerlo lowercase
def normalize_text(text):
    # Convertir a minúsculas y eliminar caracteres no deseados
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)  # Eliminar puntuación y caracteres especiales
        text = re.sub(r'\s+', ' ', text)  # Reemplazar múltiples espacios por uno solo
        return text.strip()
    return ''


data['descripcion_normalizada'] = data['descripcion'].apply(normalize_text)


# 2. Reemplazar las frases en el texto usando el archivo Sorted_Synonym_Mapping.csv
def replace_phrases(text, mapping_df):
    if isinstance(text,str):
        for i, row in mapping_df.iterrows():
            original = row['Original Skill'].lower()
            replacement = row['Mapped Skill'].lower()
            text = re.sub(rf'\b{re.escape(original)}\b', replacement, text)
    return text

data['descripcion_reemplazada'] = data['descripcion_normalizada'].apply(lambda x: replace_phrases(x, synonym_mapping))


# 3. Extraer una columna con la lista de similitud de los hard skills
def extract_skills(text, skills_df):
    found_skills = []
    if isinstance(text,str):
        for i, row in skills_df.iterrows():
            skill = row['Skills']
            if isinstance(skill,str) and re.search(rf'\b{re.escape(skill.lower())}\b', text):
                found_skills.append((skill, row['Nombre']))
    return found_skills


data['hardskills'] = data['descripcion_reemplazada'].apply(lambda x: extract_skills(x, hard_skills))

# 4. Extraer una columna con la lista de similitud de los soft skills
data['softskills'] = data['descripcion_reemplazada'].apply(lambda x: extract_skills(x, soft_skills))

# 5. Obtener un DataFrame con los IDs que contienen cada skill (tanto hard como soft skills)
def create_skill_df(skill_mapping, tipo_skill):
    skill_records = []
    for skill, details in skill_mapping.items():
        for job_id in details['ids']:
            skill_records.append({'IdSkill': skill, 'id': job_id, 'Skill': skill, 'Nombre': details['nombre'], 'TipoSkill': tipo_skill})
    return pd.DataFrame(skill_records)

hard_skill_mapping = {}
soft_skill_mapping = {}

for i, row in data.iterrows():
    # Mapeo de hard skills
    for skill, name in row['hardskills']:
        if skill not in hard_skill_mapping:
            hard_skill_mapping[skill] = {'ids': [], 'nombre': name}
        hard_skill_mapping[skill]['ids'].append(row['id'])

    # Mapeo de soft skills
    for skill, name in row['softskills']:
        if skill not in soft_skill_mapping:
            soft_skill_mapping[skill] = {'ids': [], 'nombre': name}
        soft_skill_mapping[skill]['ids'].append(row['id'])

# Añadir una columna con la longitud de la lista de IDs para cada skill
hard_skills_df = pd.DataFrame([(k, v['nombre'], v['ids'], len(v['ids']), 'HardSkill') for k, v in hard_skill_mapping.items()],
                              columns=['Skill', 'Nombre', 'ID List', 'Conteo', 'TipoSkill'])
soft_skills_df = pd.DataFrame([(k, v['nombre'], v['ids'], len(v['ids']), 'SoftSkill') for k, v in soft_skill_mapping.items()],
                              columns=['Skill', 'Nombre', 'ID List', 'Conteo', 'TipoSkill'])

# Guardar el resultado en archivos CSV
hard_skills_df.to_csv('Hard_Skills_Conteo.csv', index=False)
soft_skills_df.to_csv('Soft_Skills_Conteo.csv', index=False)

# Mostrar el DataFrame final con las skills y los IDs
print(hard_skills_df)
print(soft_skills_df)

# Concatenar los DataFrames de hard y soft skills
combined_skills_df = pd.concat([hard_skills_df, soft_skills_df], ignore_index=True)

# Guardar el resultado en un archivo CSV
combined_skills_df.to_csv('Combined_Skills_Conteo.csv', index=False)

# Mostrar el DataFrame final con las skills y los IDs
print(combined_skills_df)

# Crear DataFrames para cada tipo de skill
hard_skills_df = create_skill_df(hard_skill_mapping, 'HardSkill')
soft_skills_df = create_skill_df(soft_skill_mapping, 'SoftSkill')

# Concatenar ambos DataFrames
skills_df = pd.concat([hard_skills_df, soft_skills_df], ignore_index=True)

# Guardar los resultados en archivos CSV
skills_df.to_csv('Skills_List.csv', index=False)

# Mostrar el DataFrame final con las skills y los IDs
print(skills_df)
