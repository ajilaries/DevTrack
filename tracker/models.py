from django.db import models
from django.contrib.auth.models import User


class StudyLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    hours = models.FloatField()

    topic = models.CharField(max_length=100)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic}"