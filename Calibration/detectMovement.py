import cv2 as cv
import numpy as np
import os
import chess 

board = chess.Board()

UMBRAL_CAMBIO = 2

alto = 640
ancho = 480 
# Definir puntos de correspondencia (ejemplo)
puntos_origen = np.float32([[138, 19], [557, 18], [142, 455], [576, 441]])
puntos_destino = np.float32([[0, 0], [ancho, 0], [0, alto], [ancho, alto]])

# Calcular la matriz de transformación
matriz = cv.getPerspectiveTransform(puntos_origen, puntos_destino)


def dividir_tablero(imagen):
    casillas = []
    altura, ancho = imagen.shape[:2]
    tamaño_casilla_x = ancho // 8
    tamaño_casilla_y = altura // 8
    for fila in range(7, -1, -1):  # Recorre las filas de abajo hacia arriba
        for columna in range(8):  # Recorre las columnas de izquierda a derecha
            x_inicio = columna * tamaño_casilla_x
            y_inicio = fila * tamaño_casilla_y
            casilla = imagen[y_inicio:y_inicio + tamaño_casilla_y, x_inicio:x_inicio + tamaño_casilla_x]
            casillas.append(casilla)
    return casillas



def diferencia_color(casilla1, casilla2):
    # Convertir a espacio de color RGB
    casilla1_rgb = cv.cvtColor(casilla1, cv.COLOR_BGR2RGB)
    casilla2_rgb = cv.cvtColor(casilla2, cv.COLOR_BGR2RGB)
    
    # Calcular la diferencia absoluta
    diferencia = cv.absdiff(casilla1_rgb, casilla2_rgb)
    
    # Calcular la suma de diferencias
    suma_diferencia = np.sum(diferencia)
    
    # Calcular la media de la intensidad de píxeles
    mean1 = np.mean(casilla1_rgb)
    mean2 = np.mean(casilla2_rgb)
    
    # Determinar el cambio de intensidad
    cambio = mean2 - mean1  # Positivo: aumento de intensidad (posible adición), Negativo: disminución (posible remoción)
    
    return suma_diferencia, cambio


def index_to_chess_notation(index):
            col = chr(97 + (index % 8))  # De 0-7 -> 'a'-'h'
            row = str(1 + (index // 8))  # De 0-7 -> '1'-'8'
            return col + row

def detect_movement():

    diferencias = []
    for i in range(64):
        diff, cambio = diferencia_color(casillas_anterior[i], casillas_actual[i])
        diferencias.append((i, diff, cambio))

    # Ordenar las diferencias de mayor a menor
    diferencias_ordenadas = sorted(diferencias, key=lambda x: x[1], reverse=True)

    # Seleccionar las cuatro casillas con mayor cambio
    casillas_cambiadas = diferencias_ordenadas[:4]

    diferencias_filtradas = [casilla for casilla in casillas_cambiadas if abs(casilla[2]) > UMBRAL_CAMBIO]

    
    if diferencias_filtradas == 2:
        casillero_1 = diferencias_filtradas[0][0]
        casillero_2 = diferencias_filtradas[1][0]
        print(str(casillas_cambiadas))
        print(str(diferencias_filtradas))

        square_1 = index_to_chess_notation(casillero_1)
        square_2 = index_to_chess_notation(casillero_2)

        print(square_1)
        print(square_2)

        print(board)

        piece_square_1 = board.piece_at(casillero_1)

        print(piece_square_1)

        if piece_square_1 != None and piece_square_1.color: # Es blanca
            movement = square_1 + square_2
        else:
            movement = square_2 + square_1

    elif diferencias_filtradas == 3: 
        casillero_1 = diferencias_filtradas[0][0]
        casillero_2 = diferencias_filtradas[1][0]
        casillero_3 = diferencias_filtradas[2][0]

        square_1 = index_to_chess_notation(casillero_1)
        square_2 = index_to_chess_notation(casillero_2)
        square_3 = index_to_chess_notation(casillero_3)

        piece_square_1 = board.piece_at(casillero_1)
        piece_square_2 = board.piece_at(casillero_2)
        piece_square_3 = board.piece_at(casillero_3)

        if piece_square_1 != None and piece_square_1.color:
            movement = square_1 + square_3
        else: 
            movement = square_2 + square_3

    elif diferencias_filtradas == 4:

        casillero_1 = diferencias_filtradas[0][0]
        casillero_2 = diferencias_filtradas[1][0]
        casillero_3 = diferencias_filtradas[2][0]
        casillero_4 = diferencias_filtradas[3][0]

        square_1 = index_to_chess_notation(casillero_1)
        square_2 = index_to_chess_notation(casillero_2)
        square_3 = index_to_chess_notation(casillero_3)
        square_4 = index_to_chess_notation(casillero_4)

        piece_square_1 = board.piece_at(casillero_1)
        piece_square_2 = board.piece_at(casillero_2)
        piece_square_3 = board.piece_at(casillero_3)
        piece_square_4 = board.piece_at(casillero_4)

        if piece_square_1.color and piece_square_4.color: 
            if piece_square_1.piece_type == 4 and piece_square_4.piece_type == 6:
                movement = square_4 + square_2
            elif piece_square_1.piece_type == 6 and piece_square_4.piece_type == 6: 
                movement = square_1 + square_3
    else: 
        movement = None

    print(f"Movimiento detectado: {movement}")

def generate_fen(chess_board):
    # Mapeo de nombres de piezas a notación FEN
    piece_map = {
        "WhitePawn": "P",
        "WhiteRook": "R",
        "WhiteKnight": "N",
        "WhiteBishop": "B",
        "WhiteQueen": "Q",
        "WhiteKing": "K",
        "BlackPawn": "p",
        "BlackRook": "r",
        "BlackKnight": "n",
        "BlackBishop": "b",
        "BlackQueen": "q",
        "BlackKing": "k"
    }
    
    fen_rows = []
    
    # Recorrer las filas de 8 a 1
    for rank in range(8, 0, -1):
        fen_row = ""
        empty_count = 0
        # Recorrer las columnas de A a H
        for file in range(65, 73):  # ASCII de 'A' a 'H' son 65 a 72
            square = f"{chr(file)}{rank}"
            piece = chess_board.get(square, {}).get(1, None)  # Asumiendo que la pieza está en el índice 1
            if piece:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_piece = piece_map.get(piece, "")
                fen_row += fen_piece
            else:
                empty_count += 1
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    
    # Unir las filas con '/'
    piece_placement = "/".join(fen_rows)
    
    # Campos adicionales de FEN
    active_color = "w"  # Suponiendo que es el turno de las blancas
    castling = "KQkq"    # Suponiendo que ambos lados tienen todos los derechos de enroque
    en_passant = "-"     # Sin posibilidad de captura al paso
    halfmove_clock = "0" # Reinicio del contador de medio movimientos
    fullmove_number = "1" # Número de movimientos completos
    
    # Construir la cadena FEN completa
    fen = f"{piece_placement} {active_color} {castling} {en_passant} {halfmove_clock} {fullmove_number}"
    
    return fen


cv.namedWindow("Cam", cv.WINDOW_NORMAL)

cam = cv.VideoCapture(2)
width = cam.get(cv.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
newSize = (640, int(640 * height / width))

def guardar_imagen(frame, nombreFoto, carpeta='fotos'):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    ruta_completa = os.path.join(carpeta, nombreFoto)
    cv.imwrite(ruta_completa, frame)
    print(f"Imagen guardada en: {ruta_completa}")
    return ruta_completa

def cargar_imagen(nombreFoto, carpeta='fotos'):
    ruta_completa = os.path.join(carpeta, nombreFoto)
    if not os.path.exists(ruta_completa):
        print(f"Error: La imagen '{ruta_completa}' no existe.")
        return None
    imagen = cv.imread(ruta_completa)
    if imagen is None:
        print(f"Error: No se pudo cargar la imagen '{ruta_completa}'.")
        return None
    return imagen

while True:
    ret, im = cam.read()
    if ret:                                                
        imLowRes = cv.resize(im, newSize)

    cv.imshow('Cam', im)

    
    key = cv.waitKey(30)
    if key >= 0:
        key = chr(key)
        match key:
            case ' ':
                guardar_imagen(im, "imagen_anterior.png")
                print("foto guardada")
            case 'a':
                guardar_imagen(imLowRes, "imagen_actual.png")
                print("foto guardada")
            case 'd':
                # Cargar imágenes
                imagen_anterior = cargar_imagen('imagen_anterior.png')
                imagen_actual = cargar_imagen('imagen_actual.png')

                
                cv.imshow("Imagen Anterior", imagen_anterior)
                cv.imshow("Imagen Actual", imagen_actual)

                
                # Aplicar la transformación
                imagen_anterior_alineada = cv.warpPerspective(imagen_anterior, matriz, (ancho, alto))
                imagen_actual_alineada = cv.warpPerspective(imagen_actual, matriz, (ancho, alto))

                """
                cv.imshow("Imagen Anterior Alineada", imagen_anterior_alineada)
                cv.imshow("Imagen Actual Alineada", imagen_actual_alineada)
                """

                casillas_anterior = dividir_tablero(imagen_anterior_alineada)
                casillas_actual = dividir_tablero(imagen_actual_alineada)

                detect_movement()

            case 'e':
                break

    # Mostrar cada imagen
    """
    cv2.imshow("Imagen Anterior", imagen_anterior)
    cv2.imshow("Imagen Actual", imagen_actual)
    cv2.imshow("Imagen Anterior Alineada", imagen_anterior_alineada)
    cv2.imshow("Imagen Actual Alineada", imagen_actual_alineada)
    """

# Cerrar todas las ventanas al salir del bucle
cam.release()
cv.destroyAllWindows()

