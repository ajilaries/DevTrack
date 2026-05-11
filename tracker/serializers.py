from rest_framework import serializers

from .models import StudyLog

class StudyLogSerializer(serializers.ModelSerializer):

    class Meta:
        
        model=StudyLog
        fields='__all__'


# serializers framework provides a mechanism for "translating" Django models into other formats
