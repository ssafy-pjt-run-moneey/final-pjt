# runninggame/models.py
from django.db import models
from django.conf import settings

class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answers = models.JSONField()
    result_type = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def calculate_result(self):
        # O는 1, X는 0으로 변환하여 2진수로 계산
        binary = ''
        for q in ['risk', 'time', 'style', 'money']:
            binary += '1' if self.answers.get(q) == 'O' else '0'
        
        # 2진수를 10진수로 변환하여 1을 더함 (1-16 범위로 만들기 위해)
        result = int(binary, 2) + 1
        return result

    def save(self, *args, **kwargs):
        # 결과 계산
        self.result_type = self.calculate_result()
        
        # 사용자의 dog_type 업데이트
        self.user.dog_type = self.result_type
        self.user.save()
        
        super().save(*args, **kwargs)