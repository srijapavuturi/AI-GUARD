from django.db import models
from django.contrib.auth.models import User


class JobAnalysis(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    job_description = models.TextField()

    risk_score = models.IntegerField()

    risk_level = models.CharField(
        max_length=50
    )

    warning_signs = models.TextField()

    recommendation = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        username = self.user.username if self.user else "Old Record"

        return f"{username} - {self.risk_level} - {self.risk_score}/100"

