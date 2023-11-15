# import the necessary packages
import argparse
import time
from cv2 import *
import cv2
import os

# Ejemplos de ejecución: 
# 1. python super_res_image.py --model models/EDSR_x4.pb --image examples/adrian.png
# 2. python super_res_image.py --model models/ESPCN_x4.pb --image examples/butterfly.png
# 3. python super_res_image.py --model models/FSRCNN_x3.pb --image examples/jurassic_park.png
# 4. python super_res_image.py --model models/LapSRN_x8.pb --image examples/zebra.png

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image we want to increase resolution of")
args = vars(ap.parse_args())

model_path = "PicStrainer\ESPCN_x4.pb"  # Puedes cambiar el modelo según tus necesidades
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
image = cv2.imread(args["image"])
print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))
# use the super resolution model to upscale the image, timing how
# long it takes
start = time.time()
upscaled = sr.upsample(image)
end = time.time()
print("[INFO] super resolution took {:.6f} seconds".format(
	end - start))
# show the spatial dimensions of the super resolution image
print("[INFO] w: {}, h: {}".format(upscaled.shape[1],
	upscaled.shape[0]))

# resize the image using standard bicubic interpolation
start = time.time()
bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]),
	interpolation=cv2.INTER_CUBIC)
end = time.time()
print("[INFO] bicubic interpolation took {:.6f} seconds".format(
	end - start))

# show the original input image, bicubic interpolation image, and
# super resolution deep learning output
# Separa la ruta del archivo y la extensión
file_path, extension = os.path.splitext(args["image"])

# Añade 'upscaled' antes de la extensión
output_path = file_path + 'upscaled' + extension

cv2.imwrite(output_path, bicubic)
