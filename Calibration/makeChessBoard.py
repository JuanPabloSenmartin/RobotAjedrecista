import cv2 as cv
import numpy as np
import yaml
import os

chessBoard = {} # key: Casillero, value: [[coordinadas sistema del robot], [nombre de la pieza]]
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

def get_calibration_parameters() :
    input_file = os.path.join('parameters', 'intrinsic_parameters.yaml')
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)  
    K = np.array(data.get('K'))
    distCoef = np.array(data.get('distCoef'))
    return K, distCoef

def makeChessBoard(saved_corners): 
    
    pixelCounter = 0

    matrix = get_transformation_matrix()


    corner0 = saved_corners[0][0]
    corner1 = saved_corners[1][0]
    corners7 = saved_corners[7][0]
    hVariationX = corner1[0] - corner0[0]
    hVariationY = corner1[1] - corner0[1]
    yVariationX = corners7[0] - corner0[0]
    yVariationY = corners7[1] - corner0[1]
    h = [hVariationX, hVariationY]    # Variacion en [x, y]
    v = [yVariationX, yVariationY]

    print("variation: " + str(h))
    print("variation: " + str(v))

    for i in range(8, 0, -1):
        #print(i)
        letterCounter = 1
        if i == 1: 
            pixelCounter = 42
        for j in range(1, 8):                             
            if i == 8 and j == 1:                               # Esquina superior izquierda  # [superio izq, superior der, inferior der, inferior izq]          
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                squareCorners = [(lowerRightCorner[0] - h[0] - v[0], lowerRightCorner[1] - h[1] - v[1]),    # Esquina superior izq 
                                 (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                  # Esquina superior der 
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                # Esquina inferior der 
                                 (lowerRightCorner[0] - h[0], lowerRightCorner[1] - h[1])]                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1
            elif i == 8 and j == 7:                             # Esquina superior derecha  # [superio izq, superior der, inferior der, inferior izq]  
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [(lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    # Esquina superior izq 
                                 (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                  # Esquina superior der 
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1

                letter = chr(letterCounter + 64)
                lowerLeftCorner = saved_corners[pixelCounter][0]
                squareCorners = [(lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    # Esquina superior izq 
                                 (lowerLeftCorner[0] + h[0] - v[0], lowerLeftCorner[1] + h[1] - v[1]),      # Esquina superior der 
                                 (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                    # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1
            elif i == 1 and j == 1:                             # Esquina inferior izquierda  # [superio izq, superior der, inferior der, inferior izq]                                                    
                letter = chr(letterCounter + 64)
                upperRightCorner = saved_corners[pixelCounter][0]
                squareCorners = [(upperRightCorner[0] - h[0], upperRightCorner[1] - h[1]),                  # Esquina superior izq 
                                 (upperRightCorner[0], upperRightCorner[1]),                                # Esquina superior der 
                                 (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),                  # Esquina inferior der 
                                 (upperRightCorner[0] - h[0] + v[0], upperRightCorner[1] - h[1] + v[1])]    # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]
                
                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1
            elif i == 1 and j == 7:                             # Esquina inferior derecha  # [superio izq, superior der, inferior der, inferior izq] 
                letter = chr(letterCounter + 64)
                upperRightCorner = saved_corners[pixelCounter][0]
                upperLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                    # Esquina superior izq 
                                 (upperRightCorner[0], upperRightCorner[1]),                  # Esquina superior der 
                                 (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),                                # Esquina inferior der 
                                 (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1

                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  # Esquina superior izq 
                                 (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                    # Esquina superior der 
                                 (upperLeftCorner[0] + h[0] + v[0], upperLeftCorner[1] + h[1] + v[1]),      # Esquina inferior der 
                                 (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])]                    # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1    
            elif i == 8:                                        # Lado de arriba  # [superio izq, superior der, inferior der, inferior izq]  
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [(lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    # Esquina superior izq 
                                 (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                  # Esquina superior der 
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1
            elif j == 1:                                        # Lado de la izquierda  # [superio izq, superior der, inferior der, inferior izq]  
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                upperRightCorner = saved_corners[pixelCounter - 7][0]
                squareCorners = [(upperRightCorner[0] - h[0], upperRightCorner[1] - h[1]),                  # Esquina superior izq 
                                 (upperRightCorner[0], upperRightCorner[1]),                                # Esquina superior der 
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                 # Esquina inferior der 
                                 (lowerRightCorner[0] - h[0], lowerRightCorner[1] - h[1])]                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1
            elif j == 7:                                        # Lado de la derecha  # [superio izq, superior der, inferior der, inferior izq]
                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter - 8][0]
                upperRightCorner = saved_corners[pixelCounter - 7][0]
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  # Esquina superior izq 
                                 (upperRightCorner[0], upperRightCorner[1]),                                 # Esquina superior der 
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                
                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 7][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  # Esquina superior izq 
                                 (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                    # Esquina superior der 
                                 (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                    # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1
            elif i == 1:                                        # Lado de abajo  # [superio izq, superior der, inferior der, inferior izq]
                letter = chr(letterCounter + 64)
                upperRightCorner = saved_corners[pixelCounter][0]
                upperLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                    # Esquina superior izq 
                                 (upperRightCorner[0], upperRightCorner[1]),                  # Esquina superior der 
                                 (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),                                # Esquina inferior der 
                                 (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1
            else:                                               # Cuadrados del medio  # [superio izq, superior der, inferior der, inferior izq]
                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter - 8][0]
                upperRightCorner = saved_corners[pixelCounter - 7][0]
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  # Esquina superior izq 
                                 (upperRightCorner[0], upperRightCorner[1]),                                 # Esquina superior der 
                                 (lowerRightCorner[0], lowerRightCorner[1]),                                # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
                
                center = find_center_np(squareCorners)
                transformed_point = cv.perspectiveTransform(center, matrix)
                robotMap[str(letter) + str(i)] = transformed_point[0][0]

                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1



    output_file = os.path.join('parameters', 'map.yaml')
    serializable_data = {key: value.tolist() for key, value in robotMap.items()}
    with open(output_file, 'w') as file:
        yaml.dump(serializable_data, file, default_flow_style=False)
    
                
    return chessBoard # CAMBIAR A ROBOT MAP

def setup(initialChessBoard):
    # Place white pawns on row 2
    for col in range(8):
        initialChessBoard[f"{chr(65 + col)}2"][1] = "WhitePawn"

    # Place black pawns on row 7
    for col in range(8):
        initialChessBoard[f"{chr(65 + col)}7"][1] = "BlackPawn"

    # Place white pieces on row 1
    white_pieces = ["WhiteRook", "WhiteKnight", "WhiteBishop", "WhiteQueen", "WhiteKing", "WhiteBishop", "WhiteKnight", "WhiteRook"]
    for col, piece in enumerate(white_pieces):
        initialChessBoard[f"{chr(65 + col)}1"][1] = piece

    # Place black pieces on row 8
    black_pieces = ["BlackRook", "BlackKnight", "BlackBishop", "BlackQueen", "BlackKing", "BlackBishop", "BlackKnight", "BlackRook"]
    for col, piece in enumerate(black_pieces):
        initialChessBoard[f"{chr(65 + col)}8"][1] = piece

    return initialChessBoard

cv.namedWindow("Cam", cv.WINDOW_NORMAL)
#cv.namedWindow("Cam1", cv.WINDOW_NORMAL)
cv.namedWindow("Cam2", cv.WINDOW_NORMAL)

chessBoardSize = (7,7)
cam = cv.VideoCapture(2)

width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
newSize = (640, int(640 * height / width))

def draw_polygons_on_image(image, dictionary, keys_to_draw=None):
    """
    Draws polygons on an image for specified keys.

    :param image: The image on which to draw.
    :param dictionary: Dictionary containing key-polygon mapping.
    :param keys_to_draw: List of keys to draw. If None, draws all keys.
    :return: Image with polygons drawn.
    """
    if keys_to_draw is None:
        keys_to_draw = list(dictionary.keys())  # Draw all keys if none specified

    for key in keys_to_draw:
        if key in dictionary:
            points = dictionary[key][0]  # Get the list of points for the current key
            if points:
                points = [(int(x), int(y)) for x, y in points]  # Convert to integers
                # Draw the polygon
                cv.polylines(image, [np.array(points)], isClosed=True, color=(0, 0, 255), thickness=2)   
    return image



while True:
    ret, im = cam.read()
    if ret:
        imLowRes = cv.resize(im, newSize)
        imGrayLowRes = cv.cvtColor(imLowRes, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(imGrayLowRes, chessBoardSize, None)
        if ret:
            cv.drawChessboardCorners(imLowRes, chessBoardSize, corners, ret)

        # Display images
        cv.imshow('Cam', imLowRes)
        #cv.imshow('Cam1', imGrayLowRes)
       

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key)
        match key:
            case ' ':  # Capture corners and create dictionary
                K, distCoef = get_calibration_parameters()
                undistorted_img = cv.undistort(im, K, distCoef)
                ret_2, undisorted_corners = cv.findChessboardCorners(undistorted_img, chessBoardSize, None)
                dictionary = makeChessBoard(undisorted_corners)    
                # Check if dictionary is not empty and draw polygons on the Cam2 image
                imCam2 = imLowRes.copy()
                imCam2 = cv.undistort(im, K, distCoef)
                print(dictionary)
                if dictionary:
                    # specific_keys = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'] 
                    imCam2 = draw_polygons_on_image(imCam2, dictionary) # Dibujar los cuadrados en la imagen para asegurarse de que estan bien. 
                cv.imshow('Cam2', imCam2)
                print("///////////////////////////////////////")
                print(str(robotMap))
                
                
                points_A8 = dictionary['A8'][0]
                center = find_center_np(points_A8)
                print(center)
                matrix = get_transformation_matrix()
                transformed_point1 = cv.perspectiveTransform(center, matrix)
                point = robotMap['A8'] / 1000
                print(str(point))
                print(str(transformed_point1))

                
               
                def load_from_yaml(filename):
                    input_file = os.path.join('parameters', 'map.yaml')
                    with open(input_file, 'r') as file:
                        loaded_data = yaml.safe_load(file)  
                    return {key: np.array(value, dtype=np.float32) for key, value in loaded_data.items()}

                loaded_data = load_from_yaml('map.yml')
                print(loaded_data)
                A8 = loaded_data['A8']
                x = A8[0] / 1000
                y = A8[1] / 1000
                print(A8)
                print(x)
                print(y)


            case "e":  # Exit loop
                break
            






"""
Setup donde las piezas tienen id.
def setup():
    for col in range(8):
        chessBoard[f"{chr(65 + col)}2"][1] = [col + 1, f"WhitePawn{col + 1}"]

    # Place black pawns on row 7
    for col in range(8):
        chessBoard[f"{chr(65 + col)}7"][1] = [col + 1, f"BlackPawn{col + 1}"]

    # Place white pieces on row 1
    white_pieces = ["WhiteRook1", "WhiteKnight1", "WhiteBishop1", "WhiteQueen", "WhiteKing", "WhiteBishop2", "WhiteKnight2", "WhiteRook2"]
    for col, piece in enumerate(white_pieces):
        chessBoard[f"{chr(65 + col)}1"][1] = [col + 1, piece]

    # Place black pieces on row 8
    black_pieces = ["BlackRook1", "BlackKnight1", "BlackBishop1", "BlackQueen", "BlackKing", "BlackBishop2", "BlackKnight2", "BlackRook2"]
    for col, piece in enumerate(black_pieces):
        chessBoard[f"{chr(65 + col)}8"][1] = [col + 1, piece]


def makeChessBoard(saved_corners): 
    pixelCounter = 0
    rowCounter = 8

    #horizontal --> Tengo que ver cuanto se mueve en y entre cada cuadrado. 

    for i in range(1, 9):
        letterCounter = 1
        for j in range(1, 8):
            if rowCounter == 1: 
                if j == 7:
                    letter = chr(letterCounter + 64) # chr(65) == A
                    pixel = saved_corners[pixelCounter]                                 # [[372.50427 122.00555]] corners[0][0][0], corners[0][0][1]
                    coordinates = [pixel[0][0] - 2, pixel[0][1] + 2]
                    chessBoard[str(letter) + str(rowCounter)] = [coordinates, None]      # Por ahora estamos poniendo que es la esquina. 
                    letterCounter += 1

                    letter = chr(letterCounter + 64) # chr(65) == A
                    pixel = saved_corners[pixelCounter]
                    coordinates = [pixel[0][0] + 2, pixel[0][1] + 2]
                    chessBoard[str(letter) + str(rowCounter)] = [coordinates, None]
                    pixelCounter += 1
                else:
                    letter = chr(letterCounter + 64) # chr(65) == A
                    pixel = saved_corners[pixelCounter]                                 # [[372.50427 122.00555]] corners[0][0][0], corners[0][0][1]
                    coordinates = [pixel[0][0] - 2, pixel[0][1] + 2]
                    chessBoard[str(letter) + str(rowCounter)] = [coordinates, None]      # Por ahora estamos poniendo que es la esquina.
                    letterCounter += 1
                    pixelCounter += 1
                    print(pixelCounter)
            else:     
                if j == 7:
                    letter = chr(letterCounter + 64) # chr(65) == A
                    pixel = saved_corners[pixelCounter]                                 # [[372.50427 122.00555]] corners[0][0][0], corners[0][0][1]
                    coordinates = [pixel[0][0] - 2, pixel[0][1] - 2]
                    chessBoard[str(letter) + str(rowCounter)] = [coordinates, None]      # Por ahora estamos poniendo que es la esquina.
                    letterCounter += 1

                    letter = chr(letterCounter + 64) # chr(65) == A
                    pixel = saved_corners[pixelCounter]
                    coordinates = [pixel[0][0] + 2, pixel[0][1] - 2]
                    chessBoard[str(letter) + str(rowCounter)] = [coordinates, None] 
                    pixelCounter += 1
                else:    
                    letter = chr(letterCounter + 64) # chr(65) == A
                    pixel = saved_corners[pixelCounter]                                 # [[372.50427 122.00555]] corners[0][0][0], corners[0][0][1]
                    coordinates = [pixel[0][0] - 2, pixel[0][1] - 2]
                    chessBoard[str(letter) + str(rowCounter)] = [coordinates, None]      # Por ahora estamos poniendo que es la esquina.
                    letterCounter += 1
                    pixelCounter += 1
        rowCounter -=1
        if rowCounter == 1: 
            pixelCounter = 42

    print(chessBoard)
    return chessBoard
"""

