from django.db import models

# Create your models here.

import os
from django.db import models

def get_image_path(instance, filename):
    return os.path.join('photos', "1", "Suyash.jpg")

class Photo(models.Model):
    image = models.ImageField(upload_to=get_image_path)
    name = models.CharField(max_length=100)
    count = models.IntegerField(max_length=10)
