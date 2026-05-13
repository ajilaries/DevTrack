from rest_framework import serializers

from .models import StudyLog

class StudyLogSerializer(serializers.ModelSerializer):

    class Meta:
        
        model=StudyLog
        fields=[
            'id',
            'topic',
            'hours',
            'notes',
            'date'
        ]


# serializers framework provides a mechanism for "translating" Django models into other formats
