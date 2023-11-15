from Docs.models import Doc
from django import forms

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Doc
        fields = ['image']
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    
def ingresar_image(self):
    nueva_imagen = Doc(image= self.data('image'))
    nueva_imagen.save()
    return 'ingreso exitoso'