import pygame
import os

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.font.init()

font_text = pygame.font.SysFont("timesnewroman", 40)

WINDOW_SIZE = (600, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tic Tac Toe")

CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
GREY = (252, 252, 252)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

ROWS, COLS = 3, 3
grid_list = [["" for i in range(COLS)] for j in range(ROWS)]

GAP = 50

players = ["X", "O"]
current_player = players[0]
draw_text = []


def mouse():
    x, y = pygame.mouse.get_pos()
    row, col = None, None

    # evaluate correct col & row
    if int(WINDOW_SIZE[0] / 3 + GAP / 2) > x > GAP and int(GAP / 2 * 3) < y < WINDOW_SIZE[1] - GAP:
        col = 0
    elif int(WINDOW_SIZE[0] / 3 * 2) > x > int(WINDOW_SIZE[0] / 3 * 1) and GAP < y < WINDOW_SIZE[1] - GAP:
        col = 1
    elif int(WINDOW_SIZE[0] - GAP) > x > int(WINDOW_SIZE[0] / 3 * 2) and GAP < y < WINDOW_SIZE[1] - GAP:
        col = 2

    if int(WINDOW_SIZE[1] / 3 * 1) > y > GAP and GAP < x < WINDOW_SIZE[0] - GAP:
        row = 0
    elif int(WINDOW_SIZE[1] / 3 * 2) > y > int(WINDOW_SIZE[1] / 3 * 1) and GAP < x < WINDOW_SIZE[0] - GAP:
        row = 1
    elif int(WINDOW_SIZE[1] - GAP) > y > int(WINDOW_SIZE[1] / 3 * 2) and GAP < x < WINDOW_SIZE[0] - GAP:
        row = 2

    # evaluate correct xpos & ypos
    if col is not None and row is not None:
        if col == 0:
            xpos = GAP / 2 * 3
        elif col == 1:
            xpos = WINDOW_SIZE[0] / 3 + GAP / 2
        elif col == 2:
            xpos = WINDOW_SIZE[0] / 3 * 2 - GAP / 2
        else:
            xpos = None

        if row == 0:
            ypos = GAP / 2 * 3
        elif row == 1:
            ypos = WINDOW_SIZE[1] / 3 + GAP / 2
        elif row == 2:
            ypos = WINDOW_SIZE[1] / 3 * 2 - GAP / 2
        else:
            ypos = None

        if xpos is not None and ypos is not None:
            pygame.draw.rect(WINDOW, GREY,
                             (int(xpos), int(ypos), int(WINDOW_SIZE[0] / 3 - GAP), int(WINDOW_SIZE[1] / 3 - GAP)))

        mouse_pressed(row, col, xpos, ypos)


def mouse_pressed(row, col, xpos, ypos):
    global current_player
    if row is not None and col is not None:
        pygame.event.get()
        if pygame.mouse.get_pressed()[0]:
            if current_player == "X" and grid_list[row][col] == "":
                grid_list[row][col] = current_player
                text = font_text.render(str(current_player), 1, BLACK)
                # need to know which symbol to draw at which position thus saving the information and blit later
                draw_text.append([current_player, int(xpos + 75 - text.get_width() / 2),
                                  int(ypos + 75 - text.get_height() / 2), row, col])
                current_player = players[1]
            elif current_player == "O" and grid_list[row][col] == "":
                grid_list[row][col] = current_player
                text = font_text.render(str(current_player), 1, BLACK)
                draw_text.append(
                    [current_player, int(xpos + 75 - text.get_width() / 2),
                     int(ypos + 75 - text.get_height() / 2), row, col])
                current_player = players[0]


def check():
    global grid_list, draw_text, current_player

    winner = False
    pstart = []
    pend = []

    # horizontal
    for i in range(0, 3):
        if grid_list[i][0] != "":
            if grid_list[i][0] == grid_list[i][1] and grid_list[i][0] == grid_list[i][2]:
                winner = grid_list[i][0]
                for j in draw_text:
                    if j[3] == i and j[4] == 0:
                        pstart.append([j[1], j[2] + 20])
                    if j[3] == i and j[4] == 2:
                        pend.append([j[1] + 25, j[2] + 20])

    # vertical
    for i in range(0, 3):
        if grid_list[0][i] != "":
            if grid_list[0][i] == grid_list[1][i] and grid_list[0][i] == grid_list[2][i]:
                winner = grid_list[0][i]
                for j in draw_text:
                    if j[3] == 0 and j[4] == i:
                        pstart.append([j[1] + 14, j[2]])
                    if j[3] == 2 and j[4] == i:
                        pend.append([j[1] + 14, j[2] + 37])

    # diagonal
    if grid_list[0][0] != "":
        if grid_list[0][0] == grid_list[1][1] and grid_list[0][0] == grid_list[2][2]:
            for j in draw_text:
                if j[3] == 0 and j[4] == 0:
                    pstart.append([j[1], j[2]])
                if j[3] == 2 and j[4] == 2:
                    pend.append([j[1] + 25, j[2] + 44])
            winner = grid_list[0][0]

    if grid_list[2][0] != "":
        if grid_list[2][0] == grid_list[1][1] and grid_list[2][0] == grid_list[0][2]:
            for j in draw_text:
                if j[3] == 2 and j[4] == 0:
                    pstart.append([j[1] - 5, j[2] + 40])
                if j[3] == 0 and j[4] == 2:
                    pend.append([j[1] + 30, j[2]])
            winner = grid_list[2][0]

    if winner is not False:
        text = font_text.render(f"Winner is {str(winner)}", 1, BLACK)
        WINDOW.blit(text, (int(WINDOW_SIZE[0] / 2 - text.get_width() / 2), 10))
        print(pstart, pend)
        pygame.draw.line(WINDOW, RED, (pstart[0][0], pstart[0][1]), (pend[0][0], pend[0][1]), 4)
        pygame.display.update()
        pygame.time.delay(3000)
        grid_list = [["" for i in range(COLS)] for j in range(ROWS)]
        current_player = players[0]
        draw_text = []
        main()


def grid():
    # vertical line
    pygame.draw.line(WINDOW, BLACK, (int(WINDOW_SIZE[0] / 3 + GAP / 2), int(GAP / 2 * 3)),
                     (int(WINDOW_SIZE[0] / 3 + GAP / 2), int(WINDOW_SIZE[1] - GAP / 2 * 3)), 4)
    pygame.draw.line(WINDOW, BLACK, (int(WINDOW_SIZE[0] / 3 * 2 - GAP / 2), int(GAP / 2 * 3)),
                     (int(WINDOW_SIZE[0] / 3 * 2 - GAP / 2), int(WINDOW_SIZE[1] - GAP / 2 * 3)), 4)

    # horizontal line
    pygame.draw.line(WINDOW, BLACK, (int(GAP + GAP / 2), int(WINDOW_SIZE[1] / 3 + GAP / 2)),
                     (int(WINDOW_SIZE[1] - GAP / 2 * 3), int(WINDOW_SIZE[1] / 3 + GAP / 2)), 4)
    pygame.draw.line(WINDOW, BLACK, (int(GAP + GAP / 2), int(WINDOW_SIZE[1] / 3 * 2 - GAP / 2)),
                     (int(WINDOW_SIZE[1] - GAP / 2 * 3), int(WINDOW_SIZE[1] / 3 * 2 - GAP / 2)), 4)


def draw():
    WINDOW.fill(WHITE)
    grid()
    mouse()
    for i in draw_text:
        text = font_text.render(str(i[0]), 1, BLACK)
        WINDOW.blit(text, (i[1], i[2]))
    pygame.display.update()
    check()


def main():
    run = True

    while run:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw()


main()
