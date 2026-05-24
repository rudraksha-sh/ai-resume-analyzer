from django.urls import path

from .views import analysis_result


urlpatterns = [

    path(
        "<int:analysis_id>/",
        analysis_result,
        name="analysis_result"
    ),
]