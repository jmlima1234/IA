import pygame
import sys
from funcs import *
import random
from pygame.locals import *


# Definição das coresWHITE = (255, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BROWN = (165, 113, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

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
idx_player_playing = random.randint(0,1)

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

def create_board(board):
    players.append(Player("Red"))
    players.append(Player("Green"))
    new_board = []
    for y, line in enumerate(board):
        new_row = []  # Create a new row for each line
        for x, cell in enumerate(line):
            if cell == " ":
                new_row.append(None)
            elif cell == "Y":
                new_row.append(Pile(None,[],(x,y)))
            elif cell == "R":
                new_row.append(Pile("Red",["Red","Green"],(x,y)))
            elif cell == "G":
                new_row.append(Pile("Green",["Green"],(x,y)))
            
            # Check if there's a pile at the current position and print its owner
            if new_row[-1]:  # If the last appended item is not None
                print(f"Iteration {x}, {y} - Cell: {cell}, Owner: {new_row[-1].owner}")
        new_board.append(new_row)  # Append the completed row to the new_board
            
    return new_board


# Função para desenhar o tabuleiro
def draw_board(screen,game_board):

    
    #print(game_board) da print de merda
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

    # Iterate over the game_board and draw the piles based on their stackedPieces
    for y, row in enumerate(game_board):
        for x, pile in enumerate(row):
            piece_x = offset_x + x * CELL_SIZE
            piece_y = offset_y + y * CELL_SIZE

            if is_within_board(x, y):
            # Draw the base of the pile
                pygame.draw.circle(screen, BROWN, (piece_x + CELL_SIZE // 2, piece_y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

            # If there is a pile and it has stacked pieces, draw them
            if pile:
                for idx, piece_color in enumerate(pile.stackedPieces):
                    color = RED if piece_color == "Red" else GREEN
                    # Calculate the rectangle position for each stacked piece
                    rect_y = piece_y + CELL_SIZE // 2 + (-20 + idx * 10)  # Adjust the Y position based on the index
                    pygame.draw.rect(screen, color, (piece_x + CELL_SIZE // 4, rect_y, CELL_SIZE // 2, CELL_SIZE // 10))

#------------------------------------------------------------------------
# FUNÇOES QUE ACRESCENTAMOS

def draw_blinking_border(screen, cell_x, cell_y, cell_size, color, blinking_on):
    if blinking_on:
        # Adjust the added radius for a closer border; reduce it for less gap
        border_radius_increase = 3  # This value adds to the radius for the border; decrease it for a closer border
        border_thickness = 3  # This is the thickness of the border; adjust as needed
        
        pygame.draw.circle(screen, color, (cell_x + cell_size // 2, cell_y + cell_size // 2), cell_size // 2 + border_radius_increase, border_thickness)

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

def draw_adjacent_borders(screen, selected_cell_x, selected_cell_y, cell_size, color, game_board):
    pile = game_board[selected_cell_y][selected_cell_x]
    if pile:
        num_steps = len(pile.stackedPieces)  # Get the number of steps based on the pile's height
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Top, right, bottom, left

        for dx, dy in directions:
            for step in range(1, num_steps + 1):
                adj_x, adj_y = selected_cell_x + step * dx, selected_cell_y + step * dy
                if 0 <= adj_x < 8 and 0 <= adj_y < 8 and is_within_board(adj_x, adj_y):
                    # Draw a border around the cell that is 'step' distance away
                    cell_x = offset_x + adj_x * cell_size
                    cell_y = offset_y + adj_y * cell_size
                    pygame.draw.circle(screen, color, (cell_x + cell_size // 2, cell_y + cell_size // 2), cell_size // 2 - 2, 4)


def is_within_board(x, y):
    # Check for the three corners on each of the four sides of the octagon.
    corners = [
        (0, 0), (0, 1), (1, 0),  # Top-left corner
        (0, 6), (0, 7), (1, 7),  # Top-right corner
        (6, 0), (7, 0), (7, 1),  # Bottom-left corner
        (6, 7), (7, 6), (7, 7)   # Bottom-right corner
    ]
    return (x, y) not in corners

def is_adjacent(clicked_cell, board_x, board_y, num_steps):
    """
    Determine if the target cell is within 'num_steps' range of the clicked cell,
    only allowing horizontal or vertical adjacency.
    """
    dx = abs(clicked_cell[0] - board_x)
    dy = abs(clicked_cell[1] - board_y)
    return (dx <= num_steps and dy == 0) or (dy <= num_steps and dx == 0)


def transfer_stack(clicked_cell, target_cell, game_board):
    """
    Transfer the stack of pieces from the clicked_cell to the target_cell.
    """
    # Get the pile objects for the clicked and target cells
    pile_from = game_board[clicked_cell[1]][clicked_cell[0]]
    pile_to = game_board[target_cell[1]][target_cell[0]]
    
    # Transfer the stack if the target pile exists
    if pile_to:
        pile_to.stackedPieces.extend(pile_from.stackedPieces)
        pile_from.stackedPieces = []    

#--------------------------------------------------------------------------------------


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

    players = [Player("Red"), Player("Green")]
    idx_player_playing = 0  # Start with the red player

    last_blink_time = pygame.time.get_ticks()
    blink_interval = 500  # milliseconds

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
        game_board = create_board(board)
        draw_board(screen,game_board)  # Initially draw the board
        while game:
            # Update the current time for blinking logic
            current_time = pygame.time.get_ticks()
            if current_time - last_blink_time > blink_interval:
                blinking_on = not blinking_on
                last_blink_time = current_time
                # Redraw the board and blinking border with every blink toggle
                draw_board(screen,game_board)
                if clicked_cell:
                    piece_x, piece_y = clicked_cell
                    cell_x = offset_x + piece_x * CELL_SIZE
                    cell_y = offset_y + piece_y * CELL_SIZE
                    draw_blinking_border(screen, cell_x, cell_y, CELL_SIZE, WHITE, blinking_on)
                    draw_adjacent_borders(screen, clicked_cell[0], clicked_cell[1], CELL_SIZE, BLUE,game_board)  # Keep adjacent borders visible
                pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    mouse_pos = pygame.mouse.get_pos()
                    board_x, board_y = get_board_position(mouse_pos, offset_x, offset_y, CELL_SIZE)
                    clicked_pile = game_board[board_y][board_x] if piece_at_click(board, board_x, board_y) else None
                    
                    # If we already have a clicked cell, we're attempting to move the piece
                    if clicked_cell:
                        # Check if the target pile exists or the move is to an empty space
                        if clicked_pile or not game_board[board_y][board_x]:
                            current_pile = game_board[clicked_cell[1]][clicked_cell[0]]
                            if is_adjacent(clicked_cell, board_x, board_y, len(current_pile.stackedPieces)):
                                # Transfer the stack and switch turns only if the target is empty or the move is onto an opponent's pile
                                if not clicked_pile or clicked_pile.owner != players[idx_player_playing].color:
                                    transfer_stack(clicked_cell, (board_x, board_y), game_board)
                                    idx_player_playing = 1 - idx_player_playing  # Switch turns
                                # Deselect the pile
                                clicked_cell = None
                        else:
                            # Deselect the current pile if the same cell is clicked again
                            clicked_cell = None if clicked_cell == (board_x, board_y) else clicked_cell
                    # If we don't have a clicked cell yet, we're selecting a piece
                    else:
                        # Proceed if the pile exists and belongs to the current player
                        if clicked_pile and clicked_pile.owner == players[idx_player_playing].color:
                            clicked_cell = (board_x, board_y)

                    # Redraw the board after any action
                    draw_board(screen, game_board)
                    if clicked_cell:
                        # Highlight the selected cell with a blinking border and draw adjacent borders
                        draw_blinking_border(screen, offset_x + board_x * CELL_SIZE, offset_y + board_y * CELL_SIZE, CELL_SIZE, WHITE, blinking_on)
                        draw_adjacent_borders(screen, clicked_cell[0], clicked_cell[1], CELL_SIZE, BLUE, game_board)
                    
                    # Update the display after handling the event
                    pygame.display.flip()

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
                # Recalculate piece_x and piece_y based on clicked_cell
                piece_x = offset_x + clicked_cell[0] * CELL_SIZE
                piece_y = offset_y + clicked_cell[1] * CELL_SIZE
                draw_blinking_border(screen, piece_x, piece_y, CELL_SIZE, WHITE, blinking_on)
            pygame.display.flip()  # Update the display

            clock.tick(60)  # Assuming you're calling this every frame
            if pygame.time.get_ticks() // 500 % 2 == 0:  # Toggle every half second
                blinking_on = not blinking_on

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
