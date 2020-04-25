from django.db import models


class Item(models.Model):
    # Add column attribute
    text = models.TextField(default='')