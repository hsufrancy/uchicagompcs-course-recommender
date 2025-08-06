![UChicago Banner](./assets/uchicago_banner)

# 📚 UChicago CS Department Course Recommender

This is a content-based NLP recommendation system for graduate-level courses in the [University of Chicago MPCS Program](https://mpcs-courses.cs.uchicago.edu/). The goal is to help students discover relevant courses based on course descriptions using deep learning and NLP techniques.

Wedsite: [Link](https://uchicagompcs-course-recommender.streamlit.app)

Demo Video: [Link](https://drive.google.com/file/d/1Z4h_SYRyn4K7OF6r8RKA9ASAbQq-yNpf/view?usp=sharing)

---

## 🧠 Project Workflow Overview

### 📌 1. Web Scraping
- Scraped detailed course info from:
  - `https://mpcs-courses.cs.uchicago.edu/2025-26/{quarter}/courses/`
- Extracted fields like:
  - `title`, `description`, `fulfills`, `instructor(s)`, `url`, `prerequisites`, etc.

### 🧹 2. Text Preprocessing
- Dropped duplicate courses based on title & instructor.
- Standardized and cleaned text fields.
- Removed HTML tags, lowercased (except for abbreviations like MA), and stripped whitespace.

### 🔤 3. Text Embedding (4 Models)
We tested four types of embeddings:

| Model | Type | Source | Dim |
|-------|------|--------|-----|
| TF-IDF | Traditional | `sklearn.TfidfVectorizer` | Varies |
| GloVe | Static Word Embedding | `glove-wiki-gigaword-50` | 50 |
| MiniLM | Sentence Transformer | `sentence-transformers/all-MiniLM-L6-v2` | 384 |
| E5-small-v2 | HF Model for Embedding | `intfloat/e5-small-v2` | 384 |

### 🤖 4. Recommendation Logic
- Used **cosine similarity** to recommend top-5 similar courses for any selected course.
- Based on the **course description embeddings**.
- Ensured that a course does **not recommend itself**.

### 📈 5. Model Evaluation

#### Method 1: Objective
- Compared whether recommended courses **share similar “fulfills” tags**.
- Example: both in *Data Analytics* or *Core Programming*.

#### Method 2: Subjective
- Manual check based on domain knowledge to judge whether a student would also be interested in the suggested courses.

---

## 🧪 📊 Evaluation Results

Here’s an example snippet from the objective evaluation for 5 selected courses across 4 models:

| Course Title | Model | Relevant Recommendations (Fulfills Match) |
|--------------|--------|------------------------------|
| NLP | TF-IDF | ✅✅✅❌❌ |
| NLP | GloVe | ✅✅❌❌❌ |
| NLP | MiniLM | ✅✅✅✅❌ |
| NLP | E5 | ✅✅✅✅✅ |

> 📌 *See full evaluation results in [`model_experiment.ipynb`](./model_experiment.ipynb)*

---

## 🌐 6. Final Deployment with Streamlit

We deployed a fully functional UI using **Streamlit**:
- Select a course from dropdown
- Recommend top 5 courses
- Displayed each course with formatted fields (description, instructor, track)
- Clickable title link redirects to official course page

### 🔗 Run Locally

```bash
streamlit run app.py```
