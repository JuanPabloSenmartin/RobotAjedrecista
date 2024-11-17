import cv2 as cv
import numpy as np


# Coordenadas en píxeles (x, y) en la imagen
img_pts = np.array([
    [660.9254, 117.75454 ],  # esquina superior izquierda
    [839.41907, 119.467354 ],  # esquina superior derecha
    [671.10284, 373.83502],  # esquina inferior derecha
    [879.0064, 373.2294]   # esquina inferior izquierda
], dtype="float32")


# Coordenadas reales (x, y) en el sistema del robot (e.g., en centímetros o milímetros)
real_pts = np.array([
    [4, 55],  # esquina superior izquierda
    [-8, 55],  # esquina superior derecha
    [4, 35.8],  # esquina inferior derecha
    [-8, 35.8]   # esquina inferior izquierda
], dtype="float32")

matrix = cv.getPerspectiveTransform(img_pts, real_pts)
print(matrix)

point1 = np.array([[[669.6579, 337.3834]]], dtype="float32")
point2 = np.array([[[843.5678, 147.28915]]], dtype="float32")
point3 = np.array([[[819.543, 236.49738]]], dtype="float32")

transformed_point1 = cv.perspectiveTransform(point1, matrix)
transformed_point2 = cv.perspectiveTransform(point2, matrix)
transformed_point3 = cv.perspectiveTransform(point3, matrix)

print(transformed_point1)
print(transformed_point2)
print(transformed_point3)