from deepface import DeepFace
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from pic.models import Image
from .models import Image
from django.contrib.auth.models import User
import os
from Docs.models import Doc
from crear_busqueda import get_completion
from django.db.models import Q

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
    if request.user.is_authenticated:
        User = request.user
    else:
    # Redirige al usuario a la página de inicio de sesión
        return redirect('loginaccount')
    mis_imagenes = Image.objects.filter(user = User)
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            # Guardar la imagen en la base de datos
            new_image = image_form.save(commit=False)
            new_image.user = User
            new_image.save()
            # Realizar el reconocimiento de rostros
            img_path1 = new_image.image.path
            InDB = DeepFace.find(img_path = img_path1, db_path="pics\imagenes\{}".format(User.get_username()))
            images = InDB[0]["identity"].tolist()
            result = DeepFace.analyze(img_path1)
            # Obtener los resultados del reconocimiento de rostros
            
            age = result[0]["age"]
            gender = result[0]["dominant_gender"]
            emotion = result[0]["dominant_emotion"]
            race = result[0]["dominant_race"]
            
            img_url = new_image.image.url
            new_image.age = int(age)
            new_image.gender = gender
            new_image.emotion = emotion
            new_image.race = race
            
            new_image.save()
            
            images.pop(0)
            # Pasar los resultados a la plantilla
            os.remove("pics/imagenes/{}/representations_vgg_face.pkl".format(User.get_username()))
            return render(request, 'home.html', {'image_form': image_form, 'imagenes': mis_imagenes,
                                                  'age': age, 'gender': gender, 'emotion': emotion,
                                                  'img_path': img_url, 'images': images, 'race': race})
        image_form = ImageUploadForm()
        return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )
    return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )
    
    
def Show_Images(request):
    if request.user.is_authenticated:
        User = request.user
    else:
    # Redirige al usuario a la página de inicio de sesión
        return redirect('loginaccount')
    search_term = request.GET.get('searchPics')
    print("Search Term:", search_term)
    my_images = Image.objects.filter(user = User)
    # Obtener las imágenes que quieres mostrar  
    if my_images:
        print("hola")
        if search_term:
            print("entromagico")
            try:
                consulta = Q(user = User)
                resultado = get_completion(search_term)
                lista_parametros = resultado.split(",")
                if lista_parametros[0] == "null" and lista_parametros[0] != "null":
                    lista_parametros[0] = 0
                    consulta &= Q(age__range=(int(lista_parametros[0]), int(lista_parametros[1])))
                elif lista_parametros[0] != "null" and lista_parametros[0] != "null":
                    consulta &= Q(age__range=(int(lista_parametros[0]), int(lista_parametros[1])))
                if lista_parametros[2] != "null":
                    consulta &= Q(race=lista_parametros[2])
                if lista_parametros[3] != "null":
                    consulta &= Q(emotion=lista_parametros[3])
                if lista_parametros[4] != "null":
                    consulta &= Q(gender=lista_parametros[4])
                my_images = Image.objects.filter(consulta)
                urls = [imagen.image.url for imagen in my_images]
            except:
                urls = [imagen.image.url for imagen in my_images]    
        else:
        # Crear una lista de URLs de las imágenes
            urls = [imagen.image.url for imagen in my_images]
    # Enviar la lista al template
        return render(request, "visualization.html", {'searchTerm':search_term,"images": urls})
    return render(request, 'home.html',{'image_form':image_form,'images':my_images} )

    
    

def Return_Home(request):
    User = request.user
    my_images = Image.objects.filter(user = User)
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )
    else:
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )  

def Start(request):
    return render(request, 'start.html')

def GoDocs(request):
    User = request.user
    my_Docs = Doc.objects.filter(user = User)
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
        return redirect('GoDocs')
    else:
        return redirect('GoDocs')
    