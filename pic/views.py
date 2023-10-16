from deepface import DeepFace
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from pic.models import Image
from .models import Image
from django.contrib.auth.models import User
import os
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

def upload_image(request):
    mis_imagenes = Image.objects.all()
    image_form = ImageUploadForm(request.POST, request.FILES)
    urls = [imagen.image.url for imagen in mis_imagenes]
    if request.method == 'POST':
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            # Guardar la imagen en la base de datos
            new_image = image_form.save()

            # Realizar el reconocimiento de rostros
            img_path1 = new_image.image.path
            InDB = DeepFace.find(img_path = img_path1, db_path="pics\imagenes")
            images = InDB[0]["identity"].tolist()
            
            result = DeepFace.analyze(img_path1)
            # Obtener los resultados del reconocimiento de rostros
            
            age = result[0]["age"]
            gender = result[0]["dominant_gender"]
            emotion = result[0]["dominant_emotion"]
            race = result[0]["dominant_race"]
            img_url = new_image.image.url
            images.pop(0)
            # Pasar los resultados a la plantilla
            os.remove("C:/Users/juanz/Desktop/PicStrainerProject/pics/imagenes/representations_vgg_face.pkl")
            return render(request, 'home.html', {'image_form': image_form, 'imagenes': mis_imagenes,
                                                  'age': age, 'gender': gender, 'emotion': emotion,
                                                  'img_path': img_url, 'images': images, 'race': race})
        image_form = ImageUploadForm()
        return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )
    return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )
    
    
def Show_Images(request):
    my_images = Image.objects.all()
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
    # Obtener las imágenes que quieres mostrar
        images = Image.objects.all()

    # Crear una lista de URLs de las imágenes
        urls = [imagen.image.url for imagen in images]
    # Enviar la lista al template
        return render(request, "visualization.html", {"images": urls})
    else:
    # Si no es una petición POST, no mostrar nada
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )
    
    

def Return_Home(request):
    my_images = Image.objects.all()
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )
    else:
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )  
    
# def ShowImage_Deepface(request):
    