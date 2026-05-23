from django.shortcuts import (
    render,
    redirect
)

from .forms import JobDescriptionForm

from ai_engine.skill_extraction.extractor import (
    extract_skills
)

from ai_engine.matching.matcher import (
    match_skills
)

from ai_engine.matching.semantic_matcher import (
    semantic_match
)

from ai_engine.suggestions.generator import (
    generate_suggestions
)

from apps.resumes.models import Resume
from apps.analysis.models import Analysis


def create_job_description(request):

    form = JobDescriptionForm()

    resume_id = request.GET.get(
        "resume_id"
    )

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

            resume = Resume.objects.get(
                id=resume_id
            )

            analysis = Analysis.objects.get(
                resume=resume
            )

            resume_skills = (
                analysis.skills_found
            )

            result = match_skills(
                resume_skills,
                jd_skills
            )

            suggestions = generate_suggestions(
                result["missing_skills"]
            )

            analysis.match_score = (
                result["match_score"]
            )

            analysis.missing_skills = (
                result["missing_skills"]
            )

            analysis.suggestions = (
                suggestions
            )

            analysis.save()

            return redirect(
                f"/analysis/{analysis.id}/"
            )

    context = {
        "form": form
    }

    return render(
        request,
        "jobs/create_jd.html",
        context
    )