import cv2 as cv
import numpy as np
import yaml
import os
from datetime import datetime

# Read calibration parameters
def get_calibration_parameters():
    input_file = os.path.join('parameters', 'intrinsic_parameters.yaml')
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)  
    intrinsic_matrix = np.array(data.get('intrinsic_matrix'))
    distortion_coefficients = np.array(data.get('distortion_coefficients'))
    return intrinsic_matrix, distortion_coefficients

# Save image
def save_image(frame, folder='photos'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_name = datetime.now().strftime("photo_%Y%m%d_%H%M%S.png")
    full_path = os.path.join(folder, file_name)
    cv.imwrite(full_path, frame)
    print(f"Image saved at: {full_path}")
    return full_path

image_points = np.zeros((4, 2), dtype="float32")

# Get image coordinates
def get_image_coordinates(saved_corners):
    upper_left_corner = saved_corners[0][0]
    upper_right_corner = saved_corners[6][0]
    lower_left_corner = saved_corners[42][0]
    lower_right_corner = saved_corners[48][0]
    
    image_points = np.array([
        [upper_left_corner[0], upper_left_corner[1]],
        [upper_right_corner[0], upper_right_corner[1]],
        [lower_left_corner[0], lower_left_corner[1]],
        [lower_right_corner[0], lower_right_corner[1]]
    ], dtype="float32")

    print(str(image_points))
    return image_points

# Complete coordinates in robot system
robot_points = np.array([
    [201, -418],
    [210, -119],
    [498, -427],
    [509, -127]
], dtype="float32")

camera = cv.VideoCapture(2)

chessboard_size = (7, 7)

frame_width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)
new_size = (640, int(640 * frame_height / frame_width))

while True:
    ret, frame = camera.read()
    if ret:
        frame_low_res = cv.resize(frame, new_size)
        frame_gray_low_res = cv.cvtColor(frame_low_res, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(frame_gray_low_res, chessboard_size, None)
        if ret:
            cv.drawChessboardCorners(frame_low_res, chessboard_size, corners, ret)
    
    cv.imshow('camera', frame_low_res)

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key)
        match key:
            case ' ':
                intrinsic_matrix, distortion_coefficients = get_calibration_parameters()
                frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                undistorted_image = cv.undistort(frame, intrinsic_matrix, distortion_coefficients)
                ret_2, undistorted_corners = cv.findChessboardCorners(undistorted_image, chessboard_size, None)
                image_points = get_image_coordinates(undistorted_corners)
            case 'm':
                transformation_matrix = cv.getPerspectiveTransform(image_points, robot_points)
                output_file = os.path.join('parameters', 'transformation_matrix.yaml')
                with open(output_file, 'w') as file:
                    yaml.dump({
                        'matrix': transformation_matrix.tolist()
                    }, file)
                print(f"Matrix saved to {output_file}")
            case 'e':
                break

camera.release()
cv.destroyAllWindows()
