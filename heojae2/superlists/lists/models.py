from django.db import models

# Create your models here.

# models.Model 을 상속 해야 이런 .save(), .objects() 같은 함수들을 쓸수 있다


class Item(models.Model):
    text = models.TextField(default='')