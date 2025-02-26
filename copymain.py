import os
import time

import numpy as np
import yaml

from Chess.chess_utils import Chess
from Cobot.cobot_utils import Cobot
import keyboard
import threading

from Interface.gui import ChessGUI

import cv2 as cv

z_high = 0.12
z_low = 0.01

limit_y_left = 0  # valid is higher (+) than this
limit_x_down = 0.18  # valid is higher (+) than this

init_position = [0.047, -0.25]

# [x,y,isOccupied]
outside_positions = []
outside_position_index = 0

chess = Chess()
cobot = Cobot()

new_map = {}
# map = {
#  'h1': [0.5076, -0.091],   'h2': [0.4568, -0.091],   'h3': [0.406, -0.091],    'h4': [0.3552, -0.091],
#  'h5': [0.3044, -0.091],   'h6': [0.2536, -0.091],   'h7': [0.2028, -0.091],   'h8': [0.152, -0.091],
#  'g1': [0.5076, -0.1443],  'g2': [0.4568, -0.1443],  'g3': [0.406, -0.1443],   'g4': [0.3552, -0.1443],
#  'g5': [0.3044, -0.1443],  'g6': [0.2536, -0.1443],  'g7': [0.2028, -0.1443],  'g8': [0.152, -0.1443],
#  'f1': [0.5076, -0.1976],  'f2': [0.4568, -0.1976],  'f3': [0.406, -0.1976],   'f4': [0.3552, -0.1976],
#  'f5': [0.3044, -0.1976],  'f6': [0.2536, -0.1976],  'f7': [0.2028, -0.1976],  'f8': [0.152, -0.1976],
#  'e1': [0.5076, -0.2509],  'e2': [0.4568, -0.2509],  'e3': [0.406, -0.2509],   'e4': [0.3552, -0.2509],
#  'e5': [0.3044, -0.2509],  'e6': [0.2536, -0.2509],  'e7': [0.2028, -0.2509],  'e8': [0.152, -0.2509],
#  'd1': [0.5076, -0.3042],  'd2': [0.4568, -0.3042],  'd3': [0.406, -0.3042],   'd4': [0.3552, -0.3042],
#  'd5': [0.3044, -0.3042],  'd6': [0.2536, -0.3042],  'd7': [0.2028, -0.3042],  'd8': [0.152, -0.3042],
#  'c1': [0.5076, -0.3575],  'c2': [0.4568, -0.3575],  'c3': [0.406, -0.3575],   'c4': [0.3552, -0.3575],
#  'c5': [0.3044, -0.3575],  'c6': [0.2536, -0.3575],  'c7': [0.2028, -0.3575],  'c8': [0.152, -0.3575],
#  'b1': [0.5076, -0.4108],  'b2': [0.4568, -0.4108],  'b3': [0.406, -0.4108],   'b4': [0.3552, -0.4108],
#  'b5': [0.3044, -0.4108],  'b6': [0.2536, -0.4108],  'b7': [0.2028, -0.4108],  'b8': [0.152, -0.4108],
#  'a1': [0.5076, -0.4641],  'a2': [0.4568, -0.4641],  'a3': [0.406, -0.4641],   'a4': [0.3552, -0.4641],
#  'a5': [0.3044, -0.4641],  'a6': [0.2536, -0.4641],  'a7': [0.2028, -0.4641],  'a8': [0.152, -0.4641]
# }

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
    init_pos = new_map.get(init_square)
    piece_height = height.get(piece)
    if next_square == 'OUT':
        next_pos = get_free_outside_position()
        drop_height = piece_height - 0.002
    else:
        next_pos = new_map.get(next_square)
        drop_height = None

    move_piece(init_pos, next_pos, piece_height, drop_height, only)


def move_piece(current_position, next_position, height_z_low, drop_height=None, only=True):
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
    global outside_positions
    global outside_position_index
    free_position = outside_positions[outside_position_index]
    outside_positions[outside_position_index] = [free_position[0], free_position[1], True]
    outside_position_index += 1
    return [free_position[0], free_position[1]]


def generate_outside_positions():
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

    result = chess.board.result()  # Get the result of the game
    # Determine the winner
    if result == "1-0":
        print("White wins!")
    elif result == "0-1":
        print("Black wins!")
    elif result == "1/2-1/2":
        print("It's a draw.")


def stop_robot():
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
puntos_origen = np.float32([[185, 11], [604, 24], [174, 447], [610, 448]])
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

def color_difference(casilla1, casilla2):
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

def detect_movement(previous_squares, current_squares, board):
    differences = []
    for i in range(64):
        diff, change = color_difference(previous_squares[i], current_squares[i])
        differences.append((i, diff, change))

    # Sort differences from largest to smallest
    sorted_differences = sorted(differences, key=lambda x: x[1], reverse=True)

    # Select the four squares with the most change
    changed_squares = sorted_differences[:4]
    filtered_differences = [square for square in changed_squares if abs(square[2]) > 2]

    movement = None
    num_filtered = len(filtered_differences)

    if num_filtered == 2:
        square_1_index, square_2_index = filtered_differences[0][0], filtered_differences[1][0]
        square_1, square_2 = index_to_chess_notation(square_1_index), index_to_chess_notation(square_2_index)
        
        piece_square_1 = board.piece_at(square_1_index)
        
        if piece_square_1 and piece_square_1.color:  # White piece
            movement = square_1 + square_2
        else:
            movement = square_2 + square_1

    elif num_filtered == 3:
        square_indexes = [filtered_differences[0][0], filtered_differences[1][0], filtered_differences[2][0]]
        
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
        square_indexes = [filtered_differences[0][0], filtered_differences[1][0], filtered_differences[2][0], filtered_differences[3][0]]

        square_indexes.sort()

        square_1 = index_to_chess_notation(square_indexes[0])
        square_2 = index_to_chess_notation(square_indexes[1])
        square_3 = index_to_chess_notation(square_indexes[2])
        square_4 = index_to_chess_notation(square_indexes[3])

        piece_square_1 = board.piece_at(square_indexes[0])
        piece_square_4 = board.piece_at(square_indexes[3])

        if piece_square_1.color and piece_square_4.color: 
            if piece_square_1.piece_type == 4 and piece_square_4.piece_type == 6:
                movement = square_4 + square_2
            elif piece_square_1.piece_type == 6 and piece_square_4.piece_type == 4: 
                movement = square_1 + square_3
    
    print(f"Detected movement: {movement}")
    return movement


if __name__ == "__main__":

    ## Init position:coordinates map
    new_map = transform_map(load_from_yaml())

    ## Move cobot to initial position
    cobot.init_position(init_position, z_high)

    ## Generate outside positions array
    generate_outside_positions()

    ## Init GUI
    gui = ChessGUI(chess.board)
    gui_thread = threading.Thread(target=gui.run, daemon=True)
    gui_thread.start()

    player_move_aux = ''

    cv.namedWindow("Cam", cv.WINDOW_NORMAL)
    cam = cv.VideoCapture(2)
    take = False
    while True:
        ret, im = cam.read()

        cv.imshow('Cam', im)
        if take:
            guardar_imagen(im, "imagen_anterior.png")
            print("foto guardada")
            take = False   

        key = cv.waitKey(30)
        if key >= 0:
            key = chr(key)
            match key: 
                case 's':
                    guardar_imagen(im, "imagen_anterior.png")
                    print("foto guardada")                             
                case ' ':
                    guardar_imagen(im, "imagen_actual.png")
                    print("foto guardada")

                    previousImage = cargar_imagen("imagen_anterior.png")
                    afterImage = cargar_imagen("imagen_actual.png")

                    imagen_anterior_alineada = cv.warpPerspective(previousImage, matriz, (ancho, alto))
                    imagen_actual_alineada = cv.warpPerspective(afterImage, matriz, (ancho, alto))

                    cv.imshow("Imagen Anterior Alineada", imagen_anterior_alineada)
                    cv.imshow("Imagen Actual Alineada", imagen_actual_alineada)
                

                    previous_squares = dividir_tablero(imagen_anterior_alineada)
                    actual_squares = dividir_tablero(imagen_actual_alineada)

                    movement = detect_movement(previous_squares, actual_squares, chess.board)

                    person_move = movement
                    ## Pieces detection

                    # is_chessboard_equal, person_move = chess.are_chessboards_equal(new_board)
                    print('person_move', person_move)
                    if person_move is not None:
                        if not chess.is_move_valid(person_move):
                            print('INVALID MOVE WAS MADE: ', person_move)
                            print('Make another move\n')
                            continue
                            # stop_robot()
                            # break
                        else:
                            # i = i + 1
                            chess.update_board(person_move)  # update MY board
                            gui.update()

                            # check checkmate or draw
                            if chess.is_game_over():
                                print_game_over()
                                stop_robot()
                                break
                            # check best move
                            best_move = chess.find_best_move()
                            print('best_move', best_move)

                            if chess.is_move_valid(best_move):
                                from_square, to_square = chess.get_move_squares(best_move)

                                is_capture = chess.is_move_capture(best_move)
                                is_en_passant, captured_square = chess.is_move_en_passant(best_move)
                                is_promotion = chess.is_move_promotion(best_move)
                                is_castle = chess.is_move_castle(best_move)

                                if is_capture:
                                    print('capture')
                                    ##move captured piece first
                                    move(to_square, 'OUT', chess.get_piece(to_square), False)

                                if is_en_passant:
                                    print('en passant')
                                    ##move other piece first
                                    move(captured_square, 'OUT', chess.get_piece(captured_square), False)

                                ##move piece
                                is_only = not (is_castle or is_promotion)
                                move(from_square, to_square, chess.get_piece(from_square), is_only)

                                if is_promotion:
                                    print('promotion')
                                    ## TODO: Implement promotion logic
                                    ##takes pawn out of the board
                                    ##move()
                                    ##brings queen back from outside the board
                                    ##move()

                                if is_castle:
                                    print('castle')
                                    ##move rook to new position
                                    init_rook_square, next_rook_square = chess.get_castling_rook_positions(best_move)
                                    move(init_rook_square, next_rook_square, chess.get_piece(init_rook_square))

                                chess.update_board(best_move)
                                gui.update()
                                # check checkmate or draw
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

    # Cerrar todas las ventanas al salir del bucle
    cam.release()
    cv.destroyAllWindows()

# Cerrar todas las ventanas al salir del bucle
cam.release()
cv.destroyAllWindows()
