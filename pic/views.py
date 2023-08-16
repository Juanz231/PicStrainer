from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from pic.models import Image

# Create your views here.

def upload_image(request):
    mis_imagenes = Image.objects.all()
    if request.method == 'POST':
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_form.save()
            return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )
        return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )
    else:
        image_form = ImageUploadForm()
        return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )
    
    
    

