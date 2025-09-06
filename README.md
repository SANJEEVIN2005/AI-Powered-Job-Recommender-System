

# 💼 AI-Powered Job Recommender

A smart and demo-ready system that recommends **live job openings, interview guides, and resume tips** based on a candidate’s skills or uploaded resume.

---

## 🚀 Features

* **Live Job Fetching** → Fetches real-time jobs from **Adzuna API** (fallback: JSearch API via RapidAPI).
* **Resume-Aware Job Matching** → Upload a PDF resume; system extracts skills and tailors recommendations.
* **Smart Recommendations** → Matches user skills/queries with live job openings.
* **Career Guidance** → Provides contextual **interview tips & resume improvement suggestions**, highlighting missing skills.
* **Streamlit UI** → Clean, interactive interface for quick demo.

---

## ⚡ Quickstart

```bash
# 1) Create virtual environment (optional)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
streamlit run app.py
```

Open the local URL shown in the terminal. 🎉

---

## 🔑 API Keys Setup

* **Adzuna API** → Required for fetching live jobs.
* **JSearch API (RapidAPI)** → Used as a fallback if Adzuna returns no results.

Add your keys directly in `app.py`:

```python
ADZUNA_APP_ID = "your_app_id"
ADZUNA_APP_KEY = "your_app_key"

JSEARCH_API_KEY = "your_rapidapi_key"
```

---

## 🏗 Project Structure

```
job_recommender/
│── app.py               # Streamlit app (main entry)
│── job_api.py           # API calls to Adzuna & JSearch
│── recommender.py       # Ranking + career guidance logic
│── resume_parser.py     # Resume parsing & skill extraction
│── requirements.txt     # Dependencies
│
├── assets/
│   ├── career_tips.json # Role-specific interview & resume tips
│   └── skills_vocab.txt # Skills vocabulary for parsing
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push this folder to a **GitHub repo**.
2. In Streamlit Cloud, create a new app → point to `app.py`.
3. Add your **API keys** under `Secrets` in Streamlit settings.

---

## 🔮 Future Enhancements

* Replace TF-IDF matching with **Sentence-BERT embeddings** for semantic similarity.
* Add **collaborative filtering** (learn from user clicks/applies).
* Expand to multiple job APIs (LinkedIn, Indeed, Naukri).
* Persist user profiles & feedback using a database.
* Smarter **resume feedback** (quantify skill gaps, ATS scoring).


