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
cv.namedWindow("Detections", cv.WINDOW_NORMAL)
cv.namedWindow("Camera", cv.WINDOW_NORMAL)

default_print_options = np.get_printoptions()

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

chessboard_size = (9, 6)

# Chessboard 3D points
chessboard_point_cloud_3d = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
chessboard_point_cloud_3d[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

image_points = []
object_points = []

gradual_darkness = 0.90

# Set VideoCapture accordingly
camera = cv.VideoCapture(2)

frame_width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)
new_size = (640, int(640 * frame_height / frame_width))
black_image = np.zeros(new_size[::-1] + (3,), dtype=np.uint8)

while True:
    ret, frame = camera.read()
    if ret:
        frame_low_res = cv.resize(frame, new_size)
        frame_gray_low_res = cv.cvtColor(frame_low_res, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(frame_gray_low_res, chessboard_size, None)
        if ret:
            cv.drawChessboardCorners(frame_low_res, chessboard_size, corners, ret)
    
    cv.imshow('Camera', frame_low_res)

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key)
        match key:
            case ' ':
                # Detects and registers chessboard with high resolution
                frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                ret, precision_corners = cv.findChessboardCorners(frame_gray, chessboard_size, None)
                if ret:
                    object_points.append(chessboard_point_cloud_3d)

                    precision_corners = cv.cornerSubPix(frame_gray, precision_corners, (11, 11), (-1, -1), criteria)
                    image_points.append(precision_corners)

                    black_image = cv.convertScaleAbs(black_image, alpha=gradual_darkness, beta=0)
                    cv.drawChessboardCorners(black_image, chessboard_size, corners, ret)
                    cv.imshow("detections", black_image)

                    print(len(image_points), "pictures taken")

            case 'c':
                # Camera calibration
                ret, intrinsic_matrix, distortion_coefficients, rotation_vectors, translation_vectors = cv.calibrateCamera(
                    object_points, image_points, frame.shape[:2][::-1], None, None, flags=cv.CALIB_ZERO_TANGENT_DIST)
                
                # Write intrinsic_matrix and distortion_coefficients to a YAML file
                output_file = os.path.join('parameters', 'intrinsic_parameters.yaml')
                with open(output_file, 'w') as file:
                    yaml.dump({
                        'intrinsic_matrix': intrinsic_matrix.tolist(),
                        'distortion_coefficients': distortion_coefficients.tolist()
                    }, file)
                print(f"Intrinsic matrix and distortion coefficients saved to {output_file}")

            case 'e':
                break

camera.release()
cv.destroyAllWindows()