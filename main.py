import os
import time
import numpy as np
import yaml
from Chess.chess_utils import Chess
from Cobot.cobot_utils import Cobot
import threading
from Interface.gui import ChessGUI
import cv2 as cv

# Robot coordinates
z_high = 0.12 # z high coordinate
z_low = 0.01 # z low coordinate
init_position = [0.047, -0.25] # initial robot position

## Init variables used to store taken pieces
outside_positions = [] # [x,y,isOccupied]
outside_position_index = 0
limit_y_left = 0.03  # store taken pieces in coordinate higher (+) than this
limit_x_down = 0.18  # store taken pieces in coordinate higher (+) than this

# Init chess and cobot
chess = Chess()
cobot = Cobot()

square_to_coordinate_map = {}

# This is the z coordinate where the robot will drop down to (depending on what piece its grabbing)
height = {
    1: 0.01,  # PAWN
    2: 0.02,  # KNIGHT
    3: 0.02,  # BISHOP
    4: 0.01,  # ROOK
    5: 0.045,  # QUEEN
    6: 0.045,  # KING
}


def load_from_yaml():
    input_file = os.path.join('Calibration/parameters', 'map.yaml')
    with open(input_file, 'r') as file:
        loaded_data = yaml.safe_load(file)
    return {key: np.array(value, dtype=np.float32) for key, value in loaded_data.items()}


def transform_map(chess_map):
    return {key.lower(): [value[0] / 1000, value[1] / 1000] for key, value in chess_map.items()}


def move(init_square, next_square, piece, only=True):
    """Moves a piece from init_square to next_square, handling special cases like moving out of the board."""
    init_pos = square_to_coordinate_map.get(init_square)
    piece_height = height.get(piece)
    if next_square == 'OUT':
        next_pos = get_free_outside_position()
        drop_height = piece_height - 0.004
    else:
        next_pos = square_to_coordinate_map.get(next_square)
        drop_height = None

    move_piece(init_pos, next_pos, piece_height, drop_height, only)


def move_piece(current_position, next_position, height_z_low, drop_height=None, only=True):
    """Handles the physical movement of a piece using the robotic arm."""
    cobot.open_gripper()
    cobot.move_robot(current_position, z_high)
    cobot.move_robot(current_position, height_z_low)
    cobot.close_gripper()
    cobot.move_robot(current_position, z_high)
    cobot.move_robot(next_position, z_high)
    if drop_height is None:
        cobot.move_robot(next_position, height_z_low)
    else:
        cobot.move_robot(next_position, drop_height)
    cobot.open_gripper()
    cobot.move_robot(next_position, z_high)
    if only:
        cobot.move_robot(init_position, z_high)


def get_free_outside_position():
    """Returns the next available position outside the board for captured pieces."""
    global outside_positions
    global outside_position_index
    free_position = outside_positions[outside_position_index]
    outside_positions[outside_position_index] = [free_position[0], free_position[1], True]
    outside_position_index += 1
    return [free_position[0], free_position[1]]


def generate_outside_positions():
    """Generates an array of outside positions for captured pieces."""
    dif = 0.05
    global outside_positions
    init_x = limit_x_down + (dif / 2)
    y = limit_y_left + (dif / 2)
    x = init_x
    for l in range(4):
        for k in range(4):
            outside_positions.append([x, y, False])
            x += dif
        y += dif
        x = init_x


def print_game_over():
    """Prints the reason for the game ending and the winner."""
    print('GAME OVER')
    print("Reason for game over:")
    if chess.board.is_checkmate():
        print("Checkmate")
    elif chess.board.is_stalemate():
        print("Stalemate")
    elif chess.board.is_insufficient_material():
        print("Insufficient material")
    elif chess.board.is_seventy_five_moves():
        print("75-move rule")
    elif chess.board.is_fivefold_repetition():
        print("Fivefold repetition")

    result = chess.board.result()
    if result == "1-0":
        print("White wins!")
    elif result == "0-1":
        print("Black wins!")
    elif result == "1/2-1/2":
        print("It's a draw.")


def stop_robot():
    """Stops the robot and moves it to the initial position."""
    cobot.move_robot(init_position, z_high)
    cobot.stop_robot()


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


alto = 640
ancho = 480

# Definir puntos de correspondencia (ejemplo)
puntos_origen = np.float32([[154, 4], [569, 13], [136, 429], [576, 439]])
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

def detect_movement(casillas_anterior, casillas_actual, board):
    diferencias = []
    for i in range(64):
        diff, cambio = diferencia_color(casillas_anterior[i], casillas_actual[i])
        diferencias.append((i, diff, cambio))

    # Ordenar las diferencias de mayor a menor
    diferencias_ordenadas = sorted(diferencias, key=lambda x: x[1], reverse=True)

    # Seleccionar las cuatro casillas con mayor cambio
    casillas_cambiadas = diferencias_ordenadas[:4]

    diferencias_filtradas = [casilla for casilla in casillas_cambiadas if abs(casilla[2]) > 4]

    movement = None
    num_filtered = len(diferencias_filtradas)

    if num_filtered == 2:
        casillero_1 = diferencias_filtradas[0][0]
        casillero_2 = diferencias_filtradas[1][0]

        square_1 = index_to_chess_notation(casillero_1)
        square_2 = index_to_chess_notation(casillero_2)

        print(square_1, square_2)

        piece_square_1 = board.piece_at(casillero_1)

        if piece_square_1 != None and piece_square_1.color:  # Es blanca
            movement = square_1 + square_2
        else:
            movement = square_2 + square_1

    elif num_filtered == 3:
        square_indexes = [diferencias_filtradas[0][0], diferencias_filtradas[1][0], diferencias_filtradas[2][0]]

        square_indexes.sort()

        square_1 = index_to_chess_notation(square_indexes[0])
        square_2 = index_to_chess_notation(square_indexes[1])
        square_3 = index_to_chess_notation(square_indexes[2])

        piece_square_1 = board.piece_at(square_indexes[0])

        if piece_square_1 != None and piece_square_1.color:
            movement = square_1 + square_3
        else:
            movement = square_2 + square_3

    elif num_filtered == 4:
        square_indexes = [diferencias_filtradas[0][0], diferencias_filtradas[1][0], diferencias_filtradas[2][0], diferencias_filtradas[3][0]]

        square_indexes.sort()

        print(square_indexes)

        square_1 = index_to_chess_notation(square_indexes[0])
        square_2 = index_to_chess_notation(square_indexes[1])
        square_3 = index_to_chess_notation(square_indexes[2])
        square_4 = index_to_chess_notation(square_indexes[3])

        print(square_1, square_4)

        piece_square_1 = board.piece_at(square_indexes[0])
        piece_square_4 = board.piece_at(square_indexes[3])

        if piece_square_1 != None and piece_square_4 != None:
            if piece_square_1.color and piece_square_4.color:
                if piece_square_1.piece_type == 4 and piece_square_4.piece_type == 6:
                    movement = square_4 + square_2
                elif piece_square_1.piece_type == 6 and piece_square_4.piece_type == 4:
                    movement = square_1 + square_3



    return movement


if __name__ == "__main__":
    """Main loop for handling the chess game with the robotic arm and GUI."""
    square_to_coordinate_map = transform_map(load_from_yaml())

    ## Move cobot to initial position
    cobot.init_position(init_position, z_high)

    ## Generate outside positions array
    generate_outside_positions()

    ## Init GUI
    gui = ChessGUI(chess.board)
    gui_thread = threading.Thread(target=gui.run, daemon=True)
    gui_thread.start()


    cv.namedWindow("Cam", cv.WINDOW_NORMAL)
    cam = cv.VideoCapture(0)
    take = False
    while True:
        ret, im = cam.read()

        cv.imshow('Cam', im)
        if take:
            time.sleep(1)
            guardar_imagen(im, "imagen_anterior.png")
            print("foto guardada")
            take = False

        key = cv.waitKey(30)
        if key >= 0:
            key = chr(key)
            if key == 's':
                guardar_imagen(im, "imagen_anterior.png")
                print("foto guardada")
            if key == ' ':
                guardar_imagen(im, "imagen_actual.png")
                print("foto guardada")

                previousImage = cargar_imagen("imagen_anterior.png")
                afterImage = cargar_imagen("imagen_actual.png")

                imagen_anterior_alineada = cv.warpPerspective(previousImage, matriz, (ancho, alto))
                imagen_actual_alineada = cv.warpPerspective(afterImage, matriz, (ancho, alto))

                previous_squares = dividir_tablero(imagen_anterior_alineada)
                actual_squares = dividir_tablero(imagen_actual_alineada)

                # Pieces detection
                person_move = detect_movement(previous_squares, actual_squares, chess.board)

                print('Move from the person: ', person_move)
                if person_move is not None:
                    if not chess.is_move_valid(person_move):
                        print('Invalid move was made: ', person_move)
                        print('Make another move\n')
                        continue
                    else:
                        chess.update_board(person_move)
                        gui.update()

                        # Check for checkmate or draw
                        if chess.is_game_over():
                            print_game_over()
                            stop_robot()
                            break

                        # Get best move for robot
                        best_move = chess.find_best_move()

                        if chess.is_move_valid(best_move):
                            print('Best move for the robot: ', best_move)
                            from_square, to_square = chess.get_move_squares(best_move)

                            is_capture = chess.is_move_capture(best_move)
                            is_en_passant, captured_square = chess.is_move_en_passant(best_move)
                            is_promotion = chess.is_move_promotion(best_move)
                            is_castle = chess.is_move_castle(best_move)

                            if is_capture:
                                # Move captured piece first
                                print('Capturing piece')
                                move(to_square, 'OUT', chess.get_piece(to_square), False)

                            if is_en_passant:
                                # Move other piece first
                                print('Doing en passant')
                                move(captured_square, 'OUT', chess.get_piece(captured_square), False)

                            # Move robot's piece
                            is_only = not (is_castle or is_promotion)
                            move(from_square, to_square, chess.get_piece(from_square), is_only)

                            if is_promotion:
                                print('Promoting')
                                ## TODO: Implement promotion logic

                            if is_castle:
                                print('Castling')
                                # Move rook to new position
                                init_rook_square, next_rook_square = chess.get_castling_rook_positions(best_move)
                                move(init_rook_square, next_rook_square, chess.get_piece(init_rook_square))

                            chess.update_board(best_move)
                            gui.update()
                            # Check checkmate or draw
                            if chess.is_game_over():
                                print_game_over()
                                stop_robot()
                                break
                            take = True
                        else:
                            print('Invalid move made by stockfish')
                            print('Stopping robot')
                            stop_robot()


                else:
                    print('No move was detected, try again')

    cam.release()
    cv.destroyAllWindows()

# Cerrar todas las ventanas al salir del bucle
cam.release()
cv.destroyAllWindows()