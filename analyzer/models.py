from django.db import models
from django.utils import timezone

class Resume(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)  # ✅ Fix migration issue
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or self.resume_file.name
