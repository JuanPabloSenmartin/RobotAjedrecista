import cv2 as cv
import numpy as np
import yaml
import os
from datetime import datetime

# Read calibration parameters
def get_calibration_parameters() :
    input_file = 'intrinsic_parameters.yaml'
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)  
    K = np.array(data.get('K'))
    distCoef = np.array(data.get('distCoef'))
    return K, distCoef

def guardar_imagen(frame, carpeta='fotos'):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre_archivo = datetime.now().strftime("foto_%Y%m%d_%H%M%S.png")
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    cv.imwrite(ruta_completa, frame)
    print(f"Imagen guardada en: {ruta_completa}")
    return ruta_completa

def get_chessboard_corners(saved_corners):

    corner_0 = saved_corners[0][0]
    corner_1 = saved_corners[1][0]
    corner_7 = saved_corners[7][0]

    # Variaciones horizontal y vertical
    h_variation_x = corner_1[0] - corner_0[0]
    h_variation_y = corner_1[1] - corner_0[1]
    v_variation_x = corner_7[0] - corner_0[0]
    v_variation_y = corner_7[1] - corner_0[1]

    h = [h_variation_x, h_variation_y] 
    v = [v_variation_x, v_variation_y]

    # Cálculo de las esquinas
    upper_left_corner = saved_corners[0][0]
    upper_right_corner = saved_corners[6][0]
    lower_left_corner = saved_corners[42][0]
    lower_right_corner = saved_corners[48][0]

    img_pts = np.array([
        [upper_left_corner[0] - h[0] - v[0], upper_left_corner[1] - h[1] - v[1]],  # esquina superior izquierda
        [upper_right_corner[0] + h[0] - v[0], upper_right_corner[1] + h[1] - v[1]],  # esquina superior derecha
        [lower_left_corner[0] - h[0] + v[0], lower_left_corner[1] - h[1] + v[1]],  # esquina inferior izquierda
        [lower_right_corner[0] + h[0] + v[0], lower_right_corner[1] + h[1] + v[1]]   # esquina inferior derecha
    ], dtype="float32")

    return img_pts

# Coordinates in robot system
robot_pts = np.array([
    [4, 55],  # esquina superior izquierda
    [-8, 55],  # esquina superior derecha
    [-8, 35.8],   # esquina inferior izquierda
    [4, 35.8]  # esquina inferior derecha
], dtype="float32")

# ------------------------- Primary loop ------------------------- #

cam = cv.VideoCapture(1)

chessBoard = (7,7)

width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
newSize = (640, int(640 * height / width))

while True:
    ret, im = cam.read()
    if ret:
        imLowRes = cv.resize(im, newSize)
        imGrayLowRes = cv.cvtColor(imLowRes, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(imGrayLowRes, chessBoard, None)
        if ret:
            cv.drawChessboardCorners(imLowRes, chessBoard, corners, ret)
    
    cv.imshow('Cam', imLowRes)

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key)
        match key:
            case ' ':
                K, distCoef = get_calibration_parameters()
                imGray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
                undistorted_img = cv.undistort(im, K, distCoef)
                guardar_imagen(undistorted_img)                 # For debuging
                ret_2, undisorted_corners = cv.findChessboardCorners(undistorted_img, chessBoard, None)
                if ret_2:
                    img_pts = get_chessboard_corners(corners)
            case 'm':
                if img_pts:
                    matrix = cv.getPerspectiveTransform(img_pts, robot_pts)
            case 'e':
                break

cam.release()
cv.destroyAllWindows()


"""
matrix = cv.getPerspectiveTransform(img_pts, robot_pts) # Sacamos la matriz de "transformacion"
print(matrix)

point1 = np.array([[[669.6579, 337.3834]]], dtype="float32")
point2 = np.array([[[843.5678, 147.28915]]], dtype="float32")
point3 = np.array([[[819.543, 236.49738]]], dtype="float32")

transformed_point1 = cv.perspectiveTransform(point1, matrix) # Transformamos los puntos de la imagen al sistema del robot
transformed_point2 = cv.perspectiveTransform(point2, matrix)
transformed_point3 = cv.perspectiveTransform(point3, matrix)
"""


