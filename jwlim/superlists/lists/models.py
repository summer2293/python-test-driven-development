from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    # Add column attribute
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
