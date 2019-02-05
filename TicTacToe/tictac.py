import pygame, numpy, os, time
from pygame.locals import *

xis = pygame.image.load('xis.png')
xis_azul = pygame.image.load('xis_azul.png')
bola = pygame.image.load('bola.png')
bola_azul = pygame.image.load('bola_azul.png')

line_h = pygame.image.load('linha.png')
line_v = pygame.image.load('linha_v.png')
line_d1 = pygame.image.load('linha_d1.png')
line_d2 = pygame.image.load('linha_d2.png')

black = (0, 0, 0)
white = (255, 255, 255)

vertical = pygame.Surface((20, 700))
vertical.fill(black)
horizontal = pygame.Surface((700, 20))
horizontal.fill(black)

SQUARESIZE = 220
LINESIZE = 20

ROWS = 3
COLUMNS = 3


def text_objects(text, pst1, pst2, size):
	
	my_font = pygame.font.Font('freesansbold.ttf', size)
	my_sentence = my_font.render(text, True, (0, 0, 0))
	
	position = centered(my_sentence, pst1, pst2)
	
	return my_sentence, position	
	

def ending(winner):
	pygame.display.update()
	time.sleep(3)

	screen.fill(white)

	if winner == 'Tie!': sentence = winner
	else: sentence = "Player " + str(int(winner)) + " Wins!"

	sentence, position = text_objects(sentence, 360, 360, 75)
	screen.blit(sentence, position)
	
	pygame.display.update()
	time.sleep(3)

	screen.fill(white)	
	
	seta_preta = pygame.image.load('seta_preta.png')
	pos1 = ((200, 450))
	pos2 = ((75, 250))
	places = pos2
	
	
	while True:
		
		my_sentence, position = text_objects('Play Again', 360, 250, 75)
		screen.blit(my_sentence, position)

		my_sentence, position = text_objects('Exit', 360, 450, 75)
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
					else: main()

def win_condition(board):
	
	for r in range(ROWS):
		if all([n == 1 for n in board[r]]) or all([n == 2 for n in board[r]]):
			screen.blit(line_h, (SQUARESIZE  - 120, r*SQUARESIZE + SQUARESIZE - 140 + r*20))
			ending(board[r][0])
	
	for c in range(COLUMNS):
		if board[0][c] != 0:
			if board[0][c] == board[1][c] == board[2][c]:
				screen.blit(line_v, (c*SQUARESIZE + SQUARESIZE - 140 + c*20,SQUARESIZE - 140))
				ending(board[0][c])

	if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
		screen.blit(line_d1, (SQUARESIZE - 150, SQUARESIZE - 150))
		ending(board[1][1])
		
	if board[2][0] == board[1][1] == board[0][2] and board[1][1] != 0:
		screen.blit(line_d2, (40, 30))
		ending(board[1][1])

	if all([n != 0 for n in board[0]]) and all([n != 0 for n in board[1]]) and all([n != 0 for n in board[2]]):
		ending('Tie!')
	

def centered(image, pst1, pst2):
	position = image.get_rect()
	position.center = (pst1, pst2)
	
	return position


def printing_board(board):
	screen.fill(white)

	screen.blit(vertical, (230, 10))
	screen.blit(vertical, (470, 10))
	screen.blit(horizontal, (10, 230))
	screen.blit(horizontal, (10, 470))

	for r in range(ROWS):
		for c in range(COLUMNS):
			if board[r][c] == 1:
				position = centered(xis, (c*SQUARESIZE + SQUARESIZE / 2 + c*20 + 10), (r*SQUARESIZE + SQUARESIZE / 2 + r*20 +10))
				screen.blit(xis, position)

			if board[r][c] == 2:
				position = centered(bola, (c*SQUARESIZE + SQUARESIZE / 2 + c*20 + 10), (r*SQUARESIZE + SQUARESIZE / 2 + r*20 +10))
				screen.blit(bola, position)

	if win_condition(board): ending()

	pygame.display.update()

def printing(board, row_pos, col_pos, obj):

	printing_board(board)

	position = centered(obj, (col_pos*SQUARESIZE + SQUARESIZE / 2 + col_pos*20 + 10), (row_pos*SQUARESIZE + SQUARESIZE / 2 + row_pos*20 +10))
	screen.blit(obj, position)	

	pygame.display.update()

def main():

	row_pos = 1
	col_pos = 1

	obj = xis_azul
	turn = 1

	board = numpy.zeros((ROWS, COLUMNS))
	printing(board, row_pos, col_pos, obj)

	while True:

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
			
				if event.key == K_UP:
					if row_pos > 0:
						row_pos-=1
					
				if event.key == K_DOWN:
					if row_pos < 2: 
						row_pos+=1
				
				if event.key == K_RIGHT:
					if col_pos < 2: 
						col_pos+=1
					
				if event.key == K_LEFT:
					if col_pos > 0: 
						col_pos-=1	

				if event.key == K_RETURN:
					if board[row_pos][col_pos] == 0:
						board[row_pos][col_pos] = turn
						
						if turn == 1: 
							obj = bola_azul
							turn = 2
						
						else:
							obj = xis_azul
							turn = 1

				printing(board, row_pos, col_pos, obj)		

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption('Tic Tac Toe')

main()