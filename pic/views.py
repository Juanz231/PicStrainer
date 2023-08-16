from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from pic.models import Image

# Create your views here.
'''
def home(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')#redirigue a donde deseas
    else:
        form = DocumentoForm()
    return render(request, 'home.html', {
        'form': form
    })
'''
from django.shortcuts import render
from .models import Image



def upload_image(request):
    mis_imagenes = Image.objects.all()
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_form.save()
            return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )
        return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )
    else:
        image_form = ImageUploadForm()
        return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )
    
def Show_Images(request):
    mis_imagenes = Image.objects.all()
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
    # Obtener las imágenes que quieres mostrar
        imagenes = Image.objects.all()

    # Crear una lista de URLs de las imágenes
        urls = [imagen.image.url for imagen in imagenes]
    # Enviar la lista al template
        return render(request, "visualization.html", {"imagenes": urls})
    else:
    # Si no es una petición POST, no mostrar nada
        return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )

def Return_Home(request):
    mis_imagenes = Image.objects.all()
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
        return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )
    else:
        return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )  
        

