import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

width = 800
height = 800

cols = 40
rows = 30

class cube():
	rows = 30
	w = 800
	def __init__(self, start, dirx=1,diry=0, color = (255,0,0)):
		self.pos = start
		self.dirx = dirx
		self.diry = diry
		self.color = color
		
	def move(self,dirx,diry):
		self.dirx = dirx
		self.diry = diry
		self.pos = (self.pos[0] + self.dirx,self.pos[1] + self.diry)
		
	def draw(self, surface):
		distance = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]
		
		pygame.draw.rect(surface, self.color, (i*distance+1,j*distance+1, distance -4,distance -4))
		
class snake():
	body = []
	turns = {}
	
	def __init__(self,color,pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head)
		self.dirx = 0
		self.diry = 1
		
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			
			else:
				keys = pygame.key.get_pressed()
				for key in keys:
					if keys[pygame.K_LEFT]:
						self.dirx = -1
						self.diry = 0
						self.turns[self.head.pos[:]] = [self.dirx,self.diry]
					elif keys[pygame.K_RIGHT]:
						self.dirx = 1
						self.diry = 0
						self.turns[self.head.pos[:]] = [self.dirx,self.diry]
					elif keys[pygame.K_UP]:
						self.dirx = 0
						self.diry = -1
						self.turns[self.head.pos[:]] = [self.dirx,self.diry	]
					elif keys[pygame.K_DOWN]:
						self.diry = 1
						self.dirx = 0
						self.turns[self.head.pos[:]] = [self.dirx,self.diry]
						
		for i,c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				c.move(c.dirx,c.diry)
				
	def reset(self,pos):
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirx= 0
		self.diry = 1
		
	def addCube(self):
		tail = self.body[-1]
		dx ,dy = tail.dirx , tail.diry
		
		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		if dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		if dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		if dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
		
		self.body[-1].dirx= dx
		self.body[-1].diry= dy
		
	def draw(self, surface):
		for i,c in enumerate(self.body):
			if i == 0:
				c.draw(surface)
			else:
				c.draw(surface)
				
def redrawWindow():
	global win
	win.fill((0,0,0))
	drawGrid(width, rows,win)
	s.draw(win)
	snack.draw(win)
	pygame.display.update()
	pass

def drawGrid(w,rows, surface):
	size = w // rows
	
	x = 0
	y = 0
	for l in range(rows):
		x = x + size
		y = y + size
		
		pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
		pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
				
def randomSnack(rows, item):
	positions = item.body
	
	while True:
		x = random.randrange(1,rows-1)
		y = random.randrange(1,rows-1)
		if len(list(filter(lambda z:z.pos == (x,y),positions)))>0:
			continue
		else:
			break
			
	return(x,y)
	
def main():
	global s, snack,win
	win = pygame.display.set_mode((width,height))
	s = snake((255,0,0), (15,15))
	s.addCube()
	snack = cube(randomSnack(rows,s), color = (0,255,0))
	flag = True
	clock = pygame.time.Clock()
	
	while flag:
		pygame.time.delay(100)
		clock.tick(10)
		s.move()
		headPos = s.head.pos
		if headPos[0] >= 30 or headPos[0] < 0 or headPos[1] >= 30 or headPos[1] < 0:
			print("Score:", len(s.body))
			s.reset((15, 15))
        
		if s.body[0].pos == snack.pos:
			s.addCube()
			snack = cube(randomSnack(rows,s), color=(0,255,0))
            
		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
				print("Score:", len(s.body))
				s.reset((15,15))
				break
                
		redrawWindow()
        
main()
