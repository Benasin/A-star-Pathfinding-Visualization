import pygame ,math, time
from pygame.locals import *
pygame.init()

width = 700
height = 700

def createWindow(width, height):
	screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
	pygame.display.set_caption('A* Pathfinding Visualization')
	return screen

class Cell(object):
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.f = 0
		self.h = 0
		self.g = 0
		self.neighbors = []
		self.previous  = None
	def addNeighbors(self,grid, obstacle ,col ,row): #Check neighbor for every conditions
		if self.i < (col - 1):
			self.neighbors.append(grid[self.i + 1][self.j])
		if self.i > 0:
			self.neighbors.append(grid[self.i - 1][self.j])
		if self.j < (row - 1):
			self.neighbors.append(grid[self.i][self.j + 1])
		if self.j > 0:
			self.neighbors.append(grid[self.i][self.j - 1])

		if self.i > 0 and self.j > 0 and grid[self.i - 1][self.j] not in obstacle and grid[self.i][self.j - 1] not in obstacle:
			self.neighbors.append(grid[self.i - 1][self.j - 1])

		if self.i > 0 and self.j < (row - 1) and grid[self.i - 1][self.j] not in obstacle and grid[self.i][self.j + 1] not in obstacle:
			self.neighbors.append(grid[self.i - 1][self.j + 1])

		if self.i < (col - 1) and self.j > 0 and grid[self.i + 1][self.j] not in obstacle and grid[self.i][self.j - 1] not in obstacle:
			self.neighbors.append(grid[self.i + 1][self.j - 1])

		if self.i < (col - 1) and self.j < (row - 1) and grid[self.i + 1][self.j] not in obstacle and grid[self.i][self.j + 1] not in obstacle:
			self.neighbors.append(grid[self.i + 1][self.j + 1])

	def color(self , color, screen):
		pygame.draw.rect(screen, (color), (self.i * 20, self.j * 20, 20, 20))
		pygame.draw.rect(screen, (0,0,0), (self.i * 20, self.j * 20, 20, 20), 1)

#Calculate the heuristic
def heuristic(a,b):
	distance = abs(a.i - b.i) + abs(a.j - b.j)
	return distance

def main():
	global width
	global height
	screen = createWindow(width,height)
	col = width // 20 + 1
	row = height // 20 + 1
	grid = []
	print(grid)
	#Create a 2D Array
	for i in range(col):
		container = []
		for j in range(row):
			container.append(Cell(i,j))
		grid.append(container)
	#color everything
	for i in range(col):
		for j in range(row):
			grid[i][j].color((255,255,255),screen)
	openSet = []
	closedSet = []
	end = []
	start = []
	obstacle = []
	path = []
	dragging_draw = False
	dragging_erase = False
	loop = True

	while True:
		for event in pygame.event.get():
			if event.type == pygame.VIDEORESIZE:
				width , height = event.size
				main()

			if event.type == QUIT:
				pygame.quit()
			x, y = pygame.mouse.get_pos()
			x_index = round(abs(x) / 20 + 0.5) - 1
			y_index = round(abs(y) / 20 + 0.5) - 1
			if event.type == pygame.MOUSEBUTTONDOWN: 
				if event.button == 3: #Erase obstacle on right click
					if grid[x_index][y_index] in obstacle:
						obstacle.remove(grid[x_index][y_index])
						grid[x_index][y_index].color((255,255,255), screen)
						dragging_erase = True
				elif event.button == 1: #Add obstacle on left click
					if grid[x_index][y_index] not in obstacle:
						grid[x_index][y_index].color((0,0,0), screen)
						obstacle.append(grid[x_index][y_index])
						dragging_draw = True
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					dragging_draw = False
				if event.button == 3:
					dragging_erase = False
			elif event.type == pygame.MOUSEMOTION: #Add dragging effect
				if dragging_draw and grid[x_index][y_index] not in obstacle:
					grid[x_index][y_index].color((0,0,0), screen)
					obstacle.append(grid[x_index][y_index])
				elif dragging_erase and  grid[x_index][y_index] in obstacle:
					obstacle.remove(grid[x_index][y_index])
					grid[x_index][y_index].color((255,255,255),screen)

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s: #Place start when press s
					grid[x_index][y_index].color((0,0,255),screen)
					start.append(grid[x_index][y_index])
					openSet.append(grid[x_index][y_index])
				elif event.key == pygame.K_e: #Place end when press e
					grid[x_index][y_index].color((255,0,0), screen)
					end.append(grid[x_index][y_index])
				elif event.key == pygame.K_r: #Reset when press r
					main()

		winner = 0 
		if len(openSet) > 0 and len(end) > 0 and len(start) > 0 and loop: # if openSet, end, start is not empty then start the loop
			for i in range(len(openSet)):
				if openSet[i].f < openSet[winner].f: # Find the cell with the smallest f cost
					winner = i
			current = openSet[winner] # the current cell will now be the cell with the smallest f cost
			openSet.remove(current) # remove current cell from openSet
			closedSet.append(current)

			for i in range(col):
				for j in range(row):
					grid[i][j].addNeighbors(grid, obstacle, col,row) # add neighbors to all cells

			neighbors = current.neighbors 
			for neighbor in neighbors:
				if neighbor not in closedSet and neighbor not in obstacle: #evaluate if the tempG will be more efficient
					tempG = current.g + 1 
					newPath = False
					if neighbor in openSet:
						if tempG < neighbor.g:
							neighbor.g = tempG
							newPath = True
					else:
						neighbor.g = tempG
						openSet.append(neighbor)
						newPath = True

					if newPath:
						neighbor.h = heuristic(neighbor, end[0])# if there is a new path calculate the f cost
						neighbor.f = neighbor.g + neighbor.h
						neighbor.previous = current #set the neighbor parent into current
			path = []
			if current == end[0]:
				temp = current
				while (temp.previous != None): #make a loop to trace back the path
					path.append(temp.previous)
					temp = temp.previous
				loop = False
				print('Done')

		#color everything
		for cell in openSet:
			cell.color((0,255,0),screen)
		for cell in closedSet:
			cell.color((231,84,128),screen)
		for cell in path:
			cell.color((135,206,250),screen)
		for cell in start:
			cell.color((0,0,255),screen)
		for cell in end:
			cell.color((255,0,0),screen)

		pygame.display.update()
if __name__ == '__main__':
	main()