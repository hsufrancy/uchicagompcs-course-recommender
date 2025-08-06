import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import string

# Load data
metadata = pd.read_csv('./data/course_preprocessed.csv')
embeddings = np.load('./data/embeddings_e5.npy')

# Title
st.set_page_config(page_title="UChicago Course Recommender", layout="wide")
st.title("🦅🔎 UChicago CS Department Course Recommender")

# Course dropdown
course_titles = metadata['title'].drop_duplicates().tolist()
selected_title = st.selectbox("Select a course title:", course_titles)

# Recommendation logic
def recommend(title, top_k=5):
    matches = metadata[metadata['title'].str.lower() == title.lower()]
    if matches.empty:
        return []
    idx = matches.index[0]
    query_vec = embeddings[idx].reshape(1, -1)
    sims = cosine_similarity(query_vec, embeddings)[0]
    sorted_idx = np.argsort(sims)[::-1]
    top_idx = [i for i in sorted_idx if i != idx][:top_k]
    return metadata.iloc[top_idx]

# Show recommendations
if st.button("Recommend 5 Courses"):
    results = recommend(selected_title)
    st.markdown("---")
    st.markdown("⬇️ **Click the course titles to see detail information.**")
    st.markdown("")

    for _, row in results.iterrows():
        # Generate title as a hyperlink
        course_title = string.capwords(row['title'])
        course_url = row['url']
        st.markdown(f"### [{course_title}]({course_url})")

        # Prepare display content without 'title', 'description', 'url'
        display_row = row.drop(['title', 'description', 'url'])
        display_data = []
        for field, value in display_row.items():
            formatted_field = string.capwords(field.replace('_', ' '))
            formatted_value = str(value).strip()
            display_data.append([formatted_field, formatted_value])

        # Render clean 7×2 table without index or headers
        st.write(
            f'<table style="width:100%;border-collapse:collapse;font-size:14px;">' +
            ''.join([
                f'<tr><td style="padding:6px 12px;border:1px solid #ccc;font-weight:600;">{row[0]}</td>' +
                f'<td style="padding:6px 12px;border:1px solid #ccc;">{row[1]}</td></tr>'
                for row in display_data
            ]) +
            '</table>',
            unsafe_allow_html=True
        )
