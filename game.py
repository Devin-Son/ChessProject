import numpy as np
from config import *
from game import *
import pygame.gfxdraw as gfxdraw
from math import floor

board = None

class Piece:
    def __init__(self, color: str, piece_type: str, coordinate: str, board: 'Board'):
        self.color = color
        self.piece_type = piece_type
        self.coordinate = coordinate
        self.position = ord(coordinate[0]) - 97, int(coordinate[1]) - 1 # x, y of piece
        self.board = board
        self.clicked = False
        self.piece_path = 'resources/pieces/'

    def __str__ (self) -> str:
        return f"{self.piece_type}{self.coordinate}"

    def check_obstruction(self, start_x: int, start_y: int, direction_x: int, direction_y: int, range_limit: int) -> list[str]:
        steps = 0
        while range_limit == None or steps < range_limit:
            if start_y + (direction_y * (steps + 1)) >= COLUMNS or start_x + (direction_x * (steps + 1)) >= ROWS:
                return steps
            elif self.board.board[start_y + (direction_y * (steps + 1))][start_x + (direction_x * (steps + 1))] == None:
                steps += 1
            else:
                return steps
            
        return steps

class Pawn(Piece):
    def __init__(self, color: str, coordinate: str, board: 'Board'):
        super().__init__(color, '', coordinate, board)
        self.visual = 'P'

    def name(self):
        return 'pawn'

    def legal_moves(self) -> list[str]:
        moves = []
        direction = [0, 1] if self.color == 'white' else [0, -1]
        
        # Vertical moves
        if self.check_obstruction(self.position[0], self.position[1], 0, direction[1], 1) > 0:                                 # 1 space 
            moves.append(f"{chr(self.position[0] + 97)}{int(self.coordinate[1]) + direction[1]}")
            if (self.check_obstruction(self.position[0], self.position[1], 0, direction[1], 2) > 1 and                         # 2 spaces
                ((self.color == 'white' and self.position[1] == 1) or (self.color == 'black' and self.position[1] == 6))):        # Has not moved
                moves.append(f"{chr(self.position[0] + 97)}{int(self.coordinate[1]) + 2 * direction[1]}")

        # Capture moves
        direction[0] = [-1, 1]

        for capture_x in direction[0]:
            try:
                if (self.check_obstruction(self.position[0], self.position[1], capture_x, direction[1], 1) == 0 and            # Obstructed diagonally
                    (self.board.board[self.position[1] + direction[1]][self.position[0] + capture_x]).color != self.color and  # Opposite color
                    (self.position[1] + direction[1]) >= 0 and (self.position[0] + capture_x) >= 0):                           # On board
                    moves.append(f"{chr(self.position[0] + 97)}x{chr(self.position[0] + 97 + capture_x)}{int(self.coordinate[1]) + direction[1]}")
            except:
                continue

        return moves

class Rook(Piece):
    def __init__(self, color: str, coordinate: str, board: 'Board'):
        super().__init__(color, 'R', coordinate, board)
        self.visual = 'R'

    def name(self):
        return 'rook'

    def legal_moves(self):
        moves = []
        direction = [[0, 1], [-1, 0], [0, -1], [1, 0]]
        

        # Moves
        for current_direction in direction:
            available_distance = self.check_obstruction(self.position[0], self.position[1], current_direction[0], current_direction[1], None)
            for step in range(available_distance):
                moves.append(f"{chr(self.position[0] + (97 + (step + 1) * current_direction[0]))}"
                             f"{int(self.coordinate[1]) + ((step + 1) * current_direction[1])}")
            # Captures
            positions = self.board.get_pieces_of_type(self.color, self.visual)
            try:
                if (self.board.board[self.position[1] + (current_direction[1] * (available_distance + 1))]
                                    [self.position[0] + (current_direction[0] * (available_distance + 1))].color != self.color):

                    # TODO distuingish captures if two rooks in same column (Rhxd3) or same row (R3xa5). If two rooks can take same piece but
                    # not in same row or column, distinguish by column. Assume that there can be any amount of rooks on the board.

                    moves.append(f"Rx{chr(self.position[0] + (current_direction[0] * (available_distance + 1)) + 97)}"
                                 f"{int(self.position[1] + (current_direction[1] * (available_distance + 1)) + 1)}")
            except:
                continue



        return moves

class Knight(Piece):
    def __init__(self, color: str, coordinate, board: 'Board'):
        super().__init__(color, 'N', coordinate, board)
        self.visual = 'N'

    def name(self):
        return 'knight'

    def legal_moves(self):
        moves = []

        return moves

class Bishop(Piece):
    def __init__(self, color: str, coordinate, board: 'Board'):
        super().__init__(color, 'B', coordinate, board)
        self.visual = 'B'

    def name(self):
        return 'bishop'

    def legal_moves(self):
        moves = []

        return moves

class Queen(Piece):
    def __init__(self, color: str, coordinate, board: 'Board'):
        super().__init__(color, 'Q', coordinate, board)
        self.visual = 'Q'

    def name(self):
        return 'queen'

    def legal_moves(self):
        moves = []

        return moves

class King(Piece):
    def __init__(self, color: str, coordinate, board: 'Board'):
        super().__init__(color, 'K', coordinate, board)
        self.visual = 'K'

    def name(self):
        return 'king'

    def legal_moves(self):
        moves = []

        return moves

class Board:
    def __init__(self, size: tuple[int, int], game):
        try:
            self.size = size
            self.board = np.full((size[1], size[0]), None)
            self.setup_pieces()
            self.DISPLAYSURF = game.DISPLAYSURF
            self.square_size = int(0.9 * game.SCREEN_HEIGHT) // 8
            self.board_dimension = self.square_size * 8
            self.board_surface = pg.Surface((self.board_dimension, self.board_dimension))
            self.board_surface.fill((255, 255, 255))
            self.color_theme = COLOR_THEME[0]
            self.clicked_piece_position = None
            self.game = game
        except:
            pass

    def setup_pieces(self):
        piece_classes = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for color, row_pawn, row_back in [('white', 1, 0), ('black', 6, 7)]:
            # Pawns
            for x in range(8):
                self.place_piece(Pawn(color, f'{chr(x + 97)}{row_pawn + 1}', self))

            # Back row
            for x, piece_class in enumerate(piece_classes):
                self.place_piece(piece_class(color, f'{chr(x + 97)}{row_back + 1}', self))

    def place_piece(self, piece: Piece):
        x, y = piece.position
        self.board[y, x] = piece

    def get_piece_at(self, coordinate: str) -> Piece:
        x, y = ord(coordinate[0].lower()) - 97, int(coordinate[1]) - 1
        return self.board[y, x] if 0 <= x < self.size[0] and 0 <= y < self.size[1] else None
    
    def get_pieces_of_type(self, color: str, type: str) -> list:
        positions = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                checking = self.board[row][column]
                if checking:
                    if checking.visual == type and checking.color == color:
                        position = checking.position[1], checking.position[0]
                        positions.append(position)
        return positions

    # Console display of board
    def display(self): 
        for y in range(self.size[1] - 1, -1, -1):
            row = ''
            for x in range(self.size[0]):
                coordinate = f'{chr(x + 97)}{y + 1}'
                piece = self.get_piece_at(coordinate)
                if not piece:
                    row += " .  "
                elif piece.piece_type == '':
                    row += " " + str(piece) + ' '
                else:
                    row += str(piece) + ' '
            print(row)

    # Window display of board
    def show_board(self, game):
        # Print squares
        toggle = False
        for rows in range(ROWS):
            toggle = not toggle
            for columns in range(COLUMNS):
                if toggle:
                    pg.draw.rect(self.board_surface, self.color_theme[0], (self._get_screen_coord_rect(columns, rows)))
                else:
                    pg.draw.rect(self.board_surface, self.color_theme[1], (self._get_screen_coord_rect(columns, rows)))
                toggle = not toggle
                self._update(game)

    # Draw pieces
    def show_pieces(self, game):
        for rows in range(len(self.board)):
            for columns in range(len(self.board[rows])):
                if self.board[rows][columns] != None:
                    piece = self.board[rows][columns]
                    piece_image = pg.image.load(f'{piece.piece_path}{piece.color}/{piece.name()}.png')
                    scale_factor = self.square_size / PIECE_SCALE
                    orig_width, orig_height = piece_image.get_size()
                    new_width = int(orig_width * scale_factor)
                    new_height = int(orig_height * scale_factor)
                    piece_image = pg.transform.smoothscale(piece_image, (new_width, new_height))

                
                    self.board_surface.blit(piece_image, self._get_screen_coord_rect(columns, 7 - rows))
                self._update(game)

    # Check if a piece has been clicked
    def get_click(self, mouse_pos, game):
        board_x = (game.SCREEN_WIDTH - self.board_dimension) // 2
        board_y = (game.SCREEN_HEIGHT - self.board_dimension) // 2

        if board_x <= mouse_pos[0] <= board_x + self.board_dimension and board_y <= mouse_pos[1] <= board_y + self.board_dimension: # Is the mouse on the board?
            col = int(floor((mouse_pos[0] - board_x) // self.square_size))
            row = int(floor((mouse_pos[1] - board_y) // self.square_size))
            board_row = int(floor(ROWS - 1 - row))
            
            clicked_piece = self.board[board_row][col]

            if clicked_piece:
                if (board_row, col) == self.clicked_piece_position:        # Unclick
                    clicked_piece.clicked = False
                    self.clicked_piece_position = None
                    return
                else:                                                      # Clicked piece
                    clicked_piece.clicked = True
                    self.clicked_piece_position = (board_row, col)
                    return
            else:                                                          # Empty
                return
 
    
    # Print legal moves
    def show_legal(self):
        if self.clicked_piece_position:
            piece = self.board[self.clicked_piece_position[0]][self.clicked_piece_position[1]]
            for move in piece.legal_moves():
                real_move = move[-3:]
                if real_move[0] != 'x':
                    real_move = ord(real_move[-2]) - 97, int(real_move[-1]) - 1
                    rect = self._get_screen_coord_rect(real_move[-2], (7 - real_move[-1]))
                    circle_radius = int((self.square_size * CIRCLE_SCALE) // 2)
                    center_x = rect[0] + (rect[2] // 2)  
                    center_y = rect[1] + (rect[3] // 2)
                    gfxdraw.filled_circle(self.board_surface, center_x, center_y, circle_radius, (0, 0, 0, 40))
                else:
                    real_move = ord(real_move[-2]) - 97, int(real_move[-1]) - 1
                    rect = self._get_screen_coord_rect(real_move[-2], (7 - real_move[-1]))
                    circle_radius = int((self.square_size * (CIRCLE_SCALE * 3.36)) // 2)
                    center_x = rect[0] + (rect[2] // 2)  
                    center_y = rect[1] + (rect[3] // 2)
                    temp_surface = pg.Surface(self.board_surface.get_size(), pg.SRCALPHA)
                    outline_thickness = int(circle_radius // 7)
                    pg.draw.circle(temp_surface, (0, 0, 0, 40), (center_x, center_y), circle_radius, outline_thickness)
                    self.board_surface.blit(temp_surface, (0, 0))

            self._update(self.game)
        

    def _get_screen_coord_rect(self, columns, rows):
        return ((columns * (self.board_dimension // COLUMNS)), (rows * (self.board_dimension // ROWS)), 
                (self.board_dimension // COLUMNS), (self.board_dimension // ROWS))

    def resize(self, screen_width, screen_height):
        self.square_size = int(0.9 * screen_height) // 8
        self.board_dimension = self.square_size * 8
        self.board_surface = pg.Surface((self.board_dimension, self.board_dimension))
        self.board_surface.fill((255, 255, 255))
        self.show_board(self.game)
        self.show_pieces(self.game)

    def _update(self, game):
        self.DISPLAYSURF.blit(self.board_surface, ((game.SCREEN_WIDTH - self.board_dimension) // 2, (game.SCREEN_HEIGHT - self.board_dimension) // 2)) # Board surface

if __name__ == '__main__':
    board = Board(BOARD_SIZE, None)
    board.place_piece(Rook('black', 'h6', board))
    board.place_piece(Pawn('white', 'a6', board))
    board.display()
    piece = board.get_piece_at(input("What piece would you like to see the available moves for? "))
    if piece:
        print(piece.legal_moves())
    else:
        print("Empty space")