

#  AI-Powered Job Recommender

A smart and demo-ready system that recommends **job links, interview guides, and resume tips** based on a candidate’s **skills or uploaded resume**.

---

## 🚀 Features

* **Resume-Aware Job Matching** → Parse PDF resumes and extract skills
* **Smart Job Recommendations** → TF-IDF + cosine similarity matching
* **Career Guidance** → Contextual interview tips & resume improvement suggestions
* **Filters** → Location, role, experience, and employment type
* **Streamlit UI** → Interactive web interface for quick demo

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

## 📂 Data

The sample dataset is located at:

```
data/jobs_sample.csv
```

Required columns:

```
job_id,title,company,location,employment_type,experience_level,skills,description
```

🔹 Replace with a larger **UTF-8 CSV** for real-world testing.
🔹 The system will auto re-index jobs on first load.



## 🌐 Deployment (Streamlit Cloud)

1. Push this folder to a GitHub repository
2. In **Streamlit Cloud**, create a new app → point to `app.py`
3. (Optional) Add API keys or secrets in Streamlit settings



## 🏗 Project Structure

```
job_recommender/
│── app.py                # Streamlit UI
│── recommender.py         # Job ranking logic
│── resume_parser.py       # Resume parsing & skill extraction
│── requirements.txt       # Dependencies
│
├── data/
│   └── jobs_sample.csv    # Sample job dataset
│
├── assets/
│   ├── career_tips.json   # Interview & resume tips
│   └── skills_vocab.txt   # Skill keywords
```


## 🔮 Future Enhancements

* Replace TF-IDF with **Sentence-BERT embeddings** for semantic matching
* Add **collaborative filtering** from user clicks/applications
* Integrate **live job feeds** via APIs (LinkedIn, Indeed, etc.)
* Store **user profiles & feedback** in a database

✨ **CareerLink helps candidates not just find jobs, but also prepare for them.**
