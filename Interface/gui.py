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
        # Map for chess pieces to corresponding PNG filenames
        piece_to_png = {
            "r": "black-rook.png", "n": "black-knight.png", "b": "black-bishop.png",
            "q": "black-queen.png", "k": "black-king.png", "p": "black-pawn.png",
            "R": "white-rook.png", "N": "white-knight.png", "B": "white-bishop.png",
            "Q": "white-queen.png", "K": "white-king.png", "P": "white-pawn.png",
        }

        piece_images = {}
        for piece, filename in piece_to_png.items():
            # Load PNG files from assets folder
            png_path = f"assets/{filename}"
            image = pygame.image.load(png_path)
            piece_images[piece] = pygame.transform.scale(image, (self.square_size, self.square_size))
        return piece_images

    def setup_screen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Chess GUI")
        self.draw_board()
        self.update_pieces()
        pygame.display.flip()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        col * self.square_size,
                        row * self.square_size,
                        self.square_size,
                        self.square_size,
                    ),
                )

    def update_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col, row = chess.square_file(square), chess.square_rank(square)
                x = col * self.square_size
                y = (7 - row) * self.square_size
                self.screen.blit(self.piece_images[piece.symbol()], (x, y))

    def run(self):
        self.setup_screen()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    def update(self):
        self.draw_board()
        self.update_pieces()
        pygame.display.flip()
