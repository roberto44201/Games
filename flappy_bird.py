import pygame
from pygame.locals import *
import sys
import random
import time
import winsound

from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))
from Games.Game_Module import Game

FPS = 60
WIDTH = 800
HEIGHT = 500

TIMER = pygame.USEREVENT

light_green = (225, 255, 205)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 80)
blue = (140, 230, 255)
green = (100, 200, 0)
obstacle_color = (160, 160, 160)
obstacle_edge = (0, 0, 0)

clock = pygame.time.Clock()

SPACE = 0
MOUSE_QUIT = 1
UP = 2
DOWN = 3
ENTER = 4

class Scenario():
	def __init__(self):
		self.tree_1 = pygame.image.load('tree_1.png')					#tree type 1
		self.tree_1 = pygame.transform.scale(self.tree_1, (90, 90))

		self.tree_2 = pygame.image.load('tree_2.png')					#tree type 2
		self.tree_2 = pygame.transform.scale(self.tree_2, (90, 67))

		self.cloud = pygame.image.load('cloud.png')
		self.cloud = pygame.transform.scale(self.cloud, (120, 80))

		self.menu_background = pygame.image.load('background.png')

		self.tree_y_position = 340
		self.tree_x_motion = -1
		self.cloud_x_motion = -0.5
		
		self.trees = (self.tree_1, self.tree_2)					#creates a tuple with both trees
		self.trees_list = []									#creates a list of trees which will be printed
		self.clouds_list = []									#creates a list of clouds which will be printed

		for x in range (1, 6):									#adds 5 new trees in the beggining of the game
			self.trees_list.append((self.trees[x % 2], [150 * x, self.tree_y_position]))	#1st element: tree type 	2nd element: tree position
		self.distance_from_next_tree = random.randint(WIDTH - 150, WIDTH)	#set a random distance from the next tree

		for x in range(1, 4):
			self.clouds_list.append((self.cloud, [250 * x, 150])) #adds 3 new clouds in the beggining of the game
		self.distance_from_next_cloud = random.randint(WIDTH - 350, WIDTH - 100)

	def print_menu(self, screen):
		screen.blit(self.menu_background, (0,0))				#print the menu background

	def add_cloud(self):										#adds a new cloud to the list, with a random y position 
		self.cloud_y_pos = random.randint(50, 200)
		self.clouds_list.append((self.cloud, [WIDTH + 120, self.cloud_y_pos]))
		self.distance_from_next_cloud = random.randint(WIDTH - 350, WIDTH - 100)	#sets a distance from the next cloud to be printed

	def add_tree(self):											#adds a new  tree to the list, which can be type 1 or 2
		tree = random.randint(0, 1)
		self.trees_list.append((self.trees[tree], [WIDTH + 90, self.tree_y_position]))
		self.distance_from_next_tree = random.randint(WIDTH - 150, WIDTH)			#sets a distance from the next tree to be printed

	def draw(self, screen):
		
		pygame.draw.rect(screen, green, (0, 400, WIDTH, 100))	#prints the grass

		for tree in self.trees_list:							#prints every tree on the list
			screen.blit(tree[0], tree[1])
			tree[1][0] += self.tree_x_motion					#change x position of every tree

			if tree[1][0] <= -90:								#if the tree has disappeared completely from the screen,
				self.trees_list.remove(tree)					#removes tree from the list

		for cloud in self.clouds_list:							#prints every cloud in the list
			screen.blit(cloud[0], cloud[1])
			cloud[1][0] += self.cloud_x_motion

			if tree[1][0] <= -120:
				self.clouds_list.remove(cloud)

		if self.clouds_list[-1][1][0] <= self.distance_from_next_cloud:	#adds a new cloud
			self.add_cloud()
		
		if self.trees_list[-1][1][0] <= self.distance_from_next_tree:	#adds a new tree
			self.add_tree()


class Bird():
	def __init__(self):
		self.bird = pygame.Surface((20, 20))
		self.bird.fill(yellow)
		self.bird_position = [170, 250]
		self.y_motion = 0

	def return_rect(self):						#returns bird rect data, but with updated positions
		bird_rect = self.bird.get_rect()
		bird_rect[0] = self.bird_position[0]
		bird_rect[1] = self.bird_position[1]
		return bird_rect

	def draw(self, screen):						#prints the bird
		screen.blit(self.bird, self.bird_position)

	def set_motion(self):						#bird motion = -5.5 when space bar is pressed 
		self.y_motion = -5.5

	def move_bird(self):						#updates the bird position, based on the bird motion
		if self.bird_position[1] + self.y_motion >= 0:	#if the bird has not reached the top yet
			self.bird_position[1] += self.y_motion

		else:											#if the bird has reached the top, it starts to fall imediatelly
			self.y_motion = -0.2
			
		self.y_motion += 0.2					#increases bird motion in 0.2

	def check_floor_collision(self):			#check if bird has not hit the floor
		if self.bird_position[1] > HEIGHT - 10:
			return True


class Obstacles():
	def __init__(self):
		self.obstacles_width = 100
		self.gap_size = 120
		self.x_motion = 3
		self.obstacles_surfaces = []
		self.obstacles_positions = []

	def return_rect(self):
		return self.rects

	def set_rects(self):		#sets a new obstacle
		self.gap_y_pos = random.randint(0, HEIGHT - self.gap_size)		#defines the gap position

		self.rect_1 = pygame.Surface((self.obstacles_width, self.gap_y_pos))	#creates rectangle 1 and 2
		self.rect_1.fill(obstacle_color)
		self.rect_2 = pygame.Surface((self.obstacles_width, HEIGHT - self.gap_y_pos - self.gap_size))
		self.rect_2.fill(obstacle_color)

		self.obstacles_surfaces.append((self.rect_1, self.rect_2))  #add rectangles to the list of obstacles surfaces

		self.rect_1_pos = [WIDTH, 0]								#sets rectangles initial positions
		self.rect_2_pos = [WIDTH, self.gap_y_pos + self.gap_size]
		self.obstacles_positions.append([self.rect_1_pos, self.rect_2_pos]) #adds positions the the list of obstacles positions

	def draw(self, screen):
		self.rects = [] #defines a list of rects, which will be used to detect collsion

		for obstacle in self.obstacles_surfaces:	#print both reactangles 1 and 2
			screen.blit(obstacle[0], self.obstacles_positions[self.obstacles_surfaces.index(obstacle)][0])
			screen.blit(obstacle[1], self.obstacles_positions[self.obstacles_surfaces.index(obstacle)][1])
			
			#defines two rects with the exact some dimensions and positions of the rectangles 1 and 2
			#which will be used to draw the edges and to detect the collision with the bird
			rect = obstacle[0].get_rect()
			rect_pos = self.obstacles_positions[self.obstacles_surfaces.index(obstacle)][0]
			rect_1 = pygame.draw.rect(screen, obstacle_edge, (rect_pos[0], rect_pos[1] - 20, rect[2], rect[3] + 20), 8)

			rect = obstacle[1].get_rect()
			rect_pos = self.obstacles_positions[self.obstacles_surfaces.index(obstacle)][1]
			rect_2 = pygame.draw.rect(screen, obstacle_edge, (rect_pos[0], rect_pos[1], rect[2], rect[3] + 20), 8)

			#adds both rects to the rects list
			self.rects.append(rect_1)
			self.rects.append(rect_2)

			#updates obstacles positions
			self.obstacles_positions[self.obstacles_surfaces.index(obstacle)][0][0] -= self.x_motion
			self.obstacles_positions[self.obstacles_surfaces.index(obstacle)][1][0] -= self.x_motion

	def check_position(self):
		if self.obstacles_positions[-1][0][0] <= 470:	#adds a new obstacle
			self.set_rects()
		if self.obstacles_positions[0][0][0] <= -self.obstacles_width: #if the obstacle has dissapeared completely from the screen,
			self.obstacles_surfaces.pop(0)							   #removes them from the list
			self.obstacles_positions.pop(0)
			return True												   #returns True to increase the score


class Flappy_Bird(Game):
	def __init__(self):
		KEY_TO_EVENTS = {K_SPACE: SPACE, K_ESCAPE: MOUSE_QUIT, K_UP: UP,
						 K_DOWN: DOWN, K_KP_ENTER: ENTER, K_RETURN: ENTER}

		Game.__init__(self, 'Flappy Bird', WIDTH, HEIGHT, KEY_TO_EVENTS)

		self.my_bird = Bird()
		self.my_obstacles = Obstacles()
		self.my_scenario = Scenario()

		with open('flappy_record.txt', 'r') as file:
			self.record = int(file.read())
		file.close()

		self.score = 0

		#coordinates of the menu arrows
		self.polygon_positions = [(((270, 225), (270, 265), (300, 245)),
								 ((270, 315), (270, 355), (300, 335))),
								 (((260, 220), (260, 260), (290, 240)),
								 ((260, 315), (260, 355), (290, 335)))]
		#rect used to erase arrows
		self.aux_rect_position = [(260, 200, 50, 200), (250, 200, 50, 200)]

	def check_collision(self):		#checks collision using bird's and obstacles' rects data
		bird_rect = self.my_bird.return_rect()
		obstacles_rect = self.my_obstacles.return_rect()
		for obstacles in obstacles_rect:
			if bird_rect.colliderect(obstacles):
				return True			#returns True to end game

	def text(self, text, x_pos, y_pos, size, center, color):	#prints text
		font = pygame.font.SysFont('showcardgothic', size)
		text = font.render(text, True, color)

		if not center:
			position = (x_pos, y_pos)

		else:
			position = text.get_rect()
			position.center = ((x_pos / 2), (y_pos / 2))

		self.screen.blit(text, position)

	def menu(self):	#draws the menu, background and texts
		self.my_scenario.print_menu(self.screen)
		self.text('Flappy Bird', WIDTH - 5, HEIGHT - 105, 50, True, black)
		self.text('Flappy Bird', WIDTH, HEIGHT - 100, 50, True, yellow)
		self.text('Press Space to start', WIDTH - 3, HEIGHT - 3, 20, True, black)
		self.text('Press Space to start', WIDTH, HEIGHT, 20, True, yellow)
		pygame.display.update()

		while True:
			key = self.return_key()

			if key == SPACE:	#returns to main loop
				return

			elif key == MOUSE_QUIT:
				sys.exit()

	def frozen_screen(self, sentence):	#draws a rect at the center of the screen, used for pause and for the end of the game
		pygame.draw.rect(self.screen, black, (200, 50, 400, 400))
		pygame.draw.rect(self.screen, light_green, (210, 60, 380, 380))
		pygame.draw.line(self.screen, black, (230, 170), (575, 170), 6)

		self.text(sentence, WIDTH - 4, 270 - 4, 40, True, black)	#sentence can be "Game Paused" or "Oops, you died!", depending on the situation
		self.text('Exit', WIDTH - 4, 670 - 4, 50, True, black)
		self.text(sentence, WIDTH, 270, 40, True, yellow)			#prints twice to make a shadow
		self.text('Exit', WIDTH, 670, 50, True, yellow)

		if sentence == 'Oops, you died!':							#if end game, prints 'menu' and saves the score
			if self.score > self.record:
				with open("flappy_record.txt", 'w') as file:
					file.write(str(self.score))

			self.text("Menu", WIDTH - 4, 500 - 4, 50, True, black)
			self.text("Menu", WIDTH, 500, 50, True, yellow)
			self.case = 0
			
		else:														#if game paused, prints 'resume'
			self.text('Resume', WIDTH - 4, 500 - 4, 50, True, black)
			self.text('Resume', WIDTH, 500, 50, True, yellow)
			self.case = 1

		#the case variables are used to set the following arrows positions, since different texts require different positions

		aux = 0
		while True:
			pygame.draw.rect(self.screen, light_green, self.aux_rect_position[self.case])
			pygame.draw.polygon(self.screen, black, self.polygon_positions[self.case][aux % 2])
			pygame.display.update()
			while True:
				key = self.return_key()
				if key == UP or key == DOWN:	#if Up or Down pressed, alternates arrow position
					aux += 1
					break

				elif key == SPACE:				#if Space pressed, returns to game or exit, depending on the arrow position
					if aux % 2 == 0:
						return True
					else:
						sys.exit()
				elif key == MOUSE_QUIT:
					sys.exit()


	def return_key(self):						#returns events
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key in Game.KEY_TO_EVENTS:
					return Game.KEY_TO_EVENTS[event.key]
			elif event.type == QUIT:
				sys.exit()

	def get_action(self):
		key = self.return_key()

		if key == SPACE:					#if pressed Space bar, set bird motion
			self.my_bird.set_motion()

		elif key == MOUSE_QUIT:				#if pressed ESC, pause game
			self.frozen_screen('Game Paused')

		clock.tick(FPS)


	def main_loop(self): #main loop
		
		self.menu()

		self.my_obstacles.set_rects()

		while True:
			self.screen.fill(blue)
			self.my_scenario.draw(self.screen)
			self.my_obstacles.draw(self.screen)
			self.my_bird.draw(self.screen)
			self.text('Score: ' + str(self.score), 10, 10, 25, False, black)
			self.text('Top Score: ' + str(self.record), 10, 40, 15, False, black)
			self.get_action()
			self.my_bird.move_bird()
			pygame.display.update()
			if self.my_obstacles.check_position():
				self.score += 1
			if self.my_bird.check_floor_collision() or self.check_collision():
				done = False
				pygame.time.set_timer(USEREVENT, 1000)
				while not done:
					for event in pygame.event.get():
						if event.type == TIMER:
							done = True
				if self.frozen_screen("Oops, you died!"):
					break

while True:
	game = Flappy_Bird()
	game.main_loop()