from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import SKILLS

# optional dependency for .docx parsing
try:
    import docx
except ImportError:
    docx = None

import io
import re


def extract_text(file_obj):
    """Extract text from a resume file. Supports PDF, DOCX and plain text.

    The `file_obj` may be an uploaded file-like object from Streamlit, which
    often provides a ``name`` attribute indicating the original filename.
    """
    name = getattr(file_obj, 'name', '') or ''
    name = name.lower()
    text = ""
    if name.endswith('.pdf'):
        reader = PdfReader(file_obj)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    elif name.endswith('.docx') and docx is not None:
        doc = docx.Document(file_obj)
        for para in doc.paragraphs:
            text += para.text + '\n'
    else:
        # fallback: treat as plain text
        try:
            content = file_obj.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            text += content
        except Exception:
            # if the object can't be read, ignore
            pass
    # normalize whitespace and lower
    text = re.sub(r"\s+", " ", text)
    return text.lower()

def extract_skills(text):
    return [skill for skill in SKILLS if skill in text]

def ml_ats_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def skill_gap(resume_skills, jd_skills):
    return list(set(jd_skills) - set(resume_skills))


def summarize_text(text, max_sentences: int = 5):
    """Return a very simple summary of `text` by grabbing the first
    `max_sentences` sentences. Useful for displaying a preview of a resume.
    """
    # naive sentence split
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return ' '.join(sentences[:max_sentences])


def generate_cover_letter(resume_text, jd_text, candidate_name="Candidate"):
    """Create a rudimentary cover letter template using resume and job
    description text. This is not AI-powered but gives a starting point.
    """
    intro = (
        f"Dear Hiring Manager,\n\n"
        f"My name is {candidate_name} and I am excited to apply for the position "
        f"outlined in the job description. With experience and skills such as "
    )
    # pick some keywords from resume
    skills = extract_skills(resume_text)
    if skills:
        intro += ", ".join(skills[:5]) + ". "
    else:
        intro += "[relevant skills] . "
    closing = (
        "\n\nI believe my background makes me a strong match for this role, "
        "and I look forward to the opportunity to discuss further.\n\nSincerely,\n"
        f"{candidate_name}"
    )
    return intro + closing

        