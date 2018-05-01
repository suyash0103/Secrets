from django.db import models

# Create your models here.

class People:
    face = models.FileField()
    name = models.CharField(max_length=100)
