import pygame
import re

# Dimensions

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900

SQUARE_WIDTH = WINDOW_WIDTH // 3
SQUARE_HEIGHT = WINDOW_HEIGHT // 3

CELL_WIDTH = WINDOW_WIDTH // 9
CELL_HEIGHT = WINDOW_HEIGHT // 9

# Colors

BLACK = (0, 0, 0)
GREY = (230, 230, 230)
WHITE = (255, 255, 255)

RED = (250, 30, 5)
GREEN = (5, 250, 30)

# Font

FONT_SIZE = 40

pygame.font.init()
font = pygame.font.SysFont('comicsansms', FONT_SIZE)

# Board basics

ROWS = 9
COLS = 9

BORDER_COLOR = BLACK

class Board:

    # GUI

    BORDER_COLOR = BORDER_COLOR
    BORDER_WIDTH = 10

    # Solver

    rows = [[0] * (ROWS + 1) for _ in range(ROWS + 1)]
    cols = [[0] * (COLS + 1) for _ in range(COLS + 1)]
    boxes = [[0] * (ROWS + 1) for _ in range(ROWS + 1)]

    completed = False

    def __init__(self, board):

        self.cells = list()
        self.squares = list()

        for row in range(ROWS):

            board_row = list()
            
            for col in range(COLS):

                num = board[row][col]
                
                cell = Cell(col * CELL_WIDTH, row * CELL_HEIGHT, num)
                
                board_row.append(cell)

                if num != 0:

                    self.place_initial_number(row, col, num)

                if row % 3 == 0 and col % 3 == 0:
                    
                    square = Square(col * CELL_WIDTH, row * CELL_HEIGHT)
                    self.squares.append(square)

            self.cells.append(board_row)
        
        self.draw()
        
    def draw(self):

        for board_row in self.cells:
            for cell in board_row:
                cell.draw()
        
        for square in self.squares:
            square.draw()
        
        board = pygame.Rect((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.draw.rect(window, self.BORDER_COLOR, board, self.BORDER_WIDTH)

        pygame.display.update()

    def can_place_number(self, row, col, num):
        
        return not (
            self.rows[row][num] or
            self.cols[col][num] or
            self.boxes[row // 3 * 3 + col // 3][num]
        )
    
    def place_initial_number(self, row, col, num):

        self.rows[row][num] = 1
        self.cols[col][num] = 1
        self.boxes[row // 3 * 3 + col // 3][num] = 1

    def place_number(self, row, col, num):

        self.rows[row][num] = 1
        self.cols[col][num] = 1
        self.boxes[row // 3 * 3 + col // 3][num] = 1

        self.cells[row][col].place_number(num)

        self.draw()

        pygame.event.pump()
        pygame.time.delay(150)

    def remove_number(self, row, col, num):

        self.rows[row][num] = 0
        self.cols[col][num] = 0
        self.boxes[row // 3 * 3 + col // 3][num] = 0

        self.cells[row][col].remove_number()

        self.draw()

        pygame.event.pump()
        pygame.time.delay(150)

    def place_next_number(self, row, col):

        if row == ROWS - 1 and col == COLS - 1:
            self.completed = True
            return
        
        if col == COLS - 1:
            self.backtrack(row + 1, 0)
        else:
            self.backtrack(row, col + 1)

    def backtrack(self, row, col):

        if self.cells[row][col].value == 0:

            for num in range(1, 10):

                if self.can_place_number(row, col, num):

                    self.place_number(row, col, num)

                    self.place_next_number(row, col)

                    if self.completed:

                        return
                    
                    self.remove_number(row, col, num)

        else:

            self.place_next_number(row, col)

    def solve(self):

        self.backtrack(0, 0)

class Square:

    BORDER_COLOR = BORDER_COLOR
    BORDER_WIDTH = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def draw(self):

        square = pygame.Rect((self.x, self.y), (SQUARE_WIDTH, SQUARE_HEIGHT))
        pygame.draw.rect(window, self.BORDER_COLOR, square, self.BORDER_WIDTH)

class Cell:

    BORDER_COLOR = BORDER_COLOR
    BORDER_WIDTH = 2

    FILL_COLOR = WHITE

    def __init__(self, x, y, value):

        self.x = x
        self.y = y

        self.value = value

        if self.value:
            self.FILL_COLOR = GREY

    def place_number(self, value):
        
        self.FILL_COLOR = GREEN
        self.value = value
    
    def remove_number(self):

        self.FILL_COLOR = RED
        self.value = 0

    def draw(self): 

        fill = pygame.Rect((self.x, self.y), (CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(window, self.FILL_COLOR, fill)

        if self.value:

            text = font.render(str(self.value), 1, BLACK)
            text_cell = text.get_rect(center=fill.center)

            window.blit(text, text_cell)

        cell = pygame.Rect((self.x, self.y), (CELL_WIDTH, CELL_HEIGHT))
        pygame.draw.rect(window, self.BORDER_COLOR, cell, self.BORDER_WIDTH)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill(WHITE)

def load_board(filename):

    with open(filename, "r") as file:
        lines = file.readlines()

    sudoku_board = list()

    for line in lines:

        sudoku_board_row = list()

        for num in line.split(", "):

            sudoku_board_row.append(int(re.sub(r"\s", "", num)))

        sudoku_board.append(sudoku_board_row)

    return sudoku_board

sudoku_board = load_board("sudoku_board.txt")

print(sudoku_board)

board = Board(sudoku_board)
board.solve()

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
quit()