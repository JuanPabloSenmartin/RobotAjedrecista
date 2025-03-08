import pygame
import chess

class ChessGUI:
    def __init__(self, board):
        self.board = board
        self.square_size = 80
        self.window_size = self.square_size * 8
        self.colors = [pygame.Color(240, 217, 181), pygame.Color(181, 136, 99)]
        self.piece_images = self.load_piece_images()
        self.screen = None

    def load_piece_images(self):
        """Load chess piece images and scale them to fit the squares."""
        piece_to_png = {
            "r": "black-rook.png", "n": "black-knight.png", "b": "black-bishop.png",
            "q": "black-queen.png", "k": "black-king.png", "p": "black-pawn.png",
            "R": "white-rook.png", "N": "white-knight.png", "B": "white-bishop.png",
            "Q": "white-queen.png", "K": "white-king.png", "P": "white-pawn.png",
        }
        return {
            piece: pygame.transform.scale(
                pygame.image.load(f"assets/{filename}"),
                (self.square_size, self.square_size)
            ) for piece, filename in piece_to_png.items()
        }

    def setup_screen(self):
        """Initialize the Pygame window and draw the board."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Chess GUI")
        self.update()

    def draw_board(self):
        """Draw the chessboard grid."""
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(
                    self.screen,
                    self.colors[(row + col) % 2],
                    pygame.Rect(
                        col * self.square_size,
                        row * self.square_size,
                        self.square_size,
                        self.square_size,
                    ),
                )

    def update_pieces(self):
        """Draw the chess pieces on the board based on the current game state."""
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                x, y = chess.square_file(square) * self.square_size, (7 - chess.square_rank(square)) * self.square_size
                self.screen.blit(self.piece_images[piece.symbol()], (x, y))

    def run(self):
        """Main loop for handling events and updating the display."""
        self.setup_screen()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    def update(self):
        """Redraw the board and pieces."""
        self.draw_board()
        self.update_pieces()
        pygame.display.flip()
