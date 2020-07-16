import pygame
import os
import math
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.font.init()

# define fonts
font_label = pygame.font.SysFont("comicsans", 50)
font_screen = pygame.font.Font("freesansbold.ttf", 80)
font_button = pygame.font.Font("freesansbold.ttf", 20)

# declaration of of constant variables
WINDOW_SIZE = (800, 600)
FPS = 60
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PLAYER_HEIGHT = 86
PLAYER_WIDTH = 64
PLAYER_START_Y = 532
PLAYER_VEL = 10
HOVER_RED = (255, 0, 0)
HOVER_GREEN = (0, 255, 0)
HOVER_BLUE = (0, 0, 255)
RECT_GREEN = (500, 350, 150, 50)
RECT_RED = (150, 350, 150, 50)
RECT_INFO = (325, 450, 150, 50)

# obstacles und platforms to check collision
Left_BORDER_1 = (130, 386)
BOTTOM_1 = [[305, 455], [532, 580]]
BOTTOM_2 =  [[130, 305], [PLAYER_START_Y, 400]]
BOTTOM_3 = [[450, 800], [PLAYER_START_Y, 400]]
PLATFORM_1 = [[0, 222], [386, 0]]

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

# loading images
player_stands_right = pygame.image.load("stands_right.png")
player_stands_left = pygame.image.load("stands_left.png")
player_walks_right1 = pygame.image.load("walks_right1.png")
player_walks_right2 = pygame.image.load("walks_right2.png")
player_walks_left1 = pygame.image.load("walks_left1.png")
player_walks_left2 = pygame.image.load("walks_left2.png")
player_walks_pause_right = pygame.image.load("walks_pause_right.png")
player_walks_pause_left = pygame.image.load("walks_pause_left.png")
player_jump_right = pygame.image.load("player_jump_right.png")
player_fall_right = pygame.image.load("player_fall_right.png")
player_jump_left = pygame.image.load("player_jump_left.png")
player_fall_left = pygame.image.load("player_fall_left.png")
enemy_walk_right = (pygame.image.load("enemy_walks_right1.png"), pygame.image.load("enemy_walks_right2.png"))
enemy_walk_left = (pygame.image.load("enemy_walks_left1.png"), pygame.image.load("enemy_walks_left2.png"))
enemy_right_attack = (pygame.image.load("enemy_right_attack1.png"), pygame.image.load("enemy_right_attack2.png"),
                      pygame.image.load("enemy_right_attack3.png"), pygame.image.load("enemy_right_attack4.png"))
enemy_left_attack = (pygame.image.load("enemy_left_attack1.png"), pygame.image.load("enemy_left_attack2.png"),
                     pygame.image.load("enemy_left_attack3.png"), pygame.image.load("enemy_left_attack4.png"))
background = pygame.image.load("background.png").convert()

bullet = pygame.mixer.Sound("bullet.wav")
hit = pygame.mixer.Sound("hit.wav")
music = pygame.mixer.music.load("dark_souls_-_E.S. Gwyn_by_RoeTaka.mp3")

bullets = []
paused = True
enemies = 1
enemy = list()


class Player:
    def __init__(self, x, y, w, h, v):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.walk_count = 0 # check steps to adjust the sprites for animations
        self.right = False # player movement right and v.c.
        self.left = False
        self.player = player_stands_right
        self.view_left = False # view of the player to adjust which sprite to use
        if bool(random.getrandbits(1)):
            self.view_left = True
            self.view_right = False
        else:
            self.view_right = True
            self.view_left = False
        self.view_up = False # same for jump
        self.view_down = False
        self.check_border_left = True # to check whether a border is near the player
        self.check_border_right = True
        self.check_jump_up = True # whether player can jump for collision
        self.check_jump_down = False
        self.is_jumped = False
        self.jump_count = 10 # same as with walk
        self.jump_vel = 10
        self.check_bottom1 = False
        self.hits = 0

    def draw(self):
        window.blit(self.player, (self.x, self.y))

    def move(self):
        keys_pressed = pygame.key.get_pressed()

        # player is allowed to jump at the start
        self.check_jump_up = True
        self.check_jump_down = False

        # checking for collision and borders
        self.border()

        if keys_pressed[pygame.K_a]:
            if self.check_border_left:
                self.x -= self.v
                # player is allowed to move right
                self.check_border_right = True
            self.left = True
            self.right = False
        elif keys_pressed[pygame.K_d]:
            if self.check_border_right:
                self.x += self.v
                self.check_border_left = True
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False
            self.walk_count = 0

        if keys_pressed[pygame.K_w]:
            self.is_jumped = True

        self.jump()
        self.animation()

    def animation(self):
        if self.right:
            self.view_left = False
            self.view_right = True
            # calculate frames per sprite
            if self.walk_count % 3 <= 0:
                self.player = player_walks_right1
                self.walk_count += 1
            elif 1 <= self.walk_count % 3 < 2:
                self.player = player_walks_right2
                self.walk_count += 1
            else:
                self.walk_count = 0

        if self.left:
            self.view_left = True
            self.view_right = False
            if self.walk_count % 3 <= 0:
                self.player = player_walks_left1
                self.walk_count += 1
            elif 1 <= self.walk_count % 3 < 2:
                self.player = player_walks_left2
                self.walk_count += 1
            else:
                self.walk_count = 0

        if not(self.right or self.left):
            if self.view_right:
                self.player = player_stands_right
            elif self.view_left:
                self.player = player_stands_left

        # adjust sprites
        if self.view_up and self.view_right:
            self.player = player_jump_right
        elif self.view_up and self.view_left:
            self.player = player_jump_left
        elif self.view_down and self.view_right:
            self.player = player_fall_right
        elif self.view_down and self.view_left:
            self.player = player_fall_left

    def jump(self):
        # quadratic formula to express the jump
        if self.is_jumped:
            if self.jump_vel > 0:
                if self.check_jump_up:
                    self.y -= int((self.jump_vel ** 2) * 0.8)
                    self.jump_vel -= 2
                    self.view_up = True
                    self.view_down = False
                    self.check_jump_down = True
                else: # stop jumping up happens when obstacle up
                    self.jump_vel = 0
            elif self.jump_vel >= -self.jump_count:
                self.y += int((self.jump_vel ** 2) * 0.8)
                # endless fall except border in front
                self.jump_count += 1
                self.jump_vel -= 2
                self.view_down = True
                self.view_up = False
                # when the border is under the player jump should stop
                if  not self.check_jump_down and self.y + self.h >= PLAYER_START_Y:
                    if BOTTOM_2[0][0] - 40 <= self.x <= BOTTOM_2[0][1]:
                        self.y = PLAYER_START_Y - self.h
                        self.jump_count = 10
                    elif  BOTTOM_1[0][0] < self.x  and self.x + self.w < BOTTOM_1[0][1]:
                        self.y = BOTTOM_1[1][1] - self.h
                        self.jump_count = 10
                    elif BOTTOM_3[0][0] < self.x + self.w < BOTTOM_3[0][1]:
                        self.y = PLAYER_START_Y - self.h
                        self.jump_count = 10
                elif self.check_jump_down and self.y > 375 - self.h:
                    self.y = 375 - self.h
                    self.check_jump_down = False
                    self.jump_vel = -15
                    self.jump_count = 10
            else:
                self.is_jumped = False
                self.jump_vel = 10
                self.jump_count = 10
                self.view_up = False
                self.view_down = False


    def border(self):
        # special conditions when the is in front of borders and platforms to reject this
        # walking limits
        if self.x < Left_BORDER_1[0] and self.y > Left_BORDER_1[1]:
            self.check_border_left = False
            # fix glitches
            if self.x < Left_BORDER_1[0] - self.v:
                self.x += self.v
        if self.x < 0 and self.y < Left_BORDER_1[1]:
            self.check_border_left = False
        if self.x + self.w >= WINDOW_SIZE[0]:
            self.check_border_right = False
        if BOTTOM_1[0][0] < self.x < BOTTOM_1[0][1] - self.w and not self.is_jumped:
            if self.y < BOTTOM_1[1][1]:
                self.y = BOTTOM_1[1][1] - self.h
        if self.y >= BOTTOM_1[1][1] - self.h:
            if self.x < BOTTOM_1[0][0]:
                self.x += self.v
            elif self.x > BOTTOM_1[0][1] - self.w:
                self.x -= self.v
        if self.y <= PLAYER_START_Y - self.h - 20 and not self.is_jumped:
            if self.x > PLATFORM_1[0][1]:
                self.y += int(self.v**2 * 0.8)

        # jumping limits
        # raw numbers are just for adjusting position to look better - difficult because of rect hitbox
        if self.y <= BOTTOM_1[1][1] and self.is_jumped:
            self.check_jump_down = False
        if PLATFORM_1[0][0] < self.x + 15 < PLATFORM_1[0][1]:
            if self.is_jumped:
                if PLATFORM_1[1][0] + 15 > self.y > PLATFORM_1[1][0] - 25:
                    self.check_jump_up = False
                elif self.y - self.h < PLATFORM_1[1][0] - 100:
                    self.check_jump_down = True

    def hit(self):
        self.hits += 1

    def score(self):
        text_score = font_label.render("Score: " + str(self.hits), True, BLACK)
        window.blit(text_score, (10, 10))


    def check(self):
        for j in enemy:
            if self.y + PLAYER_HEIGHT > j.y and self.y < j.y + j.h:
                if self.x < j.x + j.w and self.x + PLAYER_WIDTH > j.x:
                    font = pygame.font.SysFont("comicsans", 100)
                    text_score = font.render("-10", 1, RED)
                    window.blit(text_score, (int(WINDOW_SIZE[0] / 2 - (text_score.get_width() / 2)), 200))
                    pygame.display.update()
                    pygame.time.delay(500)
                    # to exit the game
                    for event in pygame.event.get():
                        if event == pygame.QUIT:
                            pygame.quit()
                            quit()
                    # respawn enemy
                    j.health = 0
                    player.hits -= 10
                    j.health_bar(j)


class Projectiles:
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.v = 20 * self.direction

    def draw(self):
        pygame.draw.circle(window, (0, 0, 255), (self.x, self.y), self.radius)

    @staticmethod
    def move(i):
        global bullets
        if 0 < i.x < WINDOW_SIZE[0]:
            i.x += i.v
        else:
            bullets.pop(bullets.index(i))

    @staticmethod
    def create_bullets():
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_s]:
            if player.view_right:
                bullets.append(Projectiles(round(player.x + player.w // 2), round(player.y + player.h // 2),
                                             6, (0, 0, 255), 1))
                bullet.play()
            else:
                bullets.append(Projectiles(round(player.x + player.w // 2), round(player.y + player.h // 2),
                                             6, (0, 0, 255), -1))

    @staticmethod
    def check(i, j):
        # check collision with enemy
        if i.y + i.radius > j.y and i.y - i.radius < j.y + j.h:
            if i.x - i.radius > j.x and i.x + i.radius < j.x + j.w:
                if len(bullets) > 0:
                    bullets.remove(i)
                player.hit()
                j.health_bar(j)
                hit.play()

        # avoiding spamming bullets
        for j in bullets:
            if len(bullets) >= 2:
                if i == bullets[-1] and j == bullets[-2]:
                    if math.sqrt(abs(i.x - j.x) ** 2 + abs(i.y - j.y) ** 2) < 200:
                        bullets.pop(-1)
        if len(bullets) >= 1:
            if i.x + i.radius < Left_BORDER_1[0] + 20 and i.y - i.radius > Left_BORDER_1[1]:
                if len(bullets) > 0:
                    bullets.remove(i)
            elif i.y + i.radius >= BOTTOM_1[1][0]:
                if i.x - i.radius < BOTTOM_1[0][0] or i.x + i.radius > BOTTOM_1[0][1]:
                    bullets.remove(i)


class Enemy:
    def __init__(self, x, y, w, h, v, start, end):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.path = [start, end]
        self.walk_count = 0
        self.enemy = player_stands_left
        self.is_jumped = False
        self.counter = 0
        self.attack = False
        self.no_attack = True
        self.walk_limit = 7
        self.health = 100
        self.dead = False # helpful to not waste ram in case of multiple enemies - not implanted atm

    def draw(self):
        if not self.dead:
            if self.walk_count >= 4 and self.counter < self.walk_limit:
                self.walk_count = 0
            else:
                if self.v > 0 and self.counter < self.walk_limit:
                    self.enemy = enemy_walk_right[self.walk_count // 2]
                    self.walk_count += 1
                    self.counter += 1
                elif self.v < 0 and self.counter < self.walk_limit:
                    self.enemy = enemy_walk_left[self.walk_count // 2]
                    self.walk_count += 1
                    self.counter+= 1
                elif self.no_attack and self.counter < 16:
                    self.walk_count = 0

            if self.counter == self.walk_limit:
                self.walk_count = 0
                self.no_attack = False
                self.attack = True

            if self.counter > self.walk_limit + 4:
                self.counter = 0
                self.walk_count = 0
                self.attack = False
                self.no_attack = True

            if self.counter >= self.walk_limit:
                if self.walk_count < 4 and self.attack:
                    if self.v > 0:
                        self.enemy = enemy_right_attack[self.walk_count // 1]
                        self.walk_count += 1
                        self.counter += 1
                    elif self.v < 0:
                        self.enemy = enemy_left_attack[self.walk_count // 1]
                        self.walk_count += 1
                        self.counter += 1
                else:
                    self.counter = 0
                    self.walk_count = 0

            window.blit(self.enemy, (self.x, self.y))
            if self.v > 0:
                pygame.draw.rect(window, RED, (self.x + 5, self.y - 15, 50, 5))
                pygame.draw.rect(window, GREEN, (self.x + 5, self.y - 15, 50 - int((0.5 * (100 - self.health))), 5))
            else:
                pygame.draw.rect(window, RED, (self.x + 10, self.y - 15, 50, 5))
                pygame.draw.rect(window, GREEN, (self.x + 10, self.y - 15, 50 - int((0.5 * (100 - self.health))), 5))

    def move(self):
        if self.v > 0:
            if self.x + self.v < self.path[1]:
                self.x += self.v
            else:
                self.v = -self.v
                self.walk_count = 0
            if BOTTOM_1[0][1] <= self.x + self.w <= BOTTOM_1[0][1] + self.v:
                self.y = PLAYER_START_Y - self.h

        else:
            if self.x + self.v > self.path[0]:
                self.x += self.v
            else:
                self.v = -self.v
                self.walk_count = 0
            if BOTTOM_1[0][0] >= self.x:
                self.y = PLAYER_START_Y - self.h

        if self.x > BOTTOM_1[0][0] and self.x + self.w < BOTTOM_1[0][1]:
            if self.y + self.h >= BOTTOM_1[1][0] and not self.is_jumped:
                self.y = BOTTOM_1[1][1] - self.h

    def health_bar(self, i):
        global enemies
        global enemy
        # 10 and not 0 otherwise needs 11 hits
        if self.health > 10:
                self.health -= 10
        else:
            enemy.remove(i)
            if len(enemy) == 0:
                #enemies += 1 no idea how to implant multiple enemies properly
                enemy = list()
                for j in range(enemies):
                    enemy_x = random.randint(100, 700)
                    while abs(player.x - enemy_x) < 350:
                        if player.x > 350:
                            enemy_x -= 1
                        else:
                            enemy_x += 1
                    if bool(random.getrandbits(1)):
                        enemy_v = PLAYER_VEL
                    else:
                        enemy_v = -PLAYER_VEL
                    if BOTTOM_1[0][0] > enemy_x > BOTTOM_1[0][1]:
                        enemy.append(Enemy(enemy_x, BOTTOM_1[1][1] - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, enemy_v, 100, 700))
                    else:
                        enemy.append(Enemy(enemy_x, PLAYER_START_Y - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, enemy_v, 100, 700))


class ButtonPause:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        global paused
        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(window, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(window, RED, RECT_RED)
        if RECT_GREEN[0] < self.mouse[0] < RECT_GREEN[0] + RECT_GREEN[2] and \
                RECT_GREEN[1] < self.mouse[1] < RECT_GREEN[1] + RECT_GREEN[3]:
            pygame.draw.rect(window, HOVER_GREEN, RECT_GREEN)
            if self.click[0] == 1:
                pygame.mixer.music.unpause()
                paused = False
        else:
            pygame.draw.rect(window, GREEN, RECT_GREEN)

    @staticmethod
    def button_text(rect, text):
        text_output = font_button.render(text, True, BLACK)
        text_rect = text_output.get_rect()
        text_rect.center = (rect[0] + int((rect[2] / 2)), rect[1] + int((rect[3] / 2)))
        window.blit(text_output, text_rect)


class ButtonIntro:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(window, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(window, RED, RECT_RED)
        if RECT_GREEN[0] < self.mouse[0] < RECT_GREEN[0] + RECT_GREEN[2] and \
                RECT_GREEN[1] < self.mouse[1] < RECT_GREEN[1] + RECT_GREEN[3]:
            pygame.draw.rect(window, HOVER_GREEN, RECT_GREEN)
            if self.click[0] == 1:
                game_loop()

        else:
            pygame.draw.rect(window, GREEN, RECT_GREEN)

    @staticmethod
    def button_text(rect, text):
        text_output = font_button.render(text, True, BLACK)
        text_rect = text_output.get_rect()
        text_rect.center = (rect[0] + int((rect[2] / 2)), rect[1] + int((rect[3] / 2)))
        window.blit(text_output, text_rect)

class ButtonInfo:
    def __init__(self, mouse, click, rect, text):
        self.mouse = mouse
        self.click = click
        self.rect = rect
        self.text = text

    def button_draw(self):
        if RECT_INFO[0] < self.mouse[0] < RECT_INFO[0] + RECT_INFO[2] and \
                RECT_INFO[1] < self.mouse[1] < RECT_INFO[1] + RECT_INFO[3]:
            pygame.draw.rect(window, HOVER_BLUE, RECT_INFO)
            if self.click[0] == 1:
                pass
                game_info()
        else:
            pygame.draw.rect(window, BLUE, RECT_INFO)

        text_output = font_button.render(self.text, True, BLACK)
        text_rect = text_output.get_rect()
        text_rect.center = (self.rect[0] + int((self.rect[2] / 2)), self.rect[1] + int((self.rect[3] / 2)))
        window.blit(text_output, text_rect)

    @staticmethod
    def info_text():
        text_output_arrows = font_button.render("Try not to get hit from the skeleton", True, BLACK, WHITE)
        text_rect_arrows = text_output_arrows.get_rect()
        text_rect_arrows.center = (int(WINDOW_SIZE[0] / 2), 200)
        window.blit(text_output_arrows, text_rect_arrows)
        text_output_spacebar = font_button.render("Use your canon (S) to shoot the enemy down", True, BLACK, WHITE)
        text_rect_spacebar = text_output_spacebar.get_rect()
        text_rect_spacebar.center = (int(WINDOW_SIZE[0] / 2), 220)
        window.blit(text_output_spacebar, text_rect_spacebar)
        text_output_obstacle = font_button.render("Your goal is to shoot the enemy as much down as you can", True, BLACK, WHITE)
        text_rect_obstacle = text_output_obstacle.get_rect()
        text_rect_obstacle.center = (int(WINDOW_SIZE[0] / 2), 240)
        window.blit(text_output_obstacle, text_rect_obstacle)
        text_output_control = font_button.render("Controls: Move with A, D & W and pause the game with the spacebar", True, BLACK, WHITE)
        text_rect_control = text_output_control.get_rect()
        text_rect_control.center = (int(WINDOW_SIZE[0] / 2), 260)
        window.blit(text_output_control, text_rect_control)


def game_intro():
    intro = True
    window.blit(background, (0, 0))
    text_output = font_screen.render("Platformer", True, BLACK)
    text_rect = text_output.get_rect()
    text_rect.center = (int(WINDOW_SIZE[0] / 2), 220)
    window.blit(text_output, text_rect)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button = ButtonIntro(mouse, click)
        button.button_draw()
        button_info = ButtonInfo(mouse, click, RECT_INFO, "Information")
        button_info.button_draw()
        button.button_text(RECT_GREEN, "GO")
        button.button_text(RECT_RED, "CHICK OUT")

        pygame.display.update()
        pygame.event.get()
        clock.tick(15)

def game_info():
    intro = True
    window.blit(background, (0, 0))
    text_output = font_screen.render("Information", True, BLACK)
    text_rect = text_output.get_rect()
    text_rect.center = (int(WINDOW_SIZE[0] / 2), 100)
    window.blit(text_output, text_rect)

    ButtonInfo.info_text()

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button = ButtonIntro(mouse, click)
        button.button_draw()
        button.button_text(RECT_GREEN, "GO")
        button.button_text(RECT_RED, "CHICK OUT")

        pygame.display.update()
        pygame.event.get()
        clock.tick(15)

def game_pause():
    pygame.mixer.music.pause()

    global paused
    paused = True

    text_output = font_screen.render("Paused", True, BLACK)
    text_rect = text_output.get_rect()
    text_rect.center = (int(WINDOWS_SIZE[0] / 2), 220)
    window.blit(text_output, text_rect)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button = ButtonPause(mouse, click)
        button.button_draw()
        button.button_text(RECT_GREEN, "Continue")
        button.button_text(RECT_RED, "CHICK OUT")

        pygame.display.update()
        pygame.event.get()
        clock.tick(15)


def draw():
    window.blit(background, (0, 0))
    player.move()
    for i in enemy:
        i.move()
    player.score()
    Projectiles.create_bullets()
    for i in bullets:
        i.move(i)
        for j in enemy:
            '''if len(enemy) >= 2:  for multiple enemies - does not work atm
                if j != enemy[-1]:'''
            i.check(i, j)
            '''else:
                i.check(i, j)'''
        i.draw()
    player.draw()
    for i in enemy:
        i.draw()
        player.check()
    pygame.display.update()


def game_loop():

    pygame.mixer.music.play(-1)

    global player
    player_x = random.randint(100, 700)
    if BOTTOM_1[0][0] > player_x > BOTTOM_1[0][1]:
        player = Player(player_x, BOTTOM_1[1][1] - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL)
    else:
        player = Player(player_x, PLAYER_START_Y - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL)

    enemy_x = random.randint(100, 700)
    while abs(player_x - enemy_x) < 350:
        if player_x > 350:
            enemy_x -= 1
        else:
            enemy_x += 1
    if bool(random.getrandbits(1)):
        enemy_v = PLAYER_VEL
    else:
        enemy_v = -PLAYER_VEL
    if BOTTOM_1[0][0] > enemy_x > BOTTOM_1[0][1]:
        enemy.append(Enemy(enemy_x, BOTTOM_1[1][1] - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, enemy_v, 100, 700))
    else:
        enemy.append(Enemy(enemy_x, PLAYER_START_Y - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, enemy_v, 100, 700))

    run = True

    while run:

        clock.tick(FPS)
        pygame.time.delay(100)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if keys_pressed[pygame.K_SPACE]:
                game_pause()

        draw()

game_intro()
game_loop()
