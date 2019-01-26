import numpy, pygame, os, time, math
from pygame.locals import *

clear = lambda: os.system('cls')

grey = (105, 105, 105)
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)

SQUARESIZE = 100
LAST_ROW = 0
ROWS = 6
COLUMNS = 7
RADIUS = int(SQUARESIZE / 2 - 7.5)


WIDTH = COLUMNS*SQUARESIZE
HEIGHT = (ROWS +  1)*SQUARESIZE


def text_objects(text, pst1, pst2, size):
	
	my_font = pygame.font.Font('freesansbold.ttf', size)
	my_sentence = my_font.render(text, True, (0, 0, 0))
	
	position = my_sentence.get_rect()
	position.center = ((pst1/2),(pst2/2))
	
	return my_sentence, position


def ending(sentence):
	time.sleep(5)
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
					else: main()


def winning_move(board, piece):

	#Horizontal checking
	for r in range(ROWS):
		for c in range(COLUMNS-3):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	#Vertical checking
	for c in range(COLUMNS):		
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	#Diagonal cheking 1
	for c in range(COLUMNS-3):		
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	#Diagonal checking 2
	for c in range(3, COLUMNS):		
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c-1] == piece and board[r+2][c-2] == piece and board[r+3][c-3] == piece:
				return True


def drop_piece(board, col, row, piece):
	board[row][col] = piece


def get_next_open_row(board, col):
	for r in range(ROWS-1, LAST_ROW-1, -1):
		if board[r][col] == 0:
			return r


def is_valid_location(board, col):
	return board[LAST_ROW][col] == 0

def creating_board():
	board = numpy.zeros((ROWS, COLUMNS))
	return board


def drawing_board(board):
	screen.fill(white)
	pygame.draw.rect(screen, grey, (0, SQUARESIZE, COLUMNS*SQUARESIZE, ROWS*SQUARESIZE))
	
	for r in range(ROWS):
		for c in range(COLUMNS):

			if board[r][c] == 0: pygame.draw.circle(screen, white, (int(c*SQUARESIZE + SQUARESIZE / 2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
			elif board[r][c] == 1: pygame.draw.circle(screen, red, (int(c*SQUARESIZE + SQUARESIZE / 2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
			else: pygame.draw.circle(screen, black, (int(c*SQUARESIZE + SQUARESIZE / 2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

	pygame.display.update()


def main():
	board = creating_board()
	drawing_board(board)
	turn = 0
	game_over = False

	while not game_over:
		
		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()
			posx = pos[0]
			
			pygame.draw.rect(screen, white, (0, 0, WIDTH, SQUARESIZE))

			if turn % 2 == 0:
					piece = 1
					pygame.draw.circle(screen, red, (posx, int(SQUARESIZE / 2)), RADIUS)
		
			else:
				piece = 2
				pygame.draw.circle(screen, black, (posx, int(SQUARESIZE / 2)), RADIUS)

			pygame.display.update()


			if event.type == MOUSEBUTTONDOWN:

				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					turn+=1
					row = get_next_open_row(board, col)
					drop_piece(board, col, row, piece)		

				clear()
				drawing_board(board)

				pygame.display.update()

				if winning_move(board, piece):
					sentence = "Player " + str(piece) + " Wins!"
					ending(sentence)
					
				if turn == ROWS * COLUMNS:
					sentence = "Tie!"
					ending(sentence)	

			if event.type == QUIT: pygame.quit()		


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
main()
