
# Recruitment Content Recommender (Static, Streamlit)

A fast, demo-ready system that recommends jobs plus interview/resume tips based on a candidate's skills or resume.

## Features
- TF-IDF + cosine similarity job matching
- Manual skills input or PDF resume parsing
- Contextual interview & resume tips by role
- Simple filters (location, role, experience, employment type)
- Streamlit UI for quick demo

## Quickstart

```bash
# 1) Create venv (optional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run app
streamlit run app.py
```

Open the local URL printed in the terminal.

## Data
The sample dataset lives at `data/jobs_sample.csv`. Replace with a larger CSV keeping columns:

```
job_id,title,company,location,employment_type,experience_level,skills,description
```

## Replace dataset
- Ensure **UTF-8** CSV
- Add as many rows as you like
- The app will automatically re-index on first load

## Deploy (Streamlit Cloud)
1. Push this folder to a GitHub repo
2. In Streamlit Cloud, create new app → point to `app.py`
3. Add secrets only if needed (not required for this static demo)

## Project Structure
```
job_recommender/
  app.py
  recommender.py
  resume_parser.py
  requirements.txt
  data/
    jobs_sample.csv
  assets/
    career_tips.json
    skills_vocab.txt
```

## Extend (after demo)
- Swap TF-IDF with Sentence-BERT embeddings
- Add collaborative filtering from click/apply logs
- Connect to a live job feed (scrapers/APIs) and filter by posted date
- Persist user profiles & feedback in a DB
```

