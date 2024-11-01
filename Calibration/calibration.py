import numpy as np
import cv2 as cv
import sys
import yaml

print("""
      Usage:
      Space: take picture
      C: calibrate with taken pictures
      ESC: quit
      """)

ESC = chr(27)
cv.namedWindow("Detecciones", cv.WINDOW_NORMAL)
cv.namedWindow("Cam", cv.WINDOW_NORMAL)
# cv.namedWindow("Tablero", cv.WINDOW_NORMAL) No se para que mostramos el tablero
# imChessboard = cv.imread("pattern_chessboard 6 x 9.png")#, flags = cv.IMREAD_GRAYSCALE)
# cv.imshow("Tablero", imChessboard) # Opens an empty window?

defaultPrintOptions = np.get_printoptions()


criteria  = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

chessBoard = (9,6)
# chessboard 3D points
chessboardPointCloud3D = np.zeros((chessBoard[0]*chessBoard[1],3), np.float32)
chessboardPointCloud3D[:,:2] = np.mgrid[0:chessBoard[0],0:chessBoard[1]].T.reshape(-1,2)

imgPoints = []
objPoints = []

gradualDarkness = 0.90

cam = cv.VideoCapture(0)
# Esto no se para que esta. Creo que es para las Windows que se muestran
width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
print("Cam resolution:", width, " x ", height)
newSize = (640, int(640 * height / width))
imBlack = np.zeros(newSize[::-1]+(3,), dtype=np.uint8)

# hasCalibratedIntrinsic = False --> Vamos a usar todas las fotos. 
# extrensicImgPoints = []
# extrensicObjPoints = []

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

    if key>=0:
        # No se para que imprimimos la key
        key = chr(key)
        # print(key)
        match key:
            case ' ':
                # Repite la detección en alta resolución y la registra
                imGray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
                ret, precisionCorners = cv.findChessboardCorners(imGray, chessBoard, None)
                if ret:
                    objPoints.append(chessboardPointCloud3D)

                    precisionCorners = cv.cornerSubPix(imGray, precisionCorners, (11,11), (-1,-1), criteria)
                    imgPoints.append(precisionCorners)

                    #if (hasCalibratedIntrinsic):
                    #    extrensicImgPoints.append(precisionCorners)
                    #    extrensicObjPoints.append(chessboardPointCloud3D)
                    #else:


                    # Anota en baja resolución. Guarda/dibuja las cornes en una pantalla en negro
                    imBlack = cv.convertScaleAbs(imBlack, alpha=gradualDarkness, beta=0)
                    cv.drawChessboardCorners(imBlack, chessBoard, corners, ret)
                    cv.imshow("Detecciones", imBlack)

                    print(len(imgPoints), "pictures taken")

            case 'c':
                # Calibra                                                                   Porque usamos im.shape[:2][::-1] ?
                ret, K, distCoef, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, im.shape[:2][::-1], None, None, flags=cv.CALIB_ZERO_TANGENT_DIST)

                # Muestra resultados
                np.set_printoptions(precision=2, suppress=True)
                print("Coeficientes de distorsión (K1, K2, P1, P2, K3):", distCoef)
                print("Matriz K", K)
                np.set_printoptions(**defaultPrintOptions)

                # Muestra resultados
                np.set_printoptions(precision=2, suppress=True)
                print("Coeficientes de rotacion:", rvecs)
                print("Coeficientes de tranformacion:", tvecs)
                np.set_printoptions(**defaultPrintOptions)
                
                # Write K and distCoef to a YAML file
                output_file = 'intrinsic_parameters.yaml'
                with open(output_file, 'w') as file:
                    yaml.dump({
                        'K': K.tolist(),
                        'distCoef': distCoef.tolist()
                    }, file)
                print(f"Intrinsic matrix K and distortion coefficients saved to {output_file}")
                hasCalibratedIntrinsic = True

                # Write rvecs and tvecs to YAML file
                output_file = 'extrinsic_parameters.yaml'
                with open(output_file, 'w') as file:
                    yaml.dump({
                        'rvecs': [rvec.tolist() for rvec in rvecs],
                        'tvecs': [tvec.tolist() for tvec in tvecs]
                    }, file)
                print(f"Coeficientes de tranformacion y rotacion guardados en {output_file}")

                #print(precisionCorners)

            case 'e':
                # Sacar puntos 
                print("Undisorted Points")
                undistorted_img = cv.undistort(im, K, distCoef)
                ret, undisortedCorners = cv.findChessboardCorners(undistorted_img, chessBoard, None)
                print(undisortedCorners)