import pygame
import random
import os
import time
import sys
from pygame.locals import *

from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))

from Games.Game_Module import Game


WIDTH = 600
HEIGHT = 600

BLOCK_SIZE = 10

black = (0, 0, 0)
green = (0, 140, 0)
red = (255, 0, 0)
white = (255, 255, 255)

UP = (0, -BLOCK_SIZE)
DOWN = (0, BLOCK_SIZE)
RIGHT = (BLOCK_SIZE, 0)
LEFT = (-BLOCK_SIZE, 0)

MOUSE_QUIT = 1
SPACE = 0


# ----------------------------------------------------------------------------
class Apple():

    def __init__(self):
        self.surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.surface.fill(red)
        self.set_position()

    def set_position(self):
        self.position = (random.randint(0, WIDTH - BLOCK_SIZE) // 10 * 10,
                         random.randint(0, HEIGHT - BLOCK_SIZE) // 10 * 10)

    def get_position(self):
        return self.position

    def draw(self, screen):
        screen.blit(self.surface, self.position)


# ----------------------------------------------------------------------------
class Snake():
    def __init__(self):

        self.head = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.head.fill(white)

        self.body = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.body.fill(green)

        self.positions = [(WIDTH / 2, HEIGHT / 2),
                          (WIDTH / 2 + BLOCK_SIZE, HEIGHT / 2),
                          (WIDTH / 2 + 2 * BLOCK_SIZE, HEIGHT / 2)]

        self.direction = random.choice([UP, DOWN, LEFT])

    def set_direction(self, my_direction):
        if my_direction is None:
            return
        self.direction = my_direction

    def move(self):

        self.positions.insert(0, self.positions[0])
        self.positions.pop()

        self.positions[0] = (self.positions[0][0] + self.direction[0],
                             self.positions[0][1] + self.direction[1])

    def grow(self):

        self.positions.append((0, 0))

    def get_head_position(self):

        return self.positions[0]

    def draw(self, my_screen):
        for position in self.positions[1:]:
            my_screen.blit(self.body, position)

        my_screen.blit(self.head, self.get_head_position())

    def collision(self):
        head = self.get_head_position()

        if head[0] < 0 or head[0] >= WIDTH:
            return True

        elif head[1] < 0 or head[1] >= HEIGHT:
            return True

        elif self.positions.count(head) > 1:
            return True


# --------------------------------------------------------------------------------
class Snake_Game(Game):

    def __init__(self):

        KEY_TO_EVENTS = {K_UP: UP, K_DOWN: DOWN, K_LEFT: LEFT,
                         K_RIGHT: RIGHT, K_SPACE: SPACE, K_ESCAPE: MOUSE_QUIT}

        Game.__init__(self, 'Snake Game', WIDTH, HEIGHT, KEY_TO_EVENTS)

        self.my_snake = Snake()
        self.my_apple = Apple()

    def text_objects(self, text, pst1, pst2, size):

        my_font = pygame.font.SysFont('comicsansms', size)
        my_sentence = my_font.render(text, True, (255, 255, 255))

        position = my_sentence.get_rect()
        position.center = ((pst1/2), (pst2/2))

        return my_sentence, position

    def start(self):
        my_sentence, position = self.text_objects('Snake Game', WIDTH, HEIGHT, 75)
        self.screen.blit(my_sentence, position)

        my_sentence, position = self.text_objects('Press Space to Start', WIDTH, HEIGHT*5/4, 30)
        self.screen.blit(my_sentence, position)

        pygame.display.update()

        while True:

            if self.get_key() == SPACE:
                return True

            if self.get_key() == MOUSE_QUIT:
                pygame.quit()

    def ending(self):
        time.sleep(2)
        self.screen.fill(black)

        my_sentence, position = self.text_objects('You Lose', WIDTH, HEIGHT, 75)
        self.screen.blit(my_sentence, position)

        my_sentence, position = self.text_objects('Press Space', WIDTH, HEIGHT*5/4, 30)
        self.screen.blit(my_sentence, position)

        pygame.display.update()

        while True:

            if self.get_key() == SPACE:
                self.__init__()
                self.run()

            if self.get_key() == MOUSE_QUIT:
                pygame.quit()


    def eat(self):
        if self.my_snake.get_head_position() == self.my_apple.get_position():
            return True

    def get_key(self):

        for event in pygame.event.get():

            if event.type == QUIT:
                return MOUSE_QUIT

            if event.type == KEYDOWN:
                if event.key in Game.KEY_TO_EVENTS:
                    return Game.KEY_TO_EVENTS[event.key]


    def run(self):

        self.start()

        while True:
            self.clock.tick(20)
            self.screen.fill(black)
            self.my_snake.set_direction(self.get_key())
            self.my_snake.move()
            self.my_apple.draw(self.screen)
            self.my_snake.draw(self.screen)

            if self.eat():
                self.my_snake.grow()
                self.my_apple.set_position()

            pygame.display.update()

            if self.my_snake.collision():
                self.ending()


# --------------------------------------------------------------------------------
game = Snake_Game()
game.run()
