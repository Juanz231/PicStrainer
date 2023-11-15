import time
from cv2 import *
import cv2
import os

# Especifica la ruta del modelo y la imagen que deseas usar
model_path = "PicStrainer\ESPCN_x4.pb"  # Puedes cambiar el modelo según tus necesidades
image_path = "PicStrainer\pics\imagenes\Juanz2314\OIF.jpeg"  # Puedes cambiar la imagen según tus necesidades

# extract the model name and model scale from the file path
modelName = model_path.split(os.path.sep)[-1].split("_")[0].lower()
modelScale = model_path.split("_x")[-1]
modelScale = 4

# initialize OpenCV's super resolution DNN object, load the super
# resolution model from disk, and set the model name and scale
print("[INFO] loading super resolution model: {}".format(model_path))
print("[INFO] model name: {}".format(modelName))
print("[INFO] model scale: {}".format(modelScale))
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(model_path)
sr.setModel(modelName, modelScale)

# load the input image from disk and display its spatial dimensions
image = cv2.imread(image_path)

print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))

# use the super resolution model to upscale the image, timing how
# long it takes
start = time.time()
upscaled = sr.upsample(image)
end = time.time()
print("[INFO] super resolution took {:.6f} seconds".format(end - start))

# show the spatial dimensions of the super resolution image
print("[INFO] w: {}, h: {}".format(upscaled.shape[1], upscaled.shape[0]))

# resize the image using standard bicubic interpolation
start = time.time()
bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]),
                    interpolation=cv2.INTER_CUBIC)
end = time.time()
print("[INFO] bicubic interpolation took {:.6f} seconds".format(end - start))

output_path = "PicStrainer\pics\imagenes\Juanz2314\OIFUpscaled2.jpg"
cv2.imwrite(output_path, bicubic)
