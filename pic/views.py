from deepface import DeepFace
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from pic.models import Image
from .models import Image
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
import os
import subprocess
from django.http import FileResponse
from Docs.models import Doc
from django.http import HttpResponse
from django.shortcuts import render
import cv2
import os
import urllib.parse

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
            print(images[1])
            # Pasar los resultados a la plantilla
            os.remove("pics/imagenes/{}/representations_vgg_face.pkl".format(User.get_username()))
            return render(request, 'home.html', {'image_form': image_form, 'imagenes': mis_imagenes,
                                                  'age': age, 'gender': gender, 'emotion': emotion,
                                                  'img_path': img_url, 'images': images, 'race': race})
        image_form = ImageUploadForm()
        return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )
    return render(request, 'home.html',{'image_form':image_form, 'usuarios':mis_imagenes} )

def super_resolution(request):
    # Obtén la ruta de la imagen desde la solicitud
    image_path = request.GET.get('image_path')
    print(image_path, 'URL que estamos usando.')
    # Carga el modelo y realiza la superresolución
    model_path = 'C:\\Users\\juanz\\Desktop\\PicStrainerProject2\\PicStrainer\\ESPCN_x4.pb'
    print('Acá llegó')
    modelName = model_path.split(os.path.sep)[-1].split("_")[0].lower()
    modelScale = model_path.split("_x")[-1]
    modelScale = 4
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    print('Acá llegó 2')
    sr.readModel(model_path)
    sr.setModel(modelName, modelScale)
    print('Acá llegó 3')
    # Carga la imagen desde la ruta especificada
    new_image_path = 'C:/Users/juanz/Desktop/PicStrainerProject2/PicStrainer'+image_path
    print(new_image_path)
    image = cv2.imread(new_image_path)
    
    if image is None:
        print("Error: No se pudo cargar la imagen desde", image_path)
        return HttpResponseServerError("Error: No se pudo cargar la imagen.")
    print('Acá llegó 4')
    # Realiza la superresolución
    upscaled = sr.upsample(image)
    print('Acá llegó 5')
    bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]),
	interpolation=cv2.INTER_CUBIC)
    print('Acá llegó 6')
    

    # Separa la ruta del archivo y la extensión
    file_path, extension = os.path.splitext(image_path)

    # Añade 'upscaled' antes de la extensión
    output_path = file_path + 'upscaled' + extension

    # Guarda la imagen reescalada
    cv2.imwrite('C:/Users/juanz/Desktop/PicStrainerProject2/PicStrainer'+output_path, bicubic)
    terminal_path = 'C:/Users/juanz/Desktop/PicStrainerProject2/PicStrainer'+output_path
    print('Acá llegó 7')
    new_image = Image.objects.create(
        image='imagenes/{0}/{1}'.format(request.user.username, os.path.basename(terminal_path)),
        user=request.user,
        age = 20,
        gender = 'male',
        emotion = 'happy',
        race = 'latinan hispanic'
        # Añade los valores predeterminados o las demás informaciones que desees almacenar
    )
    # Abre la imagen reescalada y la envía como respuesta
    with open(terminal_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="image/png")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(output_path)
        print('Acá llegó 8')
        return response


def imagen_detalle_generica(request, imagen_url):
    context = {
        'imagen_url': imagen_url,
        # Otros detalles de la imagen que desees mostrar en la página de detalle
    }
    return render(request, 'detalle_imagen_generica.html', context)    
    
def Show_Images(request):
    if request.user.is_authenticated:
        User = request.user
    else:
    # Redirige al usuario a la página de inicio de sesión
        return redirect('loginaccount')
    my_images = Image.objects.filter(user = User)
    image_form = ImageUploadForm(request.POST, request.FILES)
    if request.method == "POST":
    # Obtener las imágenes que quieres mostrar  
        if my_images:
            # Crear una lista de URLs de las imágenes
            urls = [imagen.image.url for imagen in my_images]
    # Enviar la lista al template
            return render(request, "visualization.html", {"images": urls})
        return render(request, 'home.html',{'image_form':image_form,'images':my_images} )
    else:
    # Si no es una petición POST, no mostrar nada
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
    