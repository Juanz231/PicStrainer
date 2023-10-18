from django.db import models
from django.contrib.auth.models import User  

class Image(models.Model):
    image = models.ImageField(upload_to='imagenes')
    date_time = models.DateTimeField(auto_now_add=True)