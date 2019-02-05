import pygame, random, time, os
from pygame.locals import *

def text_objects(text, pst1, pst2, size):
		
	my_font = pygame.font.Font('freesansbold.ttf', size)
	my_sentence = my_font.render(text, True, (255, 255, 255))
	
	position = my_sentence.get_rect()
	position.center = ((pst1/2),(pst2/2))
	
	return my_sentence, position

def game(screen, clock):
	
	def tens():
		x = random.randint(0,590)
		y = random.randint(0,590)
		
		return (x//10 * 10, y//10 * 10)
		
		
	def collision(c1,c2):
		return (c1[0] == c2[0]) and (c1[1] == c2[1])
		

	def self_collision(snake):
		head = snake[0]
		if snake.count(head) > 1:
			return True	
		
		if (head[0] < 0) or (head[0] > 590):
			return True
			
		if (head[1] < 0) or (head[1] > 590):
			return True

	
	screen.fill((0, 0, 0))
	pygame.display.update()		
			
	UP = 0
	RIGHT = 1
	DOWN = 2
	LEFT = 3

	snake_skin = pygame.Surface((10, 10))
	snake_skin.fill((0, 140, 0))

	snake_head = pygame.Surface((10, 10))
	snake_head.fill((255, 255, 255))

	apple_pos = tens()
	apple = pygame.Surface((10, 10))
	apple.fill((255, 0, 0))

	snake = [(200,200), (210, 200), (220, 200)]
	my_direction = LEFT

	for x in range(3, 0, -1):
		my_countdown, position = text_objects(str(x), 600, 600, 115)
		screen.blit(my_countdown, position)
		pygame.display.update()
		time.sleep(1)
		screen.fill((0, 0, 0))
		pygame.display.update()

	while True:
		
		clock.tick(20)
		
		for event in pygame.event.get():
			
			if event.type == QUIT:
				pygame.quit()
			
			if event.type == KEYDOWN:
				if event.key == K_UP:
					my_direction = UP
				if event.key == K_DOWN:
					my_direction = DOWN
				if event.key == K_RIGHT:
					my_direction = RIGHT
				if event.key == K_LEFT:
					my_direction = LEFT
		
		if collision(snake[0], apple_pos):
			apple_pos = tens()
			snake.append((0, 0))
		
		for i in range(len(snake) - 1, 0, -1):
			snake[i] = (snake[i-1][0], snake[i-1][1])
		
		if my_direction == UP:
			snake[0] = (snake[0][0], snake[0][1] - 10)
			
		if my_direction == DOWN:
			snake[0] = (snake[0][0], snake[0][1] + 10)
			
		if my_direction == RIGHT:
			snake[0] = (snake[0][0] + 10, snake[0][1])
			
		if my_direction == LEFT:
			snake[0] = (snake[0][0] - 10, snake[0][1])
		
		screen.fill((0, 0, 0))
		screen.blit(apple, apple_pos)
			
		for pos in snake:
			if pos == snake[0]:
				screen.blit(snake_head, pos)
			
			else: screen.blit(snake_skin, pos)
				
		pygame.display.update()	
		
		if self_collision(snake):
			time.sleep(2)
			ending(screen, clock)

def ending(screen, clock):

	seta = pygame.image.load('seta.png')
	screen.fill((0, 0, 0))		
	end_text = 'You Lose'

	my_sentence, position = text_objects(end_text, 600, 600, 115)
	screen.blit(my_sentence, position)

	pygame.display.update()	

	time.sleep(3)

	screen.fill((0, 0, 0))
	pygame.display.update()

	pos1 = ((100, 400))
	pos2 = ((75, 200))
	places = pos2

	while True:
		
		my_sentence, position = text_objects('Retry', 600, 400, 115)
		screen.blit(my_sentence, position)

		my_sentence, position = text_objects('Exit', 600, 800, 115)
		screen.blit(my_sentence, position)

		position = seta.get_rect()
		position.center = (places)
		screen.blit(seta, position)

		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				
			if event.type == KEYDOWN:
				if event.key == K_UP or event.key == K_DOWN:
					if places == pos2: places = pos1
					else: places = pos2
					screen.fill((0, 0, 0))
					break
					
				if event.key == K_RETURN:
					if places == pos1: pygame.quit()
					else: game(screen, clock)

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()					

my_sentence, position = text_objects('Snake Game', 600, 600, 75)
screen.blit(my_sentence, position)

pygame.display.update()
time.sleep(3)

game(screen, clock)