from django.shortcuts import render, get_object_or_404

from .models import Analysis


def analysis_result(request, analysis_id):

    analysis = get_object_or_404(
        Analysis,
        id=analysis_id
    )

    context = {
        "analysis": analysis
    }

    return render(
        request,
        "analysis/result.html",
        context
    )