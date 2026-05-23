from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import (
    login,
    logout
)

from django.contrib.auth.forms import (
    AuthenticationForm
)

from django.contrib.auth.decorators import (
    login_required
)

from .forms import SignupForm

from apps.resumes.models import Resume

from apps.analysis.models import Analysis

import json

def signup_view(request):

    form = SignupForm()

    if request.method == "POST":

        form = SignupForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect("/")

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/signup.html",
        context
    )


def login_view(request):

    form = AuthenticationForm()

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect("/")

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/login.html",
        context
    )


def logout_view(request):

    logout(request)

    return redirect("/")



@login_required
def dashboard_view(request):

    resumes = Resume.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    analyses = Analysis.objects.filter(
        resume__user=request.user
    ).order_by("-analyzed_at")

    ats_scores = []

    match_scores = []

    semantic_scores = []

    labels = []

    for analysis in analyses:

        ats_scores.append(
            analysis.ats_score
        )

        match_scores.append(
            analysis.match_score
        )

        semantic_scores.append(
            analysis.semantic_score
        )

        labels.append(
            f"Resume {analysis.resume.id}"
        )

    context = {

        "resumes": resumes,

        "analyses": analyses,

        "context_labels": json.dumps(labels),

        "ats_scores": json.dumps(ats_scores),

        "match_scores": json.dumps(match_scores),

        "semantic_scores": json.dumps(semantic_scores),
    }

    return render(
        request,
        "accounts/dashboard.html",
        context
    )