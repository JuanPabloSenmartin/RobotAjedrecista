import cv2 as cv
import numpy as np
import yaml
import os

robotMap = {}

def find_center_np(points):
    # Convert input points to a numpy array
    points_np = np.array(points, dtype=np.float32)  # Ensure float32 type

    # Compute the mean (center) of the points
    center = points_np.mean(axis=0)

    # Reshape to (1, 1, 2) for cv.perspectiveTransform compatibility
    return np.array([[[center[0], center[1]]]], dtype=np.float32)

# Read transfomation matrix parameters
def get_transformation_matrix() :
    input_file = os.path.join('parameters', 'transformation_matrix.yaml')
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)  
    matrix = np.array(data.get('matrix'))
    return matrix

def get_calibration_parameters():
    input_file = os.path.join('parameters', 'intrinsic_parameters.yaml')
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)  
    intrinsic_matrix = np.array(data.get('intrinsic_matrix'))
    distortion_coefficients = np.array(data.get('distortion_coefficients'))
    return intrinsic_matrix, distortion_coefficients

def make_virtual_cheesboard(saved_corners): 
    
    pixel_counter = 0

    matrix = get_transformation_matrix()


    corner_0 = saved_corners[0][0]
    corner_1 = saved_corners[1][0]
    corners_7 = saved_corners[7][0]
    h_variation_x = corner_1[0] - corner_0[0]
    h_variation_y = corner_1[1] - corner_0[1]
    y_variation_x = corners_7[0] - corner_0[0]
    y_variation_y = corners_7[1] - corner_0[1]
    h = [h_variation_x, h_variation_y]
    v = [y_variation_x, y_variation_y]

    for i in range(8, 0, -1):
        letter_counter = 1
        if i == 1: 
            pixel_counter = 42
        for j in range(1, 8):                             
            if i == 8 and j == 1:                               # Top Left Corner         
                letter = chr(letter_counter + 64)
                lowerRightCorner = saved_corners[pixel_counter][0]
                squareCorners = [(lowerRightCorner[0] - h[0] - v[0], lowerRightCorner[1] - h[1] - v[1]),     
                                 (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                   
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                 
                                 (lowerRightCorner[0] - h[0], lowerRightCorner[1] - h[1])]                                          
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1

            elif i == 8 and j == 7:                             # Top Right Corner  
                letter = chr(letter_counter + 64)
                lowerRightCorner = saved_corners[pixel_counter][0]
                lowerLeftCorner = saved_corners[pixel_counter - 1][0]
                squareCorners = [(lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                   
                                 (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                  
                                 (lowerRightCorner[0], lowerRightCorner[1]),                               
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                                 
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1

                letter = chr(letter_counter + 64)
                lowerLeftCorner = saved_corners[pixel_counter][0]
                squareCorners = [(lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                   
                                 (lowerLeftCorner[0] + h[0] - v[0], lowerLeftCorner[1] + h[1] - v[1]),     
                                 (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                    
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                                 
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1

            elif i == 1 and j == 1:                             # Bottom Left Corner                                                    
                letter = chr(letter_counter + 64)
                upperRightCorner = saved_corners[pixel_counter][0]
                squareCorners = [(upperRightCorner[0] - h[0], upperRightCorner[1] - h[1]),                  
                                 (upperRightCorner[0], upperRightCorner[1]),                                
                                 (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),                  
                                 (upperRightCorner[0] - h[0] + v[0], upperRightCorner[1] - h[1] + v[1])]                  
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]
                
                letter_counter += 1
                pixel_counter += 1

            elif i == 1 and j == 7:                             # Bottom Right Corner
                letter = chr(letter_counter + 64)
                upperRightCorner = saved_corners[pixel_counter][0]
                upperLeftCorner = saved_corners[pixel_counter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                   
                                 (upperRightCorner[0], upperRightCorner[1]),                  
                                 (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),                                
                                 (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])]                                                        
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1

                letter = chr(letter_counter + 64)
                upperLeftCorner = saved_corners[pixel_counter][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  
                                 (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                    
                                 (upperLeftCorner[0] + h[0] + v[0], upperLeftCorner[1] + h[1] + v[1]),     
                                 (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])]                                 
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1    

            elif i == 8:                                        # Top Side  
                letter = chr(letter_counter + 64)
                lowerRightCorner = saved_corners[pixel_counter][0]
                lowerLeftCorner = saved_corners[pixel_counter - 1][0]
                squareCorners = [(lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    
                                 (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                
                                 (lowerRightCorner[0], lowerRightCorner[1]),                               
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                                 
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1

            elif j == 1:                                        # Left Side
                letter = chr(letter_counter + 64)
                lowerRightCorner = saved_corners[pixel_counter][0]
                upperRightCorner = saved_corners[pixel_counter - 7][0]
                squareCorners = [(upperRightCorner[0] - h[0], upperRightCorner[1] - h[1]),                 
                                 (upperRightCorner[0], upperRightCorner[1]),                                
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                 
                                 (lowerRightCorner[0] - h[0], lowerRightCorner[1] - h[1])]                                
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1

            elif j == 7:                                        # Right Side 
                letter = chr(letter_counter + 64)
                upperLeftCorner = saved_corners[pixel_counter - 8][0]
                upperRightCorner = saved_corners[pixel_counter - 7][0]
                lowerRightCorner = saved_corners[pixel_counter][0]
                lowerLeftCorner = saved_corners[pixel_counter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  
                                 (upperRightCorner[0], upperRightCorner[1]),                                
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                               
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                
                letter = chr(letter_counter + 64)
                upperLeftCorner = saved_corners[pixel_counter][0]
                lowerLeftCorner = saved_corners[pixel_counter - 7][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                
                                 (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                 
                                 (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                                       
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1

            elif i == 1:                                        # Bottom Side
                letter = chr(letter_counter + 64)
                upperRightCorner = saved_corners[pixel_counter][0]
                upperLeftCorner = saved_corners[pixel_counter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                  
                                 (upperRightCorner[0], upperRightCorner[1]),               
                                 (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),                                
                                 (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])]                                                       
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1

            else:                                               # Inner Squares
                letter = chr(letter_counter + 64)
                upperLeftCorner = saved_corners[pixel_counter - 8][0]
                upperRightCorner = saved_corners[pixel_counter - 7][0]
                lowerRightCorner = saved_corners[pixel_counter][0]
                lowerLeftCorner = saved_corners[pixel_counter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                 
                                 (upperRightCorner[0], upperRightCorner[1]),                                
                                 (lowerRightCorner[0], lowerRightCorner[1]),                               
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                                     
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                letter_counter += 1
                pixel_counter += 1


    return robotMap 

cv.namedWindow("Cam", cv.WINDOW_NORMAL)
#cv.namedWindow("Cam1", cv.WINDOW_NORMAL)
cv.namedWindow("Cam2", cv.WINDOW_NORMAL)

chessboard_size = (7,7)
cam = cv.VideoCapture(2)

width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
new_size = (640, int(640 * height / width))

while True:
    ret, im = cam.read()
    if ret:
        frame_low_res = cv.resize(im, new_size)
        frame_gray_low_res = cv.cvtColor(frame_low_res, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(frame_gray_low_res, chessboard_size, None)
        if ret:
            cv.drawChessboardCorners(frame_low_res, chessboard_size, corners, ret)


        cv.imshow('Cam', frame_low_res)
       

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key)
        match key:
            case ' ':  # Capture corners and create dictionary
                K, distCoef = get_calibration_parameters()
                undistorted_img = cv.undistort(im, K, distCoef)
                ret_2, undisorted_corners = cv.findChessboardCorners(undistorted_img, chessboard_size, None)
                robotMap = make_virtual_cheesboard(undisorted_corners)

                output_file = os.path.join('parameters', 'map.yaml')
                serializable_data = {key: value.tolist() for key, value in robotMap.items()}
                with open(output_file, 'w') as file:
                    yaml.dump(serializable_data, file, default_flow_style=False)


            case "e":  # Exit loop
                break
            
