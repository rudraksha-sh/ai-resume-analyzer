from django.contrib import admin
from .models import JobDescription


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "role",
        "company",
        "created_at",
    )

    search_fields = (
        "role",
        "company",
    )