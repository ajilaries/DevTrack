
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
    xp=models.IntegerField(default=0)
    level=models.IntegerField(default=1)
    badges=models.JSONField(default=list, blank=True)

    def update_level(self):
        self.level=(self.xp//100)+1
        self.save()

    def __str__(self):
        return self.user.username
    
    def check_badges(self):
        badges=self.badges or []

        if self.xp>= 100  and "Beginner" not in badges:
            badges.append("Beginner")
        
        if self.xp>=500 and "Focused Learner" not in badges:
            badges.append("Focused Learner")
        
        if self.xp>=1000 and "Study Master" not in badges:
            badges.append("Study Master")

        self.badges=badges
        self.save()

        
    
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

# Pomodoro model

class PomodoroSession(models.Model):

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    duration=models.IntegerField(
        help_text="Duration in minutes"
    )
    completed_at=models.DateTimeField(
        auto_now_add=True

    )
    mode=models.CharField(
        max_length=20,
        default="Focus"
    )
    xp_earned=models.IntegerField(
        default=10
    )

    def __str__(self):
        return f"{self.user.username}-{self.duration} mins"