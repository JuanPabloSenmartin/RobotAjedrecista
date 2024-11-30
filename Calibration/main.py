import cv2 as cv
import numpy as np

# Antes de correr esto, abria que calibrar la camara, correr el undisort, y depues sacar la matriz de transformacion


# La idea es detectar las esquinas, para saber en que parte del tablero estoy. Despues, armarme el tablero en donde le digo: el cuadrado A1 son los pixeles tales.
# Despues de esto, me armo el tablero hardcodeado en donde digo: en la posición A1, va la pieza tal. 
# Despues, detectar los contornos y sacar el punto medio del contorno. Aca hay 2 opciones: 
# 1. Con esto puedo ver en que parte del tablero esta, y asi asignarle un id al contorno que estoy viendo. Asi puedo hacer el seguimiento. 
# 2. Tomo un boolean de que cuadrados estan tomados. Cuando hay un cambio, me fijo en mi tablero que pieza estaba en esa posición y puedo hacer el cambio. 

chessBoard = {}           # key: Casillero, value: [[4 esquinas del casillero], [id, nombre de la pieza]]

def makeChessBoard(saved_corners): 
    
    pixelCounter = 0

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
                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1

                letter = chr(letterCounter + 64)
                lowerLeftCorner = saved_corners[pixelCounter][0]
                squareCorners = [(lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    # Esquina superior izq 
                                 (lowerLeftCorner[0] + h[0] - v[0], lowerLeftCorner[1] + h[1] - v[1]),      # Esquina superior der 
                                 (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                    # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
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
                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1

                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  # Esquina superior izq 
                                 (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                    # Esquina superior der 
                                 (upperLeftCorner[0] + h[0] + v[0], upperLeftCorner[1] + h[1] + v[1]),      # Esquina inferior der 
                                 (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])]                    # Esquina inferior izq                         
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
                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                
                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 7][0]
                squareCorners = [(upperLeftCorner[0], upperLeftCorner[1]),                                  # Esquina superior izq 
                                 (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                    # Esquina superior der 
                                 (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                    # Esquina inferior der 
                                 (lowerLeftCorner[0], lowerLeftCorner[1])]                                  # Esquina inferior izq                         
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
                chessBoard[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

    print(chessBoard)
    return chessBoard

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
cv.namedWindow("Cam1", cv.WINDOW_NORMAL)
cv.namedWindow("Cam2", cv.WINDOW_NORMAL)

chessBoardSize = (7,7)
cam = cv.VideoCapture(0)

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
        imCam2 = imLowRes.copy()
        imGrayLowRes = cv.cvtColor(imLowRes, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(imGrayLowRes, chessBoardSize, None)
        if ret:
            cv.drawChessboardCorners(imLowRes, chessBoardSize, corners, ret)

        # Display images
        cv.imshow('Cam', imLowRes)
        cv.imshow('Cam1', imGrayLowRes)
       

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key)
        match key:
            case ' ':  # Capture corners and create dictionary
                print(corners)
                dictionary = makeChessBoard(corners)    
                # Check if dictionary is not empty and draw polygons on the Cam2 image
                if dictionary:
                    specific_keys = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']
                    imCam2 = draw_polygons_on_image(imCam2, dictionary)
                cv.imshow('Cam2', imCam2)
            case "c":  # Exit loop
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

