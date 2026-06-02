from django.db import models

# Memo 클래스는 Django 의 Model 클래스를 상속한다.
class Memo(models.Model): 
    content = models.CharField(max_length=1000, blank=True, null=True)