import pygame
# needed for the obstacles to set random locations
import random
# centers the window
import os
# import time needed for time.sleep() - edit: not used anymore

# has to be written before pygame initializes to center the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
# initialises all modules of pygame
pygame.init()

# deceleration of constant variables
DISPLAY_HEIGHT = 600
DISPLAY_WIDTH = 800
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
HOVER_RED = (255, 0, 0)
HOVER_GREEN = (0, 255, 0)
HOVER_BLUE = (0, 0, 255)
CAR_WIDTH = 70
CAR_HEIGHT = 120
BARREL_HEIGHT = 106
BARREL_WIDTH = 61
ROAD_HEIGHT = 600
OBSTACLES_NUMBER = 2
RECT_GREEN = (500, 350, 150, 50)
RECT_RED = (150, 350, 150, 50)
RECT_INFO = (325, 450, 150, 50)
paused = True

# defining the display - parameters as a tuple
game_display = pygame.display.set_mode(DISPLAY_SIZE)
# window title
pygame.display.set_caption("Roadtangle")
# matters for frame per second
clock = pygame.time.Clock()

# load and display images
car_img = pygame.image.load("racing_car.png")
car_img.set_colorkey(WHITE)
car_img.convert_alpha()
car_icon = pygame.image.load("racing_car_icon.png")
barrel_img = pygame.image.load("barrel.png")
barrel_img.set_colorkey(WHITE)
barrel_img.convert_alpha()
# converts the format and can process faster
road1_img = pygame.image.load("road1.png").convert()
road2_img = pygame.image.load("road2.png").convert()

# icon
pygame.display.set_icon(car_icon)

# sound and music
crash_sound = pygame.mixer.Sound("car_crash.wav")
back_music = pygame.mixer.music.load("spy_music_by_Nicole_Marie_T.wav")


# define Classes
class Cars:
    def __init__(self, x, y, x_l_change, x_r_change, x_vel, y_u_change, y_d_change, y_vel):
        self.x = x
        self.y = y
        self.x_l_change = x_l_change
        self.x_r_change = x_r_change
        self.x_vel = x_vel
        self.y_u_change = y_u_change
        self.y_d_change = y_d_change
        self.y_vel = y_vel

    def draw(self):
        game_display.blit(car_img, (self.x, self.y))

    def move(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            self.x_l_change = -self.x_vel
        else:
            self.x_l_change = 0
        if keys_pressed[pygame.K_RIGHT]:
            self.x_r_change = self.x_vel
        else:
            self.x_r_change = 0

        if keys_pressed[pygame.K_UP]:
            self.y_u_change = -self.y_vel
        else:
            self.y_u_change = 0
        if keys_pressed[pygame.K_DOWN]:
            self.y_d_change = self.y_vel
        else:
            self.y_d_change = 0

    def update(self):
        self.x += self.x_l_change + self.x_r_change
        self.y += self.y_u_change + self.y_d_change


class Obstacles:
    def __init__(self, ob_x, ob_y, ob_speed):
        self.ob_x = ob_x
        self.ob_y = ob_y
        self.ob_speed = ob_speed

    def draw(self):
        game_display.blit(barrel_img, (self.ob_x, self.ob_y))

    def move(self):
        self.ob_y += self.ob_speed
        return self.ob_y

    def set_random(self):
        if self.ob_y > DISPLAY_HEIGHT:
            obstacles = list()
            for i in range(OBSTACLES_NUMBER):
                obstacles.append(Obstacles(random.randrange(0, DISPLAY_WIDTH), random.randrange(-1000, -600),
                                           random.randrange(5, 10)))
            self.ob_y = 0 - BARREL_HEIGHT
            self.ob_x = random.randrange(0, DISPLAY_WIDTH - BARREL_WIDTH)


class Road:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, img):
        game_display.blit(img, (self.x, self.y))

    def move(self):
        self.y += 7
        if self.y > DISPLAY_HEIGHT:
            self.y = -588
        # scrolling picture in bad


class Messages:
    def __init__(self, x_car, y_car):
        self.x_car = x_car
        self.y_car = y_car

    def crash_border(self):
        if self.x_car > DISPLAY_WIDTH - CAR_WIDTH or self.x_car < 0 or self.y_car < 0 \
                or self.y_car > DISPLAY_HEIGHT - CAR_HEIGHT:
            crash("YOU CRASHED")

    def crash_ob(self, x_ob, y_ob):
        if self.y_car < y_ob + BARREL_HEIGHT and self.y_car + BARREL_HEIGHT > y_ob:
            if x_ob < self.x_car < x_ob + BARREL_WIDTH or x_ob < self.x_car + CAR_WIDTH < x_ob + BARREL_WIDTH:
                crash("YOU CRASHED")

    def score(self, points):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Score: " + str(points), True, BLACK)
        game_display.blit(text, (0, 0))


class IntroButton:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(game_display, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(game_display, RED, RECT_RED)
        if RECT_GREEN[0] < self.mouse[0] < RECT_GREEN[0] + RECT_GREEN[2] and \
                RECT_GREEN[1] < self.mouse[1] < RECT_GREEN[1] + RECT_GREEN[3]:
            pygame.draw.rect(game_display, HOVER_GREEN, RECT_GREEN)
            if self.click[0] == 1:
                game_loop()

        else:
            pygame.draw.rect(game_display, GREEN, RECT_GREEN)

    def button_text(self, rect, text):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text_output = font.render(text, True, BLACK)
        text_rect = text_output.get_rect()
        text_rect.center = (rect[0] + int((rect[2] / 2)), rect[1] + int((rect[3] / 2)))
        game_display.blit(text_output, text_rect)


class PausedButton:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        global paused
        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(game_display, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(game_display, RED, RECT_RED)
        if RECT_GREEN[0] < self.mouse[0] < RECT_GREEN[0] + RECT_GREEN[2] and \
                RECT_GREEN[1] < self.mouse[1] < RECT_GREEN[1] + RECT_GREEN[3]:
            pygame.draw.rect(game_display, HOVER_GREEN, RECT_GREEN)
            if self.click[0] == 1:
                pygame.mixer.music.unpause()
                paused = False
        else:
            pygame.draw.rect(game_display, GREEN, RECT_GREEN)

    def button_text(self, rect, text):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text_output = font.render(text, True, BLACK)
        text_rect = text_output.get_rect()
        text_rect.center = (rect[0] + int((rect[2] / 2)), rect[1] + int((rect[3] / 2)))
        game_display.blit(text_output, text_rect)


class ButtonInfo:
    def __init__(self, mouse, click, rect, text):
        self.mouse = mouse
        self.click = click
        self.rect = rect
        self.text = text

    def button_draw(self):
        if RECT_INFO[0] < self.mouse[0] < RECT_INFO[0] + RECT_INFO[2] and \
                RECT_INFO[1] < self.mouse[1] < RECT_INFO[1] + RECT_INFO[3]:
            pygame.draw.rect(game_display, HOVER_BLUE, RECT_INFO)
            if self.click[0] == 1:
                game_info()
        else:
            pygame.draw.rect(game_display, BLUE, RECT_INFO)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text_output = font.render(self.text, True, BLACK)
        text_rect = text_output.get_rect()
        text_rect.center = (self.rect[0] + int((self.rect[2] / 2)), self.rect[1] + int((self.rect[3] / 2)))
        game_display.blit(text_output, text_rect)

    def info_text(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text_output_arrows = font.render("Use The Arrows To Move Back and Forth or Sideway", True, BLACK, WHITE)
        text_rect_arrows = text_output_arrows.get_rect()
        text_rect_arrows.center = (int(DISPLAY_WIDTH / 2), 200)
        game_display.blit(text_output_arrows, text_rect_arrows)
        text_output_spacebar = font.render("The Spacebar Allows To Pause The Game", True, BLACK, WHITE)
        text_rect_spacebar = text_output_spacebar.get_rect()
        text_rect_spacebar.center = (int(DISPLAY_WIDTH / 2), 220)
        game_display.blit(text_output_spacebar, text_rect_spacebar)
        text_output_obstacle = font.render("Do Not Crash Against Obstacles", True, BLACK, WHITE)
        text_rect_obstacle = text_output_obstacle.get_rect()
        text_rect_obstacle.center = (int(DISPLAY_WIDTH / 2), 240)
        game_display.blit(text_output_obstacle, text_rect_obstacle)


# defining functions
def game_intro():
    intro = True
    game_display.blit(road1_img, (0, 0))
    font = pygame.font.Font('freesansbold.ttf', 80)
    text_output = font.render("Roadtangle", True, BLACK)
    text_rect = text_output.get_rect()
    text_rect.center = (int(DISPLAY_WIDTH / 2), 220)
    game_display.blit(text_output, text_rect)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button = IntroButton(mouse, click)
        button.button_draw()
        global button_info
        button_info = ButtonInfo(mouse, click, RECT_INFO, "Information")
        button_info.button_draw()
        button.button_text(RECT_GREEN, "GO")
        button.button_text(RECT_RED, "CHICK OUT")

        pygame.display.update()
        pygame.event.get()
        # to not take all my ram
        clock.tick(15)


def game_info():
    intro = True
    game_display.blit(road1_img, (0, 0))
    font = pygame.font.Font('freesansbold.ttf', 80)
    text_output = font.render("Information", True, BLACK)
    text_rect = text_output.get_rect()
    text_rect.center = (int(DISPLAY_WIDTH / 2), 100)
    game_display.blit(text_output, text_rect)

    button_info.info_text()

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button = IntroButton(mouse, click)
        button.button_draw()
        button.button_text(RECT_GREEN, "GO")
        button.button_text(RECT_RED, "CHICK OUT")

        pygame.display.update()
        pygame.event.get()
        clock.tick(15)


def game_loop():

    # -1 means in infinity (1: normal and 1.5: faster etc.)
    pygame.mixer.music.play(-1)

    game_exit = False
    points = 0
    obstacles = list()
    # creating instances of objects
    car = Cars(int(DISPLAY_WIDTH * 0.45), int(DISPLAY_HEIGHT * 0.8), 0, 0, 5, 0, 0, 5)
    for i in range(OBSTACLES_NUMBER):
        obstacles.append(Obstacles(random.randrange(0, DISPLAY_WIDTH), random.randrange(-1000, -600),
                                   random.randrange(5, 10)))

    road1 = Road(0, 0)
    road2 = Road(0, 600)

    while not game_exit:

        message = Messages(car.x, car.y)

        # checks all events (inputs) and creates a list per frame per second
        for event in pygame.event.get():
            # closes the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # location update
        car.move()
        car.update()
        for i in range(OBSTACLES_NUMBER):
            obstacles[i].move()

        # drawing
        game_display.fill(WHITE)
        road1.draw(road1_img)
        road1.move()
        road2.draw(road2_img)
        road2.move()
        car.draw()
        message.score(points)
        for i in range(OBSTACLES_NUMBER):
            obstacles[i].draw()

        # checking
        for i in range(OBSTACLES_NUMBER):
            if DISPLAY_HEIGHT < obstacles[i].ob_y:
                points += 50
                if points >= 1000:
                    obstacles[i].ob_speed += 1
        message.crash_border()
        for i in range(OBSTACLES_NUMBER):
            message.crash_ob(obstacles[i].ob_x, obstacles[i].ob_y)
        for i in range(OBSTACLES_NUMBER):
            obstacles[i].set_random()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE]:
            game_pause()

        # the drawing with no parameter updates everything & with parameter only this => less calculation
        pygame.display.update()

        # determine frames per second
        clock.tick(FPS)


def game_pause():
    pygame.mixer.music.pause()

    global paused
    paused = True

    font = pygame.font.Font('freesansbold.ttf', 80)
    text_output = font.render("Paused", True, BLACK)
    text_rect = text_output.get_rect()
    text_rect.center = (int(DISPLAY_WIDTH / 2), 220)
    game_display.blit(text_output, text_rect)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button = PausedButton(mouse, click)
        button.button_draw()
        button.button_text(RECT_GREEN, "Continue")
        button.button_text(RECT_RED, "CHICK OUT")

        pygame.display.update()
        pygame.event.get()
        clock.tick(15)


def crash(text):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    intro = True
    font = pygame.font.Font('freesansbold.ttf', 80)
    text_output = font.render(text, True, BLACK)
    text_rect = text_output.get_rect()
    text_rect.center = (int(DISPLAY_WIDTH / 2), 220)
    game_display.blit(text_output, text_rect)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button = IntroButton(mouse, click)
        button.button_draw()
        button.button_text(RECT_GREEN, "PLAY AGAIN!")
        button.button_text(RECT_RED, "CHICK OUT")

        pygame.display.update()
        pygame.event.get()
        clock.tick(15)


# call the game
game_intro()
game_loop()
# stop pygame
pygame.quit()
# system quit
quit()
