import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from job_api import fetch_jobs as fetch_adzuna_jobs

# ===============================
# 🔑 JSearch API Key
# ===============================
JSEARCH_API_KEY = "bf89c95dc8mshfe656c9c1b01c68p11ef91jsn28ab05b056c9"
JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"

# ===============================
# Resume Parsing
# ===============================
def extract_text_from_pdf(file):
    import PyPDF2
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + " "
    return text

def extract_text_from_docx(file):
    import docx
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + " "
    return text

# ===============================
# Skills & Career Tips
# ===============================
tips_map = {
    "python": {"resume":"Include Python projects and libraries used (pandas, Flask, NumPy).", "interview":"Prepare Python coding problems and OOP concepts."},
    "machine learning": {"resume":"Add ML models, datasets, results.", "interview":"Prepare ML model evaluation, optimization, deployment questions."},
    "data science": {"resume":"Include data science projects and results.", "interview":"Review ML algorithms, statistics, data preprocessing."},
    "sql": {"resume":"Mention SQL queries or database projects.", "interview":"Practice complex SQL queries."},
    "docker": {"resume":"Include Docker projects or usage.", "interview":"Prepare Docker commands, containerization, deployment."},
    "projects": {"resume":"Add projects section highlighting real-world applications.", "interview":"Be ready to discuss project challenges and learnings."},
    "certifications": {"resume":"Mention relevant certifications.", "interview":"Certifications demonstrate expertise; expect related questions."}
}

SKILL_SYNONYMS = {
    "machine learning":["ml","machine learning"], "data science":["data science","ds"],
    "python":["python"], "sql":["sql","structured query language"], "docker":["docker","containerization"],
    "projects":["project","projects"], "certifications":["certification","certifications"]
}

def missing_skills_and_tips(resume_text, tips_map):
    resume_text_lower = resume_text.lower()
    missing_resume_tips = []
    interview_tips = []
    for skill, synonyms in SKILL_SYNONYMS.items():
        found = any(s in resume_text_lower for s in synonyms)
        if found and tips_map.get(skill) and tips_map[skill].get("interview"):
            interview_tips.append(tips_map[skill]["interview"])
        if not found and tips_map.get(skill) and tips_map[skill].get("resume"):
            missing_resume_tips.append(tips_map[skill]["resume"])
    return missing_resume_tips, interview_tips

# ===============================
# Job Fit & Logo
# ===============================
def calculate_job_fit(resume_text, job_description):
    resume_text_lower = resume_text.lower()
    job_desc_lower = job_description.lower()
    matched_skills = []
    for skill, synonyms in SKILL_SYNONYMS.items():
        if any(s in resume_text_lower for s in synonyms) and any(s in job_desc_lower for s in synonyms):
            matched_skills.append(skill)
    fit_score = len(matched_skills)/len(SKILL_SYNONYMS)*100
    return fit_score, matched_skills

def get_company_logo(company_name):
    return f"https://logo.clearbit.com/{company_name.replace(' ','').lower()}.com"

# ===============================
# Real-Time Jobs
# ===============================
def fetch_jsearch_jobs(query, location="India", num_jobs=5):
    headers = {"x-rapidapi-key": JSEARCH_API_KEY, "x-rapidapi-host": "jsearch.p.rapidapi.com"}
    params = {"query": f"{query} in {location}", "num_pages": 1}
    try:
        response = requests.get(JSEARCH_URL, headers=headers, params=params)
        if response.status_code==200:
            data = response.json().get("data", [])
            return [{"title":j.get("job_title"), "company":j.get("employer_name"), "location":j.get("job_city"), 
                     "description":j.get("job_description"), "url":j.get("job_apply_link"),
                     "employment_type":j.get("job_employment_type",""),
                     "workplace_type":j.get("job_workplace_type",""),
                     "experience_level":j.get("job_experience_level","")
                    } for j in data][:num_jobs]
        return []
    except: return []

# ===============================
# Streamlit UI
# ===============================
st.set_page_config(page_title="💼 AI Job Recommender", layout="wide")
st.title("💼 AI-Powered Job Recommender System")

query_input = st.text_input("🔍 Enter your target role or skills (optional if uploading resume)")
location = st.text_input("📍 Enter location", "India")
num_jobs_display = st.number_input("Number of jobs to display", min_value=5, max_value=50, value=10)
uploaded_file = st.file_uploader("📄 Upload your resume (PDF/DOCX)", type=["pdf","docx"])

# ===============================
# Job Filters
# ===============================
job_types = ["All", "Full-time", "Part-time", "Internship", "Contract"]
remote_options = ["All", "Remote", "On-site", "Hybrid"]
experience_levels = ["All", "Entry", "Mid", "Senior"]

selected_job_type = st.selectbox("Filter by Job Type", job_types)
selected_remote = st.selectbox("Filter by Remote/On-site", remote_options)
selected_experience = st.selectbox("Filter by Experience Level", experience_levels)

# ===============================
if st.button("Recommend Jobs"):
    queries=[]
    resume_text=""
    missing_resume_tips=[]
    interview_tips=[]

    # ---------------- Resume Parsing ----------------
    if uploaded_file:
        if uploaded_file.type=="application/pdf":
            resume_text=extract_text_from_pdf(uploaded_file)
        else:
            resume_text=extract_text_from_docx(uploaded_file)
        missing_resume_tips, interview_tips=missing_skills_and_tips(resume_text, tips_map)
        resume_text_lower=resume_text.lower()
        for skill,synonyms in SKILL_SYNONYMS.items():
            if any(s in resume_text_lower for s in synonyms):
                queries.append(skill)
                
    # ---------------- User input ----------------
    if query_input.strip():
        queries.extend([q.strip() for q in query_input.split(",")])
    queries=list(set(queries))
    if not queries:
        st.warning("Provide role/skills or upload a resume.")
        st.stop()

    # ---------------- Fetch Jobs ----------------
    st.markdown("## 🌐 Real-Time Job Openings")
    all_live_jobs=[]
    for q in queries:
        live_jobs=fetch_adzuna_jobs(q)
        if not live_jobs: live_jobs=fetch_jsearch_jobs(q, location, num_jobs_display)
        all_live_jobs.extend(live_jobs)

    # ---------------- Calculate fit score ----------------
    for job in all_live_jobs:
        if resume_text:
            score,_=calculate_job_fit(resume_text, job['description'])
            job['fit_score']=score
        else:
            job['fit_score']=0

    # ---------------- Apply Filters ----------------
    filtered_jobs = []
    for job in all_live_jobs:
        jt = job.get("employment_type","").title()
        rd = job.get("workplace_type","").title()
        exp = job.get("experience_level","").title()

        if selected_job_type != "All" and jt != selected_job_type:
            continue
        if selected_remote != "All" and rd != selected_remote:
            continue
        if selected_experience != "All" and exp != selected_experience:
            continue
        filtered_jobs.append(job)
    all_live_jobs=sorted(filtered_jobs,key=lambda x:x['fit_score'],reverse=True)

    # ---------------- Display Jobs ----------------
    if all_live_jobs:
        for job in all_live_jobs[:num_jobs_display]:
            fit_score, matched_skills=calculate_job_fit(resume_text, job['description']) if resume_text else (0,[])
            col1,col2=st.columns([5,1])
            with col1:
                st.markdown(f"### {job['title']}")
                st.markdown(f"**🏢 {job['company']} | 📍 {job['location']}**")
                if matched_skills:
                    st.markdown(f"**🟢 Skills matched:** {', '.join(matched_skills)}")
                    st.progress(int(fit_score))
                    st.markdown(f"**📊 Resume Fit Score:** {fit_score:.0f}%")
                with st.expander("Job Description"):
                    st.write(job['description'])
            with col2:
                logo_url=get_company_logo(job['company'])
                st.image(logo_url,width=50)
                st.markdown(f"""
                    <a href="{job['url']}" target="_blank"
                       style="display:block; text-align:center; color:white; 
                              background-color:#0073e6; padding:10px 15px; 
                              border-radius:8px; text-decoration:none; font-weight:bold;">
                        🔗 Apply
                    </a>
                """,unsafe_allow_html=True)
            st.markdown("---")
        st.download_button("📥 Download Jobs as CSV", data=pd.DataFrame(all_live_jobs).to_csv(index=False), file_name="recommended_jobs.csv", mime="text/csv")
    else:
        st.warning("❌ No live jobs found. Try different keywords, filters, or location.")

    # ---------------- Resume Tips & Interview Guides ----------------
    if uploaded_file:
        if missing_resume_tips:
            st.markdown("## 📄 Resume Improvement Suggestions")
            for tip in missing_resume_tips: st.write(f"- {tip}")
        if interview_tips:
            st.markdown("## 📝 Interview Preparation Tips")
            for tip in interview_tips: st.write(f"- {tip}")
