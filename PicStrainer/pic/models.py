from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='imagenes')
    date_time = models.DateTimeField(auto_now_add=True)
