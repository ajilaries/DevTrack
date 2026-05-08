
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

# OneToOneField means one user one profile which is good for user profiles, settings and prefernces
class Profile(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE

    )

    bio=models.TextField(
        blank=True
    )
    
    github=models.URLField(
        blank=True
    )
    linkedin=models.URLField(
        blank=True
    )

    ROLE_CHOICES=(
        ('student','Student'),
        ('admin','Admin'),
        ('mentor','Mentor')
    )

    role=models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    def __str__(self):
        return self.user.username
