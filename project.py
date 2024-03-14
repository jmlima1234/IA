import pygame
import sys
from funcs import *
import random

#coisas que estou a testar
selected_piece = None  # Stores the coordinates of the selected piece as (x, y), or None if no piece is selected



#coisas que estou a testar


# Definição das coresWHITE = (255, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BROWN = (165, 113, 100)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Define yellow color

offset_x = 20
offset_y = 20
# Dimensões do tabuleiro
WIDTH = 800
HEIGHT = 800
CELL_SIZE = (WIDTH-40) // 8  # Tamanho de cada célula do tabuleiro

#Peças do tabuleiroF
green_pieces = []
red_pieces = []

#Jogadores
players = []
idx_player_playing = random.randint(1,2)

# Representação do tabuleiro
board = [
    [" "," ", "Y", "Y", "Y", "Y"," "," "],
    [" ", "R", "R", "G", "G", "R", "R"," "],
    ["Y","G", "G", "R", "R", "G", "G","Y",],
    ["Y","R", "R", "G", "G", "R","R","Y"],
    ["Y","G", "G", "R", "R", "G", "G","Y",],
    ["Y","R", "R", "G", "G", "R","R","Y"],
    [" ","G", "G", "R", "R", "G", "G"," "],
    [" "," ", "Y", "Y", "Y", "Y"," "," "]
]

def create_board(board):
    new_board = []
    x = 0
    y =0 
    for line in board:
        for cell in line:
            new_board.append([])  # Append an empty list for each line

            if cell == " ":
                new_board[x].append(None)

            elif cell == "Y":
                new_board[x].append(Pile(None,[],(x,y)))

            elif cell == "R":
                new_board[x].append(Pile("Red",["Red"],(x,y)))

            elif cell == "G":
                new_board[x].append(Pile("Green",["Green"],(x,y)))
            
            print("iteration ", cell, ": ", new_board)
            x+=1
            
    return new_board

# Função para desenhar o tabuleiro
def draw_board(screen):

    game_board = create_board(board)
    print(game_board)
    # Fill the background with gray color
    screen.fill(GRAY)
    
 
    # Center the board on the screen
    

    # Draw the octagon around the centered board
    octagon_color = GRAY
    octagon_points = [
        (offset_x, offset_y + 2 * CELL_SIZE),
        (offset_x, offset_y + 6 * CELL_SIZE),
        (offset_x + 2 * CELL_SIZE, offset_y + 8 * CELL_SIZE),
        (offset_x + 6 * CELL_SIZE, offset_y + 8 * CELL_SIZE),
        (offset_x + 8 * CELL_SIZE, offset_y + 6 * CELL_SIZE),
        (offset_x + 8 * CELL_SIZE, offset_y + 2 * CELL_SIZE),
        (offset_x + 6 * CELL_SIZE, offset_y),
        (offset_x + 2 * CELL_SIZE, offset_y)
    ]
    pygame.draw.polygon(screen, BLACK, octagon_points)
    
    players.append(Player(RED))
    players.append(Player(GREEN))

    for y in range(len(board)):
        for x in range(len(board[y])):
            if (board[y][x] != " "):
                piece_x = offset_x + x * CELL_SIZE
                piece_y = offset_y + y * CELL_SIZE
                if selected_piece == (x, y):
                    pygame.draw.circle(screen, YELLOW, (piece_x, piece_y), CELL_SIZE // 2 - 3)
    
                pygame.draw.circle(screen, BROWN, (piece_x + CELL_SIZE // 2, piece_y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

    # Draw the pieces inside the octagon
    for y in range(len(board)):
        for x in range(len(board[y])):
            if (board[y][x] != " ") & (board[y][x] != "Y"):
                color = RED if board[y][x] == "R" else GREEN 
                if color == RED:
                    red_pieces.append(Piece(color,(x,y)))
                else:
                    green_pieces.append(Piece(color,(x,y)))

                 # Check if this piece is selected
                
                piece_x = offset_x + x * CELL_SIZE
                piece_y = offset_y + y * CELL_SIZE
                pygame.draw.rect(screen, color, (piece_x + CELL_SIZE // 4, piece_y + CELL_SIZE // 2 + 24, CELL_SIZE // 2, CELL_SIZE // 10))


def get_board_position(mouse_pos, offset_x, offset_y, cell_size):
    board_x = (mouse_pos[0] - offset_x) // cell_size
    board_y = (mouse_pos[1] - offset_y) // cell_size
    return board_x, board_y

def piece_at_click(board, board_x, board_y):
    if 0 <= board_x < len(board[0]) and 0 <= board_y < len(board):
        return board[board_y][board_x] != " "
    return False



def show_menu(screen):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 50)
    title_text = font.render("Welcome to the Focus Game!", True, BLACK)
    screen.blit(title_text, (150, 200))
    
    start_text = font.render("Start", True, BLACK)
    screen.blit(start_text, (350, 300))

    exit_text = font.render("Exit", True, BLACK)
    screen.blit(exit_text, (355, 400))
    
    pygame.display.flip()

# Função principal
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Focus Board")
    clock = pygame.time.Clock()

    menu = True
    mode_select = False
    difficulty_select = False
    game = True

    bot_modes = ["Player vs Player", "Player vs Bot", "Bot vs Bot"]
    difficulties = ["Easy", "Medium", "Hard"]

    bot_mode = ""
    difficulty = ""

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 350 <= mouse_pos[0] <= 450:
                    if 300 <= mouse_pos[1] <= 350:
                        menu = False
                        mode_select = True
                    elif 400 <= mouse_pos[1] <= 450:
                        pygame.quit()
                        sys.exit()

        show_menu(screen)

    while mode_select:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 50)
        title_text = font.render("Select Game Mode:", True, BLACK)
        screen.blit(title_text, (220, 200))
        
        for i, mode in enumerate(bot_modes):
            mode_text = font.render(mode, True, BLACK)
            screen.blit(mode_text, (300, 300 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 500:
                    for i, _ in enumerate(bot_modes):
                        if 300 + i * 50 <= mouse_pos[1] <= 350 + i * 50:
                            bot_mode = bot_modes[i]
                            mode_select = False
                            if "Bot" in bot_mode:
                                difficulty_select = True

    if bot_mode == "Player vs Player":
        draw_board(screen)  # Draw the board
        while (game):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    global selected_piece  # Add this lin
                    mouse_pos = pygame.mouse.get_pos()
                    board_x, board_y = get_board_position(mouse_pos, offset_x, offset_y, CELL_SIZE)
                    if piece_at_click(board, board_x, board_y):
                        print(f"A piece was clicked at {board_x}, {board_y}")
                        if selected_piece == (board_x, board_y):
                            selected_piece = None  # Deselect if the same piece is clicked again
                        else:
                            selected_piece = (board_x, board_y)  # Select the new piece
                        # Here you can add logic to handle selecting the piece,
                        # moving it, or whatever action is appropriate for your game.
            pygame.display.flip()  # Update the display

    while difficulty_select:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 50)
        title_text = font.render("Select Difficulty:", True, BLACK)
        screen.blit(title_text, (250, 200))
        
        for i, diff in enumerate(difficulties):
            diff_text = font.render(diff, True, BLACK)
            screen.blit(diff_text, (350, 300 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 350 <= mouse_pos[0] <= 450:
                    for i, _ in enumerate(difficulties):
                        if 300 + i * 50 <= mouse_pos[1] <= 350 + i * 50:
                            difficulty = difficulties[i]
                            difficulty_select = False
    
    if (difficulty != "") & game:
        draw_board(screen)  # Draw the board
        while (game):
            pygame.display.flip()  # Update the display

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
