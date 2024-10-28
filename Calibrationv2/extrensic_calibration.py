import numpy as np
import cv2 as cv
import sys
import yaml

print("""
      EXTRENSIC CALIBRATION  
            
      Usage:
      
      Space: take picture
      C: calibrate with taken picture
      ESC: quit
      """)

ESC = chr(27)
cv.namedWindow("Detecciones", cv.WINDOW_NORMAL)
cv.namedWindow("Cam", cv.WINDOW_NORMAL)
cv.namedWindow("Tablero", cv.WINDOW_NORMAL)
defaultPrintOptions = np.get_printoptions()

chessBoard = (9,6)
gradualDarkness = 0.90
cornersubpixTerminationCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
imgPoints = []
objPoints = []

# chessboard 3D points
chessboardPointCloud3D = np.zeros((chessBoard[0]*chessBoard[1],3), np.float32)
chessboardPointCloud3D[:,:2] = np.mgrid[0:chessBoard[0],0:chessBoard[1]].T.reshape(-1,2)

imChessboard = cv.imread("pattern_chessboard 6 x 9.png")#, flags = cv.IMREAD_GRAYSCALE)
cv.imshow("Tablero", imChessboard) # Opens an empty window?

cam = cv.VideoCapture(0)
width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
print("Cam resolution:", width, " x ", height)
newSize = (640, int(640 * height / width))
imBlack = np.zeros(newSize[::-1]+(3,), dtype=np.uint8)

while True:
    ret, im = cam.read()
    if ret:
        imLowRes = cv.resize(im, newSize)
        imGrayLowRes = cv.cvtColor(imLowRes, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(imGrayLowRes, chessBoard, None)
        
        if ret:
            cv.drawChessboardCorners(imLowRes, chessBoard, corners, ret)
    
    cv.imshow('Cam', imLowRes)

    key = cv.waitKey(33)
    if key>=0:
        key = chr(key)
        print(key)
        if key == ' ':
            # Repite la detección en alta resolución y la registra
            imGray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            ret, precisionCorners = cv.findChessboardCorners(imGray, chessBoard, None)
            if ret:
                precisionCorners = cv.cornerSubPix(imGray, precisionCorners, (11, 11), (-1, -1),
                                                   cornersubpixTerminationCriteria)
                imgPoints.append(precisionCorners)
                objPoints.append(chessboardPointCloud3D)

                # Anota en baja resolución
                imBlack = cv.convertScaleAbs(imBlack, alpha=gradualDarkness, beta=0)
                cv.drawChessboardCorners(imBlack, chessBoard, corners, ret)
                cv.imshow("Detecciones", imBlack)

                print("picture taken")

        elif key == 'c':
            lastObjPoint = []
            lastObjPoint.append(objPoints[len(objPoints)-1])
            lastImgPoint = []
            lastImgPoint.append(imgPoints[len(imgPoints) - 1])
            # Calibra
            ret, K, distCoef, rvecs, tvecs = cv.calibrateCamera(lastObjPoint, lastImgPoint, im.shape[:2][::-1], None, None,
                                                                flags=cv.CALIB_ZERO_TANGENT_DIST)

            # Muestra resultados
            np.set_printoptions(precision=2, suppress=True)
            print("Coeficientes de rotacion:", rvecs)
            print("Coeficientes de tranformacion:", tvecs)
            np.set_printoptions(**defaultPrintOptions)

            output_file = 'parameters/extrinsic_parameters.yaml'
            with open(output_file, 'w') as file:
                yaml.dump({
                    'rvecs': [rvec.tolist() for rvec in rvecs],
                    'tvecs': [tvec.tolist() for tvec in tvecs]
                }, file)
            print(f"Coeficientes de tranformacion y rotacion guardados en {output_file}")

        elif key == ESC:
            print("Terminando.")
            sys.exit()