from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from Docs.models import Doc
from .models import Doc
from django.contrib.auth.models import User
import os
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image



#def upload_image(request):
    #mis_imagenes = Image.objects.all()
    #image_form = ImageUploadForm(request.POST, request.FILES)
    #if request.method == 'POST':
        #image_form = ImageUploadForm(request.POST, request.FILES)
        #if image_form.is_valid():
            #image_form.save()
            #return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )
        #return render(request, 'home.html',{'image_form':image_form,'imagenes':mis_imagenes} )
    #else:
        #image_form = ImageUploadForm()
        #return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )

def upload_doc(request):
    if request.user.is_authenticated:
        User = request.user
    else:
    # Redirige al usuario a la página de inicio de sesión
        return redirect('loginaccount')
    my_docs = Doc.objects.filter(user = User)
    doc_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        doc_form = ImageUploadForm(request.POST, request.FILES)
        if doc_form.is_valid():
            # Guardar la imagen en la base de datos
            new_doc = doc_form.save(commit=False)
            new_doc.user = User
            new_doc.save()
            
            # Realizar el reconocimiento de documentos
            
            img_path1 = new_doc.image.path
            image = Image.open(img_path1).convert('RGB')
            processor = AutoImageProcessor.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
            model = AutoModelForImageClassification.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
            
            inputs = processor(images=image, return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_idx = logits.argmax(-1).item()
            type = model.config.id2label[predicted_class_idx]
            new_doc.type = type
            new_doc.save()
            # Pasar los resultados a la plantilla
            img_path1 = new_doc.image.url
            print(img_path1)
            return render(request, 'Docshome.html',{'image_form':doc_form,'img_path':img_path1, 'Docs': my_docs, 'type': type})
        image_form = ImageUploadForm()
        return render(request, 'DocsHome.html',{'image_form':doc_form, 'Docs':my_docs} )
    return render(request, 'DocsHome.html',{'image_form':doc_form, 'Docs':my_docs} )
    
    
def Show_Docs(request):
    if request.user.is_authenticated:
        User = request.user
    else:
    # Redirige al usuario a la página de inicio de sesión
        return redirect('loginaccount')
    my_images = Doc.objects.filter(user = User)
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
    # Obtener las imágenes que quieres mostrar  
        if my_images:
            # Crear una lista de URLs de las imágenes
            urls = [imagen.image.url for imagen in my_images]
    # Enviar la lista al template
            return render(request, "VisualDocs.html", {"images": urls})
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )
    else:
    # Si no es una petición POST, no mostrar nada
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )
    
    

def Return_Home(request):
    User = request.user
    my_images = Doc.objects.filter(user = User)
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )
    else:
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )  

def Start(request):
    return render(request, 'start.html')
#def ShowImage_Deepface(request):
def GoDocs(request):
    User = request.user
    my_Docs = Doc.objects.filter(user = User)
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
        return render(request, 'DocsHome.html',{'image_form':image_form,'images':my_Docs} )
    else:
        return render(request, 'DocsHome.html',{'image_form':image_form,'images':my_Docs} )
    