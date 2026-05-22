from django.contrib import admin

from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):

    list_display = (
    "id",
    "resume",
    "ats_score",
    "match_score",
    "analyzed_at",
    )   

    list_filter = (
        "ats_score",
    )