import pygame, os, sys, random, time
from pygame.locals import *

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

HEIGHT = 500
WIDTH = 800

BLOCK_HEIGHT = 20
BLOCK_WIDTH = 20

SPACE_SIZE = 75

RECTANGLES_HEIGHT= 100

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodge Game')

clock = pygame.time.Clock()

def rectangles():
	RECTANGLE_1_WIDTH = random.randint(0, WIDTH - SPACE_SIZE)
	RECTANGLE_2_WIDTH = WIDTH - RECTANGLE_1_WIDTH - SPACE_SIZE

	return RECTANGLE_1_WIDTH, RECTANGLE_2_WIDTH

def text_objects(sentence, size):
	font = pygame.font.SysFont('comicsansms', size)
	sentence = font.render(sentence, True, black)

	return sentence

def checking(score, sentence):

	screen.blit(sentence, (10, 10))

	file = open('top_score.txt', 'r+')
	for line in file.readlines():
		top_score = line

	if score > int(top_score):
		top_score = str(score)
		file.truncate()
		file.seek(0)
		file.write(str(score))
		file.close()	

	sentence = text_objects("Top Score: " + top_score, 25)
	screen.blit(sentence, (600, 70))
	pygame.display.update()
	
	time.sleep(1)

	while True:
		for event in pygame.event.get():

			if event.type == QUIT: pygame.quit()

			if event.type == KEYDOWN:

				if event.key == K_ESCAPE: pygame.quit()
				else: main()


def main():

	y_motion = 4

	collision = False

	score = 0

	block_x_pos = WIDTH / 2 - BLOCK_WIDTH / 2
	block_y_pos = HEIGHT - 50
	block_x_pos_motion = 0
	rectangles_y_pos = -99

	RECTANGLE_1_WIDTH, RECTANGLE_2_WIDTH = rectangles()

	FPS = 60

	game_over = False

	while not game_over:

		screen.fill(white)

		for event in pygame.event.get():

			if event.type == QUIT: pygame.quit()

			if event.type == KEYDOWN:

				if event.key == K_LEFT:
					block_x_pos_motion -=  y_motion + 5

				if event.key == K_RIGHT:
					block_x_pos_motion += y_motion + 5	

			if event.type == KEYUP:
				block_x_pos_motion = 0

		clock.tick(FPS)

		block_x_pos += block_x_pos_motion

		block = pygame.draw.rect(screen, black, (block_x_pos, block_y_pos, BLOCK_WIDTH, BLOCK_HEIGHT))
		
		rectangle1 = pygame.draw.rect(screen, red, (0, rectangles_y_pos, RECTANGLE_1_WIDTH, RECTANGLES_HEIGHT))
		rectangle2 = pygame.draw.rect(screen, red, (RECTANGLE_1_WIDTH + SPACE_SIZE, rectangles_y_pos, RECTANGLE_2_WIDTH, RECTANGLES_HEIGHT))

		rectangles_y_pos += y_motion

		sentence = text_objects('Score: ' + str(score), 50)
		if score < 10: screen.blit(sentence, (597.5, 10))
		else: screen.blit(sentence, (575, 10))
		
		pygame.display.update()		

		if rectangles_y_pos > 600:

			rectangles_y_pos = -99
			RECTANGLE_1_WIDTH, RECTANGLE_2_WIDTH = rectangles()
			if y_motion < 15: y_motion += 1
			score += 1

		if block.colliderect(rectangle1) or block.colliderect(rectangle2):
			sentence = text_objects('Oops, You Died!', 50)
			collision = True

		if block_x_pos < 0 or block_x_pos > WIDTH:
			sentence = text_objects('You Hit the Border!', 50)
			collision = True
				
		if collision: checking(score, sentence)

main()