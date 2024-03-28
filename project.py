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
ORANGE = (255, 165, 0)
SILVER = (165, 169, 180)
DARK_GRAY = (50, 50, 50)

LEFT = 1
RIGHT = 3

offset_x = 20
offset_y = 20
# Dimensões do tabuleiro
WIDTH = 800
HEIGHT = 800
CELL_SIZE = (WIDTH-40) // 8  # Tamanho de cada célula do tabuleiro
# Position and radius for the reserve piece circle
RESERVE_CIRCLE_CENTER = (70, 730)
RESERVE_CIRCLE_RADIUS = CELL_SIZE // 2 + 10

#Peças do tabuleiroF
green_pieces = []
red_pieces = []

#Jogadores
players = []
idx_player_playing = random.randint(0,1)

clicked_cell = None  # This will hold the (x, y) of the last clicked cell
blinking_on = True

bot_modes = ["Player vs Player", "Player vs Bot", "Bot vs Bot"]
difficulties = ["Easy", "Medium", "Hard"]

game_board = []
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
                new_row.append(Pile("Red",["Red"],(x,y)))
            elif cell == "G":
                new_row.append(Pile("Green",["Green"],(x,y)))
            
            # Check if there's a pile at the current position and print its owner
            if new_row[-1]:  # If the last appended item is not None
                print(f"Iteration {x}, {y} - Cell: {cell}, Owner: {new_row[-1].owner}")
        new_board.append(new_row)  # Append the completed row to the new_board
            
    return new_board


# Função para desenhar o tabuleiro
def draw_board(screen, board):
    global idx_player_playing
    # Fill the background with gray color
    screen.fill(GRAY)

    player_color = RED if players[idx_player_playing].get_color() == "Red" else GREEN

    # Draw the player information in the top left corner
    font = pygame.font.SysFont(None, 25)
    player_text = font.render(f"Player: {players[idx_player_playing].get_color()}", True, player_color)
    reserved_text = font.render(f"Reserve Pieces: {players[idx_player_playing].get_reserve_pieces()}", True, player_color)
    captured_text = font.render(f"Captured Pieces: {players[idx_player_playing].get_captured_pieces()}", True, player_color)

    # Draw the reserve piece
    pygame.draw.circle(screen, ORANGE, (70, 730), RESERVE_CIRCLE_RADIUS)
    use_reserve_text= font.render("Use Reserve", True, BLACK)
    piece_text= font.render("Piece", True, BLACK)

    screen.blit(player_text, (10, 10))
    screen.blit(reserved_text, (630, 10))
    screen.blit(captured_text, (630, 40))
    screen.blit(use_reserve_text, (20, 720))
    screen.blit(piece_text, (50, 740))

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

    # Iterate over the game_board and draw the piles based on their stackedPieces
    for y, row in enumerate(board):
        for x, pile in enumerate(row):
            piece_x = offset_x + x * CELL_SIZE
            piece_y = offset_y + y * CELL_SIZE

            if is_within_board(x, y):
                # Draw the base of the pile
                pygame.draw.circle(screen, BROWN, (piece_x + CELL_SIZE // 2, piece_y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            
            # If there is a pile and it has stacked pieces, draw them
            if pile:
                for idx, piece_color in enumerate(pile.get_stack()):
                    color = RED if piece_color == "Red" else GREEN
                    pos = idx * (CELL_SIZE // 10) 
                    # Calculate the rectangle position for each stacked piece
                    pygame.draw.rect(screen, color, (piece_x + CELL_SIZE // 4, piece_y + CELL_SIZE // 2 + 24 - pos , CELL_SIZE // 2, CELL_SIZE // 10))


def draw_endgame_screen(screen, result):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 50)
    print(result)
    if result['winner'] == 'Red':
        title_text = font.render("Player RED wins the game!", True, RED)
    else: 
        title_text = font.render("Player GREEN wins the game!", True, GREEN)

    screen.blit(title_text, (150, 200))
    
    start_text = font.render("Play Again", True, BLACK)
    screen.blit(start_text, (350, 300))

    mainmenu_text = font.render("Return to Main Menu", True, BLACK)
    screen.blit(mainmenu_text, (355, 400))
    
    exit_text = font.render("Exit", True, BLACK)
    screen.blit(exit_text, (360, 500))

    pygame.display.flip()

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
    # Check if click is on the reserve piece
    dx = mouse_pos[0] - RESERVE_CIRCLE_CENTER[0]
    dy = mouse_pos[1] - RESERVE_CIRCLE_CENTER[1]
    if dx**2 + dy**2 <= RESERVE_CIRCLE_RADIUS**2:
        return "RESERVE", None  # Special value indicating a click on the reserve piece

    # Original code for board position calculation
    board_x = (mouse_pos[0] - offset_x) // cell_size
    board_y = (mouse_pos[1] - offset_y) // cell_size
    return board_x, board_y


def piece_at_click(board, board_x, board_y):
    if 0 <= board_x < len(board[0]) and 0 <= board_y < len(board):
        return board[board_y][board_x] != " "
    return False

def draw_borders_for_empty_cells(screen, cell_size, color, game_board):
    # Iterate over the entire board
    for y, row in enumerate(game_board):
        for x, pile in enumerate(row):
            # Check if the cell is within the playable area and has no owner
            if is_within_board(x, y) and pile and pile.owner is None:
                # Draw a border around the cell
                cell_x = offset_x + x * cell_size
                cell_y = offset_y + y * cell_size
                pygame.draw.circle(screen, color, (cell_x + cell_size // 2, cell_y + cell_size // 2), cell_size // 2 - 2, 4)


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
    
    game_board[clicked_cell[1]][clicked_cell[0]] = Pile(None,[],pile_from.get_coordinates())
    game_board[target_cell[1]][target_cell[0]] = pile_to.join_pieces(pile_from, pile_to, players)

def check_win_conditions(players, game_board):
    result = {"has_winner": False, "winner": None, "reason": ""}
    # Check if any player has captured 6 or more of the opponent's pieces
    for player in players:
        # Determine the opponent player
        opponent = next(p for p in players if p != player)
        if opponent.get_captured_pieces() >= 6:
            print(f"{player.get_color()} wins because the opponent has captured 6 or more pieces!")
            result.update({
                "has_winner": True,
                "winner": player.get_color(),
                "reason": f"{player.get_color()} wins because the opponent has captured 6 or more pieces."
            })
            return result


    # Check for empty spaces on the board
    board_has_empty_spaces = any(pile is None for row in game_board for pile in row)

    # Check if a player can no longer make any moves
    for player in players:
        player_has_moves = any(
            pile.owner == player.get_color() for row in game_board for pile in row if pile
        ) or (player.get_reserve_pieces_count() > 0 and board_has_empty_spaces(game_board))

        if not player_has_moves:
            # Determine the opponent player
            opponent = next(p for p in players if p != player)
            print(f"{opponent.get_color()} wins because {player.get_color()} has no moves left!")
            result.update({
                "has_winner": True,
                "winner": opponent.get_color(),
                "reason": f"{opponent.get_color()} wins because {player.get_color()} has no moves left."
            })
            return result

    return result

def board_has_empty_spaces(game_board):
    for row in game_board:
        if any(pile.owner is None for pile in row):
            return True
    return False

def can_put_reserve_piece(player,piece):    
    if player.get_reserve_pieces_count() > 0:
        if(piece.owner == None):
            return True
        return False
    return False


#--------------------------------------------------------------------------------------
def render_3d_text(surface, text, font, color, offset_color, position, depth):
    text_surface = font.render(text, True, color)
    offset_surface = font.render(text, True, offset_color)

    for i in range(depth, 0, -1):
        surface.blit(offset_surface, (position[0] + i, position[1] + i))

    surface.blit(text_surface, position)

def show_menu(screen):
    screen.fill(WHITE)
    pygame.font.init()
    font = pygame.font.SysFont('arial', 48, bold=True)
    font_bold = pygame.font.SysFont('arial', 24, bold=True)
    font_large_bold = pygame.font.SysFont('Times New Roman', 120, bold=True)
    
    # intro_text = font_bold.render("Welcome to", True, BLACK)
    # screen.blit(intro_text, (300,50))

    render_3d_text(screen, "Welcome to", font_bold, BLACK, BLACK, (320,50), depth=1)
    
    render_3d_text(screen, "FOCUS", font_large_bold, SILVER, DARK_GRAY, (200, 100), depth=5)

    render_3d_text(screen, "Start", font, BLACK, BLACK, (320,300), depth=1)

    render_3d_text(screen, "Exit", font, BLACK, BLACK, (320,400), depth=1)
    
    pygame.display.flip()

def menu_state(screen):
    
    show_menu(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 320 <= mouse_pos[0] <= 450:
                if 300 <= mouse_pos[1] <= 350:
                    return {"next_state": "mode_select"}
                elif 400 <= mouse_pos[1] <= 450:
                    pygame.quit()
                    sys.exit()
    return {"next_state": "menu"}

def mode_select_state(screen):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 50)
    title_text = font.render("Select Game Mode:", True, SILVER)
    screen.blit(title_text, (220, 200))

    for i, mode in enumerate(bot_modes):
        mode_text = font.render(mode, True, BLACK)
        screen.blit(mode_text, (300, 300 + i * 50))

    option = font.render("Return to Main Menu", True, SILVER)
    screen.blit(option, (220, 500))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            if 300 <= mouse_pos[0] <= 500:
                for i, _ in enumerate(bot_modes):
                    if 300 + i * 50 <= mouse_pos[1] <= 350 + i * 50:
                        bot_mode = bot_modes[i]
                        if "Bot" in bot_mode:
                            return {"next_state": "difficulty_select"}
                        else:
                            return {"next_state": "game"}
            elif 220 <= mouse_pos[0] <= 600:
                if 500 <= mouse_pos[1] <= 550:
                    return {"next_state": "menu"}
    return {"next_state": "mode_select"}

def difficulty_select_state(screen):
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
                        return {"next_state": "game", "difficulty": difficulty}
    return {"next_state": "difficulty_select"}

def game_state(screen):
    global clicked_cell, blinking_on, blink_timer, idx_player_playing
    clock = pygame.time.Clock()
    last_blink_time = pygame.time.get_ticks()
    blink_interval = 500  # milliseconds
    game_board = create_board(board)
    draw_board(screen,game_board)  
    game = True
    while game:
        # Update the current time for blinking logic
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_interval:
            blinking_on = not blinking_on
            last_blink_time = current_time
            draw_board(screen,game_board)
            if clicked_cell and clicked_cell != ("Reserve", None):
                piece_x, piece_y = clicked_cell
                cell_x = offset_x + piece_x * CELL_SIZE
                cell_y = offset_y + piece_y * CELL_SIZE
                draw_blinking_border(screen, cell_x, cell_y, CELL_SIZE, WHITE, blinking_on)
                draw_adjacent_borders(screen, clicked_cell[0], clicked_cell[1], CELL_SIZE, BLUE,game_board)  # Keep adjacent borders visible
            elif clicked_cell == ("Reserve", None):
                draw_borders_for_empty_cells(screen, CELL_SIZE, BLUE, game_board)     
                draw_blinking_border(screen, RESERVE_CIRCLE_CENTER[0], RESERVE_CIRCLE_CENTER[1], RESERVE_CIRCLE_RADIUS, WHITE, blinking_on)  
            pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouse_pos = pygame.mouse.get_pos()
                click_position = get_board_position(mouse_pos, offset_x, offset_y, CELL_SIZE)

                # Handle click on reserve piece
                if click_position[0] == "RESERVE":
                    clicked_pile = "Reserve", None  # Code to use a reserve piece
                    # Code to use a reserve piece
                    print("Reserve piece clicked")
                    # ... handle reserve piece usage ...
            
                # Handle click on the board
                else:
                    board_x, board_y = click_position
                    clicked_pile = game_board[board_y][board_x] if piece_at_click(board, board_x, board_y) else None
                
                # If we already have a clicked cell, we're attempting to move the piece
                if clicked_cell:

                    # Reserve Piece is selected
                    if clicked_cell == ("Reserve", None):
                        print("hello")
                        if(clicked_pile==clicked_cell):
                            clicked_cell = None


                        if clicked_pile is not None:
                            if can_put_reserve_piece(players[idx_player_playing],clicked_pile):
                                players[idx_player_playing].remove_reserve_piece()
                                game_board[board_y][board_x] = Pile(players[idx_player_playing].color,[players[idx_player_playing].color],(board_x,board_y))
                                idx_player_playing = 1 - idx_player_playing
                                clicked_cell = None
                            else:    
                                continue

                        else:
                            print("Invalid move")
                            continue    



                    # Deselect the pile if it's clicked again
                    elif clicked_cell == (board_x, board_y):
                        clicked_cell = None
                    # Check if the target pile exists
                    elif clicked_pile is not None:
                        current_pile = game_board[clicked_cell[1]][clicked_cell[0]]
                        if is_adjacent(clicked_cell, board_x, board_y, len(current_pile.stackedPieces)):
                            # Transfer the stack and switch turns
                            transfer_stack(clicked_cell, (board_x, board_y), game_board)
                            idx_player_playing = 1 - idx_player_playing  # Switch turns
                            # check_win_conditions(players, game_board)
                            # Deselect the pile
                            clicked_cell = None
                            #ACHO QUE NAO É PRECISO ESTE CODIGO DEBAIXO
                    ## If the move is to an empty space
                    #elif not piece_at_click(board, board_x, board_y):
                    #    current_pile = game_board[clicked_cell[1]][clicked_cell[0]]
                    #    if is_adjacent(clicked_cell, board_x, board_y, len(current_pile.stackedPieces)):
                    #        # Transfer the stack and switch turns
                    #        transfer_stack(clicked_cell, (board_x, board_y), game_board)
                    #        idx_player_playing = 1 - idx_player_playing  # Switch turns
                    #        # Deselect the pile
                    #        clicked_cell = None
#
#
                # If we don't have a clicked cell yet, we're selecting a piece
                else:
                    # if clicked on reserve piece
                    if clicked_pile == ("Reserve", None):
                        clicked_cell = ("Reserve", None)
                    # Proceed if the pile exists and belongs to the current player
                    elif clicked_pile and clicked_pile.owner == players[idx_player_playing].color:
                        clicked_cell = (board_x, board_y)
                    

                # Redraw the board after any action
                draw_board(screen, game_board)
                if clicked_cell != ("Reserve", None) and clicked_cell is not None:
                    #deviamos mudar este blink para o clicked cell do inicio a cena é que fica mais lento ao clickar para dar blink
                    # Highlight the selected cell with a blinking border and draw adjacent borders
                    draw_blinking_border(screen, offset_x + board_x * CELL_SIZE, offset_y + board_y * CELL_SIZE, CELL_SIZE, WHITE, blinking_on)
                    draw_adjacent_borders(screen, clicked_cell[0], clicked_cell[1], CELL_SIZE, BLUE, game_board)
                elif clicked_cell == ("Reserve", None):
                    draw_borders_for_empty_cells(screen, CELL_SIZE, BLUE, game_board)  
                    draw_blinking_border(screen, RESERVE_CIRCLE_CENTER[0], RESERVE_CIRCLE_CENTER[1], RESERVE_CIRCLE_RADIUS, WHITE, blinking_on)

                result = check_win_conditions(players, game_board)
                print(result)
                if result["has_winner"]:
                    print(result["winner"])
                    result["next_state"] = "endgame_menu"
                    return result
                
                # Update the display after handling the event
                pygame.display.flip()
    return {"next_state": "game", "has_winner": False, "winner": None, "reason": ""}
    
def endgame_menu_state(screen,result):
    result2 = {"has_winner": True, "winner": 'Red', "reason": "too good"}
    draw_endgame_screen(screen, result)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 350 <= mouse_pos[0] <= 450:
                if 300 <= mouse_pos[1] <= 350:
                    result["next_state"] = "game"
                    return result
                elif 400 <= mouse_pos[1] <= 450:
                    result["next_state"] = "menu"
                    return result
                elif 500 <= mouse_pos[1] <= 550:
                    pygame.quit()
                    sys.exit()
    pygame.display.flip()
    return result

# Função principal
def main():
    global clicked_cell, blinking_on, blink_timer, idx_player_playing
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Focus Board")

    state_machine = {
    "menu": menu_state,
    "mode_select": mode_select_state,
    "difficulty_select": difficulty_select_state,
    "game": game_state,
    "endgame_menu": endgame_menu_state
    }

    state = "menu"
    result = None
    while True:

        state_func = state_machine[state]
        if state == "endgame_menu":
            print("brefore endgame func", result)
            result = endgame_menu_state(screen, result)
        else:
            result = state_func(screen)
        state = result["next_state"]


if __name__ == "__main__":
    main()
