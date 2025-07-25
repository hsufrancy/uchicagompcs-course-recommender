import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Load preprocessed course data
df = pd.read_csv('./data/course_preprocessed.csv')
descriptions = df['description'].tolist()

# Load pre-trained model
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
print(f"Loading model: {model_name}")
model = SentenceTransformer(model_name)

# Encode descriptions
print("Encoding descriptions...")
embeddings = model.encode(descriptions, show_progress_bar=True)

# Save embeddings
np.save('./data/course_embeddings.npy', embeddings)
print("Embeddings saved to './data/course_embeddings.npy'")

# Save metadata for index-lookup
df.to_csv('./data/course_metadata.csv', index=False)
print("Metadata saved to './data/course_metadata.csv'")
