# method to avoid spamming key presses without making a delay would be nice
# enter key not working?

import pygame
import os

pygame.init()
pygame.font.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
font_time = pygame.font.SysFont("timesnewroman", 40)
font_small_number = pygame.font.SysFont("timesnewroman", 20)
font_big_number = pygame.font.SysFont("timesnewroman", 40)

CLOCK = pygame.time.Clock()
FPS = 60
WINDOW_SIZE = (540, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
WHITE = (255, 255, 255)
WINDOW.fill(WHITE)
pygame.display.set_caption("Sudoku")

BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (230, 230, 230)
MIDDLE_GREY = (128, 128, 128)
GAP = 60
ROWS, COL = 9, 9
seconds_reset = 0


class Grid:
    board = [
        [7, 8, "", 4, "", "", 1, 2, ""],
        [6, "", "", "", 7, 5, "", "", 9],
        ["", "", "", 6, "", 1, "", 7, 8],
        ["", "", 7, "", 4, "", 2, 6, ""],
        ["", "", 1, "", 5, "", 9, 3, ""],
        [9, "", 4, "", 6, "", "", "", 5],
        ["", 7, "", 3, "", "", "", 1, 2],
        [1, 2, "", "", "", 7, 4, "", ""],
        ["", 4, 9, 2, "", 6, "", "", 7]
    ]
    final_board = [
        [7, 8, 5, 4, 3, 9, 1, 2, 6],
        [6, 1, 2, 8, 7, 5, 3, 4, 9],
        [4, 9, 3, 6, 2, 1, 5, 7, 8],
        [8, 5, 7, 9, 4, 3, 2, 6, 1],
        [2, 6, 1, 7, 5, 8, 9, 3, 4],
        [9, 3, 4, 1, 6, 2, 7, 8, 5],
        [5, 7, 8, 3, 9, 4, 6, 1, 2],
        [1, 2, 6, 5, 8, 7, 4, 9, 3],
        [3, 4, 9, 2, 1, 6, 8, 5, 7]
    ]

    def __init__(self, rows, col, width, height):
        self.rows = rows
        self.col = col
        self.width = width
        self.height = height
        self.grid = list()
        self.number = list()
        self.final_number = list()
        self.count_number = list()
        self.wrong_number = list()
        self.click = False
        self.typing = False
        self.old_col = None
        self.old_row = None

    def control(self):
        self.make_grid()
        self.draw_board()
        self.get_mouse()
        self.get_key()
        self.check_input()
        self.draw_input()

    def make_grid(self):
        for i in range(ROWS):
            for j in range(COL):
                self.grid.append(pygame.draw.rect(WINDOW, GREY, (i * GAP, j * GAP, GAP, GAP), 1))

        # highlight cubes
        for i in range(ROWS):
            for j in range(COL):
                if i % 3 == 0:
                    pygame.draw.line(WINDOW, BLUE, (0, i * GAP), (WINDOW_SIZE[0], i * GAP), 3)
                if j % 3 == 0:
                    pygame.draw.line(WINDOW, BLUE, (j * GAP, 0), (j * GAP, WINDOW_SIZE[0]), 3)
        pygame.draw.line(WINDOW, BLUE, (0, WINDOW_SIZE[0]), (WINDOW_SIZE[0], WINDOW_SIZE[0]), 3)
        pygame.draw.line(WINDOW, BLUE, (WINDOW_SIZE[0] - 1, 0), (WINDOW_SIZE[0] - 1, WINDOW_SIZE[0]), 3)

    def draw_board(self):
        for i in range(ROWS):
            for j in range(COL):
                text = font_big_number.render(str(self.board[i][j]), 1, BLACK)
                WINDOW.blit(text, (j * GAP + int(GAP / 3), i * GAP + int(GAP / 6)))

    def get_mouse(self):
        mouse = pygame.mouse.get_pos()
        col, row = int(mouse[0] / GAP), int(mouse[1] / GAP)
        pygame.draw.rect(WINDOW, LIGHT_GREY, (col * GAP, row * GAP, GAP, GAP))
        clicked = pygame.mouse.get_pressed()

        if clicked[0]:  # 0 == left mouse
            self.click = not self.click
            self.old_col, self.old_row = col, row
            pygame.time.delay(200)
        # red rect to highlight box
        if self.click and self.old_col is not None:
            pygame.draw.rect(WINDOW, RED, (self.old_col * GAP, self.old_row * GAP, GAP, GAP), 2)

        # check if box is empty soduku board so the user can input numbers
        if self.old_row is not None:
            for i in range(ROWS):
                for j in range(COL):
                    if self.old_row <= 8 and self.old_col <= 8:
                        if self.board[self.old_row][self.old_col] == "":
                            self.typing = True
                        else:
                            self.typing = False
                    else:
                        self.typing = False

    def get_key(self):
        if self.click and self.typing and self.old_row is not None:  # 3rd condition at the start when nothing assigned
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_1]:
                self.number.append([1, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_2]:
                self.number.append([2, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_3]:
                self.number.append([3, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_4]:
                self.number.append([4, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_5]:
                self.number.append([5, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_6]:
                self.number.append([6, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_7]:
                self.number.append([7, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_8]:
                self.number.append([8, self.old_row, self.old_col])
                pygame.time.delay(200)
            elif keys_pressed[pygame.K_9]:
                self.number.append([9, self.old_row, self.old_col])
                pygame.time.delay(200)

    def check_input(self):
        # clear box or remove digits right mouse
        if pygame.mouse.get_pressed()[2]:
            for i in self.number:
                if [i[0], self.old_row, self.old_col] in self.wrong_number:
                    self.wrong_number.remove(i)
            for i in self.number:
                if [i[0], self.old_row, self.old_col] in self.final_number:
                    self.final_number.remove(i)
            for i in range(1, 10):
                if [i, self.old_row, self.old_col] in self.number:
                    self.number.remove([i, self.old_row, self.old_col])

        keys_pressed = pygame.key.get_pressed()
        # clear with keys pressed again
        if keys_pressed[pygame.K_1]:
            duplicate = list()
            for i in self.number:
                if i == [1, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_2]:
            duplicate = list()
            for i in self.number:
                if i == [2, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_3]:
            duplicate = list()
            for i in self.number:
                if i == [3, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_4]:
            duplicate = list()
            for i in self.number:
                if i == [4, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_5]:
            duplicate = list()
            for i in self.number:
                if i == [5, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_6]:
            duplicate = list()
            for i in self.number:
                if i == [6, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_7]:
            duplicate = list()
            for i in self.number:
                if i == [7, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_8]:
            duplicate = list()
            for i in self.number:
                if i == [8, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])
        if keys_pressed[pygame.K_9]:
            duplicate = list()
            for i in self.number:
                if i == [9, self.old_row, self.old_col]:
                    duplicate.append(i)
            if len(duplicate) > 1:
                for i in range(2):
                    self.number.remove(duplicate[1])
                    if duplicate[1] in self.final_number:
                        self.final_number.remove(duplicate[1])
                    if duplicate[1] in self.wrong_number:
                        self.wrong_number.remove(duplicate[1])

        # prevent after final input display numbers in the same box
        if len(self.final_number) > 0:
            for i in self.final_number:
                for j in range(1, 10):
                    if j != i[0] and self.old_row == i[1] and self.old_col == i[2]:
                        if [j, self.old_row, self.old_col] in self.number:
                            self.number.remove([j, self.old_row, self.old_col])

        # final input
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            self.count_number = []
            pygame.time.delay(200)
            for i in self.number:
                for j in range(1, 10):
                    if [j, self.old_row, self.old_col] == i:
                        self.count_number.append(j)
            if len(self.count_number) == 1 and [self.count_number[0], self.old_row, self.old_col] not in self.final_number:
                self.final_number.append([self.count_number[0], self.old_row, self.old_col])
            else:  # more than one number in box just delete all numbers in the box
                for z in range(1, 10):
                    if [z, self.old_row, self.old_col] in self.number:
                        self.number.remove([z, self.old_row, self.old_col])
                    if [z, self.old_row, self.old_col] in self.final_number:
                        self.final_number.remove([z, self.old_row, self.old_col])

            # check if input correct
            for i in self.final_number:
                if i[0] == self.final_board[i[1]][i[2]]:
                    self.board[i[1]][i[2]] = i[0]
                    self.final_number.remove(i)
                    self.number.remove(i)
                elif i[0] != self.final_board[i[1]][i[2]]:
                    print(1)
                    self.wrong_number.append(i)

    def draw_input(self):
        # display digits
        if len(self.number) >= 1 and not pygame.mouse.get_pressed()[2]:
            for i in self.number:
                if i in self.wrong_number:
                    text_number = font_small_number.render(str(i[0]), 1, RED)
                else:
                    text_number = font_small_number.render(str(i[0]), 1, MIDDLE_GREY)
                if str(i[0]) == "1" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP, i[1] * GAP))
                elif str(i[0]) == "2" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 3), i[1] * GAP))
                elif str(i[0]) == "3" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 1.5), i[1] * GAP))
                elif str(i[0]) == "4" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP, i[1] * GAP + int(GAP / 3)))
                elif str(i[0]) == "5" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 3), i[1] * GAP + int(GAP / 3)))
                elif str(i[0]) == "6" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 1.5), i[1] * GAP + int(GAP / 3)))
                elif str(i[0]) == "7" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP, i[1] * GAP + int(GAP / 1.5)))
                elif str(i[0]) == "8" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 3), i[1] * GAP + int(GAP / 1.5)))
                elif str(i[0]) == "9" and i not in self.final_number:
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 1.5), i[1] * GAP + int(GAP / 1.5)))
                elif i in self.final_number and i not in self.wrong_number:
                    text_number = font_big_number.render(str(i[0]), 1, MIDDLE_GREY)
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 3), i[1] * GAP + int(GAP / 6)))
                elif i in self.final_number and i in self.wrong_number:
                    text_number = font_big_number.render(str(i[0]), 1, RED)
                    WINDOW.blit(text_number, (i[2] * GAP + int(GAP / 3), i[1] * GAP + int(GAP / 6)))


def timer():
    global seconds_reset
    seconds = (pygame.time.get_ticks()) // 1000 - seconds_reset
    minutes = (pygame.time.get_ticks() // 60000)
    if seconds == 60:
        seconds_reset += seconds
        seconds = 0

    time = f"Time: {minutes}:{seconds:02}"
    text_time = font_time.render(time, 1, BLACK)
    WINDOW.blit(text_time, (WINDOW_SIZE[0] - text_time.get_width() - 10, WINDOW_SIZE[1] - text_time.get_height() - 5))


def draw(board):
    WINDOW.fill(WHITE)
    board.control()
    timer()
    board.draw_board()
    pygame.display.update()


def main():
    run = True
    board = Grid(ROWS, COL, WINDOW_SIZE[0], WINDOW_SIZE[1])

    while run:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        draw(board)


main()
