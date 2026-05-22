from django.db import models

from apps.resumes.models import Resume


class Analysis(models.Model):

    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE,
        related_name="analysis"
    )

    ats_score = models.IntegerField(
        default=0
    )

    match_score = models.IntegerField(
        default=0
    )

    skills_found = models.JSONField(
        default=list
    )

    missing_skills = models.JSONField(
        default=list
    )

    suggestions = models.JSONField(
        default=list
    )

    analyzed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Analysis - {self.resume.title}"