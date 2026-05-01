from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

from .skills import SKILLS_DB

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))  # remove duplicates

from .jobs import JOB_DB

def recommend_jobs(user_skills):
    recommended = []

    for job, skills in JOB_DB.items():
        match_count = 0

        for skill in skills:
            if skill in user_skills:
                match_count += 1

        if match_count > 0:
            match_percent = int((match_count / len(skills)) * 100)
            recommended.append((job, match_percent))

    recommended.sort(key=lambda x: x[1], reverse=True)

    return recommended