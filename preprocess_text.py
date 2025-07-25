import pandas as pd
import os
import re

# Load CSV
data_path = './data/courses.csv'
df = pd.read_csv(data_path)

# Drop duplicates based on title + instructor(s)
df = df.drop_duplicates(subset=['title', 'instructor(s)'])

# Keep only selected columns
keep_cols = [
    'url', 'title', 'course_code', 'instructor(s)', 'fulfills',
    'description', 'other_prerequisites', 'overlapping_classes',
    'eligible_programs', 'course_prerequisites'
]
df = df[[col for col in keep_cols if col in df.columns]]

# Fill missing values with empty string
df.fillna('', inplace=True)

# Basic text cleaner
def clean_text(text):
    text = str(text)
    # text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # remove excessive whitespace
    return text.strip()

# Apply text cleaning
for col in df.columns:
    df[col] = df[col].apply(clean_text)

# Save cleaned output
output_path = './data/course_preprocessed.csv'
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to '{output_path}'")
