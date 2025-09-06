
import re
import json
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Optional, Dict

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure stopwords
try:
    _ = stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"[\n\r\t]", " ", s)
    s = re.sub(r"[^a-z0-9+#./\- ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def build_corpus_row(row: pd.Series) -> str:
    parts = [
        normalize_text(row.get("title", "")),
        normalize_text(row.get("skills", "")),
        normalize_text(row.get("description", "")),
        normalize_text(row.get("location", "")),
        normalize_text(row.get("company", "")),
    ]
    return " ".join([p for p in parts if p])

def prepare_jobs_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only required columns & fillna
    for col in ["title","company","location","employment_type","experience_level","skills","description"]:
        if col not in df.columns:
            df[col] = ""
    df = df.fillna("")
    df["corpus"] = df.apply(build_corpus_row, axis=1)
    return df

def vectorize_corpus(texts: List[str]) -> Tuple[TfidfVectorizer, any]:
    vectorizer = TfidfVectorizer(
        max_features=50000,
        ngram_range=(1,2),
        stop_words=[w.lower() for w in STOPWORDS]
    )
    X = vectorizer.fit_transform(texts)
    return vectorizer, X

def vectorize_query(vectorizer: TfidfVectorizer, query: str):
    return vectorizer.transform([normalize_text(query)])

def rank_jobs(
    jobs_df: pd.DataFrame,
    query_text: str,
    vectorizer: TfidfVectorizer,
    job_matrix,
    top_n: int = 10,
    filters: Optional[Dict[str, str]] = None
) -> pd.DataFrame:
    q_vec = vectorize_query(vectorizer, query_text)
    sims = cosine_similarity(q_vec, job_matrix).ravel()

    ranked = jobs_df.copy()
    ranked["score"] = sims

    # Apply filters (simple contains match on lowercase text columns)
    if filters:
        for col, val in filters.items():
            if val:
                val = val.lower().strip()
                if col in ranked.columns:
                    ranked = ranked[ranked[col].str.lower().str.contains(val, na=False)]

    ranked = ranked.sort_values("score", ascending=False)
    return ranked.head(top_n)

def load_career_tips(tips_path: Path) -> Dict[str, List[str]]:
    if tips_path.exists():
        with open(tips_path, "r") as f:
            return json.load(f)
    return {}

def tips_for_job(title: str, tips_map: Dict[str, List[str]]) -> List[str]:
    t = title.lower()
    for key, tips in tips_map.items():
        if key in t:
            return tips
    return []

