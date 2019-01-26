import pygame, os, time
from pygame.locals import *


def dicio_line(coord, case):
	if case == 1:
		coord_dicio = {"00" : (70, 60), "10" : (70, 280), "20" : (70, 500)}
		return coord_dicio[coord]
	if case == 2:
		coord_dicio2 = {"00" : (75, 70), "01" : (300, 70), "02" : (520, 70)}
		return coord_dicio2[coord]
	
	
def dicio(coord):
	coord_dicio = {"[0][0]" : (30, 50), "[0][1]" : (250, 50), "[0][2]" : (470, 50), "[1][0]" : (30, 270), "[1][1]" : (250, 270), "[1][2]" : (470, 270), "[2][0]" : (30, 490), "[2][1]" : (250, 490), "[2][2]" : (470, 490)}
	return coord_dicio[coord]
	

def text_objects(text, pst1, pst2, size):
	
	my_font = pygame.font.Font('freesansbold.ttf', size)
	my_sentence = my_font.render(text, True, (0, 0, 0))
	
	position = my_sentence.get_rect()
	position.center = ((pst1/2),(pst2/2))
	
	return my_sentence, position	
	
	
def ending(screen, sentence):
	time.sleep(4)
	screen.fill(white)
	
	my_sentence, position = text_objects(sentence, 700, 700, 75)
	screen.blit(my_sentence, position)
	pygame.display.update()
	
	time.sleep(3)
	screen.fill(white)	
	
	seta_preta = pygame.image.load('seta_preta.png')
	pos1 = ((200, 450))
	pos2 = ((75, 250))
	places = pos2
	
	
	while True:
		
		my_sentence, position = text_objects('Play Again', 700, 500, 75)
		screen.blit(my_sentence, position)

		my_sentence, position = text_objects('Exit', 700, 900, 75)
		screen.blit(my_sentence, position)

		position = seta_preta.get_rect()
		position.center = (places)
		screen.blit(seta_preta, position)

		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				
			if event.type == KEYDOWN:
				if event.key == K_UP or event.key == K_DOWN:
					if places == pos2: places = pos1
					else: places = pos2
					screen.fill((255, 255, 255))
					break
					
				if event.key == K_RETURN:
					if places == pos1: pygame.quit()
					else: game()
					
def veryfing_player(squares, y, x):
	if y == 3: sentence = "Tie!"
	elif squares[y][x] == 1: sentence = "Player 1 Wins"
	elif squares[y][x] == 2: sentence = "Player 2 Wins"
	
	ending(screen, sentence)
	
	
def veryfing(squares):
	
	line = pygame.image.load('linha.png')
	line_v = pygame.image.load('linha_v.png')
	line_d1 = pygame.image.load('linha_d1.png')
	line_d2 = pygame.image.load('linha_d2.png')
	screen.fill(white)
	printing_squares(squares)
	
	
	for y in range(0, 3):
		if all([n == 1 for n in squares[y]]) or all([n == 2 for n in squares[y]]):
			screen.blit(line, dicio_line(str(y) + "0", 1))
			pygame.display.update()
			veryfing_player(squares, y, 0)
			
	for y in range(0, 3):
		if squares[0][y] == squares[1][y] and squares[1][y] == squares[2][y] and squares[0][y] != 0:
			screen.blit(line_v, dicio_line("0" + str(y), 2))
			pygame.display.update()
			veryfing_player(squares, 0, y)
			
	if squares[0][0] == squares[1][1] and squares[1][1] == squares[2][2] and squares[0][0] != 0:
		screen.blit(line_d1, (40, 40))
		pygame.display.update()
		veryfing_player(squares, 1, 1)
		
	if squares[2][0] == squares[1][1] and squares[1][1] == squares[0][2] and squares[1][1] != 0:
		screen.blit(line_d2, (40, 30))
		pygame.display.update()
		veryfing_player(squares, 1, 1)
		
	if all([n != 0 for n in squares[0]]) and all([n != 0 for n in squares[1]]) and all([n != 0 for n in squares[2]]):
		veryfing_player(squares, 3, 0)			
			
	
def printing_squares(squares):
	screen.blit(vertical, (230, 30))
	screen.blit(vertical, (450, 30))
	screen.blit(horizontal, (30, 230))
	screen.blit(horizontal, (30, 450))
		
	for y in range(0, 3):
			
		for x in range(0, 3):
		
			local = str([y]) + str([x])
	
			if squares[y][x] == 1:
				screen.blit(xis, dicio(local))
			elif squares[y][x] == 2:
				screen.blit(bola, dicio(local))		

	pygame.display.update()
	return 0 	


def printing(obj, coord, squares):
	screen.fill(white)
	printing_squares(squares)
	
	screen.blit(obj, coord)
	pygame.display.update()
	return 0
	
def game():
	
	global x, y
	x, y = 1, 1
	
	squares = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
	]
	
	obj = xis_azul
	
	coord = dicio("[1][1]")
	printing(obj, coord, squares)
	
	while True:
		
		pygame.display.update()
		
		for event in pygame.event.get():
			
			if event.type == QUIT:
				pygame.quit()
				
			if event.type == KEYDOWN:
			
				if event.key == K_UP:
					if x > 0:
						x-=1
					
				if event.key == K_DOWN:
					if x < 2: 
						x+=1
				
				if event.key == K_RIGHT:
					if y < 2: 
						y+=1
					
				if event.key == K_LEFT:
					if y > 0: 
						y-=1
				
				if event.key == K_RETURN:
					if squares[x][y] == 0:
										
						if obj == xis_azul:
							squares[x][y] = 1
							obj = bola_azul
						
						else:
							squares[x][y] = 2
							obj = xis_azul
						
						veryfing(squares)
						
				screen.fill(white)
				coord = str([x]) + str([y])
				coord = dicio(coord)
				printing(obj, coord, squares)
								
				break

global screen				
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()

global blue, white, black

blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

screen.fill(white)

global bola, bola_azul, xis, xis_azul

bola = pygame.image.load('bola.png')
xis = pygame.image.load('xis.png')

bola_azul = pygame.image.load('bola_azul.png')
xis_azul = pygame.image.load('xis_azul.png')

global vertical, horizontal

vertical = pygame.Surface((20, 640))
vertical.fill(black)
horizontal = pygame.Surface((640, 20))
horizontal.fill(black)

game()