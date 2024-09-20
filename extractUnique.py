# List of values
values = [
    "marketing and sales", "marketing and sales", "management and manufacturing", "other",
    "management and manufacturing", "marketing and sales", "management and manufacturing", "other",
    "sales and business development", "management and manufacturing", "other", "information technology",
    "management and manufacturing", "sales and business development", "health care provider",
    # ... (list continues)
    "design artcreative and information technology", "general business strategyplanning and marketing",
    "general business strategyplanning and marketing", "other", "management and manufacturing",
    "management and manufacturing", "education and training", "management and manufacturing",
    "health care provider", "customer service", "other", "marketing and sales",
    "customer service and sales", "business development and sales", "sales and management",
    "sales and business development", "sales and business development", "management and manufacturing",
    "education and training", "customer service business development and general business",
    "education and training", "design artcreative and information technology",
    "engineering and information technology", "human resources", "administrative", "administrative"
]

# Extract unique values
unique_values = set(values)

# Convert to a list and sort
unique_values = sorted(unique_values)

# Print unique values
for value in unique_values:
    print(value)