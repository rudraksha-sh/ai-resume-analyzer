from django.shortcuts import render

from .forms import JobDescriptionForm

from ai_engine.skill_extraction.extractor import (
    extract_skills
)

from ai_engine.matching.matcher import (
    match_skills
)

from ai_engine.suggestions.generator import (
    generate_suggestions
)

from apps.resumes.models import Resume
from apps.analysis.models import Analysis


def create_job_description(request):

    form = JobDescriptionForm()

    result = None

    if request.method == "POST":

        form = JobDescriptionForm(
            request.POST
        )

        if form.is_valid():

            job = form.save()

            jd_text = job.description

            jd_skills = extract_skills(
                jd_text
            )

            latest_resume = Resume.objects.last()

            latest_analysis = Analysis.objects.get(
                resume=latest_resume
            )

            resume_skills = (
                latest_analysis.skills_found
            )

            result = match_skills(
                resume_skills,
                jd_skills
            )

            suggestions = generate_suggestions(
                result["missing_skills"]
            )

            result["suggestions"] = suggestions

            latest_analysis.match_score = (
                result["match_score"]
            )

            latest_analysis.missing_skills = (
                result["missing_skills"]
            )

            latest_analysis.save()

            latest_analysis.suggestions = (
                suggestions
            )

    context = {

        "form": form,

        "result": result
    }

    return render(
        request,
        "jobs/create_jd.html",
        context
    )