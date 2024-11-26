##https://py-stockfish.github.io/stockfish/stockfish/models.html#Stockfish.make_moves_from_current_position
import chess
import chess.engine
import numpy as np
from stockfish import Stockfish

class Chess:
    def __init__(self):
        self.board = chess.Board()
        self.stockfish = Stockfish(path="engine/stockfish/stockfish-windows-x86-64-avx2.exe")

    def isMoveValid(self, move):
        return self.board.is_legal(chess.Move.from_uci(move))

    def isGameOver(self):
        return self.board.is_game_over()

    def printBoard(self):
        print(self.board.unicode(borders=True))

    def findBestMove(self):
        self.stockfish.set_fen_position(self.board.fen())
        return self.stockfish.get_best_move()

    def isMoveCapture(self, move: str) -> bool:
        """
        Checks if a move captures an opponent's piece.

        Args:
            move (str): The move in UCI format (e.g., 'e2e4').

        Returns:
            bool: True if the move captures a piece, False otherwise.
        """
        # Parse the move to get the start and destination squares
        chess_move = chess.Move.from_uci(move)

        # Ensure the move is legal
        if chess_move not in self.board.legal_moves:
            raise ValueError(f"Invalid move: {move}")

        # Check if the destination square is occupied by an opponent's piece
        destination_square = chess_move.to_square
        piece_at_destination = self.board.piece_at(destination_square)

        # If there's a piece at the destination and it's of the opposite color, it's a capture
        if piece_at_destination and piece_at_destination.color != self.board.turn:
            return True
        return False

    def areChessboardsEqual(self, newBoardFEN):
        """
        Compares the current chess board (self.board) with a new board represented as a FEN string.

        Args:
            newBoardFEN (str): A FEN string representing the new board state.

        Returns:
            tuple: (bool, str)
                - The first element is True if the boards are equal, otherwise False.
                - The second element is the move in UCI format (e.g., 'e2e4') if boards are not equal.
        """
        # Create a temporary board for comparison
        newBoard = chess.Board(newBoardFEN)

        # Track the origin and destination of the move
        origin, destination = None, None

        # Compare each square of the current board to the new board
        for square in chess.SQUARES:
            current_piece = self.board.piece_at(square)
            new_piece = newBoard.piece_at(square)

            if current_piece != new_piece:
                if current_piece is not None:  # A piece was removed (origin square)
                    if origin is not None:
                        print(f"Multiple origin squares found: {origin} and {square}")
                    origin = square
                if new_piece is not None:  # A piece was added (destination square)
                    if destination is not None:
                        print(f"Multiple destination squares found: {destination} and {square}")
                    destination = square

        # If no differences are found, the boards are equal
        if origin is None and destination is None:
            return True, ""  # Boards are equal

        # If either origin or destination is missing, something went wrong
        if origin is None or destination is None:
            print(f"Error: origin={origin}, destination={destination}")
            return False, ""  # Error case (invalid board state)

        # Convert origin and destination to UCI format
        move = chess.square_name(origin) + chess.square_name(destination)
        return False, move

    def check_occupied(self, target_square):

        """
        Uses `python_chess` to verify that the target square is not occupied. Will return a 1 if the square is occupied.

        `target_square` is specified from 0 to 63, starting at A1, and moving across the rows to H8.

        See: https://python-chess.readthedocs.io/en/latest/core.html#squares

        """
        if not self.board.piece_at(target_square):
            self.occupied = 0
        else:
            self.occupied = 1

        return self.occupied

    def move(self, move):
        self.board.push(chess.Move.from_uci(move))

