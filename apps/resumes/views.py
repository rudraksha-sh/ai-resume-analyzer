from django.shortcuts import render, redirect
from apps.analysis.models import Analysis
from .forms import ResumeUploadForm

from ai_engine.parsers.pdf_parser import (
    extract_text_from_pdf
)

from ai_engine.parsers.docx_parser import (
    extract_text_from_docx
)

from ai_engine.preprocessors.text_cleaner import (
    clean_text
)

from ai_engine.skill_extraction.extractor import (
    extract_skills
)

from ai_engine.scoring.ats_score import (
    calculate_ats_score
)

def upload_resume(request):

    form = ResumeUploadForm()

    if request.method == "POST":

        form = ResumeUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save(commit=False)

            resume.user = request.user

            resume.save()

            file_path = resume.resume_file.path

            extracted_text = ""

            if file_path.endswith(".pdf"):

                extracted_text = extract_text_from_pdf(
                    file_path
                )

            elif file_path.endswith(".docx"):

                extracted_text = extract_text_from_docx(
                    file_path
                )

            cleaned_text = clean_text(
                extracted_text
            )

            skills = extract_skills(
                cleaned_text
            )

            print(skills)

            ats_score = calculate_ats_score(
                skills
            )

            print("ATS SCORE:", ats_score)
         
            resume.extracted_text = cleaned_text

            resume.save()

            analysis = Analysis.objects.create(

                resume=resume,

                ats_score=ats_score,

                skills_found=skills,

                missing_skills=[],

                suggestions=[]
            )

            return redirect(
                f"/analysis/{analysis.id}/"
            )

    context = {
        "form": form
    }

    return render(
        request,
        "resumes/upload.html",
        context
    )