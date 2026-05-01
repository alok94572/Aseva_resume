import os
from django.shortcuts import render
from .forms import ResumeForm
from .models import Resume
from .utils import extract_text_from_pdf, extract_text_from_docx, extract_skills, recommend_jobs

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            file_path = resume.resume_file.path

            # Detect file type and extract text
            if file_path.endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                text = extract_text_from_docx(file_path)
            else:
                text = "Unsupported file format"

            # ✅ Error handling for empty file
            if not text.strip():
                text = "No readable content found"

            # Save extracted text
            resume.extracted_text = text

            # Extract skills and save permanently
            skills = extract_skills(text)
            resume.skills = ", ".join(skills)
            resume.save()

            # Recommend jobs with match percentage
            jobs = recommend_jobs(skills)

            # Pass everything to template
            return render(request, 'success.html', {
                'resume_text': text,
                'resume_name': resume.resume_file.name,
                'skills': skills,
                'jobs': jobs
            })
    else:
        form = ResumeForm()

    return render(request, 'upload.html', {'form': form})
