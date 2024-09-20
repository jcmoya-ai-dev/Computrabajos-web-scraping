import pandas as pd
from unidecode import unidecode


# Load the Excel file
file_path = 'computrabajoAllV2.csv'
df = pd.read_csv(file_path)

# Step 2: Extract and split skills
# Assuming 'skills' is the name of the column containing the skills
skills_text = df['skills'].dropna()  # Drop any NaN values

# Split skills by '.'
all_skills = skills_text.str.split('.', expand=True).stack()
# Step 3: Normalize skills by removing accents
# Apply unidecode to each skill
normalized_skills = all_skills.apply(lambda skill: unidecode(skill.strip().lower()) if pd.notna(skill) else '')

# Step 4: Get a set of unique skills
unique_skills = set(normalized_skills)
# Step 5: Sort the unique skills in ascending order (A to Z)
sorted_skills = sorted(unique_skills)


# Print the unique skills
print(len(sorted_skills))
print(sorted_skills)
