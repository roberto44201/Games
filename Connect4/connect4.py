import pygame
import numpy
import os
import math
import time
import sys
from pygame.locals import *

grey = (105, 105, 105)
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)

PLAYER_1 = 1
PLAYER_2 = 2

COLUMNS = 7
ROWS = 6
LAST_ROW = 0

PIECE_ROW_SIZE = 100
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 7.5)

WIDTH = COLUMNS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE + PIECE_ROW_SIZE


# ---------------------------------------------------------------------------------------
class Board():

    def __init__(self):
        self.game_spaces = numpy.zeros((ROWS, COLUMNS))
        self.game_board = pygame.Surface((COLUMNS * SQUARE_SIZE, ROWS * SQUARE_SIZE))
        self.game_board.fill(grey)

    def get_next_open_row(self, column):
        for r in range(ROWS - 1, LAST_ROW - 1, -1):
            if self.game_spaces[r][column] == 0:
                return r

    def is_column_available(self, column):
        if self.game_spaces[LAST_ROW][column] == 0:
            return True

    def draw(self, screen):
        screen.fill(white)
        screen.blit(self.game_board, (0, PIECE_ROW_SIZE))

        for rows in range(ROWS):
            for columns in range(COLUMNS):

                circle_coordenates = (int(columns*SQUARE_SIZE + SQUARE_SIZE / 2),
                                      int(rows*SQUARE_SIZE + PIECE_ROW_SIZE + SQUARE_SIZE / 2))

                if self.game_spaces[rows][columns] == 0:
                    pygame.draw.circle(screen, white, circle_coordenates, RADIUS)

                elif self.game_spaces[rows][columns] == PLAYER_1:
                    pygame.draw.circle(screen, red, circle_coordenates, RADIUS)

                elif self.game_spaces[rows][columns] == PLAYER_2:
                    pygame.draw.circle(screen, black, circle_coordenates, RADIUS)

        pygame.display.update()


# ---------------------------------------------------------------------------------------
class Players():

    def droping_piece(self, screen, piece_color):
        while True:
            self.event = game.get_event()

            self.piece_position = pygame.mouse.get_pos()
            self.piece_position_x = self.piece_position[0]
            self.piece_position_y = PIECE_ROW_SIZE / 2

            pygame.draw.rect(screen, white, (0, 0, WIDTH, PIECE_ROW_SIZE))

            pygame.draw.circle(screen, piece_color, (int(self.piece_position_x), int(self.piece_position_y)), RADIUS)

            if self.event.type == QUIT:
                pygame.quit()

            if self.event.type == MOUSEBUTTONDOWN:
                column = int(math.floor(self.piece_position_x/SQUARE_SIZE))
                return column

            pygame.display.update()


# ---------------------------------------------------------------------------------------
class Game():

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect 4")

        self.player_piece = 1
        self.piece_color = red

        self.players = Players()
        self.board = Board()

    def text_objects(self, text, pst1, pst2, size):
    
        my_font = pygame.font.SysFont('comicsansms', size)
        my_sentence = my_font.render(text, True, (0, 0, 0))
        
        position = my_sentence.get_rect()
        position.center = ((pst1/2),(pst2/2))
        
        return my_sentence, position

    def ending(self, piece_color, player_piece, screen):
        screen.fill(white)

        sentence = 'Player ' + str(player_piece) + ' Wins!'

        my_sentence, position = self.text_objects(sentence, 700, 700, 75)
        screen.blit(my_sentence, position)
        pygame.display.update()
        
        time.sleep(3)

        screen.fill(white)

        sentence = 'Press ESC to Exit or Space to Play Again'
        
        my_sentence, position = self.text_objects(sentence, 700, 700, 30)
        screen.blit(my_sentence, position)
        pygame.display.update()

        while True:
            event = self.get_event()

            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()

                elif event.key == K_SPACE:
                    self.__init__()
                    self.player_piece = player_piece
                    self.piece_color = piece_color
                    self.main()        

    def win_condition(self, piece, screen):
        
        # load win lines
        line_h = pygame.image.load('lig4_h.png')
        line_v = pygame.image.load('lig4_v.png')
        line_d1 = pygame.image.load('lig4_d1.png')
        line_d2 = pygame.image.load('lig4_d2.png')
        
        # Horizontal checking
        for r in range(ROWS):
            for c in range(COLUMNS-3):
                if self.board.game_spaces[r][c] == piece and self.board.game_spaces[r][c+1] == piece and self.board.game_spaces[r][c+2] == piece and self.board.game_spaces[r][c+3] == piece:
                    screen.blit(line_h, (c*SQUARE_SIZE + 7.5, r*SQUARE_SIZE + SQUARE_SIZE + 7.5))
                    return True

        # Vertical checking
        for c in range(COLUMNS):
            for r in range(ROWS-3):
                if self.board.game_spaces[r][c] == piece and self.board.game_spaces[r+1][c] == piece and self.board.game_spaces[r+2][c] == piece and self.board.game_spaces[r+3][c] == piece:
                    screen.blit(line_v, (c*SQUARE_SIZE + 7.5, r*SQUARE_SIZE + SQUARE_SIZE + 7.5))
                    return True

        # / Diagonal cheking
        for c in range(COLUMNS-3):
            for r in range(ROWS-3):
                if self.board.game_spaces[r][c] == piece and self.board.game_spaces[r+1][c+1] == piece and self.board.game_spaces[r+2][c+2] == piece and self.board.game_spaces[r+3][c+3] == piece:
                    screen.blit(line_d2, (c*SQUARE_SIZE + 7.5, r*SQUARE_SIZE + SQUARE_SIZE + 7.5))
                    return True

        # \ Diagonal checking
        for c in range(3, COLUMNS):
            for r in range(ROWS-3):
                if self.board.game_spaces[r][c] == piece and self.board.game_spaces[r+1][c-1] == piece and self.board.game_spaces[r+2][c-2] == piece and self.board.game_spaces[r+3][c-3] == piece:
                    screen.blit(line_d1, (c*SQUARE_SIZE - 3*SQUARE_SIZE, r*SQUARE_SIZE + SQUARE_SIZE + 7.5))
                    return True

    def get_event(self):

        while True:
            for event in pygame.event.get():
                return event

    # main function, game
    def main(self):
        # draw board
        self.board.draw(self.screen)

        while True:

            # get selected column
            column = self.players.droping_piece(self.screen, self.piece_color)

            if game.board.is_column_available(column):
                row = game.board.get_next_open_row(column)
                self.board.game_spaces[row][column] = self.player_piece

                self.board.draw(self.screen)

                if self.win_condition(self.player_piece, self.screen):
                    pygame.display.update()
                    time.sleep(3)
                    self.ending(self.piece_color, self.player_piece, self.screen)

                # change turns
                if self.player_piece == 1:
                    self.player_piece = 2
                    self.piece_color = black
                else:
                    self.player_piece = 1
                    self.piece_color = red


game = Game()
game.main()
