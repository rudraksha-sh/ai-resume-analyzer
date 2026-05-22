from django.urls import path

from .views import create_job_description


urlpatterns = [

    path(
        "create/",
        create_job_description,
        name="create_jd"
    ),
]