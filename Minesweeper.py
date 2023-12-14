"""
MINESWEEPER

a logic puzzle video game genre generally played on personal computers.
The game features a grid of clickable squares, with hidden "mines"
scattered throughout the board.
"""

import pygame
import sys
import random


def drawing_the_board():
    """
    Function draws the gamestate of the game after each click on the screen.
    :return:
    """
    global game_over

    for x in range(COLUMNS):
        for y in range(ROWS):

            COORDINATES = (MARGIN_HORIZONTAL + TILE_SIZE * x,
                           2 * MARGIN_VERTICAL + TILE_SIZE * y)

            outer_board_block = pygame.image.load("minesweeper_basic_block.png")
            outer_board_block_rect = (COORDINATES[0], COORDINATES[1])
            SCREEN.blit(outer_board_block, outer_board_block_rect)

            if mines[x][y] == 9:
                bomb_block = pygame.image.load("minesweeper_bomb.png")
                bomb_block_rect = (COORDINATES[0], COORDINATES[1])
                SCREEN.blit(bomb_block, bomb_block_rect)

            if numbers[x][y] != 0:
                number_block =\
                    pygame.image.load(f"minesweeper_{numbers[x][y]}.png")
                number_block_rect = (COORDINATES[0], COORDINATES[1])
                SCREEN.blit(number_block, number_block_rect)

            if board[x][y] == 0:
                whole_block = pygame.image.load("minesweeper_empty_block.png")
                whole_block_rect = (COORDINATES[0], COORDINATES[1])
                SCREEN.blit(whole_block, whole_block_rect)

            if flags[x][y] == 10:
                flag_block = pygame.image.load("minesweeper_flag.png")
                flag_block_rect = (COORDINATES[0], COORDINATES[1])
                SCREEN.blit(flag_block, flag_block_rect)

            if game_over:
                draw_mistakes()


def generating_bombs():
    """
    Function generates blocks, on which bombs will be positioned.
    :return:
    """
    for bomb in range(BOMBS_NUMBER):
        is_it = True
        while is_it:
            x = random.randint(0, COLUMNS - 1)
            y = random.randint(0, ROWS - 1)
            if mines[x][y] != 9:
                mines[x][y] = 9
                is_it = False


def generating_numbers():
    """
    Function generates number on each particular block which corresponds to
    number of bombs which are next to this block. Function checks each block
    which is next to the main block if there is a bomb. If yes, the number
    on this block is increasing.
    :return:
    """
    for x in range(COLUMNS):
        for y in range(ROWS):
            if mines[x][y] != 9:
                counter = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (0 <= x + i < COLUMNS) and (0 <= y + j < ROWS):
                            if mines[x + i][y + j] == 9:
                                counter += 1
                numbers[x][y] = counter


def draw_bomb_counter():
    """
    Function draws bomb counter on the screen.
    :return:
    """
    FONT = pygame.font.Font('freesansbold.ttf', 80)

    bomb_counter =\
        pygame.Rect(MARGIN_HORIZONTAL, 40,
                    COUNTER_SIZE[0] + 30, COUNTER_SIZE[1])
    pygame.draw.rect(SCREEN, BLACK, bomb_counter)

    bomb_counter_display = FONT.render(f"{BOMBS_NUMBER}", True, RED)
    bomb_counter_display_box = bomb_counter_display.get_rect()
    bomb_counter_display_place = (MARGIN_HORIZONTAL + 25, 45)
    SCREEN.blit(bomb_counter_display, bomb_counter_display_place)


def draw_time_counter():
    """
    Function draws time counter button on the screen.
    :return:
    """
    global time, clock

    time = pygame.time.get_ticks() - time_init
    time /= 1000
    time = int(time)

    FONT = pygame.font.Font('freesansbold.ttf', 80)

    X_COORDINATE = SIZE[0] - MARGIN_HORIZONTAL - 150
    X_LENGTH = COUNTER_SIZE[0] + 30

    time_counter = pygame.Rect(X_COORDINATE, 40, X_LENGTH, COUNTER_SIZE[1])
    pygame.draw.rect(SCREEN, BLACK, time_counter)

    time_counter_display = FONT.render(f"{time}", True, RED)
    time_counter_display_box = time_counter_display.get_rect()
    time_counter_display_place = (SIZE[0] - MARGIN_HORIZONTAL - 145, 45)
    SCREEN.blit(time_counter_display, time_counter_display_place)


def draw_restart_button():
    """
    Function draws restart button on the screen.
    :return:
    """
    restart_button = pygame.image.load("minesweeper_smile_face.png")
    restart_button_rect = (SIZE[0] / 2 - 40, 40)
    SCREEN.blit(restart_button, restart_button_rect)


def reveal_empty_block(x, y):
    """
    Function checks if the block is empty and reveals it.
    After that checks if the neighbours are also empty. If yes, it also reveals
    them until all neighbours which are empty, are not revealed.
    :param x:
    :param y:
    :return:
    """
    global revealed_blocks

    if board[x][y] == 0:
        board[x][y] = -1  # this block is now revealed
        revealed_blocks += 1
        if numbers[x][y] == 0:
            for neighbour_x in range(-1, 2):
                for neighbour_y in range(-1, 2):
                    if 0 <= x + neighbour_x < COLUMNS:
                        if 0 <= y + neighbour_y < ROWS:
                            reveal_empty_block(x + neighbour_x, y + neighbour_y)


def reveal_block():
    """
    Function reveals or place a flag on particular (clicked) block.
    :return:
    """
    global BOMBS_NUMBER, first_click, revealed_blocks

    position = pygame.mouse.get_pos()
    # position on x-axis which column is it
    position_x = (position[0] - MARGIN_HORIZONTAL) // TILE_SIZE
    # position on y-axis which row is it
    position_y = (position[1] - 2 * MARGIN_VERTICAL) // TILE_SIZE
    if 0 <= position_x < COLUMNS and 0 <= position_y < ROWS:
        if pygame.mouse.get_pressed()[0]:

            if first_click:
                while first_click:
                    # checking if the first move is safe
                    if mines[position_x][position_y] == 9:
                        generating_bombs()
                        generating_numbers()
                    else:
                        revealed_blocks += 1
                        first_click = False

            # the game is not over and there is no flag
            if not game_over and flags[position_x][position_y] != 10:
                # revealing all empty blocks
                reveal_empty_block(position_x, position_y)

                if mines[position_x][position_y] == 9:
                    lose_game()
                    main_bomb_block =\
                        pygame.image.load("minesweeper_main_bomb.png")
                    main_bomb_block_rect = (position_x, position_y)
                    SCREEN.blit(main_bomb_block, main_bomb_block_rect)

                else:
                    revealed_blocks += 1
                    # revealing common block
                    board[position_x][position_y] = -1

        if pygame.mouse.get_pressed()[2]:
            if not game_over:
                if flags[position_x][position_y] == 0:
                    if board[position_x][position_y] == 0:
                        flags[position_x][position_y] = 10  # putting flag
                        BOMBS_NUMBER -= 1
                elif flags[position_x][position_y] == 10:
                    flags[position_x][position_y] = 0  # hiding flag
                    BOMBS_NUMBER += 1


def click_restart():
    """
    Function checks if the user clicks on the restart button.
    If yes, function 'restart game' is working.
    :return:
    """
    restart_position = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        if SIZE[0] / 2 - 40 <= restart_position[0] <= SIZE[0] / 2 + 40 \
                and 40 <= restart_position[1] <= 120:
            restart_game()


def reveal_bombs():
    """
    Function reveals all bombs after lost the game.
    :return:
    """
    for x in range(COLUMNS):
        for y in range(ROWS):
            if mines[x][y] == 9:
                board[x][y] = 9


def draw_mistakes():
    """
    Function draws crossed bombs in places where there
    was not a bomb and the user put the flag.
    :return:
    """

    for x in range(COLUMNS):
        for y in range(ROWS):
            COORDINATES = (MARGIN_HORIZONTAL + TILE_SIZE * x,
                           2 * MARGIN_VERTICAL + TILE_SIZE * y)
            if flags[x][y] == 10 and mines[x][y] == 0:
                mistake_block = pygame.image.load("minesweeper_mistake.png")
                mistake_block_rect = (COORDINATES[0], COORDINATES[1])
                SCREEN.blit(mistake_block, mistake_block_rect)


def lose_game():
    """
    Function reveals all bombs when you lost the game.
    :return:
    """
    global game_over
    game_over = True

    for x in range(COLUMNS):
        for y in range(ROWS):
            if mines[x][y] == 9:
                board[x][y] = 9


def draw_lost_text():
    """
    Function draws on the screen text that you clicked on the bomb and
    due to this fact - you lost.
    :return:
    """
    if game_over:
        FONT = pygame.font.Font('freesansbold.ttf', 30)

        lose_text = FONT.render("You lost :cc Try again!", True, BLACK)
        lose_text_box = lose_text.get_rect()
        lose_text_place = (MARGIN_HORIZONTAL, MARGIN_VERTICAL + 40)
        SCREEN.blit(lose_text, lose_text_place)


def check_win():
    """
    Function checks if the user revealed all blocks which are not bombs.
    :return:
    """
    safe_bombs = 0
    for x in range(COLUMNS):
        for y in range(ROWS):
            if mines[x][y] == 9 and flags[x][y] == 10:
                safe_bombs += 1

    if safe_bombs == SAFE_BOMBS:
        win_game()


def win_game():
    """
    Function draws text on the screen to congratuate
    the user winning the game.
    :return:
    """
    FONT = pygame.font.Font('freesansbold.ttf', 30)

    win_text = FONT.render("Congratulations!! You won!", True, BLACK)
    win_text_box = win_text.get_rect()
    win_text_place = (MARGIN_HORIZONTAL, MARGIN_VERTICAL + 40)
    SCREEN.blit(win_text, win_text_place)


def restart_game():
    """
    Function restarts the game (generates new bombs,
    reveals each block) when the user clicks on restart button.
    :return:
    """
    global board, mines, flags, numbers, game_over,\
        first_click, BOMBS_NUMBER, FLAGS_NUMBER,\
        revealed_blocks, clock, time_init

    # initialize all arrays to 0
    board = [[0] * ROWS for y in range(COLUMNS)]
    mines = [[0] * ROWS for y in range(COLUMNS)]
    numbers = [[0] * ROWS for y in range(COLUMNS)]
    flags = [[0] * ROWS for y in range(COLUMNS)]

    # return all variables to initial values

    BOMBS_NUMBER = FLAGS_NUMBER = 10

    revealed_blocks = 0

    clock = pygame.time.Clock()
    time_init = pygame.time.get_ticks()

    game_over = False

    first_click = True

    generating_bombs()
    generating_numbers()


if __name__ == "__main__":
    # colors
    GREY = (211, 211, 211)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # title
    TITLE = "MINESWEEPER"

    # game board initialization
    ROWS = 9
    COLUMNS = 9
    TILE_SIZE = 50
    MARGIN_HORIZONTAL = 30
    MARGIN_VERTICAL = 100

    # initialization
    SIZE = (ROWS * TILE_SIZE + MARGIN_HORIZONTAL * 2,
            COLUMNS * TILE_SIZE + MARGIN_VERTICAL * 2.5)

    pygame.init()
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(TITLE)

    # game arrays (initialization - each block - 0)
    board = [[0] * ROWS for y in range(COLUMNS)]
    mines = [[0] * ROWS for y in range(COLUMNS)]
    numbers = [[0] * ROWS for y in range(COLUMNS)]
    flags = [[0] * ROWS for y in range(COLUMNS)]

    # initial values
    BOMBS_NUMBER = FLAGS_NUMBER = 10
    SAFE_BOMBS = 10

    revealed_blocks = 0

    # time clock
    clock = pygame.time.Clock()
    time_init = pygame.time.get_ticks()

    # counters' dimensions
    COUNTER_SIZE = (120, 80)

    # restart button dimensions
    X_LEFT_BOUND = SIZE[0] / 2 - 40
    X_RIGHT_BOUND = SIZE[0] / 2 + 40
    Y_UPPER_BOUND = 40
    Y_LOWER_BAND = 80

    # pictures of different blocks
    basic_block = {"file": "minesweeper_basic_block.png"}
    empty_block = {"file": "minesweeper_empty_block.png"}
    number_1 = {"file": "minesweeper_1.png"}
    number_2 = {"file": "minesweeper_2.png"}
    number_3 = {"file": "minesweeper_3.png"}
    number_4 = {"file": "minesweeper_4.png"}
    number_5 = {"file": "minesweeper_5.png"}
    number_6 = {"file": "minesweeper_6.png"}
    number_7 = {"file": "minesweeper_7.png"}
    number_8 = {"file": "minesweeper_8.png"}
    bomb = {"file": "minesweeper_bomb.png"}
    flag = {"file": "minesweeper_flag.png"}
    smiling_face = {"file": "minesweeper_smile_face.png"}
    wrong_flag = {"file": "minesweeper_mistake.png"}
    main_bomb = {"file": "minesweeper_main_bomb.png"}

    elements = [empty_block, number_1, number_2, number_3,
                number_4, number_5, number_6, number_7,
                number_8, bomb, flag, smiling_face]

    # state of the game
    first_click = True
    game_over = False

    # generating board
    generating_bombs()
    generating_numbers()

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                reveal_block()
                click_restart()

        # drawing game board
        SCREEN.fill(GREY)
        drawing_the_board()
        draw_bomb_counter()
        draw_time_counter()
        draw_restart_button()
        draw_lost_text()

        # checking if the user wins the game
        check_win()

        pygame.display.flip()
