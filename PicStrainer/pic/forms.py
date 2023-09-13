from pic.models import Image
from django import forms

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    
def ingresar_image(self):
    nueva_imagen = Image(image= self.data('image'))
    nueva_imagen.save()
    return 'ingreso exitoso'
