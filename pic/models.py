from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    #8888 Los archivos se subirán a MEDIA_ROOT / user_<id> / <filename>
    return 'imagenes/{0}/{1}'.format(instance.user.username, filename)

class Image(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now = True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=255,null=True)
    emotion = models.CharField(max_length=255,null=True)
    race = models.CharField(max_length=255,null=True)
