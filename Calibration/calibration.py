import numpy as np
import cv2 as cv
import yaml
import os

print("""
      Usage:
      Space: take picture
      C: calibrate with taken pictures
      ESC: quit
      """)

ESC = chr(27)
cv.namedWindow("Detecciones", cv.WINDOW_NORMAL)
cv.namedWindow("Cam", cv.WINDOW_NORMAL)

defaultPrintOptions = np.get_printoptions()

criteria  = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

chessBoard = (9,6)

# chessboard 3D points
chessboardPointCloud3D = np.zeros((chessBoard[0]*chessBoard[1],3), np.float32)             
chessboardPointCloud3D[:,:2] = np.mgrid[0:chessBoard[0],0:chessBoard[1]].T.reshape(-1,2)

imgPoints = []
objPoints = []

gradualDarkness = 0.90

cam = cv.VideoCapture(1)

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

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key)
        match key:
            case ' ':
                # Repeats and registers detection with high resolution
                imGray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
                ret, precisionCorners = cv.findChessboardCorners(imGray, chessBoard, None)
                if ret:
                    objPoints.append(chessboardPointCloud3D)

                    precisionCorners = cv.cornerSubPix(imGray, precisionCorners, (11,11), (-1,-1), criteria)
                    imgPoints.append(precisionCorners)

                    imBlack = cv.convertScaleAbs(imBlack, alpha=gradualDarkness, beta=0)
                    cv.drawChessboardCorners(imBlack, chessBoard, corners, ret)
                    cv.imshow("Detecciones", imBlack)

                    print(len(imgPoints), "pictures taken")

            case 'c':
                # Calibrates   
                ret, K, distCoef, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, im.shape[:2][::-1], None, None, flags=cv.CALIB_ZERO_TANGENT_DIST)
                
                # Write K and distCoef to a YAML file
                output_file = os.path.join('parameters', 'intrinsic_parameters.yaml')
                # output_file = 'intrinsic_parameters.yaml'
                with open(output_file, 'w') as file:
                    yaml.dump({
                        'K': K.tolist(),
                        'distCoef': distCoef.tolist()
                    }, file)
                print(f"Intrinsic matrix K and distortion coefficients saved to {output_file}")

            case 'e':
                break

cam.release()
cv.destroyAllWindows()