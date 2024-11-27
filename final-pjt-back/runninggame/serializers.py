from rest_framework import serializers
from .models import TestResult

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'answers', 'result_type', 'created_date']