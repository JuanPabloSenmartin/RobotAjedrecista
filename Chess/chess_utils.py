import chess
import chess.engine
import numpy as np
from stockfish import Stockfish

class Chess:
    def __init__(self):
        self.board = chess.Board()
        self.stockfish = Stockfish(path="engine/stockfish/stockfish-windows-x86-64-avx2.exe")

    def is_move_valid(self, move):
        return self.board.is_legal(chess.Move.from_uci(move))

    def is_game_over(self):
        return self.board.is_game_over()

    def print_board(self):
        print(self.board.unicode(borders=True))

    def find_best_move(self):
        self.stockfish.set_fen_position(self.board.fen())
        return self.stockfish.get_best_move()

    def get_piece(self, square: str):
        """
        Returns the type of the piece at the given square.

        Args:
            square (str): The square in algebraic notation (e.g., 'e1').

        Returns:
            chess.PieceType: The type of the piece (e.g., chess.PAWN, chess.KING) or None if the square is empty.
        """
        # Convert the square from algebraic notation to a board index
        square_index = chess.parse_square(square)

        # Get the piece at the given square
        piece = self.board.piece_at(square_index)

        # Return the piece type (e.g., chess.PAWN) or None if no piece is present
        return piece.piece_type if piece else None

    def get_castling_rook_positions(self, move: str) -> (str, str):
        """
        Returns the rook's initial and final positions for a given castling move.

        Args:
            move (str): The castling move in UCI format (e.g., 'e1g1' for kingside castling).

        Returns:
            tuple: A tuple containing:
                - initial_rook_position (str): The initial square of the rook (e.g., 'h1').
                - final_rook_position (str): The destination square of the rook (e.g., 'f1').
        """
        # Parse the move into a chess.Move object
        chess_move = chess.Move.from_uci(move)

        # Ensure the move is castling
        king_start_square = chess_move.from_square
        king_end_square = chess_move.to_square

        # Determine rook positions based on castling direction
        if king_start_square == chess.E1:  # White castling
            if king_end_square == chess.G1:  # Kingside
                return 'h1', 'f1'
            elif king_end_square == chess.C1:  # Queenside
                return 'a1', 'd1'
        elif king_start_square == chess.E8:  # Black castling
            if king_end_square == chess.G8:  # Kingside
                return 'h8', 'f8'
            elif king_end_square == chess.C8:  # Queenside
                return 'a8', 'd8'

        raise ValueError("The provided move is not a valid castling move.")

    def get_move_squares(self, move: str) -> (str, str):
        """
        Extracts the to_square and from_square from a UCI move string.

        Args:
            move (str): The move in UCI format (e.g., 'e1e3').

        Returns:
            tuple: A tuple containing:
                - from_square (str): The starting square of the move (e.g., 'e1').
                - to_square (str): The destination square of the move (e.g., 'e3').
        """
        # Parse the move into a chess.Move object
        chess_move = chess.Move.from_uci(move)

        # Convert the from_square and to_square to algebraic notation
        from_square = chess.square_name(chess_move.from_square)
        to_square = chess.square_name(chess_move.to_square)

        return from_square, to_square

    def is_move_castle(self, move: str) -> bool:
        """
        Checks if the given move is a castling move.

        Args:
            move (str): The move in UCI format (e.g., 'e1g1' for kingside castling).

        Returns:
            bool: True if the move is a castling move, False otherwise.
        """
        # Parse the move into a chess.Move object
        chess_move = chess.Move.from_uci(move)

        # Check if the move is legal
        if chess_move not in self.board.legal_moves:
            raise ValueError(f"Invalid move: {move}")

        # Castling conditions:
        # - The moving piece must be the king
        # - The move must represent a castling destination square
        moving_piece = self.board.piece_at(chess_move.from_square)
        if (
                moving_piece is not None
                and moving_piece.piece_type == chess.KING
                and abs(chess_move.from_square - chess_move.to_square) == 2
        ):
            return True

        return False

    def is_move_promotion(self, move: str) -> bool:
        """
        Checks if the given move is a pawn promotion.

        Args:
            move (str): The move in UCI format (e.g., 'e7e8q').

        Returns:
            bool: True if the move is a pawn promotion, False otherwise.
        """
        # Parse the move into a chess.Move object
        chess_move = chess.Move.from_uci(move)

        # Check if the move is legal
        if chess_move not in self.board.legal_moves:
            raise ValueError(f"Invalid move: {move}")

        # Get the moving piece
        moving_piece = self.board.piece_at(chess_move.from_square)

        # Pawn promotion conditions:
        # - The moving piece must be a pawn
        # - The move must end on the promotion rank (rank 8 for white, rank 1 for black)
        # - The UCI string must include the promoted piece (e.g., "q", "r", "b", "n")
        if (
                moving_piece is not None
                and moving_piece.piece_type == chess.PAWN
                and chess_move.promotion is not None
        ):
            return True

        return False

    def is_move_en_passant(self, move: str) -> (bool, str):
        """
        Checks if the given move is an en passant capture.

        Args:
            move (str): The move in UCI format (e.g., 'e5d6').

        Returns:
            tuple:
                - bool: True if the move is an en passant capture, False otherwise.
                - str: The position of the taken piece in algebraic notation (e.g., 'e5'), or None if not en passant.
        """
        # Parse the move into a chess.Move object
        chess_move = chess.Move.from_uci(move)

        # Ensure the move is legal
        if chess_move not in self.board.legal_moves:
            raise ValueError(f"Invalid move: {move}")

        # Check if the move is en passant
        if self.board.is_en_passant(chess_move):
            # The captured pawn is on the square behind the destination of the move
            captured_square = chess_move.to_square + (-8 if self.board.turn else 8)
            captured_position = chess.square_name(captured_square)
            return True, captured_position

        return False, None

    def is_move_capture(self, move: str) -> bool:
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

    def are_chessboards_equal(self, new_board_fen):
        """
        Compares the current chess board (self.board) with a new board represented as a FEN string.

        Args:
            new_board_fen (str): A FEN string representing the new board state.

        Returns:
            tuple: (bool, str)
                - The first element is True if the boards are equal, otherwise False.
                - The second element is the move in UCI format (e.g., 'e2e4') if boards are not equal.
        """
        # Create a temporary board for comparison
        new_board = chess.Board(new_board_fen)

        # Track the origin and destination of the move
        origin, destination = None, None

        # Compare each square of the current board to the new board
        for square in chess.SQUARES:
            current_piece = self.board.piece_at(square)
            new_piece = new_board.piece_at(square)

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

    def update_board(self, move):
        self.board.push(chess.Move.from_uci(move))

