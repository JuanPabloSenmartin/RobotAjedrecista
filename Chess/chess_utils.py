import chess
from stockfish import Stockfish


class Chess:
    def __init__(self):
        """Initializes the chessboard and Stockfish engine."""
        self.board = chess.Board()
        self.stockfish = Stockfish(path="engine/stockfish/stockfish-windows-x86-64-avx2.exe")
        self.stockfish.set_elo_rating(2000)

    def is_move_valid(self, move: str) -> bool:
        """Checks if a move in UCI format is legal."""
        return self.board.is_legal(chess.Move.from_uci(move))

    def update_board(self, move: str):
        """Applies a move to the chessboard."""
        self.board.push(chess.Move.from_uci(move))

    def is_game_over(self) -> bool:
        """Checks if the game is over."""
        return self.board.is_game_over()

    def find_best_move(self) -> str:
        """Finds the best move according to Stockfish."""
        self.stockfish.set_fen_position(self.board.fen())
        return self.stockfish.get_best_move()

    def get_piece(self, square: str):
        """Retrieves the type of piece at a given square."""
        piece = self.board.piece_at(chess.parse_square(square))
        return piece.piece_type if piece else None

    def get_castling_rook_positions(self, move: str) -> tuple:
        """Gets the initial and final positions of the rook in a castling move."""
        move_obj = chess.Move.from_uci(move)
        castling_moves = {
            (chess.E1, chess.G1): ('h1', 'f1'), (chess.E1, chess.C1): ('a1', 'd1'),
            (chess.E8, chess.G8): ('h8', 'f8'), (chess.E8, chess.C8): ('a8', 'd8')
        }
        return castling_moves.get((move_obj.from_square, move_obj.to_square), None)

    def get_move_squares(self, move: str) -> tuple:
        """Extracts the origin and destination squares from a move."""
        move_obj = chess.Move.from_uci(move)
        return chess.square_name(move_obj.from_square), chess.square_name(move_obj.to_square)

    def is_move_castle(self, move: str) -> bool:
        """Checks if a move is a castling move."""
        move_obj = chess.Move.from_uci(move)
        piece = self.board.piece_at(move_obj.from_square)
        return piece and piece.piece_type == chess.KING and abs(move_obj.from_square - move_obj.to_square) == 2

    def is_move_promotion(self, move: str) -> bool:
        """Checks if a move is a pawn promotion."""
        move_obj = chess.Move.from_uci(move)
        piece = self.board.piece_at(move_obj.from_square)
        return piece and piece.piece_type == chess.PAWN and move_obj.promotion is not None

    def is_move_en_passant(self, move: str) -> tuple:
        """Checks if a move is an en passant capture and returns the captured square."""
        move_obj = chess.Move.from_uci(move)
        if self.board.is_en_passant(move_obj):
            captured_square = move_obj.to_square + (-8 if self.board.turn else 8)
            return True, chess.square_name(captured_square)
        return False, None

    def is_move_capture(self, move: str) -> bool:
        """Determines if a move captures an opponent's piece."""
        move_obj = chess.Move.from_uci(move)
        piece_at_dest = self.board.piece_at(move_obj.to_square)
        return piece_at_dest and piece_at_dest.color != self.board.turn