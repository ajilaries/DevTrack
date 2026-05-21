
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

    profile_picture=models.ImageField(
        upload_to='profile_picture',
        default='default.png'
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
    
class Notification(models.Model):

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'

    )
    message=models.CharField(
        max_length=225,
        blank=False

    )
    is_read=models.BooleanField(
        default=False
    )
    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message
