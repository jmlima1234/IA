import pygame
import sys
from funcs import Piece, Player
import random


# Definição das coresWHITE = (255, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BROWN = (165, 113, 100)
BLACK = (0, 0, 0)

LEFT = 1
RIGHT = 3

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

clicked_cell = None  # This will hold the (x, y) of the last clicked cell
blinking_on = True


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

# Função para desenhar o tabuleiro
def draw_board(screen):
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
                print("COORDINATE x 1st piece:", piece_x)
                piece_y = offset_y + y * CELL_SIZE
                print("COORDINATE y 1st piece:", piece_y)
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

                piece_x = offset_x + x * CELL_SIZE
                piece_y = offset_y + y * CELL_SIZE
                pygame.draw.rect(screen, color, (piece_x + CELL_SIZE // 4, piece_y + CELL_SIZE // 2 + 24, CELL_SIZE // 2, CELL_SIZE // 10))


def draw_blinking_border(screen, cell_x, cell_y, cell_size, color):
    global blinking_on
    if blinking_on:
        pygame.draw.circle(screen, color, (cell_x + cell_size // 2, cell_y + cell_size // 2), cell_size // 2, 10)

def remove_border(screen, piece_x, piece_y, cell_size, color):
    pygame.draw.circle(screen, color, (cell_x + cell_size // 2, cell_y + cell_size // 2), cell_size // 2, 10)



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
    global clicked_cell, blinking_on, blink_timer
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    board_x, board_y = get_board_position(mouse_pos, offset_x, offset_y, CELL_SIZE)
                    if piece_at_click(board, board_x, board_y):
                        print(f"A piece was clicked at {board_x}, {board_y}")
                        if (clicked_cell != None):
                            remove_border(screen, board_x, board_y, CELL_SIZE, BLACK)
                        clicked_cell = (board_x, board_y)
                        if clicked_cell:
                            board_x, board_y = clicked_cell
                            piece_x = offset_x + board_x * CELL_SIZE
                            piece_y = offset_y + board_y * CELL_SIZE
                            draw_blinking_border(screen, piece_x, piece_y, CELL_SIZE, WHITE)  # WHITE for the border

                            pygame.display.flip()  # Update the display

                            
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
            if clicked_cell:
                cell_x, cell_y = clicked_cell
                piece_x = offset_x + cell_x * CELL_SIZE
                piece_y = offset_y + cell_y * CELL_SIZE
                draw_blinking_border(screen, piece_x, piece_y, CELL_SIZE, WHITE)  # WHITE for the border

            pygame.display.flip()  # Update the display

            clock.tick(60)  # Assuming you're calling this every frame
            if pygame.time.get_ticks() // 500 % 2 == 0:  # Toggle every half second
                blinking_on = not blinking_on

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
