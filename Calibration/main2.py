import cv2 as cv
import numpy as np
import math
import copy

# ------------------------- Configuración Inicial ------------------------- #

# Parámetros para la detección de contornos (ajustar según sea necesario)
THRESHOLD_VALUE = 80  # Valor de umbral para binarización
KERNEL_RADIUS = 7     # Radio del kernel para denoise
MIN_AREA = 450        # Área mínima de contornos
MAX_AREA = 95000      # Área máxima de contornos

# Diccionario para el tablero de ajedrez
# key: Casillero (e.g., 'A1'), value: [list of 4 corners, piece_type or None]
chess_board = {}

# Función para crear el tablero de ajedrez
def makeChessBoard(saved_corners): 
    pixelCounter = 0

    corner0 = saved_corners[0][0]
    corner1 = saved_corners[1][0]
    corners7 = saved_corners[7][0]
    hVariationX = corner1[0] - corner0[0]
    hVariationY = corner1[1] - corner0[1]
    yVariationX = corners7[0] - corner0[0]
    yVariationY = corners7[1] - corner0[1]
    h = [hVariationX, hVariationY]    # Variación en [x, y]
    v = [yVariationX, yVariationY]

    print("Variación horizontal: " + str(h))
    print("Variación vertical: " + str(v))

    for i in range(8, 0, -1):
        letterCounter = 1
        if i == 1: 
            pixelCounter = 42
        for j in range(1, 8):                             
            if i == 8 and j == 1:  # Esquina superior izquierda
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                squareCorners = [
                    (lowerRightCorner[0] - h[0] - v[0], lowerRightCorner[1] - h[1] - v[1]),  # Superior izq
                    (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                  # Superior der
                    (lowerRightCorner[0], lowerRightCorner[1]),                                # Inferior der
                    (lowerRightCorner[0] - h[0], lowerRightCorner[1] - h[1])                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

            elif i == 8 and j == 7:  # Esquina superior derecha
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [
                    (lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    # Superior izq
                    (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                  # Superior der
                    (lowerRightCorner[0], lowerRightCorner[1]),                                # Inferior der
                    (lowerLeftCorner[0], lowerLeftCorner[1])                                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1

                letter = chr(letterCounter + 64)
                lowerLeftCorner = saved_corners[pixelCounter][0]
                squareCorners = [
                    (lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    # Superior izq
                    (lowerLeftCorner[0] + h[0] - v[0], lowerLeftCorner[1] + h[1] - v[1]),      # Superior der
                    (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                    # Inferior der
                    (lowerLeftCorner[0], lowerLeftCorner[1])                                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1    

            elif i == 1 and j == 1:  # Esquina inferior izquierda
                letter = chr(letterCounter + 64)
                upperRightCorner = saved_corners[pixelCounter][0]
                squareCorners = [
                    (upperRightCorner[0] - h[0], upperRightCorner[1] - h[1]),                  # Superior izq
                    (upperRightCorner[0], upperRightCorner[1]),                                # Superior der
                    (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),                  # Inferior der
                    (upperRightCorner[0] - h[0] + v[0], upperRightCorner[1] - h[1] + v[1])    # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

            elif i == 1 and j == 7:  # Esquina inferior derecha
                letter = chr(letterCounter + 64)
                upperRightCorner = saved_corners[pixelCounter][0]
                upperLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [
                    (upperLeftCorner[0], upperLeftCorner[1]),                    # Superior izq
                    (upperRightCorner[0], upperRightCorner[1]),                  # Superior der
                    (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),    # Inferior der
                    (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])       # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1

                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter][0]
                squareCorners = [
                    (upperLeftCorner[0], upperLeftCorner[1]),                                  # Superior izq
                    (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                    # Superior der
                    (upperLeftCorner[0] + h[0] + v[0], upperLeftCorner[1] + h[1] + v[1]),      # Inferior der
                    (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])                     # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1    

            elif i == 8:  # Lado de arriba
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [
                    (lowerLeftCorner[0] - v[0], lowerLeftCorner[1] - v[1]),                    # Superior izq
                    (lowerRightCorner[0] - v[0], lowerRightCorner[1] - v[1]),                  # Superior der
                    (lowerRightCorner[0], lowerRightCorner[1]),                                # Inferior der
                    (lowerLeftCorner[0], lowerLeftCorner[1])                                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

            elif j == 1:  # Lado de la izquierda
                letter = chr(letterCounter + 64)
                lowerRightCorner = saved_corners[pixelCounter][0]
                upperRightCorner = saved_corners[pixelCounter - 7][0]
                squareCorners = [
                    (upperRightCorner[0] - h[0], upperRightCorner[1] - h[1]),                  # Superior izq
                    (upperRightCorner[0], upperRightCorner[1]),                                # Superior der
                    (lowerRightCorner[0], lowerRightCorner[1]),                                # Inferior der
                    (lowerRightCorner[0] - h[0], lowerRightCorner[1] - h[1])                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

            elif j == 7:  # Lado de la derecha
                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter - 8][0]
                upperRightCorner = saved_corners[pixelCounter - 7][0]
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [
                    (upperLeftCorner[0], upperLeftCorner[1]),                                  # Superior izq
                    (upperRightCorner[0], upperRightCorner[1]),                                # Superior der
                    (lowerRightCorner[0], lowerRightCorner[1]),                                # Inferior der
                    (lowerLeftCorner[0], lowerLeftCorner[1])                                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1

                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 7][0]
                squareCorners = [
                    (upperLeftCorner[0], upperLeftCorner[1]),                                  # Superior izq
                    (upperLeftCorner[0] + h[0], upperLeftCorner[1] + h[1]),                    # Superior der
                    (lowerLeftCorner[0] + h[0], lowerLeftCorner[1] + h[1]),                    # Inferior der
                    (lowerLeftCorner[0], lowerLeftCorner[1])                                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

            elif i == 1:  # Lado de abajo
                letter = chr(letterCounter + 64)
                upperRightCorner = saved_corners[pixelCounter][0]
                upperLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [
                    (upperLeftCorner[0], upperLeftCorner[1]),                    # Superior izq
                    (upperRightCorner[0], upperRightCorner[1]),                  # Superior der
                    (upperRightCorner[0] + v[0], upperRightCorner[1] + v[1]),    # Inferior der
                    (upperLeftCorner[0] + v[0], upperLeftCorner[1] + v[1])       # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

            else:  # Cuadrados del medio
                letter = chr(letterCounter + 64)
                upperLeftCorner = saved_corners[pixelCounter - 8][0]
                upperRightCorner = saved_corners[pixelCounter - 7][0]
                lowerRightCorner = saved_corners[pixelCounter][0]
                lowerLeftCorner = saved_corners[pixelCounter - 1][0]
                squareCorners = [
                    (upperLeftCorner[0], upperLeftCorner[1]),                                  # Superior izq
                    (upperRightCorner[0], upperRightCorner[1]),                                # Superior der
                    (lowerRightCorner[0], lowerRightCorner[1]),                                # Inferior der
                    (lowerLeftCorner[0], lowerLeftCorner[1])                                   # Inferior izq
                ]                         
                chess_board[str(letter) + str(i)] = [squareCorners, None]
                letterCounter += 1
                pixelCounter += 1

# Función para configurar el tablero inicial con piezas
def setup(initialChessBoard):
    # Colocar peones blancos en la fila 2
    for col in range(8):
        square = f"{chr(65 + col)}2"
        piece_type = "WhitePawn"
        initialChessBoard[square][1] = piece_type

    # Colocar peones negros en la fila 7
    for col in range(8):
        square = f"{chr(65 + col)}7"
        piece_type = "BlackPawn"
        initialChessBoard[square][1] = piece_type

    # Colocar piezas blancas en la fila 1
    white_pieces = ["WhiteRook", "WhiteKnight", "WhiteBishop", "WhiteQueen", "WhiteKing", "WhiteBishop", "WhiteKnight", "WhiteRook"]
    for col, piece in enumerate(white_pieces):
        square = f"{chr(65 + col)}1"
        initialChessBoard[square][1] = piece

    # Colocar piezas negras en la fila 8
    black_pieces = ["BlackRook", "BlackKnight", "BlackBishop", "BlackQueen", "BlackKing", "BlackBishop", "BlackKnight", "BlackRook"]
    for col, piece in enumerate(black_pieces):
        square = f"{chr(65 + col)}8"
        initialChessBoard[square][1] = piece

    return initialChessBoard

# Función para dibujar polígonos en la imagen
def draw_polygons_on_image(image, dictionary, keys_to_draw=None):
    """
    Dibuja polígonos en una imagen para las claves especificadas.

    :param image: La imagen en la que dibujar.
    :param dictionary: Diccionario que contiene el mapeo clave-polígono.
    :param keys_to_draw: Lista de claves a dibujar. Si es None, dibuja todas.
    :return: Imagen con polígonos dibujados.
    """
    if keys_to_draw is None:
        keys_to_draw = list(dictionary.keys())  # Dibuja todas si no se especifica

    for key in keys_to_draw:
        if key in dictionary:
            points = dictionary[key][0]  # Obtener la lista de puntos para la clave actual
            if points:
                points = [(int(x), int(y)) for x, y in points]  # Convertir a enteros
                # Dibujar el polígono
                cv.polylines(image, [np.array(points)], isClosed=True, color=(0, 0, 255), thickness=2)   
    return image

# ------------------------- Procesamiento de Piezas ------------------------- #

# Función para eliminar ruido
def denoise(frame, method, radius):
    kernel = cv.getStructuringElement(method, (radius, radius)) 
    opening = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel)  # Erosión - dilatación
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)  # Dilatación - erosión
    return closing

# Función para filtrar contornos por área
def filter_contours_by_area(contours, min_area, max_area):
    filtered_contours = []
    for contour in contours:
        area = cv.contourArea(contour)
        if min_area <= area <= max_area:
            filtered_contours.append(contour)
    return filtered_contours


# ------------------------- Actualizacion de Tablero ------------------------- #
def get_piece_color(piece):
    if piece[0] == "W": 
        return "White"
    elif piece[0] == "B":
        return "Black"
    else:
        raise ValueError("Piece does no have available color")

def update_chess_board(color):
    moved_piece = None 
    old_square = None
    new_square = None 
    for square, data in chess_board.items():   
        virtual_piece = virtualChessBoard[square]
        chess_board_Piece = data[1]
        if virtual_piece == None and chess_board_Piece != None:         # Limpiar el casillero de donde salio la pieza
            moved_piece = chess_board_Piece
            old_square = square
            chess_board[square][1] = None
        elif virtual_piece != None and chess_board_Piece == None:      # Movimiento simple   
            new_square = square
        elif virtual_piece != None and chess_board_Piece != None and get_piece_color(chess_board_Piece) == color:
            new_square = square

    chess_board[new_square][1] = moved_piece
    print(f"{moved_piece} se movió de {old_square} a {new_square}.")

# ------------------------- Inicialización de Ventanas y Cámara ------------------------- #

cv.namedWindow("Cam", cv.WINDOW_NORMAL)
cv.namedWindow("Cam1", cv.WINDOW_NORMAL)
cv.namedWindow("Cam2", cv.WINDOW_NORMAL)

# Tamaño del tablero de ajedrez (interior, no incluye bordes)
chessBoardSize = (7,7)
cam = cv.VideoCapture(0)

width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
newSize = (640, int(640 * height / width))

# Variables para almacenar el estado del tablero y las piezas
initial_board_setup = False
processed_contours = {"White": [], "Black": []}
virtualChessBoard = {}

# ------------------------- Bucle Principal ------------------------- #

while True:
    ret, im = cam.read()
    if ret:
        imLowRes = cv.resize(im, newSize)
        imCam2 = imLowRes.copy()
        imGrayLowRes = cv.cvtColor(imLowRes, cv.COLOR_BGR2GRAY)
        ret_corners, corners = cv.findChessboardCorners(imGrayLowRes, chessBoardSize, None)
        if ret_corners:
            cv.drawChessboardCorners(imLowRes, chessBoardSize, corners, ret_corners)

        # Mostrar la imagen del tablero
        cv.imshow('Cam', imLowRes)
        cv.imshow('Cam1', imGrayLowRes)

    key = cv.waitKey(30)

    if key >= 0:
        key = chr(key).lower()
        if key == ' ':  # Capturar esquinas y crear el tablero
            if ret_corners:
                makeChessBoard(corners)
                chess_board = setup(chess_board)
                initial_board_setup = True
                print("Tablero de ajedrez configurado.")
            else:
                print("No se detectaron esquinas del tablero.")

        elif key in ['w', 'n'] and initial_board_setup:  # Procesar y guardar contornos de piezas
            # Determinar si es blanco o negro
            piece_color = "White" if key == 'w' else "Black"
            invert_threshold = False if key == 'w' else True  # Asumir piezas negras son oscuras

            # Convertir a escala de grises
            grey_frame = cv.cvtColor(imLowRes, cv.COLOR_BGR2GRAY)

            # Aplicar umbral
            if invert_threshold:
                ret_thresh, thresh = cv.threshold(grey_frame, THRESHOLD_VALUE, 255, cv.THRESH_BINARY_INV)
            else:
                ret_thresh, thresh = cv.threshold(grey_frame, THRESHOLD_VALUE, 255, cv.THRESH_BINARY)

            # Eliminar ruido
            denoise_frame = denoise(thresh, cv.MORPH_ELLIPSE, KERNEL_RADIUS)

            # Encontrar contornos
            contours, hierarchy = cv.findContours(denoise_frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

            # Filtrar contornos por área
            filtered_contours = filter_contours_by_area(contours, MIN_AREA, MAX_AREA)

            # Limpiar contornos anteriores del color correspondiente
            processed_contours[piece_color] = []

            for contour in filtered_contours:
                # Calcular momentos del contorno
                M = cv.moments(contour)

                # Calcular centroide
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    # Asignar contorno a una posición del tablero
                    for square, data in chess_board.items():
                        corners_square = data[0]
                        # Verificar si el centroide está dentro del cuadrado
                        if cv.pointPolygonTest(np.array(corners_square), (cx, cy), False) >= 0:
                           
                            """       
                            # Asignar el tipo de pieza basado en el color
                            piece_type = data[1]  # Obtener el tipo actual de la pieza en el casillero
                            if piece_type is None:
                                # Si el casillero está vacío, asignar el tipo genérico basado en color
                                if piece_color == "White":
                                    # Asignar el primer peón disponible si se detecta un peón
                                    piece_type = "WhitePawn"
                                else:
                                    piece_type = "BlackPawn"
                            """
                            # Asignar la pieza al casillero
                            processed_contours[piece_color].append({
                                "square": square,
                                "contour": contour,
                                "centroid": (cx, cy)
                            })
                            virtualChessBoard[square] = piece_color
                            # chessBoard[square][1] = piece_type  # Actualizar el estado de la pieza
                        else:
                            virtualChessBoard[square] = None
            update_chess_board(piece_color)    

            print(f"Piezas {piece_color.lower()} detectadas: {len(processed_contours[piece_color])}")

        elif key == "a":
            if initial_board_setup:
                # Crear una copia de la imagen para dibujar
                display_image = imLowRes.copy()
                draw_polygons_on_image(display_image, chess_board)

                # Dibujar contornos de piezas blancas
                for piece in processed_contours["White"]:
                    cv.drawContours(display_image, [piece["contour"]], -1, (255, 0, 0), 2)
                    cv.circle(display_image, piece["centroid"], 5, (0, 255, 0), -1)
                    cv.putText(display_image, piece["square"], piece["centroid"], cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

                # Dibujar contornos de piezas negras
                for piece in processed_contours["Black"]:
                    cv.drawContours(display_image, [piece["contour"]], -1, (0, 255, 255), 2)
                    cv.circle(display_image, piece["centroid"], 5, (0, 0, 255), -1)
                    cv.putText(display_image, piece["square"], piece["centroid"], cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

                # Mostrar la imagen con las detecciones
                cv.imshow('Cam2', display_image)

        elif key == 'c':  # Salir del bucle
            break

# ------------------------- Liberar Recursos ------------------------- #

cam.release()
cv.destroyAllWindows()
