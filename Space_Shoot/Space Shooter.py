import pygame
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.mixer.init()

# define fonts
font = pygame.font.SysFont("comicsans", 50)
font_screen = pygame.font.Font("freesansbold.ttf", 80)
font_button = pygame.font.Font("freesansbold.ttf", 20)

# declare constants
WINDOW_SIZE = (800, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Space Shooter")
FPS = 60
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HOVER_RED = (255, 0, 0)
HOVER_GREEN = (0, 255, 0)
HOVER_BLUE = (0, 0, 255)
RECT_GREEN = (500, 350, 150, 50)
RECT_RED = (150, 350, 150, 50)
RECT_INFO = (325, 450, 150, 50)

# load images
ENEMY_RED_SHIP = pygame.image.load(os.path.join("assets", "enemyRed3.png"))  # or assets/enemy...
ENEMY_BLUE_SHIP = pygame.image.load(os.path.join("assets", "enemyBlue3.png"))
ENEMY_GREEN_SHIP = pygame.image.load(os.path.join("assets", "enemyGreen3.png"))

# player
PLAYER_RED_SHIP = pygame.image.load(os.path.join("assets", "playerShip2_red.png"))
PLAYER_SIZE = (100, 67)

# laser
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))

# sound
sound_laser = pygame.mixer.Sound("laser.wav")
sound_hit = pygame.mixer.Sound("hit.wav")
sound_crash = pygame.mixer.Sound("crash.wav")

paused = True


class Laser:
    def __init__(self, x, y, img, v=10):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.v = v

    def draw(self):
        WINDOW.blit(self.img, (self.x, self.y - 30))

    def move(self, v):
        self.y += v

    def off_screen(self):
        return self.y >= WINDOW_SIZE[1] or self.y <= 0

    @staticmethod
    def collision(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health=100, v=3):
        self.x = x
        self.y = y
        self.health = health
        self.v = v
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self):
        WINDOW.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw()

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            sound_laser.play()

    def move_laser(self, player):
        self.cooldown()
        for laser in self.lasers:
            laser.move(laser.v // 2)
            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.collision(player, laser):
                player.health -= 10
                sound_hit.play()
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Enemy(Ship):
    COLOR_MAP = {
        "red": (ENEMY_RED_SHIP, RED_LASER),
        "blue": (ENEMY_BLUE_SHIP, BLUE_LASER),
        "green": (ENEMY_GREEN_SHIP, GREEN_LASER)
    }

    wave_length = 0

    def __init__(self, x, y, color, health=100, v=3):
        super().__init__(x, y, health, v)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self):
        self.y += self.v

    def check(self, player, enemy, enemies):
        # enemy off the screen
        if Laser.collision(enemy, player):
            player.health -= 10
            sound_crash.play()
            enemies.remove(enemy)

        if self.y + self.get_height() >= WINDOW_SIZE[1]:
            player.lives -= 1
            enemies.remove(enemy)

        # no enemies left => next level
        '''if len(enemies) == 0:
            self.v += 1'''

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 10, self.y + 50, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    @staticmethod
    def create_enemy(player, enemies):
        if len(enemies) == 0:
            player.level += 1
            Enemy.wave_length += 3
            while len(enemies) < Enemy.wave_length:
                enemy = Enemy(random.randrange(50, WINDOW_SIZE[0] - 50), random.randrange(-1500, -50),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
                if len(enemies) > 1:
                    # -2 for correct indexing not including last element
                    count = len(enemies) - 2
                    for i in range(0, count):
                        if enemies[i].x <= enemy.x <= enemies[i].x + enemies[i].get_width() \
                                or enemies[i].x <= enemy.x + enemy.get_width() <= enemies[i].x + enemies[i].get_width():
                            if enemies[i].y <= enemy.y <= enemies[i].y + enemies[i].get_height() \
                                    or enemies[i].y <= enemy.y + enemy.get_height() <= enemies[i].y + \
                                    enemies[i].get_height():
                                # idc why -1: count does nothing in this loop except to set the range which is set
                                count -= 1
                                enemies.pop(-1)


class Player(Ship):
    def __init__(self, x, y, health=100, v=10):
        super().__init__(x, y, health, v)
        self.level = 0
        self.lives = 5
        self.ship_img = PLAYER_RED_SHIP
        self.laser_img = GREEN_LASER
        # pixel perfect collision mask = hitbox - edit: more or less...
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a] and self.x - self.v >= 0:
            self.x -= self.v
        elif keys_pressed[pygame.K_a] and self.x >= 0:
            self.x -= 1
        if keys_pressed[pygame.K_d] and self.x + self.v + self.get_width() <= WINDOW_SIZE[0]:
            self.x += self.v
        elif keys_pressed[pygame.K_d] and self.x + self.get_width() <= WINDOW_SIZE[0]:
            self.x += 1
        if keys_pressed[pygame.K_w] and self.y - self.v >= 0:
            self.y -= self.v
        elif keys_pressed[pygame.K_w] and self.y >= 0:
            self.y -= 1
        if keys_pressed[pygame.K_s] and self.y + self.v + self.get_height() + 25 <= WINDOW_SIZE[1]:
            self.y += self.v
        elif keys_pressed[pygame.K_s] and self.y + self.get_height() + 25 <= WINDOW_SIZE[1]:
            self.y += 1

        if keys_pressed[pygame.K_SPACE]:
            self.shoot()

    def check(self, enemies):
        # game over screen
        if self.lives <= 0 or self.health <= 0:
            game_over_text = font.render("Game Over", 1, WHITE)
            WINDOW.blit(game_over_text, (int(WINDOW_SIZE[0] / 2 - game_over_text.get_width() / 2),
                                         int(WINDOW_SIZE[1] / 2 - game_over_text.get_height() / 2)))
            self.draw()
            pygame.display.update()
            pygame.time.delay(1000)
            # to exit the game
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.level = 0
            self.lives = 5
            self.health = 100
            enemies.clear()
            Enemy.wave_length = 0
            self.x, self.y = int(WINDOW_SIZE[0] / 2 - PLAYER_SIZE[0] / 2), 500

    def move_laser(self, enemies):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-laser.v)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for enemy in enemies:
                    if laser.collision(enemy, laser):
                        sound_hit.play()
                        enemies.remove(enemy)
                        self.lasers.remove(laser)

    def health_bar(self):
        pygame.draw.rect(WINDOW, (255, 0, 0), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(WINDOW, (0, 255, 0), (self.x, self.y + self.get_height() + 10,
                                               int(self.get_width() * (self.health / self.max_health)), 10))


def draw(player, enemies, enemy):
    WINDOW.blit(BACKGROUND, (0, 0))

    # draw text
    level_text = font.render(f"Level: {player.level}", 1, WHITE)
    lives_text = font.render(f"Lives: {player.lives}", 1, WHITE)
    WINDOW.blit(level_text, (10, 10))
    WINDOW.blit(lives_text, (WINDOW_SIZE[0] - 10 - lives_text.get_width(), 10))

    enemy.create_enemy(player, enemies)

    for enemy in enemies:
        enemy.move()
        enemy.move_laser(player)
        if random.randrange(0, 2 * 60) == 1:
            enemy.shoot()
    player.move()
    player.move_laser(enemies)

    for enemy in enemies:
        enemy.draw()
        enemy.check(player, enemy, enemies)
    player.check(enemies)
    player.draw()
    player.health_bar()

    pygame.display.update()


def game_loop():
    run = True
    player = Player(int(WINDOW_SIZE[0] / 2 - PLAYER_SIZE[0] / 2), 500)
    enemies = []
    # creating an enemy to call the methods
    enemy = Enemy(0, 0, "red")

    while run:
        clock.tick(FPS)

        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if keys_pressed[pygame.K_p]:
            game_pause()

        draw(player, enemies, enemy)


class ButtonIntro:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(WINDOW, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(WINDOW, RED, RECT_RED)
        if RECT_GREEN[0] < self.mouse[0] < RECT_GREEN[0] + RECT_GREEN[2] and \
                RECT_GREEN[1] < self.mouse[1] < RECT_GREEN[1] + RECT_GREEN[3]:
            pygame.draw.rect(WINDOW, HOVER_GREEN, RECT_GREEN)
            if self.click[0] == 1:
                game_loop()

        else:
            pygame.draw.rect(WINDOW, GREEN, RECT_GREEN)

    @staticmethod
    def button_text(rect, text):
        text_output = font_button.render(text, True, WHITE)
        text_rect = text_output.get_rect()
        text_rect.center = (rect[0] + int((rect[2] / 2)), rect[1] + int((rect[3] / 2)))
        WINDOW.blit(text_output, text_rect)


class ButtonInfo:
    def __init__(self, mouse, click, rect, text):
        self.mouse = mouse
        self.click = click
        self.rect = rect
        self.text = text

    def button_draw(self):
        if RECT_INFO[0] < self.mouse[0] < RECT_INFO[0] + RECT_INFO[2] and \
                RECT_INFO[1] < self.mouse[1] < RECT_INFO[1] + RECT_INFO[3]:
            pygame.draw.rect(WINDOW, HOVER_BLUE, RECT_INFO)
            if self.click[0] == 1:
                pass
                game_info()
        else:
            pygame.draw.rect(WINDOW, BLUE, RECT_INFO)

        text_output = font_button.render(self.text, True, WHITE)
        text_rect = text_output.get_rect()
        text_rect.center = (self.rect[0] + int((self.rect[2] / 2)), self.rect[1] + int((self.rect[3] / 2)))
        WINDOW.blit(text_output, text_rect)

    @staticmethod
    def info_text():
        text_output_arrows = font_button.render("Try not to get hit from the skeleton", True, WHITE)
        text_rect_arrows = text_output_arrows.get_rect()
        text_rect_arrows.center = (int(WINDOW_SIZE[0] / 2), 200)
        WINDOW.blit(text_output_arrows, text_rect_arrows)


class ButtonPause:
    def __init__(self, mouse, click):
        self.mouse = mouse
        self.click = click

    def button_draw(self):
        global paused
        if RECT_RED[0] < self.mouse[0] < RECT_RED[0] + RECT_RED[2] and \
                RECT_RED[1] < self.mouse[1] < RECT_RED[1] + RECT_RED[3]:
            pygame.draw.rect(WINDOW, HOVER_RED, RECT_RED)
            if self.click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(WINDOW, RED, RECT_RED)
        if RECT_GREEN[0] < self.mouse[0] < RECT_GREEN[0] + RECT_GREEN[2] and \
                RECT_GREEN[1] < self.mouse[1] < RECT_GREEN[1] + RECT_GREEN[3]:
            pygame.draw.rect(WINDOW, HOVER_GREEN, RECT_GREEN)
            if self.click[0] == 1:
                pygame.mixer.music.unpause()
                paused = False
        else:
            pygame.draw.rect(WINDOW, GREEN, RECT_GREEN)

    @staticmethod
    def button_text(rect, text):
        text_output = font_button.render(text, True, WHITE)
        text_rect = text_output.get_rect()
        text_rect.center = (rect[0] + int((rect[2] / 2)), rect[1] + int((rect[3] / 2)))
        WINDOW.blit(text_output, text_rect)


def game_intro():
    intro = True
    WINDOW.blit(BACKGROUND, (0, 0))
    text_output = font_screen.render("Space Shooter", True, WHITE)
    text_rect = text_output.get_rect()
    text_rect.center = (int(WINDOW_SIZE[0] / 2), 220)
    WINDOW.blit(text_output, text_rect)

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
    WINDOW.blit(BACKGROUND, (0, 0))
    text_output = font_screen.render("Information", True, WHITE)
    text_rect = text_output.get_rect()
    text_rect.center = (int(WINDOW_SIZE[0] / 2), 100)
    WINDOW.blit(text_output, text_rect)

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

    text_output = font_screen.render("Paused", True, WHITE)
    text_rect = text_output.get_rect()
    text_rect.center = (int(WINDOW_SIZE[0] / 2), 220)
    WINDOW.blit(text_output, text_rect)

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


game_intro()
game_loop()
