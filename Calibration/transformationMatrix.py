import cv2 as cv
import numpy as np
import yaml
import os
from datetime import datetime

# Read calibration parameters
def get_calibration_parameters() :
    input_file = os.path.join('parameters', 'intrinsic_parameters.yaml')
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

img_pts = np.zeros((4, 2), dtype="float32")

def get_image_coordinates(saved_corners):

    # Cálculo de las esquinas
    upper_left_corner = saved_corners[0][0]
    upper_right_corner = saved_corners[6][0]
    lower_left_corner = saved_corners[42][0]
    lower_right_corner = saved_corners[48][0]
    
    img_pts = np.array([
        [upper_left_corner[0], upper_left_corner[1]],  # esquina superior izquierda
        [upper_right_corner[0], upper_right_corner[1]],  # esquina superior derecha
        [lower_left_corner[0], lower_left_corner[1]],  # esquina inferior izquierda
        [lower_right_corner[0], lower_right_corner[1]]   # esquina inferior derecha
    ], dtype="float32")

    print(str(img_pts))
    return img_pts

# Coordinates in robot system
robot_pts = np.array([
    [3, 3],  # esquina superior izquierda
    [3, 21],  # esquina superior derecha
    [21, 3],   # esquina inferior izquierda
    [21, 21]  # esquina inferior derecha
], dtype="float32")

# ------------------------- Primary loop ------------------------- #

cam = cv.VideoCapture(1)

chessBoard = (7,7)

width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
newSize = (640, int(640 * height / width))

while True:
    ret, im = cam.read()
    if ret:                                                     # For testing
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
                guardar_imagen(imGray)
                undistorted_img = cv.undistort(im, K, distCoef)
                guardar_imagen(undistorted_img)                 # For testing
                ret_2, undisorted_corners = cv.findChessboardCorners(undistorted_img, chessBoard, None)
                img_pts = get_image_coordinates(undisorted_corners)
            case 'm':
                matrix = cv.getPerspectiveTransform(img_pts, robot_pts)
                # Write K and distCoef to a YAML file
                output_file = os.path.join('parameters', 'transformation_matrix.yaml')
                with open(output_file, 'w') as file:
                    yaml.dump({
                        'matrix': matrix.tolist()
                    }, file)
                print(f"Matrix saved to {output_file}")
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


