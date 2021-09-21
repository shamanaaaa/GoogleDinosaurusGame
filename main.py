import random
import time
import pygame
import sys
from random import choice

pygame.init()

size = width, height = 1200, 800
background_speed = [-1, 0]
floor_speed = [-2, 0]
dyno_speed = [0, 0]
tree_speed = [-2, 0]
black = 0, 0, 0
in_jump = False
dino_jump_speed = 2
dino_jump_timer = 150
jump_timer = 0
floor_0 = 0
score = 0

screen = pygame.display.set_mode(size)
my_font = pygame.font.SysFont("monospace", 26)

floor = pygame.image.load("images/floor.png")
floor = pygame.transform.scale(floor, (2000, 150))
floor_rect = floor.get_rect()
floor_rect.update(0, 660, 0, 0)

background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (1200, 800))
background_rect = background.get_rect()
background_rect.update(0, 0, 0, 0)

background2 = pygame.image.load("images/background.jpg")
background2 = pygame.transform.scale(background2, (1200, 800))
background_rect2 = background2.get_rect()
background_rect2.update(1200, 0, 0, 0)

dino = pygame.image.load("images/dino.png")
dino = pygame.transform.scale(dino, (200, 200))
dino_rect = dino.get_rect()
dino_rect.update(105, 300, 0, 0)


def make_tree():
    return Tree(1199, 575, "images/tree1.png")


class Tree(pygame.sprite.Sprite):

    def __init__(self, dx, dy, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(x=dx, y=dy)
        self.speed = tree_speed

    def update(self):
        self.rect = self.rect.move(self.speed)

    def reset(self):
        self.rect = self.rect.move(1300, 0)

    def draw(self, screen_x):
        screen_x.blit(self.image, self.rect)


tree = make_tree()


def collision():
    if tree.rect.left - 136 == dino_rect.left and not in_jump or \
            tree.rect.left - 135 == dino_rect.left and not in_jump or \
            tree.rect.left - 137 == dino_rect.left and not in_jump:
        time.sleep(2)
        return True

    elif tree.rect.left in range(70, 190) and in_jump and dino_rect.bottom > 390:
        time.sleep(2)
        return True
    else:
        return False


def reboot_game():
    time.sleep(1)
    floor_rect.update(0, 660, 0, 0)
    background_rect.update(0, 0, 0, 0)
    background_rect2.update(1200, 0, 0, 0)
    global in_jump, jump_timer, floor_0, tree, dino_jump_timer, dino_jump_speed, score
    in_jump = False
    jump_timer = 0
    floor_0 = 0
    tree.kill()
    tree = make_tree()
    background_speed[0] = -1
    floor_speed[0] = -2
    tree.speed[0] = -2
    dino_jump_timer = 150
    dino_jump_speed = 2
    score = 0


def level_up():
    global background_speed, floor_speed, dyno_speed, tree, dino_jump_speed, dino_jump_timer, score
    if background_speed[0] < -13:
        pass
    else:
        background_speed[0] -= 1
    if floor_speed[0] < -14:
        pass
    else:
        floor_speed[0] -= 1
    if tree_speed[0] < -14:
        pass
    else:
        tree.speed[0] -= 1
    dyno_speed[1] += 1
    dino_jump_speed += 1
    dino_jump_timer -= 20
    score += 1


while True:
    # quit control
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # key jump control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        in_jump = True

    # print(pygame.mouse.get_pos())

    floor_rect = floor_rect.move(floor_speed)
    dino_rect = dino_rect.move(dyno_speed)
    background_rect = background_rect.move(background_speed)
    background_rect2 = background_rect2.move(background_speed)

    # moving floor
    if floor_rect.left < -666:
        floor_rect.update(0, 660, 0, 0)

    # moving background
    if background_rect.left < -1200:
        background_rect.update(0, 0, 0, 0)

    # moving background2
    if background_rect2.left < 0:
        background_rect2.update(1200, 0, 0, 0)

    # moving tree
    if tree.rect.left < -100:
        tree.kill()
        tree = make_tree()
        level_up()

    # jump
    if dino_jump_speed > 8:
        dino_jump_speed = 8
    if dino_jump_timer < 30:
        dino_jump_timer = 30
    if in_jump and jump_timer < dino_jump_timer:
        jump_timer += 1
        dyno_speed[1] = -1 * dino_jump_speed
    elif in_jump:
        jump_timer += 1
        dyno_speed[1] = dino_jump_speed
        if dino_rect[1] > 480:
            dyno_speed[1] = 0
            in_jump = False
            jump_timer = 0
    else:  # dino copying floor
        dino_rect.update(105, 480, 0, 0)

    if collision():
        reboot_game()
    screen.fill((0, 0, 0, 255))
    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    tree.draw(screen)
    tree.update()
    screen.blit(floor, floor_rect)
    screen.blit(dino, dino_rect)
    score_text = my_font.render(f"Score: {score}".format(screen), True, (0, 0, 0))
    screen.blit(score_text, (5, 10))
    pygame.display.update()
