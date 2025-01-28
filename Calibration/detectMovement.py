import cv2
import numpy as np

UMBRAL_CAMBIO = 2

# Cargar imágenes
imagen_anterior = cv2.imread('imagen_anterior.png')
imagen_actual = cv2.imread('imagen_actual.png')

alto = 640
ancho = 480 
# Definir puntos de correspondencia (ejemplo)
puntos_origen = np.float32([[185, 32], [600, 20], [197, 460], [625, 443]])
puntos_destino = np.float32([[0, 0], [ancho, 0], [0, alto], [ancho, alto]])

# Calcular la matriz de transformación
matriz = cv2.getPerspectiveTransform(puntos_origen, puntos_destino)

# Aplicar la transformación
imagen_anterior_alineada = cv2.warpPerspective(imagen_anterior, matriz, (ancho, alto))
imagen_actual_alineada = cv2.warpPerspective(imagen_actual, matriz, (ancho, alto))

def dividir_tablero(imagen):
    casillas = []
    altura, ancho = imagen.shape[:2]
    tamaño_casilla_x = ancho // 8
    tamaño_casilla_y = altura // 8
    for fila in range(8):
        for columna in range(8):
            x_inicio = columna * tamaño_casilla_x
            y_inicio = fila * tamaño_casilla_y
            casilla = imagen[y_inicio:y_inicio + tamaño_casilla_y, x_inicio:x_inicio + tamaño_casilla_x]
            casillas.append(casilla)
    return casillas

casillas_anterior = dividir_tablero(imagen_anterior_alineada)
casillas_actual = dividir_tablero(imagen_actual_alineada)

def diferencia_color(casilla1, casilla2):
    # Convertir a espacio de color RGB
    casilla1_rgb = cv2.cvtColor(casilla1, cv2.COLOR_BGR2RGB)
    casilla2_rgb = cv2.cvtColor(casilla2, cv2.COLOR_BGR2RGB)
    
    # Calcular la diferencia absoluta
    diferencia = cv2.absdiff(casilla1_rgb, casilla2_rgb)
    
    # Calcular la suma de diferencias
    suma_diferencia = np.sum(diferencia)
    
    # Calcular la media de la intensidad de píxeles
    mean1 = np.mean(casilla1_rgb)
    mean2 = np.mean(casilla2_rgb)
    
    # Determinar el cambio de intensidad
    cambio = mean2 - mean1  # Positivo: aumento de intensidad (posible adición), Negativo: disminución (posible remoción)
    
    return suma_diferencia, cambio


def detect_movement():

    diferencias = []
    for i in range(64):
        diff, cambio = diferencia_color(casillas_anterior[i], casillas_actual[i])
        diferencias.append((i, diff, cambio))

    # Ordenar las diferencias de mayor a menor
    diferencias_ordenadas = sorted(diferencias, key=lambda x: x[1], reverse=True)

    # Seleccionar las cuatro casillas con mayor cambio
    casillas_cambiadas = diferencias_ordenadas[:4]

    diferencias_filtradas = [casilla for casilla in diferencias if abs(casilla[2]) > UMBRAL_CAMBIO]

    casillero_1 = diferencias_filtradas[0]
    casillero_2 = diferencias_filtradas[1]
    print(str(casillas_cambiadas))
    print(str(diferencias_filtradas))

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

while True:
    # Mostrar cada imagen
    cv2.imshow("Imagen Anterior", imagen_anterior)
    cv2.imshow("Imagen Actual", imagen_actual)
    cv2.imshow("Imagen Anterior Alineada", imagen_anterior_alineada)
    cv2.imshow("Imagen Actual Alineada", imagen_actual_alineada)
    
    # Esperar una tecla para cerrar
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
        break

# Cerrar todas las ventanas al salir del bucle
cv2.destroyAllWindows()

