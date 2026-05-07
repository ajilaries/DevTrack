
from django.db import models
from django.contrib.auth.models import User

class StudyLog(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    topic=models.CharField(max_length=200)
    hours=models.IntegerField()
    notes=models.TextField()
    date=models.DateField(auto_now_add=True)