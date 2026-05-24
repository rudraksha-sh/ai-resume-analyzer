from django.db import models


class JobDescription(models.Model):

    role = models.CharField(max_length=255)

    company = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.role