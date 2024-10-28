import numpy as np
import cv2 as cv

# Tu vector de rotación
vector = np.array([[-0.86], [0.05], [-0.02]])

# Convertir el vector de rotación en una matriz de rotación
rotation_matrix, _ = cv.Rodrigues(vector)

print(rotation_matrix)