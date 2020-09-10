import pygame
import time
import os
import random

pygame.init()
pygame.font.init()
font_score = pygame.font.SysFont("timesnewroman", 40)
font_gameover = pygame.font.SysFont("timesnewroman", 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
os.environ['SDL_VIDEO_CENTERED'] = '1'

WINDOW_SIZE = (600, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Flappy Bird")
CLOCK = pygame.time.Clock()
FPS = 30

BIRD_IMGS = [pygame.image.load(os.path.join("imgs", "bird1.png")),
             pygame.image.load(os.path.join("imgs", "bird2.png")),
             pygame.image.load(os.path.join("imgs", "bird3.png"))]
PIPE_IMG = pygame.image.load(os.path.join("imgs", "pipe.png"))
BG_IMG = pygame.image.load(os.path.join("imgs", "bg.png"))
BASE_IMG = pygame.image.load(os.path.join("imgs", "base.png"))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            self.vel = -8
            self.tick_count = 0
            self.height = self.y

    def move(self):
        self.tick_count += 1

        d = (self.vel * self.tick_count) + 1.5 * self.tick_count ** 2

        if d >= 10:
            d = 10

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # to tilt around the center - idk why it works...
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(int(self.x), int(self.y))).center)

        WINDOW.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 150
    VEL = 7

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0                                 # x and y bool?
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 300)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self):
        WINDOW.blit(self.PIPE_TOP, (self.x, self.top))
        WINDOW.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 7
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        WINDOW.blit(self.IMG, (self.x1, self.y))
        WINDOW.blit(self.IMG, (self.x2, self.y))


def draw_window(bird, pipes, base, score):
    WINDOW.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw()
    base.draw()
    text_score = font_score.render(f"Score: {score}", 1, BLACK)
    WINDOW.blit(text_score, (10, 10))
    bird.draw()
    pygame.display.update()


def gameover():
    text_gameover = font_gameover.render("Game Over", 1, RED)
    WINDOW.blit(text_gameover, (int(WINDOW_SIZE[0] / 2 - text_gameover.get_width() / 2),
                                int(WINDOW_SIZE[1] / 2 - text_gameover.get_height() / 2)))
    pygame.display.update()
    pygame.time.delay(2000)
    main()


def main():
    run = True
    bird = Bird(100, 150)
    pipes = [Pipe(WINDOW_SIZE[0])]
    base = Base(WINDOW_SIZE[0] - BASE_IMG.get_height())
    score = 0

    while run:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                gameover()

            if not pipe.passed and pipe.x - 50 < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(WINDOW_SIZE[0]))

        for r in rem:
            pipes.remove(r)

        if bird.y > WINDOW_SIZE[1] - BASE_IMG.get_height():
            gameover()

        base.move()
        bird.jump()
        bird.move()
        draw_window(bird, pipes, base, score)


main()
