
from pathlib import Path
from typing import List, Set
import re

from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)

def load_skill_vocab(vocab_path: Path) -> Set[str]:
    skills = set()
    with open(vocab_path, "r") as f:
        for line in f:
            s = line.strip().lower()
            if s:
                skills.add(s)
    return skills

def extract_skills(text: str, vocab: Set[str]) -> List[str]:
    t = re.sub(r"[^a-z0-9+\-/#. ]+", " ", text.lower())
    tokens = set([w.strip() for w in t.split() if w.strip()])
    # Match single tokens or n-grams present in vocab
    found = set()
    for skill in vocab:
        if " " in skill:
            if skill in t:
                found.add(skill)
        else:
            if skill in tokens:
                found.add(skill)
    return sorted(found)
